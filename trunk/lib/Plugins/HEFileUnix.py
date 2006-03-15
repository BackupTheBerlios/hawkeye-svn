import os
import string
from stat import *
import thread
		
from HawkEye import HEUri
from HawkEye import HEPlugin
from HawkEye import HEException

class HEFileUnix( HEPlugin.HEPlugin ):

	def __init__(self):
		HEPlugin.HEPlugin.__init__(self, "File")
		self.__initInstructions()
	
	def __initInstructions(self):
		self.addInstruction("GET", self.get)
		self.addInstruction("REMOVE", self.remove)
		self.addInstruction("MOVE", self.move)
		self.addInstruction("GO_UP", self.go_up)
		self.addInstruction("COPY", self.copy)
		self.addInstruction("STAT", self.stat)
		self.addInstruction("EXISTS", self.exists)


	# ---- checks the uri and repairs it if needed and possible
	def checkUri(self, uri):
		if HEUri.getPath(uri) == "":
			uri = HEUri.getUri("file","/")
		while string.find(HEUri.getPath(uri), "//") != -1:
			uri = HEUri.getUri("file", string.replace(HEUri.getPath(uri), "//", "/"))
		if HEUri.getPath(uri)[len(HEUri.getPath(uri))-1] != "/":
			uri += "/"
		return uri
		
	def go_up(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		pos = HEUri.getPath(params[0]).rfind("/")
		if pos == 0:
			return params[0]
		else:
			params[0] = HEUri.getUri("file", HEUri.getPath(params[0])[0:HEUri.getPath(params[0])[0:len(HEUri.getPath(params[0]))-2].rfind("/")])
			return params[0]
	
	# ---- checks if the HEUri exists
	def file_exists(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(HEUri.getPath(params[0])):
			return True
		else:
			return False

	def get(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(HEUri.getPath(params[0])):
			item_list = os.listdir(HEUri.getPath(params[0]))
			tmp_list = [params[0]]
		
			for item in item_list:
				if os.path.isdir(HEUri.getPath(params[0])+"/"+item):
					tmp_list.append(params[0]+"/"+item)
				else:
					tmp_list.append(params[0]+"/"+item)
			
			return tmp_list
		else:
			raise HEException.HEException("path "+params[0]+" does not exist")
		
		
	# ---- removes the Container in the HEUri passed with params[0] 
	def remove(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(HEUri.getPath(params[0])):
			os.remove(HEUri.getPath(params[0]))
		else:
			raise HEException.HEException("path "+params[0]+" does not exist")

	# ---- copy method ---- the first callback it will use for progress
	def copy(self, params, callbacks = None):
		return 1
		
	def move(self, params, callbacks = None):
		return 1
		
	def exists(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(HEUri.getPath(params[0])):
			return True
		else:
			return False
		
	# ---- returns a array with File Data
	def stat(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(HEUri.getPath(params[0])):
			return os.stat(HEUri.getPath(params[0]))[ST_SIZE]
		else:
			raise HEException.HEException("path "+params[0]+" does not exist")
