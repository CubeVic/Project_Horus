from onvif import ONVIFCamera
import asyncio

async def fetch_device(cam_ip, cam_port, cam_user, cam_password ):
	mycam = ONVIFCamera(cam_ip, cam_port, cam_user, cam_password)
	await mycam.update_xaddrs()


	#Create the service devicemgmt
	devicemgmt_service = mycam.create_devicemgmt_service() 

	#Get the response for GetDeviceInfo
	device_info = await devicemgmt_service.GetDeviceInformation()
	# print(type(device_info))
	print(f'\nManufacture: {device_info.Manufacturer} ')
	print(f'Model: {device_info.Model}')
	print(f'Firmware Version: {device_info.FirmwareVersion}')
	print(f'Serial Number: {device_info.SerialNumber}')
	print(f'Hardware ID: {device_info.HardwareId}')

	#Returns information about services on the device.
	services = await devicemgmt_service.GetServices(True)
	print(f'\n#####')
	print(f'service: {services}')

	#GetNetworkProtocol
	network_protocol = await devicemgmt_service.GetNetworkProtocols()
	print(f'\n####')
	print(f'network protocol: {network_protocol}')

	#GetScope
	scopes = await devicemgmt_service.GetScopes()
	print(f'\n#####')
	print(f'scope {scopes}')



	await mycam.close()

if __name__ == "__main__":
	cam_ip = input("Camera IP: ") or "172.16.18.162"
	cam_port = input("Camera cam_port: ") or 80
	cam_user = input("Camera User: ") or 'admin'
	cam_password = input("Camera password: ") or '123456'
	loop = asyncio.get_event_loop()
	loop.run_until_complete(fetch_device(cam_ip, cam_port, cam_user, cam_password))