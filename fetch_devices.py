from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import QName, Scope
import re

import sensecam_discovery

def display(any_list):
	for item in any_list:
		print(item)



def fetch_devices():
	wsd = WSDiscovery()
	scope1 = Scope("onvif://www.onvif.org/")
	ttype1 = QName("http://www.onvif.org/ver10/device/wsdl", "Device")
	# ttype2 = Qname("http://www.onvif.org/ver10/media/wsdl","Media")
	wsd.start()
	services = wsd.searchServices(types=[ttype1], scopes=[scope1])
	# services = wsd.searchServices(scopes=[scope1])
	ipaddresses = []
	for service in services:
	#filter those devices that dont have ONVIF service
		ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
		ipaddresses.append(ipaddress)
		print(display(service.getScopes()))
		print('----------END')

	print(f'\nnumber of devices detected: {len(services)}')
	wsd.stop()
	return ipaddresses



if __name__ == "__main__":
	onvif_devices_IPs = fetch_devices()
	display(sorted(onvif_devices_IPs))

	# by_sensecam = sensecam_discovery.discover()
	# display(sorted(by_sensecam))
	# print(f'\nnumber of devices detected: {len(by_sensecam)}\n')
	# for device in onvif_devices:
	# 	print(f'IP Address: {device}')
	# fetch_camera()
	# fetch_camera()