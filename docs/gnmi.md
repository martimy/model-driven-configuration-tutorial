# gNMI

gNMI (gRPC Network Management Interface) is a gRPC-based protocol developed by the OpenConfig project for configuration management and streaming telemetry on network devices (routers, switches, etc.). It provides a single, unified, high-performance service for both modifying/retrieving configuration and generating real-time telemetry streams.

Current specification: version 0.10.0 (published 2023), defined via Protocol Buffers (proto3) in the openconfig/gnmi GitHub repository.

It was created to address the need for efficient, model-driven management - combining configuration (like NETCONF) and telemetry (previously handled separately, e.g., via SNMP traps or proprietary mechanisms) into one modern, binary-efficient protocol built on gRPC.

## Key Characteristics

- Uses gRPC over TLS (>=1.2) for secure, bidirectional communication; mutual authentication via X.509 certificates is required.
- Encoding → Protocol Buffers (preferred for efficiency) with TypedValue (scalars: string, int64, uint64, bool, double, bytes, arrays); also supports JSON, JSON_IETF (RFC 7951), Bytes, ASCII. JSON is mandatory minimum support.
- Paths → XPath-like, structured as ordered lists of PathElem (name + optional key-value pairs); support prefix for common base paths, wildcards (*), origins (e.g., "openconfig", "cli" for vendor-specific).
- Schema-agnostic at protocol level but designed for YANG/OpenConfig models; uses `origin` field to disambiguate schemas.
- Supports transactional configuration changes (atomic all-or-nothing).
- Streaming telemetry via long-lived subscriptions with multiple modes.
- Single gRPC service with four RPCs.

## Main Operations (RPCs)

- Capabilities : Discovery handshake: reports supported models (name/org/version), encodings, gNMI version, extensions.
- Get : Retrieve snapshot of data for specified paths; filter by datatype (CONFIG, STATE, OPERATIONAL); returns timestamped Notification messages with updates/deletes.
- Set : Atomic modification: supports delete (recursive), replace (full subtree overwrite), update (merge leaf changes), union_replace; operations processed in order (delete → replace → update); full rollback on failure.
- Subscribe - Streaming telemetry:
  - ONCE → one-off sync, closes after initial data.
  - POLL → long-lived, client-triggered updates via Poll messages.
  - STREAM → continuous:
    - ON_CHANGE → push on value change + optional heartbeat.
    - SAMPLE → periodic (nanosecond interval) + suppress_redundant option.
    - TARGET_DEFINED → device decides per-leaf mode.
  - Supports qos marking, updates_only (skip initial sync), aggregation.

## Configuration vs Telemetry Handling

- Configuration → read/write ("config true" in YANG); modified via Set.
- State/Operational → read-only telemetry data; retrieved via Get or Subscribe.
- No separate datastores like NETCONF (candidate/running); changes are direct but atomic.

## Advantages

- Unified interface for config + telemetry → simplifies client and device implementations.
- High performance → gRPC streaming + binary Protobuf encoding → low latency/overhead for large-scale telemetry.
- Real-time push telemetry (vs. polling) with fine-grained modes (change detection, sampling).
- Model-driven → strong OpenConfig YANG alignment for vendor neutrality; capabilities ensure compatibility.
- Secure by default → TLS mandatory, supports per-RPC authorization.
- Better suited for SDN, automation pipelines, and large-scale monitoring than legacy protocols.

gNMI has become a cornerstone of modern network automation and telemetry, widely adopted by vendors (Cisco, Juniper, Arista, Nokia, etc.) alongside OpenConfig models, complementing NETCONF (configuration-focused) with superior streaming capabilities.
