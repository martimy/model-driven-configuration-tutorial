# Tutorial: 

This tutorial teaches you how to configure network devices using YANG data models. The tutorial is built on Containerlab, an open-source network emulation platform that spins up virtual instances of Nokia SR-Linux and Arista cEOS on your laptop. 

## Objectives


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



