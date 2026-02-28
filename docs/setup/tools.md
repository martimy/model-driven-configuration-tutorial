# Tools

You will need a the following tools (but not all at once):

## Infrastructure

- Linux Environment: A native Linux system or WSL2 on Windows is necessary to run Containerlab and Docker.
- [Docker](https://docs.docker.com/engine/install/): Required to run the containerized router images.
- [Containerlab](https://containerlab.dev/install/): This is esential to create the lab environment.

## Protocol Transport Libraries (Python)

These libraries allow your automation scripts to communicate with the devices:

- ncclient: A Python library for NETCONF transport.
- pygnmi: A Python client library for gNMI.

## Interactive CLI Tools for Discovery

These are used for manual exploration and "reverse engineering" before writing code:

- gnmic: A CLI client for gNMI. It is used to explore device capabilities, retrieve state, and test telemetry subscriptions.
- netconf-console2: A CLI clients for NETCONF. They are useful for checking connectivity, retrieving schemas, and testing XML filters without writing Python code.

## YANG Modeling & Validation Tools

- pyang: The essential tool for YANG visualization. It converts verbose YANG source files into a readable tree format (`pyang -f tree`), which acts as your map for constructing configuration paths.
- yanglint (libyang2-tools): A command-line utility used for offline validation. It checks your XML or JSON payloads against the YANG schema to catch errors before they ever touch a live device.
- yangson: A Python library used for programmatic validation and data manipulation within automation scripts.

## Development & Automation Tools

- Python 3 & venv: Used for writing the automation logic; virtual environments (`venv`) are recommended to isolate dependencies.
- Jinja2: A templating engine used to separate the structure of YANG-modeled payloads from the variable data (e.g., IP addresses), making the code more modular.
- xmltodict: Useful for converting XML-based NETCONF responses into Python dictionaries for easier processing.
- VSCode with YANG extension: Provides syntax highlighting and tree navigation for YANG files, which is critical when browsing large vendor model repositories.
