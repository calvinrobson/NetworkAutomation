#! usr/bin/env python3

import yaml
from copy import deepcopy
import netmiko
import csv
import re

import logging
import netdev

logging.basicConfig(level=logging.INFO)
netdev.logger.setLevel(logging.DEBUG)


SITENAME = 'Home'
COMMAND = ['show version | i process']

# Regular Expressions to show version serial number
SHOW_VERSION_REGEXP = [
    re.compile(r'(?P<Version>ID\s[A-Z0-9]+$)', re.M)
    ]
    
def read_yaml(path='devices.yml'):
    with open(path) as file:
        device_list = yaml.full_load(file.read())
    return device_list

def pull_yaml_data(parsed_yaml, site='all'):
    parsed_yaml = deepcopy(parsed_yaml)
    result = {}
    credentials = parsed_yaml['all']['vars']
    sites = parsed_yaml['all']['groups'].get(site)
    if sites is None:
        raise KeyError('This site {} is not specified in inventory Yaml file'.format(site))
    for host in sites['hosts']:
        host_dict = {}
        host_dict.update(credentials)
        host_dict.update(host)
        yield host_dict

def netmiko_connection(parameters, commands):
    for device in parameters:
        hostname = device.pop('hostname')
        connect = netmiko.ConnectHandler(**device)
        device_result = ['{0} {1} {0}'.format('' , hostname)]

        for comm in commands:
            command_result = connect.send_command(comm)
            device_result.append(command_result)
        
            connect.disconnect()
        yield device_result

def get_serial_number(cli_output):
    result_dictionary = dict()
    for regexp in SHOW_VERSION_REGEXP:
        result_dictionary.update(regexp.search(cli_output).groupdict())
    return result_dictionary


def main():
    parsed_yaml = read_yaml()
    connection_parameters = pull_yaml_data(parsed_yaml, site=SITENAME)
    for device_result in netmiko_connection(connection_parameters, COMMAND):
        with open ('test.csv', 'w', newline='') as a:
            write = csv.writer(a)
            write.writerow(['Hostname', 'Serial Number', 'Version and System Image'])
            write.writerow([device_result,'',''])

    
if __name__ == '__main__':
    main()
