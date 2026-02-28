# NETCONF

NETCONF (Network Configuration Protocol) is an IETF-standardized network management protocol (RFC 6241, RFC 4741) designed to securely install, manipulate, modify, and delete configuration data on network devices such as routers, switches, and firewalls.

It was created to overcome limitations of older approaches like SNMP (which lacks robust configuration control) and manual/automated CLI scripting (which can be insecure, inconsistent, and hard to automate reliably).

## Key Characteristics

- Uses XML for encoding both protocol messages and configuration data → structured, hierarchical, and machine-readable.
- Follows a client-server model with Remote Procedure Call (RPC) communication.
- Runs over secure, connection-oriented transports, most commonly SSH (port 830), but also supports TLS and others.
- Organized in four conceptual layers:

    1. Content layer (configuration data, often modeled with YANG).
    2. Operations layer (core RPC operations).
    3. Messages layer (framing RPCs and notifications).
    4. Secure transport layer.

## Main Operations

- `<get>` : Retrieve running state and configuration data.
- `<get-config>` : Retrieve configuration from a specific datastore.
- `<edit-config>` : Load or modify configuration data.
- `<copy-config>` : Replace entire datastore contents.
- `<delete-config>` : Remove a non-running datastore.
- `<lock>` / `<unlock>` : Prevent concurrent modifications.
- `<close-session>` / `<kill-session>` : End sessions gracefully or forcefully.
- Supports notifications (e.g., RFC 5277) for asynchronous event reporting.

## Configuration Datastores

Devices maintain separate datastores (e.g., running, candidate, startup), allowing changes to be staged, validated, and committed atomically : a major improvement for safe automation.

## Advantages

- Secure by design (strong transport encryption + authentication).
- Transaction-like behavior and rollback support.
- Programmable and automation-friendly, especially when combined with YANG data models.
- Better suited for large-scale, programmatic network management than SNMP or CLI scraping.

NETCONF has become a foundational protocol for modern network automation, SDN, and intent-based networking, widely supported by vendors like Cisco, Juniper, Nokia, Huawei, and others.
