import yaml

path = 'inventory.yml'

def open_yml():
    with open(path) as f:
        yaml_content = yaml.full_load(f.read())
        password = yaml_content["all"]["groups"]["Home"]["hosts"]["password"]
    return password

def main():
    print(open_yml())

if __name__ == '__main__':
    main()