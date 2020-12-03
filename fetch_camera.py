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

def get_onvifCamera_client(username: str, password: str):
	""" get the onvif.client.ONVIFCamera"""
	try:
		camera = ONVIFCamera('172.16.18.162',80,username,password)
	except Exception as e:
		# logger_file.error(f"Getting camera object ...Failed")
		# logger.error(f'Getting camera object ...Failed')
		raise ONVIFError(e)

	return camera

def get_camera_info(devicemgmt_service):
	""" get back information about the device
	such as: 
	* Manufacture
	* Model
	* Firmware version
	* Serial Number
	* Hardware ID
	"""
	camera_info = devicemgmt_service.GetDeviceInformation()
	# create a dictionary with camera info
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
	return snapshot_uri

def get_snapshot(url, username: str, password: str):
	""" get the snapshot 
		TODO:
		- [x] Automate Auth
	"""
	response = requests.get(url, auth=(username, password))
	img = Image.open(BytesIO(response.content))
	if_save = input("do you want to save the snapshoot: ") or False
	
	if if_save.upper() in ('Y','YES'):
		snapshoot_name = 'snashoot.png'
		img.save(snapshoot_name)
		print(f"\n--->Snatpshoot save - {snapshoot_name}\n")
		img.show()# to show the image
	else:
		print("\n--->Snatpshoot no saved\n")

# def get_rtsp(media_service, token):
# 	""" get the URI for the stream using RTSP """

# 	# TODO
# 	stream_setup = {'StreamSetup' : 
# 						{ 'Stream' : 'RTP_unicast', 
# 						  'Transport' : { 'Protocol' : 'RTSP' } 
# 						  }, 
# 						'ProfileToken' : token}
# 	uri = media_service.GetStreamUri(stream_setup)
# 	rtsp_stream = uri.Uri
# 	print(f'uri: {uri.Uri}')
# 	return rtsp_stream

def get_capabilities(media_service, profile_token):
	""" get the capabilities of the device, such as 
	* snapshotUri
	* Rotation
	* video Sources
	* OSD
	* Streaming capabilities

	There are more info in https://www.onvif.org/ver10/media/wsdl/media.wsdl
	"""
	cam_snapshot_uri =  get_snapshot_URI(cam_media_service,profile_token)
	capabilities = media_service.GetServiceCapabilities()
	profile_capabilities = capabilities['ProfileCapabilities'] 
	streaming_capabilities = capabilities['StreamingCapabilities']
	snapshot = capabilities['SnapshotUri']
	snapshot_uri = cam_snapshot_uri
	rotatio_status = capabilities['Rotation']
	#creating a dictionary with the capabilities
	cam_capabilities = { 'ProfileCapabilities': {'Max_Number_Of_Profiles': profile_capabilities['MaximumNumberOfProfiles']},
							'StreamingCapabilities' : {
										'RTPMulticast' : streaming_capabilities['RTPMulticast'],
										'RTPTCP' : streaming_capabilities['RTP_TCP'],
										'RTPRTSPTCP' : streaming_capabilities['RTP_RTSP_TCP']},
							'SnapshotURI' :{'snapshotUri' :snapshot,
											'URI': snapshot_uri },
							'Rotation' : rotatio_status
						}

	return cam_capabilities

if __name__ == "__main__":

	# load_logger()

	username =  input('Input username: ') or 'admin'
	password = input('Input Password: ') or '123456'

	cam = get_onvifCamera_client(username, password)
	cam_devicemgmt_service = cam.create_devicemgmt_service()
	cam_info = get_camera_info(cam_devicemgmt_service)

	cam_media_service = cam.create_media_service()
	cam_profiles_and_tokens = get_camera_profiles(cam_media_service)
	cam_profile_token = cam_profiles_and_tokens[0]['token']
	
	cam_capabilities = get_capabilities(cam_media_service,cam_profile_token)
	get_snapshot(cam_capabilities['SnapshotURI']['URI'], username, password)
	# get_rtsp(cam_media_service,cam_profile_token)
	
	###### Test area
	print(cam_devicemgmt_service.GetNetworkInterfaces())