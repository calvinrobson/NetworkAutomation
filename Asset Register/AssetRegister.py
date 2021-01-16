#!/usr/bin/env python3

import yaml
import copy
import pprint
import netdev
import asyncio
from copy import deepcopy
import csv

SITE_NAME = 'btl'

COMMANDS_LIST = [
    'show run | i hostname'
    ]
COMMANDS_LIST1 = [
    'sh version | i Process'
]
COMMANDS_LIST2 = [
    'show version | i IOS'
    ]

def read_yaml(file='devices.yml'):
    """
    Reads devices yaml file and returns dictionary with parsed values
    Args:
        file(str): file to inventory YAML
    Returns:
        dict: parsed YAML values
    """
    with open(file) as f:
        client_devices = yaml.full_load(f.read())
    return client_devices

def connection_paramater(new_yaml, site='all'):
    """
    Pulls the parameters for the asyncio connection.
    Args:
        new_yaml(dict): dictionary with all the YAML logins
    Returns:
        site: name of the site with the default being 'all'
    """

    new_yaml = deepcopy(new_yaml)
    # deepcopy creates a new dictionary copy of new_yaml.
    result = {}
    global_parameter = new_yaml['all']['vars']
    # these are the global parameters, which are the default username and password in devices.yml
    site_detail = new_yaml['all']['groups'].get(site)
    # provides the details of the sites in the devices.yml file
    if site_detail is None:
        raise KeyError('This site {} is not specified in inventory Yaml file'.format(site))
    for host in site_detail['hosts']:
        host_dict = {}
        host_dict.update(global_parameter)
        host_dict.update(host)
        yield host_dict

async def collect_outputs(device_params, commands):
    """
    Collects commands from the dictionary of the device
    Args:
        devices (dict): dictionary where the key is the hostname, value is the netmiko connection dictionary
        commands (list): list of commands to be executed on every device

    Returns:
        dict: key is the hostname, value is string with all outputs
    """
    hostname = device_params.pop('hostname')
    async with netdev.create(**device_params) as connection:
        # for device reference look in the main function at the bottom.
        device_result = []

        for command in commands:
            command_result = await connection.send_command(command)
          #  device_result.append('{0} {1} {0}'.format('=' * 20, command ))
            device_result.append(command_result)

        device_result_string = '\n\n'.join(device_result)
        return device_result_string  

def main():
    new_yaml = read_yaml()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(collect_outputs(device, COMMANDS_LIST))
             for device in connection_paramater(new_yaml, site=SITE_NAME)]
    tasks1 = [loop.create_task(collect_outputs(device, COMMANDS_LIST1))
             for device in connection_paramater(new_yaml, site=SITE_NAME)]
    tasks2 = [loop.create_task(collect_outputs(device, COMMANDS_LIST2))
             for device in connection_paramater(new_yaml, site=SITE_NAME)]
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        print(task.result())
    for task2 in tasks2:
        print(task2.result())
    for task1 in tasks1:
        print(task1.result())        

        
        with open ('test.csv', 'w', newline='') as a:
            write = csv.writer(a)
            write.writerow(['Hostname', 'Serial Number', 'Version and System Image'])
            write.writerow([task.result(), task1.result(), task2.result()])

if __name__ == '__main__':
    main()
