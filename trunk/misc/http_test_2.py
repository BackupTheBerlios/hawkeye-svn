#!/usr/bin/env python

from HawkEye import *
import gobject
import urllib

def return_handler(result_list):
	print "Return: ",result_list
	
def error_handler(error):
	print "Error: ",error
	
	
#src = "http://kernel.org/pub/linux/kernel/v2.6/patch-2.6.15.6.bz2"
target = "/tmp/YeahYeah.ogg"
src = "http://shared.nebulon.de/music/Yeah%20Yeah%20Yeahs%20-%20Gold%20Lion.ogg"

client = HEClient.getHEClient()
client.request("GET", [src,target], return_handler, error_handler)

mainloop = gobject.MainLoop()
mainloop.run()
