# Task 4 - Inspect Device Capabilities

Both NETCONF and gNMI provide a way for a client to discover what a device supports before performing configuration or telemetry operations. 

## NETCONF Capabilities

In [Task 2](../tasks/verify-netconf.md), When you run:

```bash
netconf-console2 --host=srl-01 --port 830 -u admin -p 'NokiaSrl1!' --hello
```

the device returns the following in XML format:

- NETCONF versions (1.0, 1.1) and optional features like candidate, confirmed-commit, validate, etc.
- A detailed list of supported modules, including their URNs, names, revision dates, supported features, deviations, augmentations, and explicitly lists multiple modules per URN.

The key characteristics of the output:

- Includes rich metadata such as feature support, deviations, augmentations, and dependencies.
- Each YANG module is individually listed, often with query strings for module details.
- IETF, OpenConfig and vendor-specific modules are included.
- Supports NMDA (Network Management Datastore Architecture) capabilities.


Example:

```bash
<?xml version='1.0' encoding='UTF-8'?>
<nc:hello xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <nc:capabilities>
    <nc:capability>urn:ietf:params:netconf:base:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:base:1.1</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:candidate:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:confirmed-commit:1.1</nc:capability>
    ....
    <nc:capability>urn:ietf:params:xml:ns:yang:ietf-yang-library?module=ietf-yang-library&amp;revision=2019-01-04</nc:capability>
    <nc:capability>urn:nokia.com:srlinux:aaa:aaa?module=srl_nokia-aaa&amp;revision=2025-10-31</nc:capability>
    <nc:capability>urn:nokia.com:srlinux:aaa:aaa-password?module=srl_nokia-aaa-password&amp;revision=2025-07-31</nc:capability>
    <nc:capability>urn:nokia.com:srlinux:aaa:aaa-types?module=srl_nokia-aaa-types&amp;revision=2023-03-31</nc:capability>
    ....
```


## gNMI Capabilities

In [Task 3](../tasks/verify-gnmi.md), When you run:

```bash
gnmic -a srl-01:57400 -u admin -p NokiaSrl1! --skip-verify capabilities
```

the device returns the following in plain text:

- gNMI version (e.g., 0.10.0).
- List of YANG models by URN, including module name, publisher, and revision date.
- Supported encodings: Lists encoding formats such as JSON_IETF, PROTO, ASCII, and related numeric codes.

The key characteristics of the output:

- Provides only the essential details for a gNMI client: supported models and encodings.
- Does not specify per-module features or deviations.
- Models are listed solely by URNs, without feature flags or module breakdowns.


Example:

```bash
gNMI version: 0.10.0
supported models:
  - urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring:ietf-netconf-monitoring, IETF NETCONF (Network Configuration) Working Group, 2010-10-04
  - urn:ietf:params:xml:ns:yang:ietf-yang-library:ietf-yang-library, IETF NETCONF (Network Configuration) Working Group, 2019-01-04
  - urn:nokia.com:srlinux:aaa:aaa:srl_nokia-aaa, Nokia, 2025-10-31
  ...
  - http://openconfig.net/yang/aaa:openconfig-aaa, OpenConfig working group, 2022-07-29
  - http://openconfig.net/yang/acl:openconfig-acl, OpenConfig working group, 2023-02-06
  - http://openconfig.net/yang/aft/ni:openconfig-aft-network-instance, OpenConfig working group, 2023-04-25
  ...
```


In the examples above, the distinction between lines starting with `urn:` and those starting with `http:` reflects the naming authority and origin of the YANG models:

- `urn:` prefixes indicate Nokia proprietary models (e.g., `urn:nokia.com:srlinux:aaa:aaa`). These are internal, vendor-specific schemas defined by Nokia for their SRLinux implementation. They follow a URN format using the `nokia.com` domain.
- `http://` prefixes indicate IETF or OpenConfig models (e.g., `http://openconfig.net/yang/interfaces`). These are industry-standard models defined by OpenConfig working group.
- `https://` prefixes (seen in NETCONF output) indicate OpenConfig gNSI models (e.g., `https://github.com/openconfig/yang/gnsi/authz`), though these appear as `http://` in the gNMI output for simplicity.

This dual-namespace approach allows the device to support both:
1. **Standardized models** (`http://`) for multi-vendor compatibility
2. **Vendor-specific extensions** (`urn:`) for advanced Nokia features not covered by standards


## Conclusion

The gNMI and NETCONF capabilities responses differ in both format and the type of information they convey. NETCONF exposes protocol workflow features while gNMI exposes data model and encoding features. This reflects the different philosophies of the two protocols:

- NETCONF is designed for transactional, configuration-oriented management with deep model introspection.
- gNMI is designed for lightweight, high-frequency streaming and minimal overhead.


## Exercise

Compare the capabilities returned by `ceo-01` for both NETCONF and gNMI. Does cEOS support the same NETCONF capabilities as SR Linux? Explain the difference in the format of the capabilities returned by gNMI?

The differences you notice in both the capabilities, supported models, and formatting, highlight one of the challenges in managing the network via data models in multi-vendor environment.