import netifaces as ni

def get_local_ip():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface == 'lo':
            continue
        addresses = ni.ifaddresses(interface)
        if ni.AF_INET in addresses:
            ip_address = addresses[ni.AF_INET][0]['addr']
            return ip_address

print("Local IP address:", get_local_ip())
