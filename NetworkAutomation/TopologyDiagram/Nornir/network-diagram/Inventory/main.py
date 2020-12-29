#!/usr/bin/env python3

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

def main():
    with InitNornir("config.yaml") as nr:
        result = nr.run(task=netmiko_send_command, command_string="show cdp neighbor", use_textfsm=True)
        print_result(result)

if __name__ == '__main__':
    main()
