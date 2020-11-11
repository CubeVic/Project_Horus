from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope
import re


base = 'onvif://www.onvif.org/'
profile_scope = base + 'Profile/'


scope1 = Scope(base) # to be use later to filter just those with ONVIF services
scope2 = Scope(profile_scope)

def fetch_devices(services):
	for service in services:
	#filter those devices that dont have ONVIF service
	# print(f'\nAddress:\n{service.getXAddrs()[0]}\n')
		ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
		print(f'\nIP Address: {ipaddress}')
		for scope in service.getScopes():
			#Scope methods getMatchBy, getQuotedValue, getValue
			print(scope.getValue())
	print(f'\nnumber of devices detected: {len(services)}')

wsd = WSDiscovery()
wsd.start()
# devices_services = wsd.searchServices(scopes=[scope1])
devices_services = wsd.searchServices()

fetch_devices(devices_services)

wsd.stop()