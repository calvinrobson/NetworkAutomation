import json 
from copy import deepcopy

with open('sites.json', 'r') as myfile:
    obj = json.loads(data)
    
for items in obj ['name']['slug']:
    print(items)