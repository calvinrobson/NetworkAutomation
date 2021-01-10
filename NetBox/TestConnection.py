import netmiko
from netmiko import ConnectHandler

host = input("Enter IP address: ")

account = {
    'device_type': 'cisco_ios',
    'host':  host,
    'username': 'calvin',
    'password': 'password',
    'secret': 'password',
}

net_connect = ConnectHandler(**account)
connect = net_connect.send_command('show version')

print(connect)