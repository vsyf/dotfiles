#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
Content_Description
{
  UINT32     object_id;
  UINT32     size;
  UINT16      object_version
 ;

  if (object_version == 0)
  {
    UINT16    title_len;
    UINT8[title_len]  title;
    UINT16    author_len;
    UINT8[author_len]  author;
    UINT16    copyright_len;
    UINT8[copyright_len]  copyright;
    UINT16    comment_len;
    UINT8[comment_len]  comment;
  }
}
"""
import sys
import trunk

class CONT(trunk.Trunk):
    def parse(self, buf):
        super(CONT, self).parse(buf)
        if self.object_version == 0:
            self.title_len = buf.readint16()
            self.title = buf.readstr(self.title_len)
            self.author_len = buf.readint16()
            self.author = buf.readstr(self.author_len)
            self.copyright_len = buf.readint16()
            self.copyright = buf.readstr(self.copyright_len)
            self.comment_len = buf.readint16()
            self.comment = buf.readstr(self.comment_len)

            self.consumed_bytes += 8 + self.title_len + self.author_len + self.comment_len + self.comment_len

    def generate_fields(self):
        print "cont fields"
        for x in super(CONT, self).generate_fields():
            yield x
        if self.object_version == 0:
            yield ("title_len", self.title_len)
            yield ("title", self.title)
            yield ("author_len", self.author_len)
            yield ("author", self.author)
            yield ("copyright_len", self.copyright_len)
            yield ("copyright", self.copyright)
            yield ("comment_len", self.comment_len)
            yield ("comment", self.comment)

    def __str__(self):
        return "%s (%d butes)" % (self.id, self.size)

trunk_map = {
        'CONT' : CONT,
        }
