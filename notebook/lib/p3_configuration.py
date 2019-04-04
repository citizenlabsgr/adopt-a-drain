import json
from pprint import pprint

def get_configuration(filename='p3_configuration.json'):
    return json.load(open(filename))

def main():

    rc = get_configuration()

    print('rc: ', rc)
    pprint(rc)

if __name__ == "__main__":
    # execute only if run as a script
    main()