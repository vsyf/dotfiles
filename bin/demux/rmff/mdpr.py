#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
Media_Properties
{
  UINT32     object_id;
  UINT32     size;
  UINT16     object_version;

  if (object_version == 0)
  {
    UINT16                      stream_number;
    UINT32                      max_bit_rate;
    UINT32                      avg_bit_rate;
    UINT32                      max_packet_size;
    UINT32                      avg_packet_size;
    UINT32                      start_time;
    UINT32                      preroll;
    UINT32                      duration;
    UINT8                       stream_name_size;
    UINT8[stream_name_size]     stream_name;
    UINT8                       mime_type_size;
    UINT8[mime_type_size]       mime_type;
    UINT32                      type_specific_len;
    UINT8[type_specific_len]    type_specific_data;
  }
}
"""
import sys
import trunk

class MDPR(trunk.Trunk):
    def parse(self, buf):
        super(MDPR, self).parse(buf)
        if self.object_version == 0:
            self.stream_num = buf.readint16()
            self.max_bit_rate = buf.readint32()
            self.avg_bit_rate = buf.readint32()
            self.max_packet_size = buf.readint32()
            self.avg_packet_size = buf.readint32()
            self.start_time = buf.readint32()
            self.preroll = buf.readint32()
            self.duration = buf.readint32()
            self.stream_name_size = buf.readbyte()
            self.stream_name = buf.readstr(self.stream_name_size)
            self.mime_type_size = buf.readbyte()
            self.mime_type = buf.readstr(self.mime_type_size)
            self.type_specific_len = buf.readint32()
            self.type_specific_data = buf.readstr(self.type_specific_len)

            self.consumed_bytes += 34 + self.stream_name_size + self.mime_type_size + self.type_specific_len
            

    def generate_fields(self):
        for x in super(MDPR, self).generate_fields():
            yield x
        if self.object_version == 0:
            yield ("stream_num", self.stream_num)
            yield ("max_bit_rate", self.max_bit_rate)
            yield ("avg_bit_rate", self.avg_bit_rate)
            yield ("max_packet_size", self.max_packet_size)
            yield ("avg_packet_size", self.avg_packet_size)
            yield ("start_time", self.start_time)
            yield ("preroll", self.preroll)
            yield ("duration", self.duration)
            yield ("stream_name_size", self.stream_name_size)
            yield ("stream_name", self.stream_name)
            yield ("mime_type_size", self.mime_type_size)
            yield ("mime_type", self.mime_type)
            yield ("type_specific_len", self.type_specific_len)
            yield ("type_specific_data", self.type_specific_data)

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

trunk_map = {
        'MDPR' : MDPR,
        }
