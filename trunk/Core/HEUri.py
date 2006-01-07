from string import *

class HEUri:

	def __init__(self, backendType = None, path = None, dataType = None):
		self.__path = path
		if backendType != None:
			backendType = lower(backendType)
		self.__backendType = backendType
		self.__dataType = dataType
		
	def setFromUri(self, uri):
		tmp = uri.split("://")
		if len(tmp) > 1:
			self.__backendType = lower(tmp[0])
			self.__path = tmp[1]
			return True
		else:
			return False
		
	# --- checks and repairs --------------------------------------------------------
	def checkUri(self):
		if self.__path == "":
			self.__path = "/"
		while self.__path.find("//") != -1:
			self.__path = self.__path.replace("//", "/")
		if self.__dataType == HEDataType.HEContainer:
			if self.__path[len(self.__path)-1] != "/":
				self.__path = self.__path+"/"


	# --- getter and setter --------------------------------------------------------
	def getPath(self):
		return self.__path

	def setPath(self, path):
		self.__path = path
		
	def appendPath(self, path):
		self.__path = self.__path+"/"+path

	def getBackendType(self):
		return self.__backendType

	def setBackendType(self, backendType):
		self.__backendType = lower(backendType)

	def getDataType(self):
		return self.__dataType
		
	def setDataType(self, dataType):
		self.__dataType = dataType
