from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope
import re


base = 'onvif://www.onvif.org/'
type_scope = base + 'type/'
hardware_scope = base + 'hardware/'
profile_scope = base + 'Profile/'
name_scope = base + 'name/'
location_scope = base + 'location/'
register_status_scope = base + 'register_status/'
reigster_server_scope = base + 'register_server/'
regist_id_scope = base + 'regist_id/'
manufacture_scope = base + 'manufacturer/'
video_source_number = base + 'VideoSourceNumber/'
version_scope = base + 'version/'
serial_scope = base + 'serial/'
mac_addr_scope = base + 'macaddr/'
max_resolution_scope = base + 'max_resolution/'
activeCode_scope = base + 'ActiveCode/'
cloudUserName = base + 'CloudUserName/'
acc_scope = base + 'acc/'

scope1 = Scope(base) # to be use later to filter just those with ONVIF services

wsd = WSDiscovery()
wsd.start()
devices_services = wsd.searchServices(scopes=[scope1])


for service in devices_services:
	#filter those devices that dont have ONVIF service
	# print(f'\nAddress:\n{service.getXAddrs()[0]}\n')
	ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
	print(f'\nIP Address: {ipaddress}')
	for scope in service.getScopes():
		#Scope methods getMatchBy, getQuotedValue, getValue
		print(scope.getValue())

wsd.stop()