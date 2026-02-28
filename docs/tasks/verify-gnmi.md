## Task 3 - Verify gNMI Connectivity

Verify that `gNMI` is reachable (typically on port 57400) using the gnmic client:

```bash
gnmic -a ceos-01:6030 -u admin -p admin --insecure capabilities
```

You will need a different port number and flag for SR Linux routers

```bash
gnmic -a srl-01:57400 -u admin -p NokiaSrl1! --skip-verify capabilities
```

> Install gnmic using: `bash -c "$(curl -sL https://get-gnmic.openconfig.net)"`

