from HawkEye import HEException

import thread

import dbus
import dbus.service
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib

instance = None

def getHEClient():
    global instance
    if instance == None:
        instance = __HEClient()
    return instance

class __HEClient:
    
	def __init__(self):
		try:
			proxy = dbus.SessionBus().get_object('de.nebulon.Hawkeye', '/de/nebulon/Hawkeye')
			self.interface = dbus.Interface(proxy, 'de.nebulon.HawkeyeIFace')
		except dbus.dbus_bindings.DBusException, e:
			raise HEException.HEException("[HEClient]\tno connection to the messagebus")
 
	# --- return_handler:	gets as param a list ('return_value1,'return_value2') <- as many as the request returns
	# --- error_handler:		gets as param one error-string
	def request(self, instruction, params, return_handler, error_handler, timeout = 1000000):
		dbus_params = dbus.Array([], type=dbus.String)
		if params != None:
			for param in params:
				dbus_params.append(str(param))
			self.interface.request(instruction, dbus_params, reply_handler=return_handler, error_handler=error_handler, timeout = timeout)
			
