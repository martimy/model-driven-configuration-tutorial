# Tutorial: 

This tutorial teaches you how to configure network devices using YANG data models. The tutorial is built on Containerlab, an open-source network emulation platform that spins up virtual instances of Nokia SR-Linux and Arista cEOS on your laptop. 

## Prerequisites

- Familiarity with networking fundamentals: IP addressing, routing protocols, etc.
- Comfort with the Linux command line and a text editor
- Docker installed on your workstation (required for Containerlab)
 
## Objectives

## Requirements

To deploy this lab, the following two Docker images are required:

- `ceos:image`**: This image is required for the **Arista cEOS** node (`ceos-01`).
- `ghcr.io/nokia/srlinux`**: This image is required for both **Nokia SR Linux** nodes (`srl-01` and `srl-02`).

**Getting Arista cEOS image**

To obtain Arista cEOS images:

- Register/Login: Create an account on the [Arista website](https://www.arista.com/en/login).
- Locate Image: Go to the Software Downloads section, select "cEOS-lab", and choose the desired release (this tutorial uses: cEOS-lab-4.35.1F.tar.xz).
- Download: Download the cEOS-lab-xxx.tar.xz file to your local machine.
- Transfer: Move the file to your lab environment (e.g., Ubuntu VM or Docker host) using sftp or scp.
- Import: Import the image into Docker:

```bash
docker import  cEOS-lab-4.35.1F.tar.xz ceos:image
```

**Getting SR Linux image**

Nokia SR Linux follows a free and open distribution model. You can pull SR Linux container from a public registry:

```
docker pull ghcr.io/nokia/srlinux
```

  
## Environment

This tutorial is based on a simple three-node multi-vendor network arranged in a ring topology. The topology consists of the following components and connections:

- Nodes: The lab environment includes three routers from two different vendors:

  - ceos-01: An Arista cEOS node.
  - srl-01: A Nokia SR Linux node.
  - srl-02: A second Nokia SR Linux node.

- Managemnet Network: All nodes are connected to a management network named `api-lab` using the IPv4 subnet `192.168.100.0/24`. The IP addresses assigned are:

  - ceos-01: 192.168.100.11
  - srl-01: 192.168.100.12
  - srl-02: 192.168.100.13



