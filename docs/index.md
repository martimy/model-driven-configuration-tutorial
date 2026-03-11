# Model-Driven Network Configuration Tutorial

This tutorial teaches you how to configure network devices using YANG data models. The tutorial is built on Containerlab, an open-source network emulation platform that spins up virtual instances of Nokia SR Linux and Arista cEOS routers on your laptop. 

## Motivation

Modern networks are no longer small, static environments managed primarily through manual configuration. Today’s infrastructures are large-scale, multi-vendor, automated, and continuously changing, which requires management interfaces that are reliable, structured, and programmatically accessible.

Traditional router configuration approaches—especially those centered on CLI interaction—are increasingly inadequate for these environments. To address these challenges, modern network systems are evolving toward an API-first architecture. In this model, configuration and operational state are accessed through structured programmatic interfaces, while the CLI is repositioned as just another client layered on top of these APIs rather than being the primary control interface.

The most significant architectural shift enabling this transition is the adoption of model-driven management, centered around the YANG data modeling language.

## Objectives

In this tutorial, you will:

- Deploy a multi-vendor network topology using Containerlab.
- Understand the core concepts of YANG data modeling and XML/JSON representations.
- Interact with network devices using modern protocols: NETCONF and gNMI.
- Explore device capabilities and download YANG modules directly from routers.
- Configure interfaces, network instances, and IPv4 addressing via model-driven APIs.

## Tasks

Each task introduces a concept, and then provides a set of instructions to explore or implement the concept. Complete the tasks in order as each task builds upon the previous one.
