# Stream Telemetry with gNMI Subscribe

In the previous tasks, you used the gNMI `Get` RPC to retrieve snapshots of configuration and operational state. This is useful for one-off queries but requires repeated polling to track changes over time. gNMI addresses this with the `Subscribe` RPC, which establishes a long-lived stream from the device to the client — the device pushes updates rather than the client pulling them.

This task introduces streaming telemetry using interface counters as the data source. Counters make an ideal first telemetry target: they change continuously whenever traffic is present, the data is easy to interpret, and they are reliably supported across vendors.

## Subscribe Modes

The gNMI specification defines three subscription modes:

- `ONCE` — the device sends a single snapshot and closes the stream. Functionally similar to `Get` but using the Subscribe RPC.
- `POLL` — the client sends explicit poll requests over a persistent stream; the device responds to each one.
- `STREAM` — the device pushes updates continuously. This is the mode used for real telemetry and supports two sub-modes:
  - `ON_CHANGE` — the device sends an update only when a value changes.
  - `SAMPLE` — the device sends updates at a fixed interval regardless of whether the value has changed.

Interface counters are better suited to `SAMPLE` mode because they change with every packet and `ON_CHANGE` would generate excessive updates under any meaningful traffic load.

## Subscribe to Interface Counters

Open two terminals. In the first terminal, start a continuous ping between the two routers to generate traffic:

```bash
# From ceos-01 CLI
ping 192.168.1.3 repeat 10000 interval 1
```

In the second terminal, start a gNMI subscription to interface counters on SR Linux:

```bash
gnmic --config srl-gnmic.yml subscribe \
  --path /interface[name=ethernet-1/1]/statistics \
  --mode stream \
  --stream-mode sample \
  --sample-interval 5s
```

You should see counter updates pushed to your terminal every five seconds. The `in-octets` and `out-octets` fields will increment with each sample, reflecting the ping traffic:

```json
{
  "source": "srl-01:57400",
  "subscription-name": "default-1773182967",
  "timestamp": 1773183053033074178,
  "time": "2026-03-10T22:50:53.033074178Z",
  "updates": [
    {
      "Path": "srl_nokia-interfaces:interface[name=ethernet-1/1]/statistics",
      "values": {
        "srl_nokia-interfaces:interface/statistics": {
          "carrier-transitions": "0",
          "in-broadcast-packets": "11",
          "in-discarded-packets": "188392",
          "in-error-packets": "0",
          "in-fcs-error-packets": "0",
          "in-multicast-packets": "224215",
          "in-octets": "32038668",
          "in-packets": "244453",
          "in-unicast-packets": "20227",
          "out-broadcast-packets": "11",
          "out-discarded-packets": "0",
          "out-error-packets": "0",
          "out-multicast-packets": "43674",
          "out-octets": "8495740",
          "out-packets": "63944",
          "out-unicast-packets": "20259"
        }
      }
    }
  ]
}
```

Press `Ctrl+C` to stop the subscription.

Repeat for cEOS using the OpenConfig path:

```bash
gnmic --config ceos-gnmic.yml subscribe \
  --path /interfaces/interface[name=Ethernet1]/state/counters \
  --mode stream \
  --stream-mode sample \
  --sample-interval 5s
```

Notice that the path structure differs between the two vendors. SR Linux uses `/interface[name=...]/statistics` via its native model, while cEOS uses `/interfaces/interface[name=...]/state/counters` via the OpenConfig model. Both return counter data, but the field names and hierarchy reflect their respective YANG modules.

## Using a gnmic Configuration File for Subscriptions

For more complex or reusable subscriptions, you can define them in the gnmic configuration file rather than passing all flags on the command line. Add a `subscriptions` block to your `srl-gnmic.yml`:

```yaml
subscriptions:
  interface-counters:
    paths:
      - /interface[name=ethernet-1/1]/statistics
      - /interface[name=ethernet-1/2]/statistics
    mode: stream
    stream-mode: sample
    sample-interval: 5s
```

Then invoke it by name:

```bash
gnmic --config srl-gnmic.yml subscribe --name interface-counters
```

This approach scales naturally to production use cases where you might subscribe to dozens of paths simultaneously across multiple devices.

## Conclusion

The `Subscribe` RPC is what makes gNMI fundamentally different from NETCONF. NETCONF is a transaction-oriented protocol. You send a request and receive a response. gNMI's streaming model inverts this relationship: the device continuously pushes data to the collector, enabling real-time visibility at scale without repeated polling overhead.

Polling a large network for interface counters every 30 seconds places a predictable but significant load on both devices and the management system. A gNMI subscription with a 30-second sample interval achieves the same result with a single persistent connection per device and a fraction of the overhead, and can be reduced to five seconds or less without meaningful impact on device performance.


As you complete this tutorial, the most important takeaway is not any specific command or YANG path — those change with every software release. It is the workflow: discover what the device supports, find the right module, read the tree, construct the payload, validate before pushing, and know when to fall back to native models. That workflow applies regardless of vendor, protocol version, or automation tool, and it is the foundation on which everything else in network automation is built.
