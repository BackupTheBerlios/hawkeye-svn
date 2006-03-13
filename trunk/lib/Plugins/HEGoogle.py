import os
import string
import thread
import SOAPpy
from SOAPpy import WSDL

from HawkEye import HEException
from HawkEye import HEPlugin
from HawkEye import HEUri

SOAPpy.Config.debug = 0

class HEGoogle( HEPlugin.HEPlugin ):

	def __init__( self ):
		HEPlugin.HEPlugin.__init__(self, "Google")
		self.__initInstructions()
		self.__key = None
		self.__wsdl_path = None
		self.__server = None

	def __initInstructions( self ):
		self.addInstruction("SETKEY", self.set_key)
		self.addInstruction("SETWSDL", self.set_wsdl)
		self.addInstruction("SEARCH", self.search)
		
	def set_key(self, params, callbacks=None):
		params[0] = HEUri.getPath(params[0])
		if params[0] != "":
			self.__key = params[0]
			return "OK"
		else:
			raise HEException.HEException("Google API Key is empty")

	def set_wsdl(self, params, callback=None):
		params[0] = "/" + HEUri.getPath(params[0])
		if params[0] != "" and os.path.isfile(params[0]):
			self.__wsdl_path = params[0]
			return "OK"
		else:
			raise HEException.HEException("WSDL path is empty or the WSDL file does not exist")

	def search(self, params, callback=None):
		try: 
			if HEUri.getPath(params[0])  != "":
				if self.__server == None:
					self.__server = WSDL.Proxy(self.__wsdl_path)
				else:
					raise HEException.HEException("WSDL file is not set")
				if self.__key != None:
					length = 10
					if len(params) == 2:
						length = HEUri.getPath(params[1])
					results = self.__server.doGoogleSearch(self.__key, HEUri.getPath(params[0]) , 0, length, False, "", False, "", "utf-8", "utf-8")
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
