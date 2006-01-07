# Author:	Johannes Zellner
# Email:		webmaster@nebulon.de

import os
import sys
from xml.dom import minidom

import pygtk
pygtk.require("2.0")
import gtk

from HawkEye import *

_doc_name = "mime"
_public_id = "HawkEye::Mime::1.0"
_system_id = "http://hawkeye.nebulon.de/dtd/1.0/mime"
_namespace = "http://hawkeye.nebulon.de/1.0/mime"

instance = None

def getHEMime():
	global instance
	if instance == None:
		instance = HEMime()
	return instance
	
class HEMime:

	def __init__(self, mimedb_path):
		self.mimedb_path = mimedb_path
		self.content = {}
		self.loadMimeType("default")
		
		
	# ---- returns the dataType of a HEUri --------------------------------
	def getTypeFromUri(self, uri):
		return uri.getPath()[uri.getPath().rfind(".")+1:]
		
		
	# ---- Comment --------------------------------------------------------
	def getComment(self, dataType, language=None):
		if self.content.has_key(dataType):
			if len(self.content[dataType]["comments"]) > 0:
				if language != None:
					if self.content[dataType]["comments"].has_key(language):
						return self.content[dataType]["comments"][language]
					elif self.content[dataType]["comments"].has_key("default"):
						return self.content[dataType]["comments"]["default"]
		return self.content["default"]["applications"]

	def setComment(self, dataType, comment, language=None):
		if self.content.has_key(dataType):
			if len(self.content[dataType]["comments"]) == 0:
				self.content[dataType].update({"comments": {}})
			if language == None:
				language = "default"
			if self.content[dataType]["comments"].has_key(language):
				self.content[dataType]["comments"][language] = comment
			else:
				self.content[dataType]["comments"].update({language: comment})
		

	# ---- Applications ---------------------------------------------------
	def getApplications(self, dataType):
		if self.content.has_key(dataType):
			if len(self.content[dataType]["applications"]) > 0:
				return self.content[dataType]["applications"]
		return self.content["default"]["applications"]

	def addApplication(self, dataType, name, path, comment = ""):
		if not self.content.has_key(dataType):
			self.content.update({dataType: {}})
		if not self.content[dataType]["applications"]:
				self.content[dataType].update({"applications": {}})
		if not self.content[dataType]["applications"].has_key(name):
			self.content[dataType]["applications"].update({name: {"path": path, "default": "False", "app-comments": {}}})
		else:
			return False

	def deleteApplication(self, dataType, application):
		return
		

	# ---- Icons ----------------------------------------------------------
	def getIcon(self, dataType):
		if self.loadMimeType(dataType):
			if len(self.content[dataType]["icons"]) > 0:
				return self.content[dataType]["icons"][0][1]
		return self.content["default"]["icons"][0][1]

	def setIcon(self, dataType, uri):
		pass
		

	# ---- MimeType -------------------------------------------------------
	def addMime(self, dataType, comments, icon):
		return

	def deleteMime(self, dataType):
		return
		
		
	# ---- Write the XML-files ----------------------------------------------
	def save(self):
		for elem in self.content:
			code = "<mime>\n"
			if self.content[elem].has_key("comments"):
				for comment in self.content[elem]["comments"]:
					if comment == "default":
						code += "\t<comment>"+self.content[elem]["comments"][comment]+"</comment>\n"
					else:
						code += "\t<comment lang=\""+comment+"\">"+self.content[elem]["comments"][comment]+"</comment>\n"
			if self.content[elem].has_key("applications"):
				for application in self.content[elem]["applications"]:
					code += "\t<application name=\""+application+"\" default=\""+self.content[elem]["applications"][application]["default"]+"\">\n"
					code += "\t\t<path>"+self.content[elem]["applications"][application]["path"]+"</path>\n"
					if self.content[elem]["applications"][application].has_key("appcomments"):
						for app_comment in self.content[elem]["applications"][application]["appcomments"]:
							if comment == "default":
								code += "\t\t<appcomment>"+self.content[elem]["applications"][application]["appcomments"][app_comment]+"</appcomment>\n"
							else:
								code += "\t\t<appcomment lang=\""+app_comment+"\">"+self.content[elem]["applications"][application]["appcomments"][app_comment]+"</appcomment>\n"
					code += "\t</application>\n"
			if self.content[elem].has_key("icons"):
				for icon in self.content[elem]["icons"]:
					code += "\t<icon>"+icon[0]+"</icon>\n"
			code += "</mime>\n"
			
			fd = open(self.mimedb_path.getPath()+"/"+elem+".xml", "w")
			fd.write(code)	
			fd.close()
			
			
	# ---- parse the XML-files ----------------------------------------------
	def loadMimeType(self, mimeType):
		if not self.content.has_key(mimeType):
			core = HEClient.getHEClient()
		
			xmlfile = HEUri.HEUri("file", self.mimedb_path.getPath(), HEDataType.HEFile)
			xmlfile.appendPath(mimeType+".xml")
			
			if core.request("EXISTS", [xmlfile]):
				dom = minidom.parse(xmlfile.getPath())
				
				for element in dom.getElementsByTagName("mime"):
					content = {}
			
					content.update(self.getComments(element))
					content.update(self.getIcons(element))
					content.update(self.getApplications(element))
			
					self.content.update({mimeType: content})
		
				# free xmlfile
				dom.unlink()
			else:
				return False
		return True
		
	def getComments(self, node):
		comments = {}
		for comment in node.getElementsByTagName("comment"):
			if comment.hasAttribute("lang"):
				comments.update({comment.getAttribute("lang"): comment.firstChild.data})
			else:
				comments.update({"default": comment.firstChild.data})
		return {"comments": comments}
		
			
	def getIcons(self, node):
		icons = []
		for icon in node.getElementsByTagName("icon"):
			icons.append([icon.firstChild.data, gtk.gdk.pixbuf_new_from_file(icon.firstChild.data)])
		return {"icons": icons}
		
		
	def getApplications(self, node):
		applications = {}
		for application in node.getElementsByTagName("application"):
			name = application.getAttribute("name")
			default = application.getAttribute("default")
			path = application.getElementsByTagName("path")[0].firstChild.data
			
			comments = {}
			for comment in application.getElementsByTagName("appcomment"):
				if comment.hasAttribute("lang"):
					comments.update({comment.getAttribute("lang"): comment.firstChild.data})
				else:
					comments.update({"default": comment.firstChild.data})
		
			applications.update({name: {"path": path, "default": default, "appcomments": comments}})
			
		return {"applications": applications}
