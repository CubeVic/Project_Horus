from onvif import ONVIFCamera
import asyncio

async def fetch_profiles(cam_ip, cam_port, cam_user, cam_password ):
    mycam = ONVIFCamera(cam_ip, cam_port, cam_user, cam_password)
    await mycam.update_xaddrs()
    media_service = mycam.create_media_service()
    profiles = await media_service.GetProfiles()
    print(f'profile {profiles[0].Name} :\n {profiles[0]}')
    with open('profile.txt','w') as file:
        file.write(str(profiles))
    # token = profiles[0].token
    # print(token)
    return await mycam.close()

cam_ip = input("Camera IP: ")
cam_port = input("Camera cam_port: ") or 80
cam_user = input("Camera User: ") or 'admin'
cam_password = input("Camera password: ") or '123456'
asyncio.run(fetch_profiles(cam_ip, cam_port, cam_user, cam_password))