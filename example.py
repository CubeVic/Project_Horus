
from onvif import ONVIFCamera


mycam = ONVIFCamera('172.16.18.110', 80, 'admin', '123456', '/etc/onvif/wsdl/')
await mycam.update_xaddrs()

resp = await mycam.devicemgmt.GetHostname()
print('My camera`s hostname: ' + str(resp.Name))