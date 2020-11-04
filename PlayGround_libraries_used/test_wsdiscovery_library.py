from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery.publishing import ThreadedWSPublishing as WSPublishing
from wsdiscovery import QName, Scope

# Define type, scope & address of service
# ttype1 = QName("http://www.onvif.org/ver10/device/wsdl", "Device")
# scope1 = Scope("onvif://www.onvif.org/Model")
# xAddr1 = "127.0.0.1:8998/abc"

# Publish the service
# wsp = WSPublishing()
# wsp.start()
# wsp.clearLocalServices()
# wsp.publishService(types=[ttype1], scopes=[scope1], xAddrs=[xAddr1])

# Discover it (along with any other service out there)
wsd = WSDiscovery()
wsd.start()
services = wsd.searchServices()
addr = list()
for service in services:
	# print("searching for service")
	# print(service.getEPR() + ":" + service.getXAddrs()[0])
	# print(f'{service.getXAddrs()}\n')
	print(f'\nthis is the addres: {service.getXAddrs()[0]}')
	print(f'this the scopes: {service.getScopes()}')
	print(f'this getTypes() {service.getTypes()}\n')
	addr.append(service.getXAddrs()[0])
# print(dir(wsd))
# print(addr)
# print(len(addr))
wsd.stop()

########################################################
####    not fully understood, but enought            ###
####    to get what i need, the onvif devices        ###
####    on the network, new script                   ###
####    called: "fetch_webservices_wsdiscovery.py"   ###
####    is a refined version of this script          ###
########################################################