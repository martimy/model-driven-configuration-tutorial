# Model-Driven Network Configuration Tutorial

[![Docs](https://img.shields.io/badge/Docs-github.io-blue)](https://martimy.github.io/model-driven-configuration-tutorial/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Containerlab](https://img.shields.io/badge/Built%20with-Containerlab-informational)](https://containerlab.dev)

Modern networks are managed through APIs, not CLI sessions. The protocols, NETCONF and gNMI, are well-documented. The gap is everything in between: understanding YANG data models well enough to construct valid configuration payloads, navigating multi-vendor inconsistencies, and knowing why the same OpenConfig path behaves differently on Nokia SR Linux and Arista cEOS.

This tutorial closes that gap. It is a hands-on, lab-based guide to configuring real network devices using YANG models — not scripts, not automation frameworks, just you, the models, and the devices.

📖 **[Read the full tutorial](https://martimy.github.io/model-driven-configuration-tutorial)**

## What You Will Learn

- How YANG modules are structured and how to read them with `pyang`
- How NETCONF and gNMI work at the protocol level, and how they differ
- How to discover what models a device supports and fetch them directly from the device
- How to construct XML and JSON configuration payloads from scratch
- Why multi-vendor environments are harder than the standards suggest, and how to handle it
- Configuring interfaces, IP addressing, network instances, and OSPF across a mixed Nokia/Arista topology

## Why This Tutorial Is Different

Most network automation tutorials skip straight to Python libraries and abstraction frameworks. This one deliberately does not. Understanding the model layer, before any automation tool is involved, is what separates engineers who can debug broken automation from those who cannot.

The lab uses real vendor images (Nokia SR Linux and Arista cEOS) running in Containerlab on your laptop. Every task exposes a real challenge: revision mismatches between vendors, modules that advertise support but cannot be used for configuration, augmentation-only modules that break naive tooling assumptions. These are not edge cases — they are everyday realities in multi-vendor deployments.

This tutorial does not replace vendor documentation or the broader network automation community's work. It synthesizes them into a single, sequenced learning path. The Further Reading section points to the primary sources this tutorial draws from and resources worth exploring once you have completed the lab.

## Prerequisites

- Networking fundamentals: IP addressing, routing protocols
- Linux command line basics
- No prior YANG or NETCONF/gNMI experience required

## Quick Start

```bash
git clone https://github.com/martimy/model-driven-configuration-tutorial.git
cd model-driven-configuration-tutorial
```

You will need [Docker](https://docs.docker.com/engine/install/) and [Containerlab](https://containerlab.dev/install/) installed, as well as the Arista cEOS and Nokia SR Linux container images. See the [Setup guide](https://martimy.github.io/model-driven-configuration-tutorial/setup/docker-images/) for details.

## Repository Structure

```
├── docs/        # Tutorial content (source for GitHub Pages)
├── topology/    # Containerlab topology file and device configs
└── scripts/     # Python scripts for NETCONF and gNMI interaction
```

## Further Reading

This tutorial builds on the work of many contributors to the network automation community. The following are primary sources and recommended next steps:

**Protocols and Standards**
- [RFC 6241 — NETCONF](https://datatracker.ietf.org/doc/html/rfc6241)
- [RFC 7950 — YANG 1.1](https://datatracker.ietf.org/doc/html/rfc7950)
- [gNMI Specification](https://github.com/openconfig/gnmi)

**Vendor Documentation**
- [Nokia SR Linux documentation](https://documentation.nokia.com/srlinux/)
- [Nokia SR Linux YANG models](https://github.com/nokia/srlinux-yang-models)
- [Arista EOS YANG models](https://github.com/aristanetworks/yang)
- [Arista EOS NETCONF/gNMI documentation](https://www.arista.com/en/support/product-documentation)

**Tools**
- [Containerlab](https://containerlab.dev) — the network emulation platform this tutorial is built on
- [gnmic](https://gnmic.openconfig.net) — gNMI CLI client and documentation
- [pyang](https://github.com/mbj4668/pyang) — YANG validation and tree visualization

**Community and Further Learning**
- [OpenConfig working group](https://openconfig.net)
- [YANG models repository](https://github.com/YangModels/yang)
- [Network to Code blog](https://blog.networktocode.com) — practical network automation writing
- [Packet Coders](https://www.packetcoders.io) — network automation training and tutorials

## License

MIT License — see [LICENSE](LICENSE) for details.
