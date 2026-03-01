import sys
from ncclient import manager

devices = {
    "srl": {
        "host": "srl-01",
        "port": 830,
        "username": "admin",
        "password": "NokiaSrl1!",
        "hostkey_verify": False,
    },
    "ceos": {
        "host": "ceos-01",
        "port": 830,
        "username": "admin",
        "password": "admin",
        "hostkey_verify": False,
    },
}


if len(sys.argv) < 2:
    print(f"Expecting: {sys.argv[0]} <device>")
    sys.exit(0)

device = sys.argv[1]
if device in devices:
    with manager.connect(**devices[device]) as m:
        # Filter for YANG model capabilities specifically
        caps = [c for c in m.server_capabilities if "module=" in c]
        for cap in sorted(caps):
            print(cap)
else:
    print(f"Avaliable devices are: {', '.join(devices.keys())}.")
