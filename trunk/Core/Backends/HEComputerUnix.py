import os
from string import *

from HawkEye import HEDataType
from HawkEye import HEException
from HawkEye import HEUri
from HawkEye import HEBackend
from HawkEye import HEException

class HEComputerUnix( HEBackend.HEBackend ):

	def __init__(self):
		HEBackend.HEBackend.__init__(self, "File")
		self.__initInstructions()
	
	def __initInstructions(self):
		self.addInstruction("GET", HEDataType.HEContainer, self.get, 2)
		self.addInstruction("GET_DATATYPE", None, self.get_datatype, 1)
		self.addInstruction("MOUNT", HEDataType.HEContainer, self.mount, 1)
		self.addInstruction("UMOUNT", HEDataType.HEContainer, self.umount, 1)
		self.addInstruction("IS_MOUNTED", HEDataType.HEContainer, self.is_mounted, 1)
		
	# ---- checks the uri and repairs it if needed and possible
	def checkUri(self, uri):
		if uri.getDataType() == None:
			uri.setDataType(self.get_datatype([uri]))
		if uri.getDataType() == HEDataType.HEContainer:
			while uri.getPath().find("//") != -1:
				uri.setPath(uri.getPath().replace("//", "/"))
			if uri.getPath()[len(uri.getPath())-1] != "/":
				uri.setPath(uri.getPath()+"/")
		return uri

# ----- all instructions only really bare written today :), so don't use them


	def get(self, params):
		params[0] = self.checkUri(params[0])
		if params[0].getPath() == "":
			item_list = []
		
			fd = open("/etc/fstab", "r")
			for line in fd.readlines():
				line = line.strip()
				if len(line) > 0 and line[0] != "#":
					line = line.replace("\t", " ")
					while line.find("  ") != -1:
						line = line.replace("  ", " ")
						
					tmp_cols = line.split(" ")
					
					if len(params[1]) > 0: 
						if tmp_cols[2] in params[1]:
							item_list.append(tmp_cols)
					else:
						item_list.append(tmp_cols)
				
			fd.close()
		
			return item_list
		else:
			return []

	# ---- returns the DataType of the HEUri passed with params[0] 
	def get_datatype(self, params, callbacks = None):
		return HEDataType.HELink
		
	# ---- simple mount
	def mount(self, params, callbacks = None):
		pass
		
	# ---- simple umount
	def umount(self, params, callbacks = None):
		pass
		
	def is_mounted(self, params, callbacks = None):
		return True
