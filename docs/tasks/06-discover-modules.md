# Discover YANG Modules

Before starting configuring a devices, you must discover what YANG models the device supports and understand the shape of the data those models describe. This task covers the discovery workflow.


**Read the Documentations**

Reading the device documentation must be the first step in the process if configuring a device. Familiarize yourself with the content of the documents before proceeding. The links to Arista and Nokia devices are provided in the [References](../reference/network-topology.md).


## Step 1: Retrieve Modules

Every NETCONF session begins with a capabilities exchange. The device advertises every YANG module it supports, along with the exact revision date. This is the authoritative list of what you can configure.

Use the Python script `netconf-tool` to extract the modules from the device's advertised YANG capabilities:

```bash
./scripts/netconf_tool.py srl-01 modules
```

The code filters and prints the YANG modules from the capabilities:

```python
def get_modules(m):
    """Prints the YANG modules supported by the device."""
    mods = [c for c in m.server_capabilities if "module=" in c]
    for cap in sorted(mods):
        print(cap)
}
```

Each capability string contains the module name, namespace, and revision. For example: 

```bash
urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&revision=2014-05-08
```

or, for cEOS

```
urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&revision=2018-02-20
```

The URN identifies the IETF model for configuring and monitoring network interfaces.

- Namespace: urn:ietf:params:xml:ns:yang:ietf-interfaces
- Name: ietf-interfaces
- Revision: 2014-05-08 (2018-02-20)

Note the revision date — always use models that match this exact revision when building payloads.


**Using gNMI**

Use the Python script `gnmi-tool` to extract the modules from the device's advertised YANG capabilities:

```bash
./scripts/gnmi_tool.py srl-01 modules 
```

which will execute the function:

```python
def get_modules(gc):
    """Prints the modules supported by the device."""
    capabilities = gc.capabilities()
    mods = [
        f'{c["name"]}, {c["organization"]}, {c["version"]}'
        for c in capabilities["supported_models"]
    ]
    for mod in sorted(mods):
        print(mod)
```

The output will look like:

```bash
http://openconfig.net/yang/interfaces:openconfig-interfaces, OpenConfig working group, 2024-04-04
```

The module identifies the OpenConfig model for configuring and monitoring network interfaces.

- Name: "http://openconfig.net/yang/interfaces:openconfig-interfaces"
- Organization: OpenConfig working group
- Version: 2024-04-04



**Note about Model Support**


If you search modules for the keyword `interfaces` (e.g. using `grep`), you will find that SR Linux supports bot IETF and OpenConfig modules:

```bash
urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&revision=2014-05-08
http://openconfig.net/yang/interfaces?module=openconfig-interfaces&revision=2024-04-04&deviations=openconfig-srl-deviations
```

Similarly in cEOS:

```bash
urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&revision=2018-02-20
http://openconfig.net/yang/interfaces?module=openconfig-interfaces&revision=2024-12-05
```

This means the a module may exists on the device for various reasons (operational state, compatibility, or partial configuration), but it does not necessarily mean it is the primary configuration model.


## Step 2: Fetch the Schema (NETCONF)

Once you know which modules the device supports, you can pull the actual YANG source files directly from the device using the `get-schema` NETCONF RPC. This will get the exact model version the device is running:


Run the script for both devices for both the IETF and OpenConfig models (the file name will be \<model-name\>.yang):

```bash
./scripts/netconf_tool.py srl-01 schema ietf-interfaces
Schema saved to ietf-interfaces.yang
./scripts/netconf_tool.py srl-01 schema openconfig-interfaces
Schema saved to openconfig-interfaces.yang
```


## Step 3: Visualize the Tree with pyang

Raw YANG source is verbose and difficult to read. The pyang tool renders any YANG model as a concise indented tree that shows every configuration path, its data type, and whether it is mandatory. This tree is your primary reference when building payloads:

```bash
pyang -f tree ietf-interfaces.yang
```

```
module: ietf-interfaces
  +--rw interfaces
  |  +--rw interface* [name]
  |     +--rw name                        string
  |     +--rw description?                string
  |     +--rw type                        identityref
  |     +--rw enabled?                    boolean
  |     +--rw link-up-down-trap-enable?   enumeration {if-mib}?
  +--ro interfaces-state
     +--ro interface* [name]
        +--ro name               string
        +--ro type               identityref
        ...
```

For OpenConfig (ignore the output errors for now):

```bash
pyang -f tree openconfig-interfaces.yang
```

```
module: openconfig-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                  -> ../config/name
        +--rw config
        |  +--rw name?            string
        |  +--rw type             identityref
        |  +--rw mtu?             uint16
        |  +--rw loopback-mode?   oc-opt-types:loopback-mode-type
        |  +--rw description?     string
        |  +--rw enabled?         boolean
        +--ro state
        |  +--ro name?            string
        |  +--ro type             identityref
        ...
```

**Reading the Tree**

The `+--rw` prefix means read-write (configurable). `+--ro` means read-only (operational state). A `*` after the node name means it is a list (multiple entries). A `?` means the field is optional. These symbols tell you exactly what your payload must and can include.


Notices that both YANG modules sperate the configuration fields from the state fields but using two different conventions. OpenConfig's style is generally considered more operator-friendly for automation and streaming telemetry, which is why it became very popular despite not being the original IETF approach. (Later IETF NMDA work moved closer to unified views in many newer modules.)

We will focus out interest in configuration for now. To show only the configuration nodes:

```bash
pyang -f tree --tree-path /interfaces/interface ietf-interfaces.yang
```

```
module: ietf-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                        string
        +--rw description?                string
        +--rw type                        identityref
        +--rw enabled?                    boolean
        +--rw link-up-down-trap-enable?   enumeration {if-mib}?
```

## Step 4: Determining Configuration Models

A quick way to determine which modules is used for configuration is to use a NETCONF `get-config` to read configuration on the devices using simplified XPATH filter

```bash
./nc_wrapper.sh srl-01 --get-config --filter /interfaces
```

Or

```bash
./nc_wrapper.sh srl-01 intf.xml
```


The result clearly indicate that SR Linux uses the OpenConfig module for interface configuration.

```
<?xml version='1.0' encoding='UTF-8'?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
        ...
```

And so does cEOS:

```
<?xml version='1.0' encoding='UTF-8'?>
<data xmlns:netconf="http://arista.com/yang/rpc/netconf" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" netconf:time-modified="2026-03-05T17:12:16.876169374Z">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
  ...
```
