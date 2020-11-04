from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery

wsd = WSDiscovery()
wsd.start()
devices_services = wsd.searchServices()
print(f'services: {dir(devices_services[0])}')
for service in devices_services:
	print(f'\nthis is the address with getXAddrs():\n-->{service.getXAddrs()[0]}\n')
	print(f'this are the scopes:')
	for scope in service.getScopes():
		print(f'- {scope}\n')
	print(f'this getTypes(), type of services:')
	for type_service in service.getTypes():
		print(f'- {type_service}\n')
# print(dir(wsd))
# print(addr)
# print(len(addr))
wsd.stop()