import requests
from requests import request
import os
import decouple
from helper import read_yaml, form_device_params_from_yaml



NETBOX_URL = 'http://192.168.1.226:8000/api'
FOR_DEVICES = '/dcim/devices/'
FOR_SITES = '/dcim/sites/'
api_token = "49476caca9def74d8526d2ea6d6cb07b35db6edf"

SITES = [
    {
        'name': 'Slough',
        'slug': 'slo'
    }
]

class NetboxAPITokenNotFound(Exception):
    pass

def netbox_headers():
    if api_token is None:
        raise NetboxAPITokenNotFound('NETBOX_API_TOKEN was not found in environmental variables')
    
    headers = {
        'Authorization': 'Token {}'.format(api_token),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return headers

def add_site(name, slug):
 #  api_token = decouple.config("NETBOX_API_TOKEN")
    headers = netbox_headers()
    data = {
        'name': name,
        'slug': slug
    }
    r = requests.post(NETBOX_URL + FOR_SITES, headers=headers, json=data)

    if r.status_code == 201:
        print("Site {} was a success".format(name))
    else:
        r.raise_for_status()
    
def add_sites():
# Retrieve the sites for the SITE dictionary

    for site in SITES:
        add_site(**site)

def add_device(name, device_type_id, site_id, device_role_id):
    headers = netbox_headers()

    data = {
        "name": name,
        "display_name": name,
        "device_type": device_type_id,  
        "site": site_id, 
        "device_role":device_role_id,
        "status": "active"
    }
    print(data)
    if device_role_id is not None:
        data["device_role"] = device_role_id

    r = requests.post(
        NETBOX_URL + FOR_DEVICES, headers=headers, json=data
    )

    if r.status_code == 201:
        print(f"Device {name} was added successfully")
    else:
        r.raise_for_status()

def add_devices():
    parsed_yaml = read_yaml()
    devices_params_gen = form_device_params_from_yaml(parsed_yaml)
    for device_params in devices_params_gen:
        add_device(**device_params)
    print("All devices have been imported")

def main():
    # headers = netbox_headers()
    # add_sites()
    add_devices()

if __name__=='__main__':
    main()