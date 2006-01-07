import os
import string
from stat import *
import thread
		
from HawkEye import HEDataType
from HawkEye import HEUri
from HawkEye import HEBackend

class HEFileUnix( HEBackend.HEBackend ):

	def __init__(self):
		HEBackend.HEBackend.__init__(self, "File")
		self.__initInstructions()
	
	def __initInstructions(self):
		self.addInstruction("GET", HEDataType.HEContainer, self.container_get, 1)
		self.addInstruction("REMOVE", HEDataType.HEContainer, self.container_remove, 1)
		self.addInstruction("REMOVE", HEDataType.HEFile, self.file_remove, 1)
		self.addInstruction("GET_DATATYPE", None, self.get_datatype, 1)
		self.addInstruction("GO_UP", HEDataType.HEContainer, self.go_up_container, 1)
		self.addInstruction("WRITE", HEDataType.HEFile, self.write_file, 1)
		self.addInstruction("READ", HEDataType.HEFile, self.read_file, 1)
		self.addInstruction("COPY", HEDataType.HEFile, self.copy_file, 2)
		self.addInstruction("STAT", HEDataType.HEFile, self.stat_file, 2)
		self.addInstruction("STAT", HEDataType.HEContainer, self.stat_file, 2)
		self.addInstruction("EXISTS", HEDataType.HEFile, self.file_exists, 1)


	# ---- checks the uri and repairs it if needed and possible
	def checkUri(self, uri):
		if uri.getBackendType() == None:
			uri.setBackendType("file")
		if uri.getPath() == "":
			uri.setPath("/")
		if uri.getDataType() == None:
			uri.setDataType(self.get_datatype([uri]))
		if uri.getDataType() == HEDataType.HEContainer:
			while string.find(uri.getPath(), "//") != -1:
				uri.setPath(string.replace(uri.getPath(), "//", "/"))
			if uri.getPath()[len(uri.getPath())-1] != "/":
				uri.setPath(uri.getPath()+"/")
		return uri
		
	
# ----- all instructions only really bare written today :), so don't use them
		
	def go_up_container(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		pos = params[0].getPath().rfind("/")
		if pos == 0:
			return params[0]
		else:
			params[0].setPath(params[0].getPath()[0:params[0].getPath()[0:len(params[0].getPath())-2].rfind("/")])
			return params[0]
	
	# ---- checks if the HEUri exists
	def file_exists(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			return True
		else:
			return False
			

	# ---- returns an array with the DataTypes in the HEUri passed with params[0] 
	def container_get(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			item_list = os.listdir(params[0].getPath())
			tmp_list = [params[0]]
		
			for item in item_list:
				if os.path.isdir(params[0].getPath()+"/"+item):
					tmp_list.append([HEUri.HEUri("file", params[0].getPath()+"/"+item, HEDataType.HEContainer), item])
				else:
					tmp_list.append([HEUri.HEUri("file", params[0].getPath()+"/"+item, HEDataType.HEFile), item])
			
			return tmp_list
		else:
			raise HEException.HEException("path "+params[0].getPath()+" does not exist")
		
		
	# ---- removes the Container in the HEUri passed with params[0] 
	def container_remove(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			os.removedirs(params[0].getPath())
		else:
			raise HEException.HEException("path "+params[0].getPath()+" does not exist")
		
		
	# ---- removes the File in the HEUri passed with params[0] 
	def file_remove(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			os.remove(params[0].getPath())
		else:
			raise HEException.HEException("path "+params[0].getPath()+" does not exist")
		
		
	# ---- returns the DataType of the HEUri passed with params[0] 
	def get_datatype(self, params, callbacks = None):
		if os.path.exists(params[0].getPath()):
			if os.path.isdir(params[0].getPath()):
				return HEDataType.HEContainer
			elif os.path.islink(params[0].getPath()):
				return HEDataType.HELink
			else:
				return HEDataType.HEFile
		else:
			raise HEException.HEException("path "+params[0].getPath()+" does not exist")

			
	# ---- returns a FileDescriptor to the open file for writing
	def write_file(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			fd = open(params[0].getPath(), "w+")
			return fd
		else:
			raise HEException.HEException("path "+params[0].getPath()+" exists")
		
		
	# ---- returns a FileDescriptor to the open file for reading
	def read_file(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			fd = open(params[0].getPath(), "r")
			return fd
		else:
			raise HEException.HEException("path "+params[0].getPath()+" does not exist")

	# ---- copy method ---- the first callback it will use for progress
	def copy_file(self, params, callbacks = None):
		# open the filedescriptors
		try:
			src_fd = self.read_file([params[0]])
		except HEException.HEException, e:
			raise e
		
		try:
			target_fd = self.write_file([params[1]])
		except HEException.HEException, e:
			raise e
			
		# do copy
		buffer_size = 1000
		buffer_count = 0
		file_size = self.stat_file(params)
		
		while True:
			buffer = src_fd.read(buffer_size)
			if buffer != "":
				target_fd.write(buffer)
				buffer_count += 1
				if callbacks != None and len(callbacks) > 0:
					callbacks[0](len(buffer)*buffer_count, file_size) 
			else:
				break
					
		src_fd.close()
		target_fd.close()
		
	# ---- returns a array with File Data
	def stat_file(self, params, callbacks = None):
		params[0] = self.checkUri(params[0])
		if os.path.exists(params[0].getPath()):
			return os.stat(params[0].getPath())[ST_SIZE]
		else:
			raise HEException.HEException("path "+params[0].getPath()+" does not exist")
