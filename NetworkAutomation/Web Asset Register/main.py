#!/usr/bin/env python3
import netmiko

host = input("Enter the CPE's IP: ")
username = input("Enter the CPE's username: ")
password = input("Enter the CPE's password: ")

device = {
    'device_type': 'cisco_ios'
    'host': host,
    'username': username,
    'password': password,
}

def main():
    connection = ConnectHandler(***device)
    output = connection.send_command("show version", use_textfsm=True)
    print(output)

if __name__ == "__main__":
    main()

    