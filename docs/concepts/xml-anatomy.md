# Anatomy of the XML file 

When you retrieve configuration from a device using NETCONF `<get-config>`, the reply is an XML-encoded instance of a YANG data model.

Below is a structured breakdown of the anatomy of that XML, using examples aligned with:

- Arista cEOS
- Nokia SR Linux

## High-Level NETCONF Envelope

A devices receives (see how to replicate this below):

```xml
<rpc message-id="101"
     xmlns="urn:ietf:params:netconf:base:1.0">
  <get-config>
    <source>
      <running/>
    </source>
  </get-config>
</rpc>
```

The device replies with:

```xml
<rpc-reply message-id="101"
           xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
      ...
  </data>
</rpc-reply>
```

The the XML includes the NETCONF response container `<rpc-reply>`, the `message-id`, which correlates requests and responses and `<data>`, which contains YANG-modeled configuration data. Everything inside `<data>` is structured according to YANG.

## YANG-to-XML Mapping

Here is the YANG-to-XML mapping:

| YANG Concept | XML Representation        |
---|---
| container    | XML element               |
| list         | Repeated XML elements     |
| list key     | Child element inside list |
| leaf         | XML element with text     |
| leaf-list    | Repeated XML elements     |
| namespace    | `xmlns="..."` attribute   |


### Example: Arista cEOS (OpenConfig Interfaces)

cEOS commonly supports OpenConfig YANG models.

Example YANG structure (simplified OpenConfig):

```yang
container interfaces {
  list interface {
    key "name";
    leaf name { type string; }
    container config {
      leaf name { type string; }
      ...
    }
  }
}
```

XML returned by `<get-config>`

```xml
<data>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <interface>
        <name>Management0</name>
        <config>
          <name>Management0</name>
          ...
        </config>
  </interfaces>
</data>
```

**Anatomy Breakdown**

1. Namespace

    ```xml
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
    ```

    - Tells us which YANG module this data belongs to
    - Prevents name collisions
    - Critical for XML parsing

2. Container

    ```xml
    <interfaces>
    ```

    Maps directly to:

    ```yang
    container interfaces
    ```

3. List

    ```xml
    <interface>
    ```

    Maps to:

    ```yang
    list interface
    ```

    Each `<interface>` is one list entry.

4. List Key

    ```xml
    <name>Management0</name>
    ```

    - This is the key leaf
    - Identifies the list instance
    - Required for uniqueness

    Equivalent to:

    ```yang
    key "name";
    ```

5. Nested Container

    ```xml
    <config>
    ```

    Maps to:

    ```yang
    container config
    ```

6. Leaf Nodes

    ```xml
    <name>Management0</name>
    ...
    ```


## Understanding Config vs State

Often you'll see:

```xml
<interfaces>
  <interface>
    <config>...</config>
    <state>...</state>
  </interface>
</interfaces>
```

This is because OpenConfig separates:

- `config`  for intended configuration
- `state` for operational values (read-only)

If you use `<get-config>`, you usually retrieve only `config`. If you use `<get>`, you retrieve both.


## Namespaces in Detail

You may also see prefixed namespaces:

```xml
<oc-if:interfaces
   xmlns:oc-if="http://openconfig.net/yang/interfaces">
```

This happens when:

- Multiple YANG modules are used in one payload
- The device includes augmentations

Example:

```xml
<interfaces xmlns="http://openconfig.net/yang/interfaces">
  <interface>
    <name>Ethernet1</name>
    <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
      <config>
        <port-speed>SPEED_100GB</port-speed>
      </config>
    </ethernet>
  </interface>
</interfaces>
```

Different namespace results in a different YANG module.

## How to Read Any `<get-config>` XML

When teaching or analyzing, follow this order:

1. Identify the namespace → which YANG module?
2. Identify top-level container
3. Identify lists and their keys
4. Separate config vs state
5. Map XML elements back to YANG definitions
6. Check for augmentations (extra namespaces)


## Debugging using SSH

The first section shows a raw NETONF command `get-config` being sent to a device. Typically, tools such as `ncclient` or 'netconf-console2` hide the details of the exchanges between the device and the client. To exchanges raw messages, you can use `ssh`:

```bash
ssh -s -p 830 admin@srl-01 netconf
```

SR Linux immediately sends you its `<hello>`, so you will need to send your `<hello>` message as well. Copy and paste this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
```

Then copy and paste the `<get-config>` command:

```xml
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get-config>
    <source>
      <running/>
    </source>
  </get-config>
</rpc>
]]>]]>
```

The device will reply with its running configuration.

> Note that the correct XML namespace is `urn:ietf:params:xml:ns:netconf:base:1.0`, which is what's defined in RFC 4741 (NETCONF 1.0) and is what SR Linux actually validates against. The URN returned in the capabilities `urn:ietf:params:netconf:base:1.0` is an abbreviated version of the namespace.

