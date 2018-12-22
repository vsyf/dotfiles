#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""

"""
import os
import shutil
import math
from xml.etree import ElementTree

class Parser:
	name = []
	path = []
	revision = []
	tmp_path = ""
	def __init__ (self):
		print "Start ..."

	def parse_node(self, node):
		if node.attrib.has_key("name") > 0 :
			self.name.append(node.attrib['name'] + ".git")
		if node.attrib.has_key("path") > 0 :
			self.path.append(node.attrib['path'])
		if node.attrib.has_key("revision") > 0 :
			self.revision.append(node.attrib['revision'])

	def copy_path2name(self):
		if len(self.path) != 0 and len(self.path) == len(self.name):
			print "path/name len = %d" % len(self.path)
 		else:
			print "!!!!!!!!!! Error !!!!!!!!!!!"
		for i in range(0,len(self.path)):
			#print "path = %s" % self.path[i]
#                       if os.path.isdir(self.name[i]) != 0:
#				os.removedirs(self.name[i])
#			if os.path.isdir(self.path[i]) == 0:
#				os.makedirs(self.path[i])
#				shutil.copy(testfile, self.path[i])

			if os.path.isdir(self.path[i]) != 0:
#				shutil.copytree(self.path[i], self.name[i])
				#shutil.copy(self.path, self.name)
				#shutil.move(self.path, self.name)

                # mkdir -p /tmp/all-patches/path[i]
				tmp_path = "/tmp/all-patches/" + self.path[i]
				os.makedirs(tmp_path)

                # cd path[i]
				print self.path[i]
				t_path = "/data/lenovo-cht61/" + self.path[i]
				os.chdir(t_path)
				cmd = "git format-patch " + self.revision[i] + " -o " + tmp_path
				os.system(cmd)
                # git format-patch revision -o /tmp/all-patches/path[i]
				os.chdir("/data/lenovo-cht61/")
                # cd croot
				print "Success!!!"
			else:
				print "Error!!!!! path = %s" % self.path[i]
				print "name = %s" % self.name[i]

	def read_xml(self, text):
		root = ElementTree.fromstring(text)
		lst_node = root.getiterator("project")
		for node in lst_node:
			self.parse_node(node)


if __name__ == '__main__':
	parser=Parser()
	parser.read_xml(open("manifest-full-20160627-2014_ww26.xml").read())
	parser.copy_path2name()
	print "End !!!"

