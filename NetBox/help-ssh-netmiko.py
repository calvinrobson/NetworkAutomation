#!/usr/bin/env python3

import netmiko
from .yamlreader import read_yaml, form_connection_params_from_yaml

import logging
import netdev

logging.basicConfig(level=logging.INFO)
netdev.logger.setLevel(logging.DEBUG)

SITE_NAME = 'Home'

COMMANDS_LIST = [
    'show clock',
    'show ip interface brief'
]

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
