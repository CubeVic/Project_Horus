from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import QName, Scope
import re


def display_IPs(any_list):
	for item in any_list:
		print(item)


def fetch_devices():
	wsd = WSDiscovery()
	scope1 = Scope("onvif://www.onvif.org/")
	ttype1 = QName("http://www.onvif.org/ver10/device/wsdl", "Device")
	# ttype2 = Qname("http://www.onvif.org/ver10/media/wsdl","Media")
	wsd.start()
	services = wsd.searchServices(types=[ttype1], scopes=[scope1], timeout=6)
	# services = wsd.searchServices(scopes=[scope1])
	ipaddresses = []
	for service in services:
	#filter those devices that dont have ONVIF service
		ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
		ipaddresses.append(ipaddress)

	print(f'\nnumber of devices detected: {len(services)}')
	wsd.stop()
	return ipaddresses



if __name__ == "__main__":

	onvif_devices_IPs = fetch_devices()
	display_IPs(sorted(onvif_devices_IPs))