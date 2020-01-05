#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""

"""

import sys

def string_to_hex(s):
    x = [ "%02x" %ord(ch) for ch in s]
    return " ".join(x)

class Trunk(object):
    trunk_id_names = {
            '.RMF' : 'RealMedia File Header',
            'PROP' : 'Properties Header',
            'CONT' : 'Content Description Header',
            'MDPR' : 'Media Properties Header',
            'DATA' : 'Data Chunk',
            'INDX' : 'Index Section',
            }
    """docstring for Trunk"""
    def __init__(self, buf, parent=None):
        super(Trunk, self).__init__()
        self.parent = parent
        pos = buf.current_position()
        self.buffer_offset = pos

        #parse
        self.parse(buf)
        self.consumed_bytes = buf.current_position() - pos
        if self.consumed_bytes < self.size:
            print "Skipping tailing bytes: Possible parse error (or unhandled trunk) in %s: consumed %d, skip %d" % (self, self.consumed_bytes, self.size - self.consumed_bytes)
        buf.skipbytes(self.size - self.consumed_bytes)
        self.consumed_bytes = self.size

    def parse(self, buf):
        self.id = buf.readstr(4)
        self.size = buf.readint32()
        self.object_version = buf.readint16()
        self.consumed_bytes = 10

    def generate_fields(self):
        yield ("size", self.size)
        #yield ("object_version", self.object_version)

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

    @staticmethod
    def get_next_trunk(buf, parent=None):
        import prop
        import cont
        import mdpr
        import indx
        import data
        trunk_map = {
                '.RMF' : RMFH,
                }
        trunk_map.update(prop.trunk_map)
        trunk_map.update(cont.trunk_map)
        trunk_map.update(mdpr.trunk_map)
        trunk_map.update(indx.trunk_map)
        trunk_map.update(data.trunk_map)
        obj_id = buf.peekstr(4, 0)
        if obj_id in trunk_map:
            trunk = trunk_map[obj_id](buf, parent)
        else:
            trunk = Trunk(buf, parent)
            buf.skipbytes(trunk.size - trunk.consumed_bytes)
        return trunk

    @staticmethod
    def get_trunk_desc(name):
        if name in Trunk.trunk_id_names:
            return Trunk.trunk_id_names[name]
        else:
            name.upper()



class RMFH(Trunk):
    def parse(self, buf):
        super(RMFH, self).parse(buf)
        if self.object_version == 0 or self.object_version == 1:
            self.file_version = buf.readint32()
            self.num_headers = buf.readint32()

    def generate_fields(self):
        for x in super(RMFH, self).generate_fields():
            yield x
        yield ("file_version", self.file_version)
        yield ("num_headers", self.num_headers)

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

