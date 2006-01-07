import dbus
import pickle

from HawkEye import HEException

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
            raise HEException.HEException("1: no connection to the messagebus")
        
    def request(self, instruction, params):
            dbus_params = dbus.Array([], type=dbus.String)
            if params != None:
                for param in params:
                    dbus_params.append(pickle.dumps(param))
#===============================================================================
#            try:
#===============================================================================
            return pickle.loads(self.interface.request(instruction, dbus_params))
#===============================================================================
#            except dbus.dbus_bindings.DBusException, e:
#                raise HEException.HEException("2: no connection to the messagebus")
#===============================================================================