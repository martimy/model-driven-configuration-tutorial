# Task 9 - Configure Remaining Interfaces with gNMI

In the previous task, we used NETCONF to configure the link between `ceos-01` and `srl-01`. Now, we will configure the remaining links in our topology using gNMI (gRPC Network Management Interface). This task will move at a faster pace since you are now familiar with the OpenConfig modules.


We need to configure the following remaining links:

| Link | Device A | Interface | IP | Device B | Interface | IP |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2 | ceos-01 | Ethernet2 | 192.168.1.4/31 | srl-02 | ethernet-1/1 | 192.168.1.5/31 |
| 3 | srl-01 | ethernet-1/2.0 | 192.168.1.6/31 | srl-02 | ethernet-1/2.0 | 192.168.1.7/31` |

## Technique 1: Using Existing Configuration

Unlike NETCONF's XML, gNMI typically uses JSON for its payload. We will use the same OpenConfig `interfaces` model.

I recommended that you review [gNMi paths](../concepts/gnmi-paths.md) before proceeding as you will use them extensively in this task.. 

### Get Existing Configuration

The easiest way to configure the interfaces is to get the configuration of the interface that we already completed:

```bash
gnmic --config srl-gnmic.yml get --path /interface[name=ethernet-1/1]/subinterface[index=0] -t config
```

```json
[
  {
    "source": "srl-01:57400",
    "timestamp": 1772910234636631063,
    "time": "2026-03-07T19:03:54.636631063Z",
    "updates": [
      {
        "Path": "srl_nokia-interfaces:interface[name=ethernet-1/1]/subinterface[index=0]",
        "values": {
          "srl_nokia-interfaces:interface/subinterface": {
            "admin-state": "enable",
            "ipv4": {
              "address": [
                {
                  "ip-prefix": "192.168.1.3/31"
                }
              ],
              "admin-state": "enable"
            }
          }
        }
      }
    ]
  }
]
```

Do the same for the network instance:

```bash
gnmic --config srl-gnmic.yml get --path /network-instance[name=default] -t config
```

```json
[
  {
    "source": "srl-01:57400",
    "timestamp": 1772910838388260967,
    "time": "2026-03-07T19:13:58.388260967Z",
    "updates": [
      {
        "Path": "srl_nokia-network-instance:network-instance[name=default]",
        "values": {
          "srl_nokia-network-instance:network-instance": {
            "description": "Default",
            "interface": [
              {
                "interface-ref": {
                  "interface": "ethernet-1/1",
                  "subinterface": 0
                },
                "name": "ethernet-1/1"
              }
            ]
          }
        }
      }
    ]
  }
]
```

### Edit Configuration

Edit the `updates` list in the configuration to match the interfaces table above:


```json
"Path": "srl_nokia-interfaces:interface[name=ethernet-1/1]/subinterface[index=0]",
"values": {
  "srl_nokia-interfaces:interface/subinterface": {
    "admin-state": "enable",
    "ipv4": {
      "address": [
        {
          "ip-prefix": "192.168.1.5/31"
        }
      ],
      "admin-state": "enable"
    }
  }
}
```

```json
"Path": "srl_nokia-network-instance:network-instance[name=default]",
"values": {
  "srl_nokia-network-instance:network-instance": {
    "description": "Default",
    "interface": [
      {
        "interface-ref": {
          "interface": "ethernet-1/1",
          "subinterface": 0
        },
        "name": "ethernet-1/1"
      }
    ]
  }
}
```

### Push Configuration using `gnmic`

The `gnmic` tool uses `set` operation to push the configuration. Let's configure the link between `ceos-01` and `srl-02`, starting from `srl-02`

We use the `Path` and `values` above mostly unchanged, but the path must conform to the gNMI format. Notice also the single quotes that surround the configuration object:  

```bash
gnmic --config srl-gnmic.yml -a srl-02 set \
--update-path /interface[name=ethernet-1/1]/subinterface[index=0] \
--update-value '{"admin-state": "enable","ipv4": {"address": [{"ip-prefix": "192.168.1.5/31"}],"admin-state": "enable"}}'
```

`gnmic` sends this update to the running configuration. The output confirms the success of the update:

```json
{
  "source": "srl-02",
  "timestamp": 1772912676743318280,
  "time": "2026-03-07T19:44:36.74331828Z",
  "results": [
    {
      "operation": "UPDATE",
      "path": "interface[name=ethernet-1/1]/subinterface[index=0]"
    }
  ]
}
```

Repeat for binding the interface to the network instance:

```bash
gnmic --config srl-gnmic.yml -a srl-02 set \
--update-path /network-instance[name=default]  \
--update-value '{"description": "Default","interface": [{"interface-ref": {"interface": "ethernet-1/1","subinterface": 0},"name": "ethernet-1/1"}]}'
```

### Verify with `gnmi_tool.py`

Now use the `gnmic` again verify that the configuration was applied correctly.

```bash
gnmic --config srl-gnmic.yml -a srl-02 get --path /interface[name=ethernet-1/1]/subinterface[index=0] -t config
```

You should see the JSON output reflecting the new IP address and interface state.


## Technique 2: 

The previous technique is useful for small changes, like enabling an interface, and when you are familiar with the required payload. More efficient method is needed.

The `gnmic` tool is able to generate configuration payload based on the target YANG data module. The `gnmic` `generate` command takes the target's YANG modules as input and generates:

- Paths in xpath or gNMI formats.
- Configuration payloads that can be used as update or replace input files for the Set command.
- A Set request file that can be used as a template with the Set command.

Use the next example to generate the configuration payload for the interface in cEOS and save it to a file. The default format will be YAML.

```bash
gnmic generate --file openconfig set-request --update /interfaces/interface/subinterfaces/ > ceos_request.yml
```

Unlike the previous technique, the command `generate` with subcommand `set-request` provides a configuration payload ready to upload after editing

You need to make the following change to the file `ceos_request.yml`

- Update the path to include the interface name
- Fill the missing values
- Remove the quotes surrounding the boolean and integer values
- Removed unneeded items

The file should look like this:

```yaml
updates:
- path: /interfaces/interface[name=Ethernet2]/subinterfaces
  value:
    subinterface:
    - config:
        description: "To srl-02"
        enabled: true
        index: 0
      index: 0
      ipv4:
        addresses:
          address:
          - config:
              ip: "192.168.1.4"
              prefix-length: "31"
              type: PRIMARY
            ip: "192.168.1.4"
        config:
          enabled: true
```

The file includes these components:

- updates: This is a list that contains one or more update entries. Each entry specifies a path and the value to set at that path.
- path: This specifies the path to the configuration that is being updated. There are two paths.
- value: This section contains the configuration details for the specified path.

To upload this configuration, we use the `set` command


```bash
gnmic --config ceos-gnmic.yml set --request-file ceos_request.yml
```

The result should confirm the success of the update.

```
{
  "source": "ceos-01:6030",
  "timestamp": 1772930223840040329,
  "time": "2026-03-08T00:37:03.840040329Z",
  "results": [
    {
      "operation": "UPDATE",
      "path": "interfaces/interface[name=Ethernet2]/subinterfaces"
    }
  ]
}
```

## Complete Link 3

Using what you've learned, configure the third link between `srl-01` and `srl-02` on their respective `ethernet-1/2` interfaces. Don't forget that on SR Linux, you also need to associate the subinterface with the network-instance `default`.

## Summary

You have now successfully configured a multi-vendor network using two different model-driven protocols!
