""" Streaming example for python-onvif-zeep-async """
import asyncio

from onvif import ONVIFCamera

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
	mycam = ONVIFCamera("172.16.18.110", 80, "admin", "123456")
	await mycam.update_xaddrs()
	media_service = mycam.create_media_service()

	# get Camera Profiles

	profiles = await media_service.GetProfiles()
	# print(profiles)
	print(f'Number of profiles available: {len(profiles)}')
	for profile in profiles:
		print(f'- Profile Name: {profile.Name} ')
		print(f'	- Token: {profile.token}')
	

	# use the first profile
	token = profiles[0].token

	#Get all encoder configuration
	configuration_list = await media_service.GetVideoEncoderConfigurations()

	#Use the first profile of the configuration
	video_encoder_configuration = configuration_list[0]
	print(video_encoder_configuration)

	#get Video encoder configuration option
	option = await media_service.GetVideoEncoderConfigurationOptions({"ProfileToken": token})
	# print(option)

	#Setup Stream configuration
	video_encoder_configuration.Encoding = "H264"

	#Setup Resolution
	video_encoder_configuration.Resolution.Width = option.H264.ResolutionsAvailable[0].Width
	video_encoder_configuration.Resolution.Height = option.H264.ResolutionsAvailable[0].Height
	print(f'Resolution:\n- Width: {video_encoder_configuration.Resolution.Width}')
	print(f'- Height: {video_encoder_configuration.Resolution.Height}')

	await mycam.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(media_profile_configuration())