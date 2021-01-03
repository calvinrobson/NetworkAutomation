#!/usr/bin/env python3

import yaml 
from netmiko import ConnectHandler
from decouple import config
import logging
import re
import csv

INVENTORY = 'mac_address_table_inventory.yml'

TEST_IP = ['192.168.16.131', '192.168.129.139']

SHOW_VERSION_REGEXP = [
    re.compile(r'(?P<Version>ID\s[A-Z0-9]+$)', re.M)
    ]

GLOBAL_PARAMS = {
    'device_type':'cisco_ios',
    'username':'calvin',
    'password':'password',
    'secret':'password'
}
def read_yaml(file_name = INVENTORY):
    with open(file_name) as f:
        result = yaml.full_load(f)
    return result

def get_routers_ip():
    return read_yaml()['routers']

def connection(host):
    device_params = GLOBAL_PARAMS.copy()
    device_params['ip'] = host
    connection = ConnectHandler(**device_params)

    version = get_serial_number(connection.send_command('show version'))
    with open ('test.csv', 'w', newline='') as a:
            write = csv.writer(a)
            write.writerow(['Hostname', 'Serial Number', 'Version and System Image'])
            write.writerow([version,'',''])


    connection.disconnect()
    
def get_serial_number(cli_output):
    result_dictionary = dict()
    for regexp in SHOW_VERSION_REGEXP:
        result_dictionary.update(regexp.search(cli_output).groupdict())
    return result_dictionary

def main():
    ip_list = TEST_IP
    for ip in ip_list:
        connection(ip)
        


if __name__ == '__main__':
    main()