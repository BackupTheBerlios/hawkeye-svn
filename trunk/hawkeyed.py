#!/usr/bin/env python

import gobject

from HawkEye import *

if __name__ == "__main__":
	print "running hawkeyed ..."
	core = HECore.HECore()
	mainloop = gobject.MainLoop()
	mainloop.run()
    