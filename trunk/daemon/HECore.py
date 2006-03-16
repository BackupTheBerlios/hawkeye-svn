from HawkEye import HEPlugin
from HawkEye import HEUri
from HawkEye import HEException
from HawkEye import Plugins
from HawkEye.Plugins import *

from string import *
from threading import Thread

import gobject
import dbus
import dbus.service
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib



class RequestThread(Thread):
	def __init__(self, method, return_cb, params):
		Thread.__init__(self)
		self.params = params
		self.return_cb = return_cb
		self.method = method
		
	def run(self):
		self.method(self.return_cb, self.params)
		
		
		
class HECore(dbus.service.Object):
        
	def __init__(self):
		self.__plugins = {}
		try:
			bus_name = dbus.service.BusName('de.nebulon.Hawkeye', bus=dbus.SessionBus())
			dbus.service.Object.__init__(self, bus_name, '/de/nebulon/Hawkeye')
		except dbus.dbus_bindings.DBusException, e:
			raise HEException.HEException("[HECore]\tno connection to the messagebus")


	# --- the request needs to start for every request a new thread....so we should do this ;-)
	@dbus.service.method('de.nebulon.HawkeyeIFace', async_callbacks=('return_cb', 'error_cb'))
	def request(self, instruction, params, return_cb, error_cb):
		if len(params) >= 1:
			plugin_type = HEUri.getPluginType(params[0])
			# check if the plugin is loaded
			if not self.__plugins.has_key(plugin_type):
				try:
					self.loadPlugin(plugin_type)
				except HEException.HEException, e:
					raise e
				print "[HECore]\t'"+plugin_type+"' loaded"
			# check if the backend provides this request and excute it
			method = self.__plugins[plugin_type].getInstruction(instruction)
			if method:
				try:
					thread = RequestThread(method, return_cb, params)
					thread.start()
					return "OK"
				except HEException.HEException, e:
					return "Error"
			else:
				raise HEException.HEException("[HECore]\tinstruction '"+instruction+"' not available in '"+plugin_type+"' Backend")
				
	# --- this system needs a complete rewrite:
	# ---		1)	more directories with plugins
	# ---		2) no real loading is done, because of "from plugins import *" every plugin is loaded at startup
	def loadPlugin(self, plugin_key):
		found = False
		for plugin in Plugins.__all__:
			if plugin.find("HE"+capitalize(plugin_key)) != -1:
				found = True       
				exec("new_plugin = "+plugin+"."+plugin+"()")
				self.__plugins.update({plugin_key: new_plugin})
		if not found:
			raise HEException.HEException("[HECore]\tthe needed plugin '"+plugin_key+"' couldn't be loaded")
    
