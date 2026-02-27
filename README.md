# Tutorial: 

This tutorial teaches you how to configure network devices using YANG data models. The tutorial is built on Containerlab, an open-source network emulation platform that spins up virtual instances of Nokia SR-Linux and Arista cEOS on your laptop. 

## Prerequisites

- Familiarity with networking fundamentals: IP addressing, routing protocols, etc.
- Comfort with the Linux command line and a text editor

 
## Objectives

## Requirements

### Docker images

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

### Tools

You will need a the following tools:

**1. Infrastructure**

- Linux Environment: A native Linux system or WSL2 on Windows is necessary to run Containerlab and Docker.
- [Docker](https://docs.docker.com/engine/install/): Required to run the containerized router images.
- [Containerlab](https://containerlab.dev/install/): This is esential to create the lab environment.

**2. Protocol Transport Libraries (Python)**

These libraries allow your automation scripts to communicate with the devices:

- ncclient: A Python library for NETCONF transport.
- pygnmi: A Python client library for gNMI.

**3. Interactive CLI Tools for Discovery**

These are used for manual exploration and "reverse engineering" before writing code:

- gnmic: A CLI client for gNMI. It is used to explore device capabilities, retrieve state, and test telemetry subscriptions.
- netconf-console2: A CLI clients for NETCONF. They are useful for checking connectivity, retrieving schemas, and testing XML filters without writing Python code.

**4. YANG Modeling & Validation Tools**

- pyang: The essential tool for YANG visualization. It converts verbose YANG source files into a readable tree format (`pyang -f tree`), which acts as your map for constructing configuration paths.
- yanglint (libyang2-tools): A command-line utility used for offline validation. It checks your XML or JSON payloads against the YANG schema to catch errors before they ever touch a live device.
- yangson: A Python library used for programmatic validation and data manipulation within automation scripts.

**5. Development & Automation Tools**

- Python 3 & venv: Used for writing the automation logic; virtual environments (`venv`) are recommended to isolate dependencies.
- Jinja2: A templating engine used to separate the structure of YANG-modeled payloads from the variable data (e.g., IP addresses), making the code more modular.
- xmltodict: Useful for converting XML-based NETCONF responses into Python dictionaries for easier processing.
- VSCode with YANG extension: Provides syntax highlighting and tree navigation for YANG files, which is critical when browsing large vendor model repositories.
  
## Network Environment

This tutorial is based on a simple three-node multi-vendor network arranged in a ring topology. The topology consists of the following components and connections:

- Nodes: The lab environment includes three routers from two different vendors:

  - ceos-01: An Arista cEOS node.
  - srl-01: A Nokia SR Linux node.
  - srl-02: A second Nokia SR Linux node.

- Managemnet Network: All nodes are connected to a management network named `api-lab` using the IPv4 subnet `192.168.100.0/24`. The IP addresses assigned are:

  - ceos-01: 192.168.100.11
  - srl-01: 192.168.100.12
  - srl-02: 192.168.100.13



