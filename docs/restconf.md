# RESTCONF

RESTCONF is an IETF-standardized HTTP-based protocol (RFC 8040, January 2017) that provides a programmatic RESTful interface for accessing, configuring, and managing data on network devices (routers, switches, firewalls, etc.). It enables CRUD operations (Create, Read, Update, Delete) on YANG-modeled configuration data, operational state data, RPC operations, and event notifications using standard HTTP methods.

It was designed as a RESTful evolution/complement to NETCONF, addressing the need for a more developer-friendly, web-oriented API that leverages familiar HTTP/REST principles while remaining compatible with NETCONF's YANG datastores and models : making it easier to integrate into modern automation tools, web apps, and orchestration systems.

## Key Characteristics

- Uses HTTP/HTTPS (typically TLS-secured) for transport → stateless, request-response model.
- Encoding → Primarily JSON (preferred for simplicity and web compatibility); also supports XML; content types like `application/yang-data+json` or `application/yang-data+xml`.
- Paths/URIs → Resource-oriented, hierarchical paths derived from YANG models (e.g., `/restconf/data/openconfig-interfaces:interfaces/interface=eth0`); supports query parameters for filtering, pagination, content selection (e.g., `?content=config`, `?depth=`, `?fields=` : device-dependent).
- Relies on YANG data models (RFC 7950) for structure, semantics, and validation; exposes both configuration ("config true") and state/operational data.
- Stateless → Each HTTP request is independent; no built-in sessions or locks like NETCONF (though some implementations may add extensions).
- Supports notifications via Server-Sent Events (SSE) or other mechanisms for asynchronous event streams.
- Security → Mandatory HTTPS/TLS; supports standard HTTP authentication (Basic, Token, OAuth, etc.).

## Main Operations (HTTP Methods)

- GET : Retrieve data (configuration, state, or lists); supports filtering and partial responses.
- POST : Create new resources (e.g., add interface, user); also used for YANG RPC invocation.
- PUT : Replace entire resource/subtree (full overwrite).
- PATCH : Partial update/merge (often with YANG-Patch media type per RFC 8072).
- DELETE : Remove resources.
- OPTIONS / HEAD : Discovery and metadata.
- Additional: Access to /.well-known/restconf or monitoring paths for capabilities discovery; event streams via `/restconf/streams`.

## Configuration vs Operational Data

- Configuration → Writable data stored in device's conceptual datastore(s); supports access to running config (and sometimes candidate/startup via extensions like RFC 8527 for NMDA).
- Operational/State → Read-only runtime data (e.g., interface counters, BGP neighbors).
- No native candidate datastore or atomic multi-operation transactions like NETCONF : changes are direct and immediate (non-transactional by default); suitable for simpler or incremental updates.

## Advantages

- RESTful & familiar → Uses standard HTTP tools/libraries (curl, Postman, Python requests) → low barrier for developers and DevOps teams.
- Web-friendly → Easy integration with web apps, APIs, CI/CD pipelines, cloud orchestration (Ansible, Terraform, etc.).
- Lightweight & scalable → Lower overhead than XML/RPC-based NETCONF for many use cases; stateless design suits distributed systems.
- Vendor-neutral → YANG + RESTCONF promotes consistency across multi-vendor environments.
- Better for rapid prototyping, monitoring, and simple config changes than CLI scraping or full NETCONF stacks.

## Comparison to NETCONF

- Transport/Encoding → RESTCONF: HTTP/HTTPS + JSON/XML; NETCONF: SSH/TLS + XML RPCs.
- Operations → RESTCONF: HTTP methods (CRUD); NETCONF: Structured RPCs (`<edit-config>`, etc.).
- Transactions → NETCONF: Supports candidate datastore, locks, commit/rollback (ACID-like); RESTCONF: Lightweight, no native transactions.
- Use Cases → RESTCONF excels at web/automation integration and quick queries; NETCONF better for complex, safe, batched configuration changes.

RESTCONF has seen growing adoption (Cisco, Juniper, Huawei, Nokia, Arista, etc.), especially in SDN, intent-based networking, and automation ecosystems : often used alongside NETCONF (for config) and gNMI (for telemetry) to provide a modern, API-driven management plane.
