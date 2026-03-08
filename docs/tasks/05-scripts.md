# Python Scripts

In addition to `netconf-console2` and `gnmic`, we can use Python scripts to interact with the routers. These scripts are intended to be thin wrappers for some protocol functions, but they are not full automation tools.

Ensure your Containerlab environment is running and your Python virtual environment is activated:

```bash
# Start the lab (if not already running)
sudo containerlab deploy -t topology/tutorial.clab.yml

# Activate the virtual environment
source .pyenv/bin/activate
```

## 1. Using the NETCONF Tool (`netconf_tool.py`)

The NETCONF tool allows you to explore capabilities, retrieve configurations, and download YANG modules.

Usage: `./scripts/netconf_tool.py <device> <action> [schema-name]`

-   List Capabilities: See which NETCONF capabilities the router has.

    ```bash
    ./scripts/netconf_tool.py ceos-01 capabilities
    ```

-   List Modules: See which YANG modules the router supports.

    ```bash
    ./scripts/netconf_tool.py ceos-01 modules
    ```

-   Get Configuration: Retrieve the current `network-instance` configuration in XML format.

    ```bash
    ./scripts/netconf_tool.py srl-02 config '<network-instance/>'
    ```

-   Download a Module (e.g. `openconfig-interfaces`): Save a specific YANG module to a file for inspection.

    ```bash
    ./scripts/netconf_tool.py ceos-01 schema openconfig-interfaces
    ```

## 2. Using the gNMI Tool (`gnmi_tool.py`)

The gNMI tool provides a way to interact with the device's state and configuration using gRPC.

Usage: `./scripts/gnmi_tool.py <device> <action>`

-   List Modules: Retrieve the supported modules.

    ```bash
    ./scripts/gnmi_tool.py srl-01 modules
    ```

- Get Configuration: Retrieve the current configuration (e.g. interfaces). The output is formatted in JSON.

    ```bash
    ./scripts/gnmi_tool.py ceos-01 config 'interfaces'
    ```

## Summary Table

| Tool | Action | Description |
| :--- | :--- | :--- |
| `netconf_tool.py` | `capabilities` | Lists supported NETCONF capabilities. |
| `netconf_tool.py` | `modules` | Lists supported YANG modules. |
| `netconf_tool.py` | `config` | Shows running XML configuration. |
| `netconf_tool.py` | `schema` | Saves a `.yang` file for a specific module. |
| `gnmi_tool.py` | `modules` | Lists gNMI supported modules. |
| `gnmi_tool.py` | `config` | Shows configuration in JSON format. |
