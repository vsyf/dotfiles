#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 youfa <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
copy from https://github.com/drothlis/clang-ctags

"""

#!/usr/bin/env python2

import argparse
import os
import StringIO
import sys
import time
import traceback
from contextlib import contextmanager
from os.path import basename, dirname, isabs, isdir, join, realpath, relpath
from textwrap import dedent

import subprocess
import re

import clang.cindex
from clang.cindex import CompilationDatabase, CursorKind, Diagnostic, \
    TranslationUnit


def main(argv):
    global args, invocation_dir  # pylint:disable=global-variable-undefined
    args = parse_args(argv)
    invocation_dir = os.getcwd()
    tagger = Tagger()

    if args.compile_commands:
        db_dir = (args.compile_commands if isdir(args.compile_commands)
                  else dirname(args.compile_commands))
        db = CompilationDatabase.fromDirectory(db_dir)
        source_files = [realpath(x) for x in args.source_files]
        for i, f in enumerate(source_files):
            debug("Processing file %d of %d: %s" % (i+1, len(source_files), f))
            for c in db.getCompileCommands(f) or []:
                debug("* Found compile command: " + " ".join(list(c.arguments)))
                with cwd(join(db_dir, c.directory)):
                    debug("  run from directory: " + os.getcwd())
                    do_tags(list(c.arguments)[1:], tagger, source_files)
    else:
        do_tags(args.compiler_command_line, tagger)

    if args.output == "-":
        out = sys.stdout
    else:
        out = open(args.output, ("a" if args.append else "w") + "b")

    formatter = etags if args.etags else ctags
    out.write(formatter(tagger.tags))


def clang_default_include():
    sub = subprocess.Popen(['clang', '-v', '-x', 'c++', '-'],
                           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    _, out = sub.communicate('')
    reg = re.compile('lib/clang.*/include$')
    return next(line.strip() for line in out.split('\n') if reg.search(line))


def do_tags(compiler_command_line, tagger, source_files=None):
    index = clang.cindex.Index.create()

    compiler_command_line = ['-I', clang_default_include()] + \
                            compiler_command_line
    try:
        start = time.time()
        tu = index.parse(None, compiler_command_line,
                         options=TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)
        debug("  clang parse took %.2fs" % (time.time() - start))
    except Exception:
        debug(traceback.format_exc())
        error("Clang failed to parse '%s'" % " ".join(compiler_command_line))

    errors = [d for d in tu.diagnostics
              if d.severity in (Diagnostic.Error, Diagnostic.Fatal)]
    if len(errors) > 0:
        debug("\n".join([d.spelling for d in errors]))
        error("File '%s' failed clang's parsing and type-checking" %
              tu.spelling)

    if not source_files:
        source_files = [realpath(tu.spelling)]

    start = time.time()
    for c in tu.cursor.get_children():
        do_cursor(c, tagger, source_files)
    debug("  tag generation took %.2fs" % (time.time() - start))


def do_cursor(cursor, tagger, source_files):
    if not should_tag_file(cursor.location.file, source_files):
        return

    if is_definition(cursor):
        parents = semantic_parents(cursor)
        if args.extra_qualifier_tags:
            tagger.tag(
                cursor, "::" + "::".join(parents + [cursor.displayname]))
            for i in range(len(parents) + 1):
                tagger.tag(
                    cursor, "::".join(parents[i:] + [cursor.displayname]))
        else:
            tagger.tag(cursor, "::".join(parents + [cursor.displayname]))

    if should_tag_children(cursor):
        for c in cursor.get_children():
            do_cursor(c, tagger, source_files)


def should_tag_file(f, source_files):
    def is_system_header():
        return (isabs(f.name) and
                relpath(f.name, invocation_dir).startswith(".."))

    return (f and
            (args.all_headers or
             (args.non_system_headers and not is_system_header()) or
             realpath(f.name) in source_files))


def is_definition(cursor):
    return (
        (cursor.is_definition() and not cursor.kind in [
            CursorKind.CXX_ACCESS_SPEC_DECL,
            CursorKind.TEMPLATE_TYPE_PARAMETER,
            CursorKind.UNEXPOSED_DECL,
            ]) or
        # work around bug (?) whereby using PARSE_SKIP_FUNCTION_BODIES earlier
        # causes libclang to report cursor.is_definition() as false for
        # function definitions.
        cursor.kind in [
            CursorKind.FUNCTION_DECL,
            CursorKind.CXX_METHOD,
            CursorKind.FUNCTION_TEMPLATE,
            ])


def semantic_parents(cursor):
    import collections

    p = collections.deque()
    c = cursor.semantic_parent
    while c and is_named_scope(c):
        p.appendleft(c.displayname)
        c = c.semantic_parent
    return list(p)


def should_tag_children(cursor):
    return is_named_scope(cursor) or cursor.kind in [
        # 'extern "C" { ... }' should be LINKAGE_SPEC but is UNEXPOSED_DECL
        CursorKind.UNEXPOSED_DECL,
        ]


def is_named_scope(cursor):
    return cursor.kind in [
        CursorKind.NAMESPACE,
        CursorKind.STRUCT_DECL,
        CursorKind.UNION_DECL,
        CursorKind.ENUM_DECL,
        CursorKind.CLASS_DECL,
        CursorKind.CLASS_TEMPLATE,
        CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION,
        ]


class Tagger(object):
    def __init__(self):
        self.tags = {}  # {file: [(line, tag, linenumber, bytenumber), ...]}
        self.current_file_name = None
        self.current_file_lines = None

    def tag(self, cursor, tagname):
        """The complete tags file entry for symbol 'tag'."""
        if self.current_file_name != realpath(cursor.location.file.name):
            self.current_file_name = realpath(cursor.location.file.name)
            with open(self.current_file_name) as f:
                self.current_file_lines = f.readlines()

        if self.current_file_name not in self.tags:
            self.tags[self.current_file_name] = set()

        self.tags[self.current_file_name].add((
            self.current_file_lines[cursor.location.line - 1].rstrip(),
            tagname,
            cursor.location.line,
            cursor.location.offset))


def etags(tags):
    """Write tags in the format understood by Emacs.

    See http://bzr.savannah.gnu.org/lh/emacs/trunk/annotate/head:/etc/ETAGS.EBNF
    """
    out = StringIO.StringIO()
    for f in tags:
        out.write("\x0c\x0a" + f + ",\x0a")
        for t in tags[f]:
            out.write("%s\x7f%s\x01%d,%d\x0a" % t)
    return out.getvalue()


def ctags(tags):
    """Write tags in the format understood by Vi.

    Currently generates the basic, original vi format (what the
    Exuberant Ctags man page calls "level 1"); doesn't generate the
    "level 2" extension fields.

    The man page for Exuberant Ctags (http://ctags.sourceforge.net)
    documents the tags file format.
    """
    out = StringIO.StringIO()
    out.write(dedent("""\
        !_TAG_FILE_FORMAT\t1\t/basic format; no extension fields/
        !_TAG_FILE_SORTED\t0\t/0=unsorted, 1=sorted, 2=foldcase/
        !_TAG_PROGRAM_NAME\tclang-ctags\t//
        !_TAG_PROGRAM_URL\thttp://github.com/drothlis/clang-ctags\t//
        """))
    for f in tags:
        for (line, t, _n, _) in tags[f]:
            out.write("%s\t%s\t%s\n" % (
                t,
                f,
                "/^%s$/" % line))
    return out.getvalue()


@contextmanager
def cwd(directory):
    """Run a block of code from a specified working directory"""
    old_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(old_dir)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Generate tag file for C++ source code.",
        usage="\nclang-ctags [options] -- <compiler command line>"
              "\nclang-ctags [options] "
              "--compile-commands=<compile_commands.json> <source-file> ...")
    parser.add_argument("-e", action="store_true",
                        help='output tags in Emacs format (default: vi format)'
                             ' (implied if the program name contains "etags")')
    parser.add_argument("-a", "--append", action="store_true",
                        help="append tag entries to existing tag file")
    parser.add_argument("-f", "-o", "--output", metavar="FILE",
                        help='write the tags to %(metavar)s;'
                             ' "-" writes tags to stdout'
                             ' (default: "tags", or "TAGS" when -e supplied)')
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="enable debugging output")
    parser.add_argument("--version", action="version",
                        version="clang-ctags 0.2")
    parser.add_argument("--compile-commands", metavar="COMPILE_COMMANDS.JSON",
        help="database of compilation command lines for each source file")
    parser.add_argument("--all-headers", action="store_true",
        help="write tags for all header files encountered "
             "(not just those specified on the command line)")
    parser.add_argument("--non-system-headers", action="store_true",
        help="write tags for all non-system header files encountered")
    parser.add_argument("--extra-qualifier-tags", action="store_true",
        help="write separate tags for each level of namespace/class qualifier")
    parser.add_argument("--suppress-qualifier-tags", action="store_false",
        dest="extra_qualifier_tags", help=argparse.SUPPRESS)
    parser.add_argument("args", nargs="+", help=argparse.SUPPRESS)

    a = parser.parse_args(argv[1:])
    a.etags = bool(a.e or re.search("etags", argv[0]))
    if not a.output:
        a.output = "TAGS" if a.etags else "tags"
    if a.compile_commands:
        a.source_files = a.args
    else:
        a.source_files = []
        a.compiler_command_line = a.args

    if a.all_headers and len(a.source_files) > 1:
        warn("`--all-headers` is being used with more than one source file. "
             "This can lead to an unusably large tag file.")

    return a


def debug(s):
    if args.verbose:
        sys.stderr.write(s + "\n")

def warn(s):
    sys.stderr.write("%s: Warning: %s\n" % (basename(sys.argv[0]), s))

def error(s):
    sys.stderr.write("%s: Error: %s\n" % (basename(sys.argv[0]), s))
    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
