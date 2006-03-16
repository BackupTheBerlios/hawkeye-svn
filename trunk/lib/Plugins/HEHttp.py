import os
import string
from stat import *

import httplib
import urllib
import urlparse

from HawkEye import HEUri
from HawkEye import HEPlugin

class HEHttp( HEPlugin.HEPlugin ):

	def __init__(self):
		HEPlugin.HEPlugin.__init__(self, "Http")
		self.__initInstructions()
	
	
	def __initInstructions(self):
		self.addInstruction("GET", self.get)
		self.addInstruction("EXISTS", self.exists)
		
		
	def exists(self, params, return_callback=None):
		url = urlparse.urlparse(params[0])
		conn = httplib.HTTPConnection(url[1])
		conn.request("GET", params[0])
		response = conn.getresponse()
		if response.status >= 400:
			reply = False
		else:
			reply = True
			
		if return_callback:
			return_callback(reply)
		else:
			return reply
			

	# ---- returns an array with the DataTypes in the HEUri passed with params[0] 
	def get(self, params, return_callback=None):
		if not self.exists(params):
			if return_callback:
				return_callback("File not exists")
			else:
				return "File not exists"
		
		def statusHandler(blocks, bytes, size):
			print "[Http]\t[GET]\tblocks: ", blocks, "\tbytes: ", bytes, "\tsize: ", size
				
		try:
			fd = urllib.urlretrieve(params[0], params[1], statusHandler)
		except IOError, e:
			if return_callback:
				return_callback(str(e))
			else:
				return e
		
		return_callback("Download complete")
