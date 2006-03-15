#!/usr/bin/env python

import gobject

from threading import Thread
import time

import HECore
		
if __name__ == "__main__":
	print "running hawkeyed ..."
	
	gobject.threads_init()
	
	core = HECore.HECore()

	mainloop = gobject.MainLoop()
	mainloop.run()
	
    
