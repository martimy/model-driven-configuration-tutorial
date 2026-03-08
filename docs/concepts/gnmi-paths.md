# Paths in gNMI

In gNMI (gRPC Network Management Interface), paths identify specific nodes in the data tree, whether for retrieving configuration/state (Get), modifying data (Set), or subscribing to telemetry updates (Subscribe).

gNMI deliberately uses a structured, efficient path representation rather than raw strings or full XPath. This design keeps the protocol lightweight, strongly typed, and easy to parse/validate against YANG models.

## String Representation

Most tools, CLIs, documentation, and clients (gnmic, pygnmi, etc.) display and accept paths using a familiar XPath-like string syntax (defined in gNMI Path Conventions):

```
/interfaces/interface[name=eth1/1]/state/counters
/openconfig-interfaces:interfaces/interface[name=*]/state/admin-status
/interfaces/interface[name=eth1/1]/config/description
```

Key features of this string form:

- `/` separates hierarchy levels
- `[key=value]` selects list entries (multiple keys allowed: `[ifIndex=42,name=eth1]`)
- `*` acts as a wildcard for all list instances
- No support for full XPath axes (`//`, `..`, `contains()`, functions, complex predicates)

The string form is not sent on the wire. clients/tools convert it to/from the structured `Path` protobuf.

## Key Characteristics

- Simplified XPath subset: familiar to NETCONF/RESTCONF users, but intentionally limited for performance and simplicity.
- Origin field: disambiguates schemas when multiple models exist (e.g. `openconfig`, `ietf`, vendor-native).
- Prefix support: common ancestor path can be factored out to reduce message size in subscriptions.
- Wildcard support: mainly `*` for all instances of a list (no deep `//` recursion).

