import HEBackend
import HEUri
from HawkEye import HEException
from HawkEye import Backends
from HawkEye.Backends import *

from string import *

import pickle
import gobject
import dbus
import dbus.service
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib
        
class HECore(dbus.service.Object):
        
    def __init__(self):
        self.__backends = {}
        try:
            bus_name = dbus.service.BusName('de.nebulon.Hawkeye', bus=dbus.SessionBus())
            dbus.service.Object.__init__(self, bus_name, '/de/nebulon/Hawkeye')
        except dbus.dbus_bindings.DBusException, e:
            raise HEException.HEException("[HECore]\tno connection to the messagebus")
        
    @dbus.service.method('de.nebulon.HawkeyeIFace')
    def request(self, instruction, params):
        if len(params) >=1:
            uris = []
            # temporary
            callbacks = None
            for param in params:
                uris.append(pickle.loads(param))
            # check if the backend is loaded
            if not self.__backends.has_key(uris[0].getBackendType()):
                try:
                    self.loadBackend(uris[0].getBackendType())
                except HEException.HEException, e:
                    raise e
                print "backend '"+uris[0].getBackendType()+"' loaded"
            backend = self.__backends[uris[0].getBackendType()]
            
            # check if the backend provides this request and excute it
            method = backend.isInstructionAvailable(instruction, uris[0].getDataType(), len(uris))
            if method:
                return pickle.dumps(method(uris))
            else:
                raise HEException.HEException("[HECore]\tinstruction "+instruction+" not available in '"+uris[0].getBackendType()+"' Backend")
                
    def loadBackend(self, backend_key):
        # check if this backend is available
        for backend in Backends.__all__:
            if backend.find("HE"+capitalize(backend_key)) != -1:                
                exec("new_backend = "+backend+"."+backend+"()")
                
                # check if the backend has the needed methods
                if new_backend.checkUri == None:
                    raise HEException.HEException("[HECore]\tBackend "+backend_key+" does not have checkUri function implemented")
                self.__backends.update({backend_key: new_backend})
                return
        raise HEException.HEException("[HECore]\tthe needed backend '"+backend_key+"' couldn't be loaded")

    def unloadBackend(self, backend_key):
        return 0
    