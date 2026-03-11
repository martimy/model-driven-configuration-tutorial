# Task 10 - Configure OSPF

This task covers configuring OSPF using NETCONF following the typical workflow of module discovery, payload editing, and loading.


## OSPF Model Support


SR Linux supports native and OpenConfig OSPF models but it uses the native model for configuration.

``` 
http://openconfig.net/yang/ospfv2?module=openconfig-ospfv2&revision=2024-06-17
urn:nokia.com:srlinux:ospf:ospf?module=srl_nokia-ospf&revision=2025-10-31
```

cEOS supports only OpenConfig OSPF model.

```
http://openconfig.net/yang/ospf?module=openconfig-ospf&revision=2025-02-13
```


# cEOS Configuration

To discover the OSPF YANG module, you will need to use the `openconfig-network-instance` (downloaded in previous tasks) and `openconfig-ospfv2`

```bash
(.pyenv) automan@autobook:~/tutorial$ ./scripts/netconf_tool.py ceos-01 schema openconfig-ospfv2
```

Visualize the tree using a depth limit of 7 to get only the top containers in the ospfv2 branch:

```bash
pyang -f tree -p openconfig \
--tree-path network-instances/network-instance/protocols/protocol/ospfv2 \
openconfig-network-instance.yang --tree-depth=7
```

```
module: openconfig-network-instance
  +--rw network-instances
     +--rw network-instance* [name]
        +--rw protocols
           +--rw protocol* [identifier name]
              +--rw ospfv2
                 +--rw global
                 |  +--rw config
                 |  |     ...
                 |  +--ro state
                 |  |     ...
                 |  +--rw timers
                 |  |     ...
                 |  +--rw graceful-restart
                 |  |     ...
                 |  +--rw mpls
                 |  |     ...
                 |  +--rw inter-area-propagation-policies
                 |        ...
                 +--rw areas
                    +--rw area* [identifier]
```

From the generated tree, we are interested in the `global` and `areas` containers and their mandatory children nodes. Also notice that we need to identify the network instance `name` and the protocol `identifier name`.

Under `global`, we will need to set a `router-id`:

```bash
pyang -f tree -p openconfig \
--tree-path network-instances/network-instance/protocols/protocol/ospfv2/global/config \
openconfig-network-instance.yang --tree-depth=8
```

```
module: openconfig-network-instance
  +--rw network-instances
     +--rw network-instance* [name]
        +--rw protocols
           +--rw protocol* [identifier name]
              +--rw ospfv2
                 +--rw global
                    +--rw config
                       +--rw router-id?                    yang:dotted-quad
                       +--rw summary-route-cost-mode?      enumeration
                       +--rw igp-shortcuts?                boolean
                       +--rw log-adjacency-changes?        boolean
                       +--rw hide-transit-only-networks?   boolean
```

Under `areas`, we need to set the area's `identifier`, and a list if interface `id`s:

```bash
pyang -f tree -p openconfig \
--tree-path network-instances/network-instance/protocols/protocol/ospfv2/areas \
openconfig-network-instance.yang --tree-depth=11
```

```
module: openconfig-network-instance
  +--rw network-instances
     +--rw network-instance* [name]
        +--rw protocols
           +--rw protocol* [identifier name]
              +--rw ospfv2
                 +--rw areas
                    +--rw area* [identifier]
                       +--rw identifier       -> ../config/identifier
                       +--rw config
                       |  +--rw identifier?   oc-ospf-types:ospf-area-identifier
                       ...
                       +--rw interfaces
                       |  +--rw interface* [id]
                       |     +--rw id               -> ../config/id
                       |     +--rw config
                       |     |  +--rw id?                             oc-if:interface-id
                       |     |  +--rw network-type?                   identityref
                       |     |  +--rw priority?                       uint8
                       |     |  +--rw multi-area-adjacency-primary?   boolean
                       |     |  +--rw authentication-type?            string
                       |     |  +--rw metric?                         oc-ospf-types:ospf-metric
                       |     |  +--rw passive?                        boolean
                       |     |  +--rw hide-network?                   boolean
```


