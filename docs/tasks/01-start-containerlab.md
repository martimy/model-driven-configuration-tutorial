# Task 1 - Starting Containerlab

A Containerlab topology is described in a YAML file. If you are not familier with Conatinerlab, here are the basic steps to deploy the topology and interact with the nodes:  

## 1. Start the lab

You deploy the lab using the `deploy` command from the main tutorial folder:

```bash
sudo containerlab deploy -t topology/tutorial.clab.yml
```

or from the topology folder:

```bash
cd topology
sudo containerlab deploy [-t tutorial.clab.yml]
```

> The name of the topology file is optional if there is only one file with this name format in the current folder

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
clab inspect -t topology
```

> `clab` is an alias of `containerlab`



## 2. Access the nodes

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

## 3. End the lab

You can end the lab using the `destroy` command:

```bash
sudo clab destroy [--cleanup]
```

> The local `--cleanup | -c` flag instructs containerlab to remove the lab directory `topology/clab-lab` and all its content. Without this flag present, containerlab will keep the lab directory. Do not use this flag if you want to keep the configuration you saved in the routers.


Containerlab CLI has a large set of commands and flags. Check out the [Command reference](https://containerlab.dev/cmd/deploy/) section to get familiar with all the commands and their usage.
