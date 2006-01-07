#!/usr/bin/env python

from HawkEye import *

client = HEClient.getHEClient()
uri = HEUri.HEUri()

uri.setFromUri("google://FViw8hpQFHKaXU0epHdlLPgrXeud3/Wi")
client.request("SETKEY", [uri])
uri.setFromUri("google://home/the_hippie/Projekte/hawkeye/trunk/Misc/GoogleSearch.wsdl")
client.request("SETWSDL", [uri])

uri.setFromUri("google://hawkeye")
client.request("SEARCH", [uri])
