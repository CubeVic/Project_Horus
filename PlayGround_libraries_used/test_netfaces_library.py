""" test file in order to understand more about the library netifaces """
import netifaces

print(f'\n Interfaces: {netifaces.interfaces()} \n')

""" there are some constants
AF_LINK --> Ethernet (link layer interface)
AF_INET --> Normal internet address
AF_INET6 -> IPV6

{ 18: [...], 2: [...], 30: [...] }
Each of the numbers refers to a particular address family. 
In this case, we have three address families listed; on my system, 
18 is AF_LINK (which means the link layer interface, e.g. Ethernet), 
2 is AF_INET (normal Internet addresses), 
and 30 is AF_INET6 (IPv6).
""" 
def extract_scope(interface):
	if netifaces.AF_INET in netifaces.ifaddresses(interface):
		ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
		return ip


scope = None 
if not scope:
	# extrat the IP "scope" of the IP range of the Ethernet interface
	ips = list(map(extract_scope,netifaces.interfaces()))

# Extract the first two numbers of the address
scope = ['.'.join(ip.split('.')[:2]) for ip in ips if ip]
# ['127.0', '192.168']
print(scope) #the scope, 

################################################
####    I create a new script                ###
####    called: "fetch_ipaddress_iface.py"   ###
####    is a refined version of this script  ###
################################################