from onvif import ONVIFCamera
import asyncio

async def fetch_device(cam_ip, cam_port, cam_user, cam_password ):
	mycam = ONVIFCamera(cam_ip, cam_port, cam_user, cam_password)
	await mycam.update_xaddrs()


	#Create the service devicemgmt
	devicemgmt_service = mycam.create_devicemgmt_service() 

	#Get the response for GetDeviceInfo
	device_info = await devicemgmt_service.GetDeviceInformation()
	print(device_info)
	print(f'\nManufacture: {device_info.Manufacturer} ')
	print(f'Model: {device_info.Model}')
	print(f'Firmware Version: {device_info.FirmwareVersion}')
	print(f'Serial Number: {device_info.SerialNumber}')
	print(f'Hardware ID: {device_info.HardwareId}')

	#Get the host name
	host_name = await devicemgmt_service.GetHostname()
	# print(f'{host_name}')
	print(f'\nHost Name: {host_name.Name}')

	#Returns information about services on the device.
	services = await devicemgmt_service.GetServices(True)
	# print(f'\n#####')
	# print(f'service: {services}')

	#Get the network interfaces
	network_interfaces = await devicemgmt_service.GetNetworkInterfaces()
	print(network_interfaces)
	print(f'MAC address: {network_interfaces[0].Info.HwAddress} ')
	print(f'Manual: {network_interfaces[0].IPv4.Config.Manual}') #List of manually added IPv4 addresses.
	if network_interfaces[0].IPv4.Config.LinkLocal:
		print(f'Link local: {network_interfaces[0].IPv4.Config.LinkLocal.Address}')
	print(f'From DHCP: {network_interfaces[0].IPv4.Config.FromDHCP.Address}')

	#GetNetworkProtocol
	network_protocol = await devicemgmt_service.GetNetworkProtocols()
	# print(f'\n####')
	# print(f'network protocol: {network_protocol}')

	ntp = await devicemgmt_service.GetNTP()
	# print(ntp)

	#GetScope
	scopes = await devicemgmt_service.GetScopes()
	# print(f'\n#####')
	# print(f'scope {scopes}')

	await mycam.close()

if __name__ == "__main__":
	cam_ip = input("Camera IP: ") or "172.16.18.162"
	cam_port = input("Camera cam_port: ") or 80
	cam_user = input("Camera User: ") or 'admin'
	cam_password = input("Camera password: ") or '123456'
	loop = asyncio.get_event_loop()
	loop.run_until_complete(fetch_device(cam_ip, cam_port, cam_user, cam_password))