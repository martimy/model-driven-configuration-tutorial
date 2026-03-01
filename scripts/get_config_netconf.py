from ncclient import manager

srl_params = {
    "host": "srl-01",
    "port": 830,
    "username": "admin",
    "password": "NokiaSrl1!",
    "hostkey_verify": False,
}

ceos_params = {
    "host": "ceos-01",
    "port": 830,
    "username": "admin",
    "password": "admin",
    "hostkey_verify": False,
}

# Filter: Get one specific interface by name
ONE_SRL_INTERFACE = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>ethernet-1/1</name>
    </interface>
</interfaces>
"""

ONE_CEOS_INTERFACE = """
<interfaces>
    <interface>
        <name>Ethernet1</name>
    </interface>
</interfaces>
"""

SRL_OSPF = """
<network-instance xmlns="urn:nokia.com:srlinux:net-inst:network-instance">
    <protocols>
        <ospf xmlns="urn:nokia.com:srlinux:ospf:ospf"/>
    </protocols>
</network-instance>
"""

CEOS_OSPF = """
<network-instances xmlns="http://openconfig.net/yang/network-instance">
<network-instance>
    <name>default</name>
    <protocols>
    <protocol>
        <identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:OSPF</identifier>
        <name>100</name>
    </protocol>
    </protocols>
</network-instance>
</network-instances>
"""

NETWORK_INSTANCE = """
<network-instances xmlns="http://openconfig.net/yang/network-instance"/>
"""

with manager.connect(**srl_params) as m:
    config = m.get_config(source="running", filter=("subtree", NETWORK_INSTANCE))

    print(config.data_xml)
