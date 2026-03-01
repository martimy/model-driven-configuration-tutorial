import sys
import json
from pygnmi.client import gNMIclient

# Device connection parameters
DEVICES = {
    "srl-01": {
        "target": ("srl-01", 57400),
        "username": "admin",
        "password": "NokiaSrl1!",
        "skip_verify": True,
    },
    "srl-02": {
        "target": ("srl-02", 57400),
        "username": "admin",
        "password": "NokiaSrl1!",
        "skip_verify": True,
    },
    "ceos-01": {
        "target": ("ceos-01", 6030),
        "username": "admin",
        "password": "admin",
        "insecure": True,
    },
}

def get_capabilities(gc):
    """Prints the capabilities of the device."""
    capabilities = gc.capabilities()
    caps = [
        f'{c["name"]}, {c["organization"]}, {c["version"]}'
        for c in capabilities["supported_models"]
    ]
    for cap in sorted(caps):
        print(cap)

def get_config(gc, path):
    """Retrieves and prints configuration."""
    result = gc.get(path=[path], datatype="config")
    # path should be a list
    # Using json.dumps for pretty printing the result
    print(json.dumps(result, indent=2))

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <device> <action> [path]")
        print(f"Devices: {', '.join(list(DEVICES.keys()))}")
        print("Actions: capabilities, config")
        sys.exit(1)

    device_name = sys.argv[1]
    action = sys.argv[2]

    if device_name not in DEVICES:
        print(f"Error: Unknown device '{device_name}'. Available: {', '.join(list(DEVICES.keys()))}")
        sys.exit(1)

    # Connect to the device and perform the action
    with gNMIclient(**DEVICES[device_name]) as gc:
        if action == "capabilities":
            get_capabilities(gc)
        elif action == "config":
            if len(sys.argv) < 4:
                print("Error: Action 'config' requires a path.")
                print(f"Usage: {sys.argv[0]} {device_name} config <path>")
                sys.exit(1)
            get_config(gc, sys.argv[3])
        else:
            print(f"Error: Unknown action '{action}'.")

if __name__ == "__main__":
    main()
