# Model-Driven Network Configuration Tutorial

[![Static Badge](https://img.shields.io/badge/Docs-github.io-blue)](https://martimy.github.io/model-driven-configuration-tutorial/)


This tutorial teaches you how to configure network devices using YANG data models. The tutorial is built on Containerlab, an open-source network emulation platform that spins up virtual instances of Nokia SR-Linux and Arista cEOS routers on your laptop.

📖 **[Read the full tutorial →](https://martimy.github.io/model-driven-configuration-tutorial)**

## Prerequisites

- Familiarity with networking fundamentals: IP addressing, routing protocols, etc.
- Comfort with the Linux command line and a text editor

## Quick Start

Clone the repository and deploy the lab topology:

```bash
git clone https://github.com/martimy/model-driven-configuration-tutorial.git
cd model-driven-configuration-tutorial
```

You will need [Docker](https://docs.docker.com/engine/install/) and [Containerlab](https://containerlab.dev/install/) installed, as well as the Arista cEOS and Nokia SR Linux container images. See the [Setup](https://martimy.github.io/model-driven-configuration-tutorial/setup/docker-images/) in the tutorial for details.

## Repository Structure

```
├── docs/        # Tutorial content (source for GitHub Pages)
├── topology/    # Containerlab topology file and device configs
└── scripts/     # Python automation scripts
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.