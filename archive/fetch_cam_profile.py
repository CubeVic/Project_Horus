import asyncio
from onvif import ONVIFCamera

async def fetch_profiles():
    mycam = ONVIFCamera('172.16.18.110', 80, 'admin', '123456')
    # await mycam.update_xaddrs()
    media_service = mycam.create_media_service()
    profiles = await media_service.GetProfiles()
    print(f'profile {profiles[0].Name} :\n {profiles[0]}')
    with open('profile.txt','w') as file:
        file.write(str(profiles))
    # token = profiles[0].token
    # print(token)
    return await mycam.close()

# cam_ip = input("Camera IP: ") or "172.16.18.147"
# cam_port = input("Camera cam_port: ") or 80
# cam_user = input("Camera User: ") or 'admin'
# cam_password = input("Camera password: ") or '123456'
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_profiles())