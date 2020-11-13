""" Small script to fetch the ipaddress of the network interface
In this case focus in the Ethernet and the internet (need to clarify that concept in the future)
main goal is get a subnet of a scope to later look for devices withing that scope
Example: Scope = 192.168  a device with 192.168.0.100 will be within that scope"""
from netifaces import interfaces, ifaddresses, AF_INET

# AF_INET - Address Family - Normal internet address

#Todo:
"""set logging system for this script"""
print(f'\n Interfaces: {interfaces()} \n------------>\n')

def extract_scope_(interface):
	""" it willl filter the Ethernet/internet interface
	and return just the IP address """
	if AF_INET in ifaddresses(interface):
		print(f'interface {interface} : {ifaddresses(interface)[AF_INET]}')
		ip_address = ifaddresses(interface)[AF_INET][0]['addr']
		return ip_address


scope = None 

# extrat the IP "scope" of the IP range of the Ethernet interface
if not scope : ips = list(map(extract_scope_,interfaces())) 

# Extract the first two numbers of the address
scope = ['.'.join(ip.split('.')[:2]) for ip in ips if ip]

print(f'\n------------>\nscope {scope}') #the scope,
# ['127.0', '192.168'] 