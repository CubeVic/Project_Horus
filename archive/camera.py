import sensecam_discovery

cameras = sensecam_discovery.discover()

print(cameras)


#--------------------------------------------------------
#  the class to get more info from the camera was Camera
# now is not working, something with the media ( ONVIF) 
# therefore i will use just the discovery 
#---------------------------------------------------------

# def get_info_cam(cam):
#     try:
#         camera = Camera(cam, 'admin', '123456')
#         print(f'camera IP: {cam}')
#         print(f'Hostname: {camera.hostname}')
#         print(f'Manufacture: {camera.manufacturer}')
#         print(f'Camera Model: {camera.model}')
#         print(f'Camera Firmware: {camera.firmware_version}')
#         # print(f'Camera Mac addess: {camera.mac_address}')# provide the same value that the serial numbers
#         print(f'Hardware ID: {camera.hardware_id}') 
#         print(f'Resolution Available: {camera.resolutions_available}')
#         print(f'Fame rate range: {camera.frame_rate_range}')
#         print(f'Date: {camera.date}')
#         print(f'Time: {camera.time}')
#         print(f'Is PTZ? {camera.is_ptz}')
#     except Exception as e:
#         print("\n {}, {} \n".format(cam, e))

# for cam in set(cameras):
#     get_info_cam(cam)