# YANG

YANG (Yet Another Next Generation) is a data modeling language used to programmatically represent both configuration and operational state data on network devices. It is defined in RFC 6020 and serves as the foundation for modern, model-driven network management and automation.

## Purpose and Benefits

YANG promotes unification in networking by enabling structured, programmatic interfaces to devices (e.g., routers and switches) using protocols like NETCONF, RESTCONF, or gNMI. It replaces traditional unstructured CLI outputs or legacy protocols like SNMP with vendor-neutral, hierarchical data models that map directly to programmable entities (like JSON structures). Key advantages include:

- Vendor-neutral modeling for consistency across devices.
- Structured data for easier automation and integration with tools/languages.
- Extensibility through augmentations and deviations.
- Better support for DevOps/NetDevOps workflows (e.g., Ansible, pyATS, Terraform).

## How YANG Models Work

YANG organizes data hierarchically as a tree, where each element is a node with a name and either a value or child nodes. Models are written in modules, which include:

- Header statements (name, namespace, prefix, imports).
- Revision statements (version history).
- Definition statements (the core data model).

YANG defines four main node types:

- Leaf : A single value (no children), e.g., interface name (string) or enabled status (boolean).
- Leaf-list : An ordered sequence of leaf values.
- Container : Groups related nodes (no value itself); can be configuration (`config true`, read-write) or operational state (`config false`, read-only).
- List : A sequence of entries (like a list of interfaces), each identified by a key (e.g., interface name).

## Standard vs. Vendor-Specific Models

- Industry-standard models : Developed by IETF (e.g., `ietf-interfaces.yang`, `ietf-ip.yang`) or OpenConfig for broad compatibility.
- Vendor-specific (native) models : Tailored to a specfic platform. These are often required when standard models lack coverage for vendor-unique features.

All models are publicly available on GitHub:

- https://github.com/YangModels/yang/ 
- https://github.com/openconfig/public/.

## Key Features: Augmentations and Deviations

- Augmentations : Extend base models (e.g., `ietf-ip.yang` adds IPv4/IPv6 details to `ietf-interfaces.yang` using `augment` and conditional `when` statements).
- Deviations : Handle implementation differences (e.g., marking a feature as `not-supported` in a specific OS release).

## Practical Mapping and Tools

YANG structures map naturally to programming concepts, especially Python:

| YANG Element   | Python Equivalent |
|----------------|-------------------|
| Container      | Dictionary        |
| Leaf name      | Dictionary key    |
| Leaf           | Dictionary value  |
| List           | List              |
| String/Boolean/Integer | Corresponding types |
| Empty          | None              |

Tools like Pyang (`pip install pyang`) let you validate models and visualize them as trees (e.g., `pyang -f tree ietf-interfaces.yang`).
