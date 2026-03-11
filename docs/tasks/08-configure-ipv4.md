# Task 8 - Configure IPv4 Address

This task involves assigning IPv4 address to the two interfaces we configured thus far. According the topology [diagram](../reference/network-topology.md), the IPv4 addresses required are:

Device | Interface | IPv4 address/mask
---|---|---
ceos-01 | Ethernet1 | 192.168.1.2/31
srl-01 | ethernet-1/1.0 | 192.168.1.3/31


## Configuration Tasks

We will follow the same workflow but I will skip the discovery steps.

Both devices support the OpenConfig module `openconfig-if-ip` (different versions), so we will get the module and build the XML file.

```bash
./scripts/netconf_tool.py srl-01 schema openconfig-if-ip
```

```bash
pyang -f tree -p openconfig openconfig-if-ip.yang
```

```
module: openconfig-if-ip

  augment /oc-if:interfaces/oc-if:interface/oc-if:subinterfaces/oc-if:subinterface:
    +--rw ipv4
       +--rw addresses
       |  +--rw address* [ip]
       |     +--rw ip        -> ../config/ip
       |     +--rw config
       |     |  +--rw ip?              oc-inet:ipv4-address
       |     |  +--rw prefix-length?   uint8
```

Looking at the top few lines of the tree, we see that we need the tree branch `/interfaces/interface/subinterfaces/subinterface/ipv4`

However, if we try to grab the this branch using `--tree-path`, we don't get the tree we want.

```bash
 pyang -f tree -p openconfig --tree-path /interfaces/interface/subinterfaces/subinterface/ipv4 openconfig-if-ip.yang
```

```
module: openconfig-if-ip

  augment /oc-if:interfaces/oc-if:interface/oc-if:subinterfaces/oc-if:subinterface:
    +--rw ipv4
  augment /oc-if:interfaces/oc-if:interface/oc-if:subinterfaces/oc-if:subinterface:
    +--rw ipv6
  augment /oc-if:interfaces/oc-if:interface/oc-vlan:routed-vlan:
    +--rw ipv4
  augment /oc-if:interfaces/oc-if:interface/oc-vlan:routed-vlan:
    +--rw ipv6
(.pyenv) automan@autobook:~/tutorial$
```


The command produces only the empty elements because `openconfig-if-ip.yang` is *an augmentation-only* module. 

> Note: "The Plugin Analogy"  
Think of `openconfig-if-ip` like a plugin. It doesn't create the interface list itself; it "plugs into" the existing `/interfaces/interface` module to add IPv4 and IPv6 address capabilities. If you don't include the base module on the `pyang` command line, the plugin has nothing to "plug into," and you get an empty tree.


To get this branch using `--tree-path` we have to include all the top modules:

```bash
pyang -f tree -p openconfig --tree-path /interfaces/interface/subinterfaces/subinterface/ipv4 openconfig/release/models/interfaces/*.yang
```

Similarly, to get the XML skeleton (this time we need to include the interface):

```bash
pyang -f sample-xml-skeleton -p openconfig \
 --sample-xml-skeleton-path=/interfaces/interface --sample-xml-skeleton-doctype=config openconfig/release/models/interfaces/*.yang
```

Create an XML file that includes only the parts we need for now:

```xml
<interfaces xmlns="http://openconfig.net/yang/interfaces">
   <interface>
   <name/>
   <subinterfaces>
      <subinterface>
         <index/>
         <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
         <addresses>
            <address>
               <ip/>
               <config>
               <ip/>
               <prefix-length/>
               </config>
            </address>
         </addresses>
            <config>
            </enabled>
            </config>
         </ipv4>
      </subinterface>
   </subinterfaces>
   </interface>
</interfaces>
```

Edit the file for both routers. For `srl-01`, it will look like this:

```xml
<interfaces xmlns="http://openconfig.net/yang/interfaces">
  <interface>
    <name>ethernet-1/1</name>
    <subinterfaces>
      <subinterface>
        <index>0</index>
        <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
          <addresses>
            <address>
              <ip>192.168.1.3</ip>
              <config>
                <ip>192.168.1.3</ip>
                <prefix-length>31</prefix-length>
              </config>
            </address>
          </addresses>
          <config>
            <enabled>true</enabled>
          </config>
        </ipv4>
      </subinterface>
    </subinterfaces>
  </interface>
</interfaces>
```

## Connectivity Verification

Before pinging, you need to check if routing is enabled on `ceos-01`.

cEOS devices operate as switches at startup. To enable routing functions, ip routing must be enabled and the switch mode must be disabled on L3 interfaces. As of this writing, I could not find a mechanism to do this via NETCONF or gNMI, so it must be done via cLI. This represents one of the important real-world implementation challenges that this tutorial aim to highlight.

```
ceos-01>enable
ceos-01#configure
ceos-01(config)#ip routing
ceos-01(config)#exit
```

A portion of the device configuration should look like this:

```
interface Ethernet1
   description To SRL-01
   no switchport
   ip address 192.168.1.2/31
!
interface Ethernet2
!
interface Management0
   vrf MGMT
   ip address 192.168.100.11/24
!
ip routing
```

From the CLI, you should be able to ping successfully between the two devices.


## Conclusions

You just completed the entire process of establishing a link between two routers. This process involved creating a subinterface, binding it to a network instance, then assigning an IPv4 address. A keen observer, will notice that we can combine creating a subinterface and assigning an IP address in one step. In fact, we can do all tasks in one step. This is what we will do configure the remaining interfaces in the toplogy.
 