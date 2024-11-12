import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

R1_IP_Address = os.getenv("R1_IP_ADDRESS")
R2_IP_Address = os.getenv("R2_IP_ADDRESS")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

R1 = {
    "host": R1_IP_Address,
    "username": "cisco",
    "password": "cisco"
}

R2 = {
    "host": R2_IP_Address,
    "username": "cisco",
    "password": "cisco"
}

headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

def configure_interface(device, interface, ip_address, netmask):
    url = f"https://{device['host']}/restconf/data/ietf-interfaces:interfaces/interface={interface}"
    payload = {
        "ietf-interfaces:interface": {
            "name": interface,
            "description": "Configured by RESTCONF",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip_address,
                        "netmask": netmask
                    }
                ]
            }
        }
    }
    response = requests.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(device['username'], device['password']), verify=False)
    return response.status_code, response.text

def configure_static_route(device, prefix, next_hop):
    url = f"https://{device['host']}/restconf/data/ietf-routing:routing/routing-instance=default/routing-protocols/routing-protocol=static,1/static-routes/ipv4/route={prefix}"
    payload = {
        "ietf-routing:route": {
            "destination-prefix": prefix,
            "next-hop": {
                "next-hop-address": next_hop
            }
        }
    }
    response = requests.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(device['username'], device['password']), verify=False)
    return response.status_code, response.text

print(configure_interface(R1, "GigabitEthernet0/0", "10.10.10.1", "255.255.255.0"))
print(configure_static_route(R1, "10.10.20.0/24", "10.10.10.2"))
print(configure_static_route(R1, "0.0.0.0/0", "10.10.10.2"))

print(configure_interface(R2, "GigabitEthernet0/0", "10.10.20.1", "255.255.255.0"))
print(configure_interface(R2, "Loopback1", "10.10.30.1", "255.255.255.0"))
print(configure_static_route(R2, "10.10.10.0/24", "10.10.20.2"))