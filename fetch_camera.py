from onvif import ONVIFCamera
from onvif.exceptions import ONVIFError
import  yaml
import logging
import logging.config
from PIL import Image
import requests
from io import BytesIO # to read the image/snapshot
# import cv2 as cv

# logger_file.debug('logger_file debug message')
# logger_file.info('logger_file info message')
# logger_file.warning('logger_file warn message')
# logger_file.error('logger_file error message')
# logger_file.critical('logger_file critical message')
def load_logger():
	with open('log_config.yml', 'r') as config:
		try: 
			configuration = yaml.safe_load(config.read())
			logging.config.dictConfig(configuration)
			logger = logging.getLogger('console_logger')
			logger_file = logging.getLogger('file_logger')
		except yaml.YAMLError as exc:
			 print(exc)	

def get_onvifCamera_client():
	""" get the onvif.client.ONVIFCamera"""
	try:
		camera = ONVIFCamera('172.16.18.162',80,'admin','123456')
	except Exception as e:
		logger_file.error(f"Getting camera object ...Failed")
		logger.error(f'Getting camera object ...Failed')
		raise ONVIFError(e)

	return camera

def get_camera_info(camera):
	""" get back information about the device
	such as: 
	* Manufacture
	* Model
	* Firmware version
	* Serial Number
	* Hardware ID
	"""
	devicemgmt_service = camera.create_devicemgmt_service()
	camera_info = devicemgmt_service.GetDeviceInformation()
	# print(f'devicemgmt_service is type: {type(devicemgmt_service)}')
	# print(f'camera_information is type: {type(camera_info)}') 
	cam = {'Manufacturer':camera_info.Manufacturer,
		'Model': camera_info.Model,
		'FirmwareVersion': camera_info.FirmwareVersion,
		'SerialNumber': camera_info.SerialNumber,
		'HardwareId': camera_info.HardwareId}
	return cam

def get_camera_profiles(media_service):
	""" get back list of dictionaries with the profile name and tokens"""
	camera_profiles_description = media_service.GetProfiles()
	# print(camera_profiles_description)
	profiles_tokens = []
	for description in camera_profiles_description:
		profile_token = {'Name': description.Name,
						'token': description.token}
		profiles_tokens.append(profile_token)
	return profiles_tokens

def get_snapshot_URI(media_service, token):
	""" get the snapshot URI for the snapshot depending of the profile passed"""
	snapshot_uri_dict = media_service.GetSnapshotUri(token)
	snapshot_uri = snapshot_uri_dict['Uri']
	print(f"snapshot URI: {snapshot_uri}")
	return snapshot_uri

def get_snapshot(url):
	""" get the snapshot 
		TODO:
		- Automate Auth
	"""
	response = requests.get(url, auth=('admin', '123456'))
	print(type(response.content))
	img = Image.open(BytesIO(response.content))
	img.show()# to show the image


# def get_rtsp(media_service, token):
#     """ get the URI for the stream using RTSP """

#     # TODO
#     stream_setup = {'StreamSetup' : 
#                         { 'Stream' : 'RTP_unicast', 
#                           'Transport' : { 'Protocol' : 'UDP' } 
#                           }, 
#                         'ProfileToken' : token}
#     uri = media_service.GetStreamUri(stream_setup)
#     rtsp_stream = uri.Uri
#     print(f'uri: {uri.Uri}')
#     return rtsp_stream

def get_capabilities(media_service):
	""" get the capabilities of the device, such as 
	* snapshotUri
	* Rotation
	* video Sources
	* OSD
	* Streaming capabilities
	"""
	capabilities = media_service.GetServiceCapabilities()
	print(capabilities)

if __name__ == "__main__":

	load_logger()

	cam = get_onvifCamera_client()
	cam_info = get_camera_info(cam)

	cam_media_service = cam.create_media_service()
	cam_profiles_and_tokens = get_camera_profiles(cam_media_service)

	cam_snapshot_uri =  get_snapshot_URI(cam_media_service,cam_profiles_and_tokens[0]['token'] )
	# cam_streaming_rtsp_url = get_rtsp(cam_media_service,cam_profiles_and_tokens[0]['token'])
	get_capabilities(cam_media_service)
	get_snapshot(cam_snapshot_uri)