""" Streaming example for python-onvif-zeep-async """
import asyncio

from onvif import ONVIFCamera

from PIL import Image
import io



async def media_profile_configuration():
	"""
	A media profile consists of configuration entities such as:
		* video/audio.
		* source configuration. 
		* video/audio encoder configuration.
		* PTZ configuration. 
	This use case describes how to change one configuration entity 
	which has been already added to the media profile.
	"""

	# Create a media service 
	mycam = ONVIFCamera("172.16.18.162", 80, "admin", "123456")
	await mycam.update_xaddrs()
	media_service = mycam.create_media_service()

	# get Camera Profiles

	profiles = await media_service.GetProfiles()
	print(profiles[0])
	print(f'Number of profiles available: {len(profiles)}')
	for profile in profiles:
		print(f'Profile Name: {profile.Name} ')
		print(f'	- Token: {profile.token}')
	

	# use the first profile
	token = profiles[0].token

	#Get all encoder configuration
	configuration_list = await media_service.GetVideoEncoderConfigurations()
	# print(f'Configuration list: {configuration_list}')

	#Use the first profile of the configuration
	video_encoder_configuration = configuration_list[0]
	# print(video_encoder_configuration)

	#get Video encoder configuration option
	options = await media_service.GetVideoEncoderConfigurationOptions({"ProfileToken": token})
	# print(f'options : {options}')

	#Setup Stream configuration
	video_encoder_configuration.Encoding = "H264"

	#Setup Resolution
	video_encoder_configuration.Resolution.Width = options.H264.ResolutionsAvailable[0].Width
	video_encoder_configuration.Resolution.Height = options.H264.ResolutionsAvailable[0].Height
	print(f'Resolution:\n- Width: {video_encoder_configuration.Resolution.Width}')
	print(f'- Height: {video_encoder_configuration.Resolution.Height}')

	#Setup Quality
	video_encoder_configuration.Quality = options.QualityRange.Min # yes without the H264
	print(f'Quality: {video_encoder_configuration.Quality}')

	#SetUp FrameRate
	video_encoder_configuration.RateControl.FrameRateLimit = options.H264.FrameRateRange.Min
	print(f'FrameRate: {video_encoder_configuration.RateControl.FrameRateLimit}')

	#Setup EncodingInterval
	video_encoder_configuration.RateControl.EncodingInterval = options.H264.EncodingIntervalRange.Min
	print(f'Encoding Interval: {video_encoder_configuration.RateControl.EncodingInterval}')

	#Setup Bitrate
	# video_encoder_configuration.RateControl.BitrateLimit = options.Extension.H264[0].BitrateRange[0].Min[0]

	#Create request type instance
	request = media_service.create_type('SetVideoEncoderConfiguration')
	request.Configuration = video_encoder_configuration
    # ForcePersistence is obsolete and should always be assumed to be True
	request.ForcePersistence = True
    # Set the video encoder configuration
	await media_service.SetVideoEncoderConfiguration(request)

	uri_snapshot = await mycam.get_snapshot_uri(token)
	print(f'snapshot URI: {uri_snapshot}')
	snapshot = await mycam.get_snapshot(token, basic_auth=True)
	# print(type(snapshot))

	# #read the bytes
	# im = Image.open(io.BytesIO(snapshot))
	# #display the image
	# im.show() 
	# thumbnail_size = 128,128
	# im.thumbnail(size)
	# im.show()
	stream_setup = {'StreamSetup' : 
	{'Stream' : 'RTP_unicast', 
	'Transport' : { 
	'Protocol' : 'TCP' }}, 
	'ProfileToken' : token}
	print(stream_setup)
	uri = await media_service.GetStreamUri(stream_setup)
	print(uri)
	await mycam.close()

    # rtsp_stream = uri.Uri
    # print(f'uri: {uri.Uri}')
    # return rtsp_stream

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(media_profile_configuration())
	


##########################################################
#####                                               ######
#####     Example of configuration of a stream      ######
#####												######
##########################################################