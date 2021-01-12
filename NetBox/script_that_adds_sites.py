import requests
from requests import request
import os
import decouple


NETBOX_URL = 'http://192.168.1.226:8000/api'
FOR_DEVICES = '/dcim/devices/'
FOR_SITES = '/dcim/sites/'
api_token = "49476caca9def74d8526d2ea6d6cb07b35db6edf"

SITES = [
    {
        'name': 'Cape Town',
        'slug': 'cape-town'
    }
    
]

class NetboxAPITokenNotFound(Exception):
    pass

def add_site(name, slug):
 #   api_token = decouple.config("NETBOX_API_TOKEN")
    if api_token is None:
        raise NetboxAPITokenNotFound('NETBOX_API_TOKEN was not found in environmental variables')
    
    headers = {
        'Authorization': 'Token {}'.format(api_token),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'name': name,
        'slug': slug
    }
    r = requests.post(NETBOX_URL + FOR_SITES, headers=headers, json=data)

    if r.status_code == 201:
        print(f"Site {} was a success".format(name))
    else:
        r.raise_for_status()
    
def add_sites():
# Retrieve the sites for the SITE dictionary

    for site in SITES:
        add_site(**site)

def main():
    add_sites()

if __name__=='__main__':
    main()