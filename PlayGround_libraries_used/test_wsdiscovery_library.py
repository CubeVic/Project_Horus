from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery.publishing import ThreadedWSPublishing as WSPublishing
from wsdiscovery import QName, Scope

# Define type, scope & address of service
ttype1 = QName("http://www.onvif.org/ver10/device/wsdl", "Device")
scope1 = Scope("onvif://www.onvif.org/Model")
xAddr1 = "127.0.0.1:8998/abc"

# Publish the service
wsp = WSPublishing()
wsp.start()
wsp.clearLocalServices()
wsp.publishService(types=[ttype1], scopes=[scope1], xAddrs=[xAddr1])

# Discover it (along with any other service out there)
wsd = WSDiscovery()
wsd.start()
wsd.clearRemoteServices()
print(wsd.clearRemoteServices())
print(wsd.start())
services = wsd.searchServices()
for service in services:
	print(service.getEPR() + ":" + service.getXAddrs()[0])
	print("searching for service")
wsd.stop()