Generate a XML skeleton using **Technique 1: pyang Sample XML Skeleton** at a subtree:


```bash
pyang -f sample-xml-skeleton --sample-xml-skeleton-path=/network-instances/network-instance/protocols/protocol \
--sample-xml-skeleton-doctype=config -p openconfig openconfig-network-instance.yang -o ospf.xml
```

The generated skeleton does not include the network instance name so will add it using what we know from [Task 7](../tasks/07-configure-ns.md).

Edit the file `ospf.xml` by filling the mandatory information and remove the nodes that are not required:

- Network Instance: `default`
- Protocol Identifier: `oc-pol-types:OSPF` (obtained from [here](https://github.com/openconfig/public/blob/master/release/models/network-instance/openconfig-network-instance.yang))
- Protocol Name: `100`
- Router ID: `1.1.1.1`
- Area: `0.0.0.0`
- Interface ID's: `Ethernet1` and `Ethernet2` 

```xml
<network-instances xmlns="http://openconfig.net/yang/network-instance">
<network-instance>
    <name>default</name>
    <protocols>
    <protocol>
        <identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:OSPF</identifier>
        <name>100</name>
        <config>
        <identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:OSPF</identifier>
        <enabled>true</enabled>
        </config>
        <ospfv2>
        <global>
            <config>
            <router-id>1.1.1.1</router-id>
            </config>
        </global>
        <areas>
            <area>
            <identifier>0.0.0.0</identifier>
            <config>
                <identifier>0.0.0.0</identifier>
            </config>
            <interfaces>
                <interface>
                <id>Ethernet1</id>
                <config>
                    <id>Ethernet1</id>
                </config>
                </interface>
                <interface>
                <id>Ethernet2</id>
                <config>
                    <id>Ethernet2</id>
                </config>
                </interface>
            </interfaces>
            </area>
        </areas>
        </ospfv2>
    </protocol>
    </protocols>
</network-instance>
</network-instances>
```

Upload the configuration payload to the candidate datastore and commit:

```bash
./nc_wrapper.sh ceos-01 --edit-config=ospf.xml --db=candidate --commit
```



## SR Linux Configuration

SR Linux uses a native OSPF YANG. Yet, similar to cEOS, we need the following:

- OSPF version number (v2 in this task)
- Router ID: Each router running OSPF must be configured with a unique router ID.
- An area: At least one OSPF area must be created. An interface must be assigned to each OSPF area.
- Interfaces: An interface has a single IP address and mask (unless the network is an unnumbered point-to-point network).


Configuring all of the above will be done at the network instance level, so let's visit the network instance tree again:


```bash
./scripts/netconf_tool.py srl-01 schema srl_nokia-network-instance
```

```bash
pyang -f tree -p nokia  srl_nokia-network-instance.yang --tree-path /network-instance --tree-depth=2 --ignore-errors
```

Like the OpenConfig module, the OSPF fits inside the `protocols` container:

```xml
module: srl_nokia-network-instance
  +--rw network-instance* [name]
     +--rw name                                     srl_nokia-comm:restricted-name
     +--rw type?                                    identityref
     +--rw admin-state?                             srl_nokia-comm:admin-state
     +--ro oper-state?                              srl_nokia-comm:oper-state
     +--ro oper-down-reason?                        enumeration
     +--ro oper-mac-vrf-mtu?                        uint16
     +--ro oper-vpws-mtu?                           uint16 {srl-feat:vpws}?
     +--rw description?                             srl_nokia-comm:description
     +--rw router-id?                               srl_nokia-comm:dotted-quad
     +--rw mpls-forwarding
     |     ...
     +--rw ip-forwarding!
     |     ...
     +--rw ip-tunnel-statistics {srl-feat:gribi-host-prefix-ip-tunnel-statistics}?
     |     ...
     +--rw interface* [name]
     |     ...
     +--ro system-ipv4-address
     |     ...
     +--ro system-ipv6-address
     |     ...
     +--rw vxlan-interface* [name] {srl-feat:vxlan}?
     |     ...
     +--ro icmp
     |     ...
     +--ro icmp6
     |     ...
     +--rw protocols
     |     ...
     +--rw bridge-table! {srl-feat:bridged}?
     |     ...
     +--ro route-table
     +--ro tunnel-table
     +--ro multicast-forwarding-information-base
     +--rw connection-point* [name] {srl-feat:connection-point}?
           ...
```

You can also inspect the OSPF module tree, which is also large:

```bash
./scripts/netconf_tool.py srl-01 schema srl_nokia-ospf
```

```bash
pyang -f tree -p nokia srl_nokia-ospf.yang | head -n 15
```

```xml
module: srl_nokia-ospf

  augment /srl_nokia-netinst:network-instance/srl_nokia-netinst:protocols:
    +--rw ospf!
       +--rw instance* [name]
          +--rw name                           srl_nokia-comm:name
          +--rw admin-state?                   srl_nokia-comm:admin-state
          +--rw version                        identityref
          +--rw address-family?                identityref
          +--rw instance-id?                   uint32
          +--rw router-id?                     yang:dotted-quad
          +--rw max-ecmp-paths?                srl_nokia-ospf-types:ospf-ecmp
          +--rw advertise-router-capability?   enumeration
          +--rw export-policy?                 -> /srl-rpol:routing-policy/policy/name
          +--rw asbr!
```

It is worth mentioning that the `!` symbol immediately following a node name (ospf!) indicates that the node is a presence container. A presence container exists in the configuration just by being created, even if it has no child nodes and its existence signifies that OSPF is enabled in the network instance.

Typically, what you could do next is to generate the XML skeleton file that includes the minimum configuration items mentioned above. However, for such complex configuration, we can use **Technique 2: Configure via CLI, Then Read Back**, similar to what we did in [Task 6](../tasks/06-configure-interface.md). 

Configure OSPF using the CLI on `srl-01`, then retrieve the configuration. 

For this configuration, we assign the router id to `2.2.2.2` in `srl-01` and `3.3.3.3` in `srl-02`. We also create area `0.0.0.0` and assign both interfaces to it.  

- Network Instance: `default`
- OSPF Instance Name: `100` 
- Router ID: `2.2.2.2` and `3.3.3.3` (for `srl-01` and `srl-02`, respectively) 
- Area ID: `0.0.0.0`
- Interface Names: `Ethernet1` and `Ethernet2`


```bash
./nc_wrapper.sh srl-01 --get-config --filter /network-instance/protocols/ospf
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <network-instance xmlns="urn:nokia.com:srlinux:net-inst:network-instance">
    <name>default</name>
    <protocols>
      <ospf xmlns="urn:nokia.com:srlinux:ospf:ospf">
        <instance>
          <name>100</name>
          <version xmlns:srl_nokia-ospf-types="urn:nokia.com:srlinux:general:ospf-types">srl_nokia-ospf-types:ospf-v2</version>
          <router-id>2.2.2.2</router-id>
          <area>
            <area-id>0.0.0.0</area-id>
            <interface>
              <interface-name>ethernet-1/1.0</interface-name>
            </interface>
            <interface>
              <interface-name>ethernet-1/2.0</interface-name>
            </interface>
          </area>
        </instance>
      </ospf>
    </protocols>
  </network-instance>
</data>
```

Save the retrieved configuration in a file `ospf.xml`. Edit the file and upload it to `srl-02`.

```bash
./nc_wrapper.sh srl-02 --edit-config=ospf.xml --db=candidate --commit
```

You can verify by reading the configuration back:

```bash
./nc_wrapper.sh srl-02 --get-config --filter /network-instance[name=default]/protocols/ospf
```

## Conclusion 

As this point, you have successfully configured a functioning, yet simple, network using YANG models with NETCONF and gNMi.
 