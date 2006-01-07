import os
import string
import thread
import SOAPpy
from SOAPpy import WSDL

from HawkEye import HEException
from HawkEye import HEBackend

SOAPpy.Config.debug = 0

class HEGoogle( HEBackend.HEBackend ):

	def __init__( self ):
		HEBackend.HEBackend.__init__(self, "Google")
		self.__initInstructions()
		self.__key = None
		self.__wsdl_path = None
		self.__server = None

	def __initInstructions( self ):
		self.addInstruction("SETKEY", None, self.set_key, 1)
		self.addInstruction("SETWSDL", None, self.set_wsdl, 1)
		self.addInstruction("SEARCH", None, self.search, 1)

	def checkUri(self, uri):
		return uri
		
	def set_key(self, params, callbacks=None):
		params[0] = params[0].getPath()
		if params[0] != "":
			self.__key = params[0]
		else:
			raise HEException.HEException("Google API Key is empty")

	def set_wsdl(self, params, callback=None):
		params[0] = "/" + params[0].getPath()
		if params[0] != "" and os.path.isfile(params[0]):
			self.__wsdl_path = params[0]
		else:
			raise HEException.HEException("WSDL path is empty or the WSDL file does not exist")

	def search(self, params, callback=None):
		try: 
			if params[0].getPath()  != "":
				if self.__server == None:
					self.__server = WSDL.Proxy(self.__wsdl_path)
				else:
					raise HEException.HEException("WSDL file is not set")
				if self.__key != None:
					length = 10
					if len(params) == 2:
						length = params[1].getPath()
					results = self.__server.doGoogleSearch(self.__key, params[0].getPath() , 0, length, False, "", False, "", "utf-8", "utf-8")
					result = []
					for data in results.resultElements:
						cur = []
						cur.append(data.URL)
						cur.append(data.title)
						cur.append(data.summary)
						result.append(cur)
					return result
				else:
					raise HEException.HEException("Key is not set")
			else:
				raise HEException.HEException("Search string is empty")
		except:
			raise HEException.HEException("Problem with search")
