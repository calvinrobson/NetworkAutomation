#!/usr/bin/env python3

from copy import deepcopy
from pprint import pprint
import netmiko
import yaml

import logging
import netdev

logging.basicConfig(level=logging.INFO)
netdev.logger.setLevel(logging.DEBUG)

SITE_NAME = 'Home'

COMMANDS_LIST = [
    'show clock',
    'show ip interface brief'
]

def read_yaml(path='inventory.yml'):

    """
    Reads inventory  yaml file and returns dictionary with parsed values
    Args:
        path(str): path to inventory YAML
    Returns:
        dict: parsed YAML values
    """
    with open(path) as f:
        yaml_content = yaml.full_load(f.read())
    return yaml_content

def form_connection_params_from_yaml(parsed_yaml, site='all'):
    """
    Form Dictionary of netmiko connections parameters for all devices on the site

    Args:
        parsed_yaml (dict): dictionary with parsed yaml file
        site(str): name of the site. Default is 'all'
    
    Returns:
        dict: key is hostname, value is dictionary containing connection parameters for netmiko

    """

    parsed_yaml = deepcopy(parsed_yaml)
    result = {}
    global_params = parsed_yaml['all']['vars'] # username and password.
    site_dict = parsed_yaml['all']['groups'].get(site) # the sites such as Home.
    if site_dict is None:
        raise KeyError('This site {} is not specified in inventory Yaml file'.format(site))
    for host in site_dict['hosts']: 
        host_dict = {}
        host_dict.update(global_params)
        host_dict.update(host)
        yield host_dict


def collect_outputs(devices, commands):
    """
    Collects commands from the dictionary of the device
    Args:
        devices (dict): dictionary where the key is the hostname, value is the netmiko connection dictionary
        commands (list): list of commands to be executed on every device

    Returns:
        dict: key is the hostname, value is string with all outputs
    """
    for device in devices:
        hostname = device.pop('hostname')
        connection = netmiko.ConnectHandler(**device)
        device_result = ['{0} {1} {0}'.format('=' * 20, hostname)]

        for command in commands:
            command_result = connection.send_command(command)
            device_result.append('{0} {1} {0}'.format('=' * 20, command ))
            device_result.append(command_result)
            
        device_result_string = '\n\n'.join(device_result)
        connection.disconnect()
        yield device_result_string

def main():
    parsed_yaml = read_yaml()
    connection_params = form_connection_params_from_yaml(parsed_yaml, site=SITE_NAME)
    pprint(connection_params)
    for device_result in collect_outputs(connection_params, COMMANDS_LIST):
        print(device_result)

if __name__ == '__main__':
    main()
