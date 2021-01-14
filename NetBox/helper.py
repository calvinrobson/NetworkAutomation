import yaml

from copy import deepcopy

SITES = {
    'cape-town':6,
    'smt':5,
    'edm':4,
}

DEVICE_ROLES = {
    'access':1,
    'edge':2,
    'cpe':3,
}

DEVICE_TYPES = {
    'cisco-1710':2,
}

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

def form_device_params_from_yaml(parsed_yaml):
    """
    Form Dictionary of device parameters for all devices on the site to import to Netbox

    Args:
        parsed_yaml (dict): dictionary with parsed yaml file
    
    Returns:
        dict: key is hostname, value is dictionary containing connection parameters to import to Netbox

    """

    parsed_yaml = deepcopy(parsed_yaml)
    for site_dict in parsed_yaml["all"]["sites"]:
        site_name = site_dict["name"]
        site_id = SITES.get(site_name)
        for host_dict in site_dict["hosts"]:
            device_params = dict()
            device_params["name"] = host_dict["hostname"]
            device_params["site_id"] = site_id
            device_params["device_type_id"] = DEVICE_TYPES.get(
                host_dict.get("device_type")
            )
            device_params["device_role_id"] = DEVICE_ROLES.get(
                host_dict.get("device_role")
            )
            yield device_params