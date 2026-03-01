# Task 2 - Verify NETCONF Connectivity

The goal of this task is to initiate a connection to each device and retrieve the HELLO message exchanged at the start of a NETCONF session. This message advertises the device capabilities (such as supported YANG models and protocol features). The NETCONF protocol is designed to run securely over SSH, and port 830 is assigned as the standard default port for this connection.

If you have not done so already, install `netconf-console2`, preferably in [Python virtual environment](../setup/pyvirtual.md).

Once the lab is running, verify that NETCONF is reachable on port 830 using netconf-console2:


```bash
netconf-console2 --host=srl-01 --port 830 -u admin -p NokiaSrl1! --hello
```

> Install netconf-console2 using `pip install netconf-console2`

Alternatively, you may use raw ssh connection:

```bash
ssh admin@ceos-01 -p 830 -s netconf
```

> **What Both Commands Are Actually Doing**  
`netconf-console2` is a dedicated NETCONF client. It handles the SSH transport internally, sends a proper NETCONF <hello> message with its own capabilities, waits for the device's <hello> in response, and then presents the result to you cleanly. It understands the NETCONF framing protocol (the ]]>]]> end-of-message marker in NETCONF 1.0, or chunked framing in 1.1).  
`ssh -s netconf` is raw SSH. It opens the subsystem channel but does nothing after that. You are dropped directly into the NETCONF session at the XML layer. The device sends its <hello> message immediately, and then waits for yours. If you just sit there, nothing further happens — you would need to type raw XML to continue. It is useful for confirming the port is open and the device is responding, but it is not a practical way to send operations.


Moving forwards, you can avoid adding credentials to the `netconf-console2` command line by using a wrapper script. For example:

```bash
./nc_wrapper.sh ceos-01 --hello
```
