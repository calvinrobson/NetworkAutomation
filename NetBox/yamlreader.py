import yaml

from copy import deepcopy


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

