## Task 3 - Verify gNMI Connectivity


Verify that `gNMI` is reachable (typically on port 57400) using the `gnmic` client.

Install `gnmic`:

```bash
bash -c "$(curl -sL https://get-gnmic.openconfig.net)"
```

Check the connectivity to routers:


```bash
gnmic -a ceos-01:6030 -u admin -p admin --insecure capabilities
```

You will need a different port number and flag for SR Linux routers

```bash
gnmic -a srl-01:57400 -u admin -p NokiaSrl1! --skip-verify capabilities
```

To avoid repeating the global flags, we can use configuration files:

```bash
gnmic --config ceos-gnmic.yml capabilities
```

```bash
gnmic --config srl-gnmic.yml capabilities
```

Use To override the target device in the configuration file: 

```bash
gnmic --config srl-gnmic.yml -a srl-02 capabilities
```