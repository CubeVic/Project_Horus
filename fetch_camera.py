from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope
import re
from onvif import ONVIFCamera

import sensecam_discovery

def display(any_list):
	for item in any_list:
		print(item)



def fetch_devices():
	wsd = WSDiscovery()
	scope1 = Scope("onvif://www.onvif.org/")
	wsd.start()
	services = wsd.searchServices(scopes=[scope1])
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


def fetch_camera():
	camera = ONVIFCamera('172.16.18.162',80,'admin','123456')
	camera_media_service = camera.create_media_service()
	camera_profiles = camera_media_service.GetProfiles()
	print(f'camera {camera_profiles}')


if __name__ == "__main__":
	onvif_devices = fetch_devices()
	by_sensecam = sensecam_discovery.discover()
	display(by_sensecam)
	# for device in onvif_devices:
	# 	print(f'IP Address: {device}')
	# fetch_camera()