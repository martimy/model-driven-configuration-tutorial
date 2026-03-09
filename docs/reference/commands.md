# Command Quick Reference

## 1. Environment Setup

Containerlab

Purpose | Command
---|---------
Deploy the lab | sudo containerlab deploy -t topology/tutorial.clab.yml
List running nodes | clab inspect -t topology
Destroy the lab | sudo clab destroy [--cleanup]

Node Access

Purpose | Command
---|---------
SSH to a node | ssh admin@<node>
Access SR Linux CLI via Docker | docker exec -it srl-01 sr_cli
Access SR Linux bash via Docker | docker exec -it srl-01 bash
NETCONF raw SSH session | ssh -s -p 830 admin@srl-01 netconf

Python Virtual Environment

Purpose | Command
---|---------
Clone tutorial repo | git clone https://github.com/martimy/model-driven-configuration-tutorial tutorial
Create virtual environment | python3 -m venv .pyenv
Activate virtual environment | source .pyenv/bin/activate
Install dependencies | pip install -r requirements.txt
Deactivate virtual environment | deactivate
Install pyang | pip install pyang
Install gnmic | bash -c "$(curl -sL https://get-gnmic.openconfig.net)"

Docker Images

Purpose | Command
---|---------
Import Arista cEOS image | docker import cEOS-lab-4.35.1F.tar.xz ceos:image
Pull Nokia SR Linux image | docker pull ghcr.io/nokia/srlinux

Clone YANG Model Repositories

Purpose | Command
---|---------
IETF YANG models | git clone https://github.com/YangModels/yang ietf
OpenConfig YANG models | git clone https://github.com/openconfig/public/ openconfig
Arista EOS YANG models | git clone https://github.com/aristanetworks/yang arista
Nokia SR Linux YANG models | git clone -b v25.10.1 --depth 1 https://github.com/nokia/srlinux-yang-models nokia

## 2. NETCONF (netconf-console2 / nc_wrapper.sh)

Connectivity & Capabilities

Purpose | Command
---|---------
Verify NETCONF connectivity (hello) | netconf-console2 --host=<node> --port 830 -u admin -p <pass> --hello
Verify via wrapper script | ./nc_wrapper.sh <node> --hello
Raw SSH NETCONF probe | ssh admin@<node> -p 830 -s netconf

Discovery

Purpose | Command
---|---------
List supported YANG modules | ./scripts/netconf_tool.py <node> modules
Filter modules by keyword | ./scripts/netconf_tool.py <node> modules | grep "<keyword>"
Download a YANG module from device | ./scripts/netconf_tool.py <node> schema <module-name>
Get schema via wrapper | ./nc_wrapper.sh <node> --get-schema <module-name>
List all NETCONF capabilities | ./scripts/netconf_tool.py <node> capabilities

Configuration Retrieval

Purpose | Command
---|---------
Get full running configuration | ./nc_wrapper.sh <node> --get-config
Get config with XPath filter | ./nc_wrapper.sh <node> --get-config --filter /<top-element>
Get config using XML filter file | ./nc_wrapper.sh <node> <filter-file>.xml
Get running config (Python tool) | ./scripts/netconf_tool.py <node> config '<filter/>'

Configuration Push

Purpose | Command
---|---------
Load config to candidate datastore | ./nc_wrapper.sh <node> --edit-config=<file>.xml --db=candidate
Commit candidate to running | ./nc_wrapper.sh <node> --commit
Load and commit in one step | ./nc_wrapper.sh <node> --edit-config=<file>.xml --db=candidate --commit
Dry run (preview RPC without sending) | ./nc_wrapper.sh <node> --edit-config=<file>.xml --dry

## 3. gNMI (gnmic)

Connectivity & Capabilities

Purpose | Command
---|---------
Check cEOS capabilities (direct) | gnmic -a ceos-01:6030 -u admin -p admin --insecure capabilities
Check SR Linux capabilities (direct) | gnmic -a srl-01:57400 -u admin -p NokiaSrl1! --skip-verify capabilities
Check capabilities via config file | gnmic --config <node>-gnmic.yml capabilities
Override target in config file | gnmic --config srl-gnmic.yml -a srl-02 capabilities

Discovery

Purpose | Command
---|---------
List supported YANG modules | ./scripts/gnmi_tool.py <node> modules

Configuration Retrieval

Purpose | Command
---|---------
Get config at a path | gnmic --config <node>-gnmic.yml get --path <gnmi-path> -t config
Get config (Python tool) | ./scripts/gnmi_tool.py <node> config '<top-element>'

Configuration Push

Purpose | Command
---|---------
Set (update) a path with inline value | gnmic --config <node>-gnmic.yml set --update-path <path> --update-value '<json>'
Set using a request file | gnmic --config <node>-gnmic.yml set --request-file <file>.yml
Generate a set-request template | gnmic generate --file openconfig set-request --update <path> > <file>.yml

## 4. YANG Module Inspection (pyang)

Purpose | Command
---|---------
Validate a module | pyang <module>.yang
Display full tree | pyang -f tree <module>.yang
Tree with search path for dependencies | pyang -f tree -p <path> <module>.yang
Tree filtered to a subtree path | pyang -f tree --tree-path=/<path> <module>.yang
Tree limited to N levels deep | pyang -f tree --tree-depth=<n> <module>.yang
Tree across multiple modules (augments) | pyang -f tree -p <path> --tree-path=/<path> <dir>/*.yang
Generate XML skeleton for config | pyang -f sample-xml-skeleton --sample-xml-skeleton-doctype=config <module>.yang
Generate XML skeleton at a subtree | pyang -f sample-xml-skeleton --sample-xml-skeleton-path=/<path> --sample-xml-skeleton-doctype=config <dir>/*.yang
Generate XML skeleton to file | pyang -f sample-xml-skeleton --ignore-errors --sample-xml-skeleton-doctype=config <module>.yang > <file>.xml
Strict validation | pyang --strict <module>.yang

## 5. Payload Validation

Purpose | Command
---|---------
Validate XML syntax | xmllint --noout <file>.xml
Validate XML against YANG schema | yanglint -p <yang-path> <module>.yang <file>.xml
Format/pretty-print XML output | ./nc_wrapper.sh <node> --get-config --filter <path> | xmllint --format -

