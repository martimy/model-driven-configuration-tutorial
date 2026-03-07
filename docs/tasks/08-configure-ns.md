# Bind Interface to Network Instance

If you have followed all previous tasks successfully, you should have two interfaces enabled:

- Interface `ethernet-1/1.0` at `srl-01`
- Interface `Ethernet1` at `ceos-01`

Both interfaces face each other according to the [network topology](../reference/network-topology.md). 


## Network Instance

The OpenConfig data model requires that each subinterface is associated with a network instances (similar to a VRF) to be functional. An interface without an assigned network instance cannot be used for forwarding traffic. In cEOS, interfaces are associated with a `default` network instance. So containerlab must assign the management interface explicitly to `MGMT` instance in the topology file. In SR Linux, the management interface, `mgmt0`, is automatically added to a separate, management network instance `mgmt`. Other interfaces are not associated with any network instance by default, so the interface we created must be associated with a network instance before it can be used in routing. 


In this task, we will add the interface `ethernet-1/1.0` to the default network instance `default` at `srl-01`.

## Configuration Workflow

For SR Linux, we will follow the same workflow as in the previous task:

1. Find the supported YANG module
2. Extract a skeleton XML file
3. Edit the XML file
4. Load the configuration and commit


### Find the YANG Module

Start by searching for the `network-instance` module in the NETCONF capabilities of SR Linux router (you may also check the vendor documents):

```bash
./scripts/netconf_tool.py srl-01 modules | grep "network-instance"
```

The likely candidates are `srl_nokia-network-instance` and `openconfig-network-instance.

Next, get the module using the schema:

```bash
./scripts/netconf_tool.py srl-01 schema openconfig-network-instance
```

Visualizing both modules using `pyang -f tree`, we see that the root item is `network-instance` and `network-instances`, respectively. 

The `get-config` operation retrieves the running configuration in both cases with different namespaces, indicating that both modules can be used for configuration.


```bash
./nc_wrapper.sh srl-01 --get-config --filter /network-instances
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <network-instances xmlns="http://openconfig.net/yang/network-instance">
  ...
  </network-instances>
</data>
```

```bash
./nc_wrapper.sh srl-01 --get-config --filter /network-instance
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <network-instance xmlns="urn:nokia.com:srlinux:net-inst:network-instance">
  ...
  </network-instance>
</data>
```

When configuration is sent using either data model, SR Linux translates it into its internal data model. In practice, OpenConfig is preferred for portable, multi-vendor automation, while the Nokia native module is used when full device capabilities or vendor-specific features are required. As we have seen in the previous task that this is not always the case for all models. 

### Get the XML Skeleton

Visualize the Nokia's module:

```bash
pyang -f tree -p nokia --tree-path /network-instance/interface srl_nokia-network-instance.yang
```

```xml
module: srl_nokia-network-instance
  +--rw network-instance* [name]
     +--rw interface* [name]
        +--rw name                srl_nokia-netinst:network-instance-subintf-name
        +--rw interface-ref {srl-feat:interface-references}?
        |  +--rw interface?      -> /srl_nokia-if:interface/name
        |  +--rw subinterface?   -> /srl_nokia-if:interface[srl_nokia-if:name=current()/../interface]/subinterface/index
        +--ro oper-state?         srl_nokia-comm:oper-state
        +--ro oper-down-reason?   enumeration
        +--ro index?              uint64
        +--rw bridge-table! {srl-feat:bridged}?
        |  +--rw split-horizon-group?                 -> ../../../bridge-table/split-horizon-group/name {srl-feat:bridged and srl-feat:bt-split-horizon-groups}?
        |  +--ro mac-relearn-only?                    boolean
        |  +--ro multicast-forwarding?                srl_nokia-comm:multicast-type
        |  +--ro oper-mac-learning?                   srl_nokia-comm:oper-state
        |  +--ro oper-mac-learning-disabled-reason?   enumeration
        +--rw connection-point?   -> ../../connection-point/name {srl-feat:connection-point}?
