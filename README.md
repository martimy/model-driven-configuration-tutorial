# Model-Driven Network Configuration Tutorial


This tutorial teaches you how to configure network devices using YANG data models. The tutorial is built on Containerlab, an open-source network emulation platform that spins up virtual instances of Nokia SR-Linux and Arista cEOS routers on your laptop. 

## Prerequisites

- Familiarity with networking fundamentals: IP addressing, routing protocols, etc.
- Comfort with the Linux command line and a text editor

 
## Objectives

--to be completed--

## Requirements

### Docker images

To deploy this lab, you will need these two Docker images:

- `ceos:image`: This image is required for the Arista cEOS node (`ceos-01`).
- `ghcr.io/nokia/srlinux`: This image is required for both Nokia SR Linux nodes (`srl-01` and `srl-02`).

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

You will need a the following tools (but not all at once):

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

This tutorial is based on a simple three-node multi-vendor network arranged in a ring topology. The three routers are connected to management network named `api-lab` using the IPv4 subnet `192.168.100.0/24`.

Node | Model | Management IP
:---:|---|---
ceos-01 | Arista cEOS | 192.168.100.11
srl-01  | Nokia SR Linux node | 192.168.100.12
srl-02  | Nokia SR Linux node | 192.168.100.13


# Tasks

Each task introduces a concept, and then provides a set of instructions to explore or implement the concept. Complete the tasks in order as eah taks build upon the previous one.

## Task 1 - Starting Containerlab

A Containerlab topology is described in a YAML file. If you are not familier with Conatinerlab, here are the basic steps to deploy the topology and interact with the nodes:  

### 1. Start the lab

You deploy the lab using the `deploy` command.

```bash
sudo containerlab deploy [-t tutroial.clab.yml]
```
> The name of the topology file is optinal if there is only one file with this name format in the current folder

You will see the summary table with the deployed lab nodes.

```bash
╭─────────┬───────────────────────┬─────────┬────────────────╮
│   Name  │       Kind/Image      │  State  │ IPv4/6 Address │
├─────────┼───────────────────────┼─────────┼────────────────┤
│ ceos-01 │ arista_ceos           │ running │ 192.168.100.11 │
│         │ ceos:image            │         │ N/A            │
├─────────┼───────────────────────┼─────────┼────────────────┤
│ srl-01  │ nokia_srlinux         │ running │ 192.168.100.12 │
│         │ ghcr.io/nokia/srlinux │         │ N/A            │
├─────────┼───────────────────────┼─────────┼────────────────┤
│ srl-02  │ nokia_srlinux         │ running │ 192.168.100.13 │
│         │ ghcr.io/nokia/srlinux │         │ N/A            │
╰─────────┴───────────────────────┴─────────┴────────────────╯
```

You can list the nodes of the lab anytime with containerlab `inspect` command.

```bash
sudo clab inspect [-t tutroial.clab.yml]
```

> `clab` is an alias of `containerlab`


### 2. Access the nodes

You can use `ssh` to access the routers' CLI using the default username/password.

Node | username | password
---|---|---
ceos-01 | admin | admin
srl-01, srl-02 | admin | NokiaSrl1!


For example:

```bash
ssh admin@ceos-01
```

Since the nodes are Docker containers, you can also connect to them through Docker:

```bash 
# access CLI
docker exec -it srl-01 sr_cli
# access bash
docker exec -it srl-01 bash
```

### 3. End the lab

You can end the lab using the `destroy` command:

```bash
sudo clab destroy [--cleanup]
```

> The local `--cleanup | -c` flag instructs containerlab to remove the lab directory and all its content. Without this flag present, containerlab will keep the lab directory and all files inside of it. Do not use this flag if you want to keep the configuration you saved in the routers.


Containerlab CLI has a large set of commands and flags. Check out the [Command reference](https://containerlab.dev/cmd/deploy/) section to get familiar with all the commands and their usage.

## Task 2 - Verifying NETCONF Connectivity

The goal of this task is to initiate a connection to each device and retrieve the HELLO message exchanged at the start of a NETCONF session. This message advertises the device capabilities (such as supported YANG models and protocol features). The NETCONF protocol is designed to run securely over SSH, and port 830 is assigned as the standard default port for this connection.


Once the lab is running, verify that NETCONF is reachable on port 830 using netconf-console2:

```bash
netconf-console2 --host=srl-01 --port 830 -u admin -p NokiaSrl1! --hello
```

> Install netconf-console2 using `pip install netconf-console2`

Alternatively, you may use raw ssh connection:

```bash
ssh admin@ceos-01 -p 830 -s netconf
```

> **What Both Commands Are Actually Doing**  
`netconf-console2` is a dedicated NETCONF client. It handles the SSH transport internally, sends a proper NETCONF <hello> message with its own capabilities, waits for the device's <hello> in response, and then presents the result to you cleanly. It understands the NETCONF framing protocol (the ]]>]]> end-of-message marker in NETCONF 1.0, or chunked framing in 1.1).  
`ssh -s netconf` is raw SSH. It opens the subsystem channel but does nothing after that. You are dropped directly into the NETCONF session at the XML layer. The device sends its <hello> message immediately, and then waits for yours. If you just sit there, nothing further happens — you would need to type raw XML to continue. It is useful for confirming the port is open and the device is responding, but it is not a practical way to send operations.


## Task 3 - Verifying gNMI Connectivity

Verify that `gNMI` is reachable (typically on port 57400) using the gnmic client:

```bash
gnmic -a ceos-01:6030 -u admin -p admin --insecure capabilities
```

You will need a different port number and flag for SR Linux routers

```bash
gnmic -a srl-01:57400 -u admin -p NokiaSrl1! --skip-verify capabilities
```

> Install gnmic using: `bash -c "$(curl -sL https://get-gnmic.openconfig.net)"`

