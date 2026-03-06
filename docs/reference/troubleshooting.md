# Troubleshooting



To get a schema:

```bash
./nc_wrapper.sh srl-01 --get-schema ietf-interfaces
```


validation:

yanglint -p ./yang openconfig-interfaces.yang interfaces.xml

xmllint --noout interfaces.xml

The `--dry` option in `netconf-console2` returns the RPC to be sent, so we can use it verify that the XML file is formatted properly.

```bash
./nc_wrapper.sh srl-01 --edit-config=interface.xml --dry
```

./nc_wrapper.sh srl-01 --get-config --filter /interfaces/interface[name=ethernet-1/1] | xmllint --format -