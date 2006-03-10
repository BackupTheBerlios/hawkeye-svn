#!/usr/bin/env python

from HawkEye import *
from HawkEye.Plugins import HEGoogle
import gobject
import urllib

def return_handler(result_list = None):
	print "Return: ",result_list
	
def error_handler(error):
	print "Error: ",error
	
client = HEClient.getHEClient()

client.request("SETKEY", ["google://FViw8hpQFHKaXU0epHdlLPgrXeud3/Wi"], return_handler, error_handler)
client.request("SETWSDL", ["google://home/the_hippie/Projekte/hawkeye/trunk/misc/GoogleSearch.wsdl"], return_handler, error_handler)
client.request("SEARCH", ["google://hawkeye"], return_handler, error_handler)

mainloop = gobject.MainLoop()
mainloop.run()
