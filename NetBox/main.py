import requests

import os

NETBOX_URL = 'http://192.168.1.226:8000/api'
FOR_DEVICES = '/dcim/devices/'
FOR_SITES = '/dcim/sites/'

def add_devices(name='', slug=''):
    r = request.post(NETBOX_URL + FOR_DEVICES, data)

def add_sites():
    r = request.