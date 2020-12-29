#!/usr/bin/env python3

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.functions.text import netmiko_send_command

def main():
    with InitNornir("config.yaml") as nr
        result = nr.run(task=netmiko_send_command, command_string="show cdp neighbors")
        print_result(result)

if __name__ == '__main__':
    main()