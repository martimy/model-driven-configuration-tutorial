#!/usr/bin/env python3

import sys
from ncclient import manager

# Device connection parameters
DEVICES = {
    "srl-01": {
        "host": "srl-01",
        "port": 830,
        "username": "admin",
        "password": "NokiaSrl1!",
        "hostkey_verify": False,
    },
    "srl-02": {
        "host": "srl-02",
        "port": 830,
        "username": "admin",
        "password": "NokiaSrl1!",
        "hostkey_verify": False,
    },
    "ceos-01": {
        "host": "ceos-01",
        "port": 830,
        "username": "admin",
        "password": "admin",
        "hostkey_verify": False,
    },
}

def get_capabilities(m):
    """Prints the YANG modules supported by the device."""
    caps = [c for c in m.server_capabilities if "module=" in c]
    for cap in sorted(caps):
        print(cap)

def get_config(m, filter_xml):
    """Retrieves and prints the network-instance configuration."""
    config = m.get_config(source="running", filter=("subtree", filter_xml))
    print(config.data_xml)

def save_schema(m, schema_name):
    """Downloads a YANG schema and saves it to a file."""
    schema = m.get_schema(schema_name)
    filename = f"{schema_name}.yang"
    with open(filename, "w") as f:
        f.write(schema.data)
    print(f"Schema saved to {filename}")

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <device> <action> [xml-filter | schema-name ]")
        print(f"Devices: {', '.join(list(DEVICES.keys()))}")
        print("Actions: capabilities, config, schema")
        sys.exit(1)

    device_name = sys.argv[1]
    action = sys.argv[2]

    if device_name not in DEVICES:
        print(f"Error: Unknown device '{device_name}'. Available: {', '.join(list(DEVICES.keys()))}")
        sys.exit(1)

    # Connect to the device and perform the action
    with manager.connect(**DEVICES[device_name]) as m:
        if action == "capabilities":
            get_capabilities(m)
        elif action == "config":
            if len(sys.argv) < 4:
                print("Error: Action 'config' requires a xml-filter.")
                print(f"Usage: {sys.argv[0]} {device_name} config <xml-filter>")
                sys.exit(1)
            get_config(m, sys.argv[3])
        elif action == "schema":
            if len(sys.argv) < 4:
                print("Error: Action 'schema' requires a schema name.")
                print(f"Usage: {sys.argv[0]} {device_name} schema <schema-name>")
                sys.exit(1)
            save_schema(m, sys.argv[3])
        else:
            print(f"Error: Unknown action '{action}'.")

if __name__ == "__main__":
    main()
