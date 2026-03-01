# Automation Scripts

Besides `netconf-console2` and `gnmic`, we can use Python scripts to interact with the routers. These scripts could simplify some complex tasks and ultimately help automate the network configuration.


Ensure your Containerlab environment is running and your Python virtual environment is activated:

```bash
# Start the lab (if not already running)
sudo containerlab deploy -t topology/tutorial.clab.yml

# Activate the virtual environment
source .pyenv/bin/activate
```

## 1. Using the NETCONF Tool (`netconf_tool.py`)

The NETCONF tool allows you to explore capabilities, retrieve configurations, and download YANG schemas.

Usage: `python scripts/netconf_tool.py <device> <action> [schema-name]`

-   List Capabilities: See which YANG modules the router supports.

    ```bash
    python scripts/netconf_tool.py ceos-01 capabilities
    ```

-   Get Configuration: Retrieve the current `network-instance` configuration in XML format.

    ```bash
    python scripts/netconf_tool.py srl-02 config '<network-instance/>'
    ```

-   Download a Schema (e.g. `openconfig-interfaces`): Save a specific YANG model to a file for inspection.

    ```bash
    python scripts/netconf_tool.py ceos-01 schema openconfig-interfaces
    ```

## 2. Using the gNMI Tool (`gnmi_tool.py`)

The gNMI tool provides a modern way to interact with the device's state and configuration using gRPC.

Usage: `python scripts/gnmi_tool.py <device> <action>`

-   List Capabilities: Retrieve the supported gNMI versions and models.

    ```bash
    python scripts/gnmi_tool.py srl-01 capabilities
    ```

- Get Configuration: Retrieve the current configuration (e.g. interfaces). The output is formatted in JSON.
    ```bash
    python scripts/gnmi_tool.py ceos-01 config 'interfaces'
    ```

## Summary Table

| Tool | Action | Description |
| :--- | :--- | :--- |
| `netconf_tool.py` | `capabilities` | Lists supported NETCONF/YANG modules. |
| `netconf_tool.py` | `config` | Shows running XML configuration. |
| `netconf_tool.py` | `schema` | Saves a `.yang` file for a specific model. |
| `gnmi_tool.py` | `capabilities` | Lists gNMI supported models and versions. |
| `gnmi_tool.py` | `config` | Shows configuration in JSON format via gNMI. |
