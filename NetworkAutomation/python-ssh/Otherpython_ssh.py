from netmiko import ConnectHandler
from datetime import datetime
from copy import deepcopy
import yaml

SH_COMMANDS = [
    "show ip route | beg Gate", "show ip interface brief | excl admin"
]

def read_yaml(path="inventory.yml"):
    with open(path) as f:
        yaml_content = yaml.safe_load(f.read())
    return yaml_content

def get_connection_parameters(parsed_yaml):
    parsed_yaml = deepcopy(parsed_yaml)
    login_credentials = parsed_yaml["all"]["vars"]
    for site_dict in parsed_yaml["all"]["sites"]:
        for host in site_dict["hosts"]:
            host_dict = {}
            host_dict.update(login_credentials)
            host_dict.update(host)
            yield host_dict

def show_commands(devices, commands):
    for device in devices:
        start_time = datetime.now()
        hostname = device.pop("hostname")
        connection = ConnectHandler(**device)
        device_result = ["{0} {1} {0}".format("=" * 15, hostname)]

        for command in commands:
            command_result = connection.send_command(command)
            device_result.append("{0} {1} {0}".format("=" * 10, command))
            device_result.append(command_result)

        device_result_string = "\n\n".join(device_result)
        connection.disconnect()
        device_result_string += "\nElapsed time: " + str(datetime.now() - start_time)
        yield device_result_string

def main():
    parsed_yaml = read_yaml()
    print(parsed_yaml)
    connection_parameters = get_connection_parameters(parsed_yaml, site_name=SITE_NAME)

    for device_result in show_commands(connection_parameters, SH_COMMANDS):
        print(device_result)


if __name__ == "__main__":
    main()