#!/usr/bin/env python

from HawkEye import *
import gobject
import urllib

def return_handler(result_list):
	print "Return: ",result_list
	
def error_handler(error):
	print "Error: ",error
	
	
dir = "file:///home/"

client = HEClient.getHEClient()
client.request("GET", [dir], return_handler, error_handler)

mainloop = gobject.MainLoop()
mainloop.run()
