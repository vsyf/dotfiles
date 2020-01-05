#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
reference https://www.helixcommunity.org/projects/common/2003/HCS_SDK_r5/htmfiles/rmff.htm
"""

import os
import sys
import argparse

from datasource import DataBuffer
from datasource import FileSource
from console import ConsoleRenderer
from tree import Tree, Attr

def get_trunk_list(buf, parent=None):
    from rmff.trunk import Trunk
    trunks = []
    try:
        while buf.hasmore():
            trunk = Trunk.get_next_trunk(buf, parent)
            trunks.append(trunk)
    except:
        import traceback
        print traceback.format_exc()
    return trunks

def get_trunk_node(trunk, args):
    from rmff.trunk import Trunk
    node = Tree(trunk.id, Trunk.get_trunk_desc(trunk.id))
    for field in trunk.generate_fields():
        if isinstance(field, Trunk):
            add_trunk(node, field, args)
        elif type(field) is not tuple:
            raise Exception("Expected a tuple, got a %s" %type(field));
        else:
            #generate fields yields a tuple of order (name, value, [formatted_value])
            value = field[1]
            if args.truncate and type(value) is list and len(value) > 10:
                value = "[%s ... %s]" %(
                    ','.join([str(i) for i in value[:3]]),
                    ','.join([str(i) for i in value[-3:]])
                )
            node.add_attr(field[0], value, field[2] if len(field) == 3 else None)
    return node

def add_trunk(parent, trunk, args):
    trunk_node = parent.add_child(get_trunk_node(trunk, args))
    #for child in trunk.children:
    #    add_trunk(trunk_node, child, args)
    return trunk_node


def get_tree_from_file(path, args):
    with open(path, 'rb') as fd:
        trunks = get_trunk_list(DataBuffer(FileSource(fd)))
    root = Tree(os.path.basename(path), "File")
    for trunk in trunks:
        add_trunk(root, trunk, args)
    return root

def main():
    parser = argparse.ArgumentParser(
        description='Process rmff file and list the trunks and their contents')
    parser.add_argument('-o', choices=['stdout','gui'], default='stdout',
        help='output format', dest='output_format')
    parser.add_argument('-e', '--expand-arrays', action='store_false',
        help='do not truncate long arrays', dest='truncate')
    parser.add_argument('-c', '--color', choices=['on', 'off'], default='on', dest='color',
        help='turn on/off colors in console based output; on by default')
    parser.add_argument('input_file', metavar='iso-base-media-file', help='Path to iso media file')
    args = parser.parse_args()

    root = get_tree_from_file(args.input_file, args)

    renderer = None
    if args.output_format == 'stdout':
        renderer = ConsoleRenderer('  ')
        if args.color == 'off':
            renderer.disable_colors()
    if args.output_format == 'gui':
        from gui import GtkRenderer
        renderer = GtkRenderer()

    renderer.render(root)


if __name__ == "__main__":
    main()

