from onvif import ONVIFCamera

def display(any_list):
	for item in any_list:
		print(item)


def fetch_camera():
	camera = ONVIFCamera('172.16.18.124',80,'admin','Aa123456!')
	
	camera_media_service = camera.create_media_service()
	camera_profiles = camera_media_service.GetProfiles()

	devicemgmt_service = camera.create_devicemgmt_service() 
	camera_information = devicemgmt_service.GetDeviceInformation()
	camera_discoverable_modes = devicemgmt_service.GetDiscoveryMode()
	print(f'camera information: {camera_information}')
	print(f'camera {camera_profiles}')
	print(f'discovery mode: {camera_discoverable_modes}')


if __name__ == "__main__":

	fetch_camera()