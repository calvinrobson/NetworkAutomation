import requests
from requests import request
import os
import decouple
import json
from django.utils.text import slugify
from copy import deepcopy


NETBOX_URL = 'http://192.168.1.226:8000/api'
FOR_DEVICES = '/dcim/devices/'
FOR_SITES = '/dcim/sites/'
TENANCY_GROUP = '/tenancy/tenant-groups/'
api_token = "49476caca9def74d8526d2ea6d6cb07b35db6edf"

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
    r = requests.post(NETBOX_URL + TENANCY_GROUP, headers=headers, json=data)

    if r.status_code == 201:
        print('Site {} was a success'.format(name))
    else:
        r.raise_for_status()
    
def add_sites():
# Retrieve the sites for the SITE dictionary
    with open('sites.json', 'r') as myfile:
        data=myfile.read()
        obj = json.loads(data)
    for items in obj:
        kite = items['name']
        name = items['slug']
        add_site(kite, name)

def main():
    add_sites()

if __name__=='__main__':
    main()