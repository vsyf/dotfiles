#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
Data_Chunk_Header
{
  UINT32     object_id;
  UINT32     size;
  UINT16      object_version;

  if (object_version == 0)
  {
    UINT32    num_packets;
    UINT32    next_data_header;
  }
}

Media_Packet_Header
{
  UINT16                object_version;

  if ((object_version == 0) || (object_version == 1))
  {
    UINT16        length;
    UINT16        stream_number;
    UINT32        timestamp;
    if (object_version == 0)
    {
      UINT8        packet_group;
      UINT8        flags;
    }
    else if (object_version == 1)
    {
      UINT16        asm_rule;
      UINT8          asm_flags;
    }

    UINT8[length]        data; //此处有误，此length应为整个media packet的length
  }
  else
  {
    StreamDone();
  }
}
"""
import sys
import trunk

class DATA(trunk.Trunk):
    def parse(self, buf):
        super(DATA, self).parse(buf)
        self.media_packets = []
        if self.object_version == 0:
            self.num_packets = buf.readint32()
            self.next_data_header = buf.readint32()
            self.consumed_bytes += 8
            
            # open it to see media packet info
            #while self.consumed_bytes < self.size:
            #    packet = MPHD.get_next_media_packet(buf, self)
            #    self.consumed_bytes += packet.consume_bytes
            #    self.media_packets.append(packet)

    def generate_fields(self):
        for x in super(DATA, self).generate_fields():
            yield x
        yield ("num_packets", self.num_packets)
        yield ("next_data_header", self.next_data_header)
        if self.object_version == 0:
            for packet in self.media_packets:
                for x in packet.generate_fields():
                    yield x

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

class MPHD(object):
    def __init__(self, buf, parent=None):
        super(MPHD, self).__init__()
        self.buffer_offset = buf.current_position()

        self.object_version = buf.readint16()
        #print "mphd, version:%s, offset:%s" % (self.object_version, self.buffer_offset)
        self.consume_bytes = 2
        if self.object_version == 0 or self.object_version == 1:
            self.length =  buf.readint16()
            self.stream_number = buf.readint16()
            self.timestamp = buf.readint32()
            #print "length:%s, stream_num:%s, ts:%s" % (self.length, self.stream_number, self.timestamp)
            if self.object_version == 0:
                self.packet_group = buf.readbyte()
                self.flags = buf.readbyte()
                #print "group:%s, flags:%s" % (self.packet_group, self.flags)
                self.consume_bytes += 10 + self.length
            else:
                self.asm_rule = buf.readint16()
                self.asm_flags = buf.readbyte()
                self.consume_bytes += 11 + self.length
            # skip data now, maybe read esdata into a file in the feature
            # length in reference is wrong
            #buf.readint(self.length - 12)
            buf.seekto(self.buffer_offset + self.length)

        self.consume_bytes = buf.current_position() - self.buffer_offset
        #print "mphd, comsumed:%s, buf.pos:%s" % (self.consume_bytes, buf.current_position())



    @staticmethod
    def get_next_media_packet(buf, parent=None):
        packet = MPHD(buf, parent)
        return packet

    def generate_fields(self):
        yield ("length", self.length)
        yield ("stream_num", self.stream_number)
        yield ("timestamp", self.timestamp)
        if self.object_version == 0:
            yield ("packet_group", self.packet_group)
            yield ("flags", self.flags)
        else:
            yield ("asm_rule", self.asm_rule)
            yield ("asm_flags", self.asm_flags)

    def __str__(self):
        return "MPHD (ts:%d)" % (self.timestamp)
        

trunk_map = {
        'DATA' : DATA,
        }
