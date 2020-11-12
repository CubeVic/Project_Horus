import asyncio
from onvif import ONVIFCamera

async def streaming():
	mycam = ONVIFCamera("172.16.18.110", 80, "admin", "123456")
	await mycam.update_xaddrs()
	media_service = mycam.create_media_service()
	profiles = await media_service.GetProfiles()
	token = profiles[0].token
	print(profiles[0])
	stream_setup = {'StreamSetup' : {'Stream' : 'RTP_unicast',
										'Transport':{'Protocol':'UDP'}},
					'ProfileToken': token}
	print(stream_setup)
	uri = await media_service.GetStreamUri({'StreamSetup':{'Stream' : 'RTP_unicast',
															'Transport':{'Protocol':'UDP'}},
											'ProfileToken':token})
	print(uri)
	print(media_service)
	print(token)
	await mycam.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(streaming())