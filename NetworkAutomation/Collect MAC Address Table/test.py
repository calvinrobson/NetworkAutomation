#!/usr/bin/env python3

import yaml

with open('devices.yml') as f:
    
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)