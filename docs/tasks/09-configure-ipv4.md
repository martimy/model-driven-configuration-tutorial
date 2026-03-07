# Configure IPv4 Address


Furthermore, cEOS devices operate as switches at startup. To enable routing functions, ip routing must be enabled and the switch mode must be disabled on each interface. As of this writing, I do not know of a mechanism to do this via NETCONF or gNMI, so it must be done via cLI:

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
!
interface Ethernet2
!
interface Management0
   vrf MGMT
   ip address 192.168.100.11/24
!
ip routing
no ip routing vrf MGMT
!
ip route vrf MGMT 0.0.0.0/0 192.168.100.1
!
```


