from HawkEye import HEException

class HEBackend:

	def __init__(self, key):
		self.__instructions = {}
		self.__key = key
				
	def isInstructionAvailable(self, instruction, data_type, arg_count):
		if self.__instructions.has_key(data_type):
			if self.__instructions[data_type].has_key(instruction):
				if self.__instructions[data_type][instruction][1] == arg_count:
					return self.__instructions[data_type][instruction][0]
		return False
		
		
	def getInstructionList(self, data_type):
		if self.__instructions.has_key(data_type):
			return self.__instructions[data_type]
		else:
			raise HEException.HEException("[WW]\tno instructions for this datatype")
		
	def getKey(self):
		return self.__key
		
	def addInstruction(self, instruction, data_type, method_handler, arg_count):
		if not self.isInstructionAvailable(instruction, data_type, arg_count):
			if not self.__instructions.has_key(data_type):
				self.__instructions.update({data_type: {}})
			self.__instructions[data_type].update({instruction: [method_handler, arg_count]})
			return True
		else:
			raise HEException.HEException("[WW]\tInstruction "+instruction+" is already available");
