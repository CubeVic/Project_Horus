from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
import wsdiscovery.scope

profile_scope = 'onvif://www.onvif.org/Profile/'
hardware_scope = "onvif://www.onvif.org/hardware/"
name_scope = "onvif://www.onvif.org/name/"
manufacture_scope = "onvif://www.onvif.org/manufacturer/"
serial_scope = "onvif://www.onvif.org/serial/"

wsd = WSDiscovery()
wsd.start()
devices_services = wsd.searchServices()
# print(f'services: {dir(devices_services[0])}')

for service in devices_services:
	#filter those devices that dont have ONVIF service
	if str(service.getTypes()[0]).find('onvif') != -1:

		print(f'\nthis is the address with getXAddrs():\n-->{service.getXAddrs()[0]}\n')

		#transform from object to string
		scopes = [str(scope) for scope in service.getScopes()]
		for scope in scopes:
			if scope.find(hardware_scope) !=-1:
				hardware = scope.split(hardware_scope)[1]
				print(f'- Hardware: {hardware} \n')	
			if scope.find(name_scope) !=-1:
				name = scope.split(name_scope)[1]
				print(f'- Name: {name} \n')	
			if scope.find(manufacture_scope) !=-1:
				manufacture = scope.split(manufacture_scope)[1]
				print(f'- Manufacture: {manufacture} \n')
			if scope.find(serial_scope) !=-1:
				serial = scope.split(serial_scope)[1]
				print(f'- Serial: {serial} \n')									
		
		# print(f'this getTypes(), type of services:')
		# for type_service in service.getTypes():
		# 	print(f'- {type_service}\n')	

wsd.stop()