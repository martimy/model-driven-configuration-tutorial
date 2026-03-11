# Task 11 - Verify OSPF Routing

In this task, you will use gNMI to retrieve the routing table from the network instance `default` on SR Linux and cEOS to confirm that OSPF is exchanging routes correctly.

## SR Linux

In [Task 10](../tasks/10-configure-ospf.md) we saw that `+--ro route-table` is one of the read-only containers in the network instance `default`. Therefore, to list all IPv4 unicast routes in the routing table on SR Linux:

```bash
gnmic --config srl-gnmic.yml get \
  --path /network-instance[name=default]/route-table/ipv4-unicast/route
```

Or to retrieve only the prefixes, which gives a more readable summary:

```bash
gnmic --config srl-gnmic.yml get \
  --path /network-instance[name=default]/route-table/ipv4-unicast/route/ipv4-prefix
```

The output confirms that the routing table contains entries from multiple sources:

```json
[
  {
    "source": "srl-01:57400",
    "timestamp": 1773162638528776120,
    "time": "2026-03-10T17:10:38.52877612Z",
    "updates": [
      {
        "Path": "srl_nokia-network-instance:network-instance[name=default]/route-table/srl_nokia-ip-route-tables:ipv4-unicast",
        "values": {
          "srl_nokia-network-instance:network-instance/route-table/srl_nokia-ip-route-tables:ipv4-unicast": {
            "route": [
              {
                "id": 9,
                "ipv4-prefix": "192.168.1.2/31",
                "origin-network-instance": "default",
                "route-owner": "net_inst_mgr",
                "route-type": "srl_nokia-common:local"
              },
              {
                "id": 9,
                "ipv4-prefix": "192.168.1.3/32",
                "origin-network-instance": "default",
                "route-owner": "net_inst_mgr",
                "route-type": "srl_nokia-common:host"
              },
              {
                "id": 0,
                "ipv4-prefix": "192.168.1.4/31",
                "origin-network-instance": "default",
                "route-owner": "ospf_mgr",
                "route-type": "srl_nokia-common:ospfv2"
              },
              {
                "id": 8,
                "ipv4-prefix": "192.168.1.6/31",
                "origin-network-instance": "default",
                "route-owner": "net_inst_mgr",
                "route-type": "srl_nokia-common:local"
              },
              {
                "id": 8,
                "ipv4-prefix": "192.168.1.6/32",
                "origin-network-instance": "default",
                "route-owner": "net_inst_mgr",
                "route-type": "srl_nokia-common:host"
              }
            ]
          }
        }
      }
    ]
  }
]
```

The `route-owner` field identifies the source of each route. The entry for `192.168.1.4/31` has `route-owner: ospf_mgr` and `route-type: srl_nokia-common:ospfv2`, confirming that this prefix was learned via OSPF from `ceos-01`. The remaining entries are locally connected prefixes and host routes managed by `net_inst_mgr`.

Note that the path used here `/network-instance[name=default]/route-table/...` is the Nokia native model path.

## cEOS

Retrieving the routing table from cEOS presents a different challenge. OpenConfig does not define a single unified operational model for the merged routing table. Instead, it models routing information in two ways:

1. RIB (Routing Information Base): The "brain" of the control plane, where each protocol (OSPF, BGP, Static) keeps its own table.
2. AFT (Abstract Forwarding Table): The "forwarding table" used by the hardware, which merges the best routes from all protocols.

OpenConfig defines these separately in `openconfig-rib-bgp` and related modules. These modules are not fully implemented on this version of cEOS.

The native EOS YANG model also does not expose a clean routing table path via gNMI in this cEOS version. Retrieving routing state programmatically on cEOS currently requires either the eAPI (Arista's HTTP-based API) or the CLI.

## Conclusion

This task highlights one of the most important practical realities of model-driven management: the gap between configuration and operational state coverage is significant and varies by vendor and software version.

For configuration, both SR Linux and cEOS support OpenConfig models reliably, as demonstrated throughout this tutorial. For operational state, the picture is less consistent. SR Linux exposes a rich native model for routing state that is accessible via gNMI, but the OpenConfig AFT (Abstract Forwarding Table) model is not yet fully supported. cEOS, in this version, does not expose the routing table via gNMI at all through either OpenConfig or native paths.