```

The SR Linux supports three types of [network-instances](https://documentation.nokia.com/srlinux/25-10/books/config-basics/network-instances.html): default, ip-vrf, and mac-vrf. Type default is the default network-instance and only one of this type is supported. Type `ip-vrf` is the regular network-instance; you can create multiple network-instances of this type.

Creating the `default` instance and binding the interface to it in one step.

Create an XML skeleton using `pyang` and redirect the output to a file:


```bash
pyang -f sample-xml-skeleton -p nokia --ignore-errors \
--sample-xml-skeleton-doctype=config srl_nokia-network-instance.yang > ni_interface.xml
```

### Edit the XML File

Edit the file to include only the mandatory fields in the interface branch (and remove the `<config>` tag). 

```xml
<network-instance xmlns="urn:nokia.com:srlinux:net-inst:network-instance">
  <name>default</name>
  <description>Default VRF</description>
  <interface>
    <name>ethernet-1/1</name>
    <interface-ref>
      <interface>ethernet-1/1</interface>
      <subinterface>0</subinterface>
    </interface-ref>
  </interface>
</network-instance>
```


**Validation**

Before loading the configuration, we can validate it.

`xmllint` looks at the XML syntax but it not aware of YANG:

```bash
xmllint --noout ni_interface.xml
```

The `--dry` option in `netconf-console2` returns the RPC to be sent, so we can use it verify that the XML file is formatted properly.

```
./nc_wrapper.sh srl-01 --edit-config=ni_interface.xml --dry
```

we can also use `yanglint` to validate the XML file against the YANG module.


## Loading the Configuration and Commit

Load the configuration to the candidate datastore and commit:

```bash
./nc_wrapper.sh srl-01 --edit-config=ni_interface.xml --db=candidate --commit
```

## Use the OpenConfig Module

The OpenConfig module can be used also for the configuration. Repeat the same steps as before: 

### Visualize the Module

```bash
pyang -f tree -p nokia --tree-path /network-instances/network-instance/interfaces openconfig-network-instance.yang
```

```xml
module: openconfig-network-instance
  +--rw network-instances
     +--rw network-instance* [name]
        +--rw interfaces
           +--rw interface* [id]
              +--rw id        -> ../config/id
              +--rw config
              |  +--rw id?                            oc-if:interface-id
              |  +--rw interface?                     -> /oc-if:interfaces/interface/name
              |  +--rw subinterface?                  -> /oc-if:interfaces/interface[oc-if:name=current()/../interface]/subinterfaces/subinterface/index
              |  +--rw associated-address-families*   identityref
              |  +--rw mac-pinning?                   boolean
              |  +--rw irb-anycast-gateway?           enumeration
              +--ro state
                 +--ro id?                            oc-if:interface-id
                 +--ro interface?                     -> /oc-if:interfaces/interface/name
                 +--ro subinterface?                  -> /oc-if:interfaces/interface[oc-if:name=current()/../interface]/subinterfaces/subinterface/index
                 +--ro associated-address-families*   identityref
                 +--ro mac-pinning?                   boolean
                 +--ro irb-anycast-gateway?           enumeration
```

### Get the XML Skeleton

```bash
pyang -f sample-xml-skeleton -p nokia openconfig-network-instance.yang
```

### Edit the XML file

```xml
<network-instances xmlns="http://openconfig.net/yang/network-instance">
  <network-instance>
    <name>default</name>
    <config>
      <name>default</name>
      <description>Default</description>
    </config>
    <interfaces>
      <interface>
        <id>1</id>
        <config>
          <id>1</id>
          <interface>ethernet-1/1</interface>
          <subinterface>0</subinterface>
        </config>
      </interface>
    </interfaces>
  </network-instance>
</network-instances>
```

### Load and Commit

```bash
./nc_wrapper.sh srl-01 --edit-config=ni_interface.xml --db=candidate --commit
```

## Summary

You are able to bind the interface with the network instance using both OpenConfig and the native YANG models because the device supports multiple external YANG data models that map to the same internal configuration datastore. The trees show that both models define a `network-instance` containing an `interface` list that references a physical interface and subinterface, but they structure and name the fields differently. One notable difference is that OpenConfig uses an `id` as key for the interface list instead of `name`.





