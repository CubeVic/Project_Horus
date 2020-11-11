from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope
import re
from onvif import ONVIFCamera
from onvif.exceptions import ONVIFAuthError, ONVIFError, ONVIFTimeoutError
import asyncio


def fetch_devices():
	wsd = WSDiscovery()
	scope1 = Scope("onvif://www.onvif.org/")
	wsd.start()
	services = wsd.searchServices(scopes=[scope1])
	ipaddresses = []
	for service in services:
	#filter those devices that dont have ONVIF service
	# print(f'\nAddress:\n{service.getXAddrs()[0]}\n')
		ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
		ipaddresses.append(ipaddress)

	print(f'\nnumber of devices detected: {len(services)}')
	wsd.stop()
	return ipaddresses

async def fetch_device(cam_ip, cam_port, cam_user, cam_password ):
	try:
		mycam = ONVIFCamera(cam_ip, cam_port, cam_user, cam_password)
		await mycam.update_xaddrs()


		#Create the service devicemgmt
		devicemgmt_service = mycam.create_devicemgmt_service() 

		device_info = await devicemgmt_service.GetDeviceInformation()
		print(f'\nManufacture: {device_info.Manufacturer} ')
		print(f'Model: {device_info.Model}')
		print(f'Firmware Version: {device_info.FirmwareVersion}')
		print(f'Serial Number: {device_info.SerialNumber}')
		print(f'Hardware ID: {device_info.HardwareId}')

		#Get the host name
		host_name = await devicemgmt_service.GetHostname()
		# print(f'{host_name}')
		print(f'Host Name: {host_name.Name}')

		#Returns information about services on the device.
		services = await devicemgmt_service.GetServices(True)
		# print(f'\n#####')
		# print(f'service: {services}')

		#Get the network interfaces
		network_interfaces = await devicemgmt_service.GetNetworkInterfaces()
		# print(network_interfaces)
		print(f'MAC address: {network_interfaces[0].Info.HwAddress} ')
		if network_interfaces[0].IPv4.Config.Manual != []:
			print(f'Manual: {network_interfaces[0].IPv4.Config.Manual[0].Address}') #List of manually added IPv4 addresses.
		if network_interfaces[0].IPv4.Config.LinkLocal:
			print(f'Link local: {network_interfaces[0].IPv4.Config.LinkLocal.Address}')
		print(f'From DHCP: {network_interfaces[0].IPv4.Config.FromDHCP.Address}')

		#GetNetworkProtocol
		network_protocol = await devicemgmt_service.GetNetworkProtocols()
		# print(f'\n####')
		# print(f'network protocol: {network_protocol}')

		# ntp = await devicemgmt_service.GetNTP()
		# print(ntp)

		#GetScope
		scopes = await devicemgmt_service.GetScopes()
		# print(f'\n#####')
		# print(f'scope {scopes}')


	except ONVIFAuthError as auth_error:
		print(f'ONVIFAuthError: something worng with the password for {cam_ip} type of error {auth_error}')
	except ONVIFError as onvif_error:
		print(f'ONVIFError: error with ONVIF with {cam_ip} type of error {onvif_error}')
	except Exception as other:
		print(f'Exception: other type of error {cam_ip} other type of error {other}')

	await mycam.close()

if __name__ == "__main__":

	devices = fetch_devices()
	print(devices)
	for cam_ip in devices:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(fetch_device(cam_ip, 80, 'admin', '123456'))
