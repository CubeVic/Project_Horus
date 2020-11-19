from onvif import ONVIFCamera
from onvif.exceptions import ONVIFError
import  yaml
import logging
import logging.config


#
# logger_file.debug('logger_file debug message')
# logger_file.info('logger_file info message')
# logger_file.warning('logger_file warn message')
# logger_file.error('logger_file error message')
# logger_file.critical('logger_file critical message')



def display(any_list):
	for item in any_list:
		print(item)


def fetch_camera():
	try:
		camera = ONVIFCamera('172.16.18.124',80,'admin','Aa12345!')
		logger_file.info(f"Getting camera object {camera}")
	except Exception as e:
		raise ONVIFError(e)
	
	
	camera_media_service = camera.create_media_service()
	camera_profiles = camera_media_service.GetProfiles()
	devicemgmt_service = camera.create_devicemgmt_service() 
	camera_information = devicemgmt_service.GetDeviceInformation()
	camera_discoverable_modes = devicemgmt_service.GetDiscoveryMode()
	print(f'camera information: {camera_information}')
	# print(f'camera {camera_profiles}')
	# print(f'discovery mode: {camera_discoverable_modes}')


if __name__ == "__main__":
	with open('config.yml', 'r') as config:
	    try: 
	        configuration = yaml.safe_load(config.read())
	        # print(configuration)
	        logging.config.dictConfig(configuration)
	        logger = logging.getLogger('simpleExample')
	        logger_file = logging.getLogger('fileLogger')
	    except yaml.YAMLError as exc:
	         print(exc)

	fetch_camera()