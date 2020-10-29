from onvif import ONVIFCamera
import asyncio

async def camera_():
    mycam = ONVIFCamera('172.16.18.130', 80, 'admin', '123456')
    await mycam.update_xaddrs()
    media_service = mycam.create_media_service()
    profiles = await media_service.GetProfiles()
    print(profiles)
    return await mycam.close()
asyncio.run(camera_())
