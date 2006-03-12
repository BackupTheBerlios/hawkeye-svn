import os
import string
from stat import *
import thread
import urllib

from HawkEye import HEUri
from HawkEye import HEPlugin

class HEHttp( HEPlugin.HEPlugin ):

	def __init__(self):
		HEPlugin.HEPlugin.__init__(self, "Http")
		self.__initInstructions()
	
	def __initInstructions(self):
		self.addInstruction("GET", self.get)

	# ---- returns an array with the DataTypes in the HEUri passed with params[0] 
	def get(self, params, callbacks = None):
		urllib.urlretrieve(params[0], params[1])
		return "Download complete"
