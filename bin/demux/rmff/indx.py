#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
Index_Chunk_Header
{
  u_int32     object_id;
  u_int32     size;
  u_int16      object_version
 ;

  if (object_version == 0)
  {
    u_int32     num_indices;
    u_int16     stream_number;
    u_int32     next_index_header;
  }
}

IndexRecord
{
  UINT16   object_version;

  if (object_version == 0)
  {
    u_int32  timestamp;
    u_int32  offset;
    u_int32   packet_count_for_this_packet;
  }
}
"""
import sys
import trunk

class INDX(trunk.Trunk):
    def parse(self, buf):
        super(INDX, self).parse(buf)
        self.indexs = []
        if self.object_version == 0:
            self.num_indices = buf.readint32()
            self.stream_num = buf.readint16()
            self.next_index_header = buf.readint32()
            self.consumed_bytes += 10
            
            while self.consumed_bytes < self.size:
                index = IndexRecord.get_next_index_record(buf, self)
                self.consumed_bytes += index.consume_bytes
                self.indexs.append(index)

    def generate_fields(self):
        for x in super(INDX, self).generate_fields():
            yield x
        yield ("num_indices", self.num_indices)
        yield ("stream_num", self.stream_num)
        yield ("next_index_header", self.next_index_header)
        if self.object_version == 0:
            for index in self.indexs:
                for x in index.generate_fields():
                    yield x

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

class IndexRecord(object):
    def __init__(self, buf, parent=None):
        super(IndexRecord, self).__init__()
        self.object_version = buf.readint16()
        self.consume_bytes = 2
        if self.object_version == 0:
            self.timestamp = buf.readint32()
            self.offset = buf.readint32()
            self.packet_count_for_this_packet = buf.readint32()
            self.consume_bytes += 12



    @staticmethod
    def get_next_index_record(buf, parent=None):
        index_record = IndexRecord(buf, parent)
        return index_record

    def generate_fields(self):
        yield ("timestame", self.timestamp)
        yield ("offset", self.offset)
        yield ("packet_count_for_this_packet", self.packet_count_for_this_packet)

    def __str__(self):
        return "IndexRecord (ts:%d, offset:%d)" % (self.timestamp, self.offset)
        

trunk_map = {
        'INDX' : INDX,
        }
