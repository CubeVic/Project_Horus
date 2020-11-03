from onvif import ONVIFCamera
import asyncio

async def camera_():
    mycam = ONVIFCamera('172.16.18.151', 80, 'admin', 'Ww80503736')
    await mycam.update_xaddrs()
    media_service = mycam.create_media_service()
    profiles = await media_service.GetProfiles()
    print(f'profile {profiles[0].Name} :\n {profiles[0]}')
    with open('A416_profile.txt','w') as file:
        file.write(str(profiles))
    # token = profiles[0].token
    # print(token)
    return await mycam.close()
asyncio.run(camera_())
