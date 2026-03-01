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


if len(sys.argv) < 4:
    print(f"Expecting: {sys.argv[0]} <device> <schema name> <folder>")
    sys.exit(0)

device, schema_name, folder = sys.argv[1], sys.argv[2], sys.argv[3]
if device in devices:
    with manager.connect(**devices[device]) as m:
        schema = m.get_schema(schema_name)
        with open(f"{folder}/{schema_name}.yang", "w") as f:
            f.write(schema.data)
else:
    print(f"Avaliable devices are: {', '.join(devices.keys())}.")
