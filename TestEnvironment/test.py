import json 
from copy import deepcopy

with open('sites.json', 'r') as myfile:
    data=myfile.read()
    obj = json.loads(data)
for items in obj:
    kite = items['name']
    name = items['slug']
    print(kite)