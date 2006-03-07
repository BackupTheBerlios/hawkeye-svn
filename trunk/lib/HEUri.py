from string import *

def getUri(pluginType, path = ""):
	return str(pluginType)+"://"+str(path)

def getPluginType(uri):
	tmp = uri.split("://")
	if len(tmp) > 0:
		return lower(tmp[0])
	else:
		return None

def getPath(uri):
	tmp = uri.split("://")
	if len(tmp) > 1:
		return tmp[1]
	else:
		return None
