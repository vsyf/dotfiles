#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
Properties
{
  UINT32    object_id;
  UINT32    size;
  UINT16    object_version;

  if (object_version == 0)
  {
    UINT32   max_bit_rate;
    UINT32   avg_bit_rate;
    UINT32   max_packet_size;
    UINT32   avg_packet_size;
    UINT32   num_packets;
    UINT32   duration;
    UINT32   preroll;
    UINT32   index_offset;
    UINT32   data_offset;
    UINT16   num_streams;
    UINT16   flags;
  }
"""
import sys
import trunk

class PROP(trunk.Trunk):
    def parse(self, buf):
        super(PROP, self).parse(buf)
        if self.object_version == 0:
            self.max_bit_rate = buf.readint32()
            self.avg_bit_rate = buf.readint32()
            self.max_packet_size = buf.readint32()
            self.avg_packet_size = buf.readint32()
            self.num_packets = buf.readint32()
            self.duration = buf.readint32()
            self.preroll = buf.readint32()
            self.index_offset = buf.readint32()
            self.data_offset = buf.readint32()
            self.num_streams = buf.readint16()
            self.flags = buf.readint16()

    def generate_fields(self):
        for x in super(PROP, self).generate_fields():
            yield x
        yield ("max_bit_rate", self.max_bit_rate)
        yield ("avg_bit_rate", self.avg_bit_rate)
        yield ("max_packet_size", self.max_packet_size)
        yield ("avg_packet_size", self.avg_packet_size)
        yield ("num_packets", self.num_packets)
        yield ("duration", self.duration)
        yield ("preroll", self.preroll)
        yield ("index_offset", self.index_offset)
        yield ("data_offset", self.data_offset)
        yield ("num_streams", self.num_streams)
        yield ("flags", self.flags)

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

trunk_map = {
        'PROP' : PROP,
        }
