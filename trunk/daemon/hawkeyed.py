#!/usr/bin/env python

import gobject

import HECore
	
if __name__ == "__main__":
	print "running hawkeyed ..."
	core = HECore.HECore()
	mainloop = gobject.MainLoop()
	mainloop.run()
    
