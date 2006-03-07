from HawkEye import HEException

class HEPlugin:

	def __init__(self, key):
		self.__instructions = {}
		self.__key = key
				
	def getInstruction(self, instruction):
		if self.__instructions.has_key(instruction):
			return self.__instructions[instruction]
		
	def getKey(self):
		return self.__key
		
	def addInstruction(self, instruction, method_handler):
		if not self.__instructions.has_key(instruction):
			self.__instructions.update({instruction: method_handler})
		else:
			raise HEException.HEException("[WW]\tInstruction "+instruction+" is already available");
