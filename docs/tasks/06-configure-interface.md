
# Task 6 - Configure an Interface

In this task, we will configure an interface using NETCONF.

From the previous task we learned:

- A device my support more than one YANG interfaces modules, but one is used for configuration.
- Both cEOS and SR Linux devices support IETF and OpenConfig Interfaces module and use the OpenConfig module for configuration.


Visualize the module tree again (clone the OpenConfig public YANG modules if you have not done so)


For OpenConfig (ignore the output errors, if any):

```bash
pyang -f tree -p openconfig openconfig-interfaces.yang
```

The tree is large, but we are concerned only with `rw` branches and we will ignore the state branch as it is read only. We may further ignore branches that are entirely optional as indicated by '?'. The remaining are mandatory fields required to configure an interface. 

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
        ... ommitted
        +--rw subinterfaces
           +--rw subinterface* [index]
              +--rw index     -> ../config/index
              +--rw config
              |  +--rw index?         uint32
              |  +--rw description?   string
              |  +--rw enabled?       boolean
              ... ommitted
```

The description of each item in the tree can be found [here](https://openconfig.net/projects/models/schemadocs/yangdoc/openconfig-interfaces.html)


By OpenConfig convention, an interface must have at least one subinterface. More subinterfaces can be configured if VLANs are used. The IP addresses (if any) are assigned to the subinterface. Both the main interface and subinterface(s) must be enabled. 

OpenConfig also use the convention of using the interface name twice. The first location serves as a key for the list interfaces in the device. The second is where the name is stored in the configuration.


## Get the Sample XML Skeleton File


To get a XML skeleton you can actually use for NETCONF configuration:

```bash
pyang -f sample-xml-skeleton -p openconfig --sample-xml-skeleton-doctype=config openconfig-interfaces.yang
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name/>
      <config>
        <name/>
        <type/>
        <mtu/>
        <description/>
      </config>
      <hold-time>
        <config/>
      </hold-time>
      <penalty-based-aied>
        <config/>
      </penalty-based-aied>
      <subinterfaces>
        <subinterface>
          <index/>
          <config>
            <description/>
          </config>
        </subinterface>
      </subinterfaces>
    </interface>
  </interfaces>
</config>
```

## Edit the XML File

Create a file `interface.xml` and use the skeleton above to fill the required elements' contents (ignore most optional elements). 

Note:

- From the topology file, we know that SR Linux interface name convention is `ethernet-x/y`.
- The interface type has a very specific value: `<type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>`. 

> What is `ethernetCsmacd`?  
This string is the official IANA (Internet Assigned Numbers Authority) identifier for "regular" Ethernet (10/100/1000 Mbps). `Csmacd` stands for *Carrier Sense Multiple Access with Collision Detection*, the foundational technology behind traditional Ethernet.

```xml
<interfaces xmlns="http://openconfig.net/yang/interfaces">
<interface>
    <name>ethernet-1/1</name>
    <config>
    <name>ethernet-1/1</name>
    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
    <description>To ceos-01</description>
    </config>
    <subinterfaces>
    <subinterface>
        <index>0</index>
        <config>
        <index>0</index>
        <enabled>true</enabled>
        </config>
    </subinterface>
    </subinterfaces>
</interface>
</interfaces>
```

## Load the Configuration

Use NETCONF's `edit-config` operation to load the interface configuration to the the candidate datastore. 

```bash
./nc_wrapper.sh srl-01 --edit-config=interface.xml --db=candidate
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
<ok xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"/>
```

The output indicates no errors, let's commit the change:

```bash
./nc_wrapper.sh srl-01 --commit
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
<ok xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"/>
```

Verify that the configuration was committed to the running datastore:

```bash
./nc_wrapper.sh srl-01 --get-config --filter /interfaces/interface[name=ethernet-1/1]
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>ethernet-1/1</name>
      <config>
        <name>ethernet-1/1</name>
        <type xmlns:iana-if-type="urn:ietf:params:xml:ns:yang:iana-if-type">iana-if-type:ethernetCsmacd</type>
        <description>To ceos-01</description>
        <enabled>true</enabled>
      </config>
      <subinterfaces>
        <subinterface>
          <index>0</index>
          <config>
            <index>0</index>
            <enabled>true</enabled>
          </config>
        </subinterface>
      </subinterfaces>
    </interface>
  </interfaces>
</data>
```

The output confirms that the interface was configured properly. Note that the `enable` element must be included to enable the subinterface. The main interface is enabled by default (by containerlab), but the subinterface must be enabled explicitly in SR Linux.

## Alternative Approach

A reliable and fast path to a create XML payload is to configure the feature manually via CLI first, then use a NETCONF `get-config` to read back exactly how the device represents that configuration in YANG. This approach is especially valuable when vendor documentation is unclear or when you are working with a native module for the first time:

We will use this approach to configure interface `Ethernet1` on `ceos-01`. Note that cEOS creates subinterface `0` and enables it by default.

Use the CLI to set the description on interface `Ethernet1` and enable it:

```
interface Ethernet1
   description To srl-01
   no switchport
!
```

Retrieve the running configuration:

```bash
./nc_wrapper.sh ceos-01 --get-config --filter /interfaces/interface[name=Ethernet1]
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<data xmlns:netconf="http://arista.com/yang/rpc/netconf" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" netconf:time-modified="2026-03-05T23:06:56.416836888Z">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>Ethernet1</name>
      <config>
        <description>To srl-01</description>
        <mtu>0</mtu>
        <name>Ethernet1</name>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
      </config>
      <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
        <config>
          <fec-encoding xmlns="http://arista.com/yang/openconfig/interfaces/augments">
            <disabled>false</disabled>
            <fire-code>false</fire-code>
            <reed-solomon>false</reed-solomon>
            <reed-solomon544>false</reed-solomon544>
          </fec-encoding>
          <mac-address>00:00:00:00:00:00</mac-address>
          <port-speed>SPEED_UNKNOWN</port-speed>
          <sfp-1000base-t xmlns="http://arista.com/yang/openconfig/interfaces/augments">false</sfp-1000base-t>
        </config>
        <pfc xmlns="http://arista.com/yang/openconfig/interfaces/augments"/>
        <tap-aggregation xmlns="http://arista.com/yang/experimental/eos/arista-ebra-octap-agg-port-config">
          <config>
            <interface-mode>NON_TAP_TOOL</interface-mode>
          </config>
          <name>Ethernet1</name>
        </tap-aggregation>
      </ethernet>
      <subinterfaces>
        <subinterface>
          <index>0</index>
          <config>
            <description>To srl-01</description>
          </config>
          <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
            <config>
              <enabled>true</enabled>
            </config>
          </ipv4>
        </subinterface>
      </subinterfaces>
    </interface>
  </interfaces>
</data>
```

Notice the namespace declarations, element names, and hierarchy you see in that XML are exactly what your payload must reproduce. This approach, however, does not differentiate between mandatory and optional fields.

Change the description element and remove most elements, then load the configuration to the router using the commands shown above.

The default behavior of the `edit-config` operation is to `merge` the new data into the existing configuration. Therefore, only the interface description will be changed while all other elements remain the same. 

```xml
<interfaces xmlns="http://openconfig.net/yang/interfaces">
  <interface>
    <name>Ethernet1</name>
    <config>
      <description>To SRL-01</description>
      <name>Ethernet1</name>
      <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
    </config>
    <subinterfaces>
      <subinterface>
        <index>0</index>
        <config>
          <description>To SRL-01</description>
        </config>
      </subinterface>
    </subinterfaces>
  </interface>
</interfaces>
```