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

SHOW_VERSION_REGEXP = [
    re.compile(r'(?P<Version>ID\s[A-Z0-9]+)', re.M)
    ]


def read_yaml(path = 'devices.yml'):
    with open(path) as f:
        devices = yaml.full_load(f)
    return devices

def devices_yaml(logins, site='all'):
    logins = deepcopy(logins)
    credentials = logins['all']['vars']
    sites = logins['all']['groups'].get(site)
    for host in sites['hosts']:
        host_dict = {}
        host_dict.update(credentials)
        host_dict.update(host)
        yield host_dict

def get_serial_number(cli_output):
    result_dictionary = dict()
    for regexp in SHOW_VERSION_REGEXP:
        result_dictionary.update(regexp.search(cli_output).groupdict())
    return result_dictionary

def netmiko_connection(parameters):
    for device in parameters:
        hostname = device.pop('hostname')
        connect = netmiko.ConnectHandler(**device)
        version = get_serial_number(connect.send_command('show version'))
        version_result = print(version)
        with open ('test.csv', 'w', newline='\r\n') as a:
            write = csv.writer(a)
            columns = write.writerow(['Hostname', 'Serial Number', 'Version and System Image'])
            write.writerow([version_result,hostname,''])
        connect.disconnect()

def main():
    logins = read_yaml()
    connection_parameters = devices_yaml(logins, site=SITENAME)
    netmiko_connection(connection_parameters)

if __name__ == '__main__':
    main()
