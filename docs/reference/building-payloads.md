# Building Configuration Payloads


Before you can configure a device using NETCONF or gNMI, you must construct a valid payload, an XML document for NETCONF or a JSON object for gNMI, that conforms precisely to the YANG module the device uses for that feature. Getting this payload right is often the most time-consuming part of model-driven configuration work.

Throughout this tutorial you have used several techniques to build these payloads. This section summarises all of them, compares their strengths and limitations, and introduces one additional approach not yet covered.


## Technique 1: pyang Sample XML Skeleton

The `pyang` tool can generate a skeleton XML document directly from a YANG module file. The skeleton contains every element defined in the module, with empty tags that you fill in. It is the closest thing to an auto-generated template for NETCONF payloads.

```bash
pyang -f sample-xml-skeleton --sample-xml-skeleton-doctype=config <module>.yang
```

For modules that augment others, such as `openconfig-if-ip`, which adds IPv4/IPv6 nodes to `openconfig-interfaces`, you must pass all related modules together and specify the subtree path you want:

```bash
pyang -f sample-xml-skeleton \
-p openconfig \
--sample-xml-skeleton-path=/interfaces/interface \
--sample-xml-skeleton-doctype=config \
openconfig/release/models/interfaces/*.yang
```

Strengths:

- Completely offline — no device connection needed.
- Covers every element in the module, including optional ones.
- Makes the full YANG tree structure immediately visible.
- Works equally well for IETF, OpenConfig, and native modules.

Limitations:

- Does not differentiate mandatory fields from optional ones — the skeleton includes everything.
- Augmentation-only modules (e.g., openconfig-if-ip) produce empty output unless parent modules are also included.
- Does not reflect vendor deviations — elements the device marks as not-supported will still appear.
- Produces XML only; not suitable for direct use as a gNMI JSON payload.


## Technique 2: Configure via CLI, Then Read Back

Configure the desired feature on the device using its CLI, then immediately retrieve that configuration over NETCONF or gNMI. The response gives you the exact YANG-encoded representation the device uses: correct namespaces, element names, key values, and hierarchy. Use that output as the basis for your payload.

Using NETCONF

```bash
./nc_wrapper.sh <node> --get-config --filter /<top-element>
```


Using gNMI

```bash
gnmic --config <node>-gnmic.yml get \
  --path /<gnmi-path> -t config
```

Strengths:

- The output is guaranteed to be valid; it is exactly what the device accepted and stored.
- Reflects vendor deviations and augmentations automatically; you see what the device actually supports, not what the standard says it should.
- Fastest technique for complex features where the YANG tree is large or poorly documented.
- Works for both XML (NETCONF) and JSON (gNMI) payloads.
- Clearly separates mandatory from optional fields. Mandatory fields will always appear; optional ones may or may not, depending on whether they hold non-default values.

Limitations:

- Requires CLI access to the device, which may not always be available or desirable.
- The retrieved configuration includes only fields that differ from defaults, so some mandatory-but-defaulted fields may be absent from the output.
- For a second device of a different vendor, you must repeat the process; the payload is not necessarily portable.
- Does not teach you the underlying YANG structure; it is a shortcut, not a substitute for understanding the model.

Note: This technique is especially valuable when working with native vendor modules for the first time, or when vendor documentation is unclear. It is also the most reliable way to discover how a device encodes a feature that involves complex augmentations or identity references.


## Technique 3: gnmic generate

The gnmic tool includes a generate subcommand that produces configuration payload templates directly from the device's advertised YANG modules. Unlike the pyang skeleton, which requires you to have the module files locally, gnmic generate fetches the models from the live device and outputs a ready-to-use set-request file in YAML format.

```bash
gnmic generate --file openconfig set-request --update /<path> > request.yml
```


The generated YAML file has the structure expected by gnmic `set --request-file`, so after editing the placeholder values it can be pushed directly to the device:

```bash
gnmic --config <node>-gnmic.yml set --request-file request.yml
```


Strengths:

- Produces JSON-structured output, making it the natural counterpart to pyang sample-xml-skeleton for gNMI workflows.
- The output is already formatted as a set-request, so no transformation step is needed before pushing.
- Pulls models from the live device, so the output reflects the exact module version the device is running.
- Useful for generating path lists as well as payload templates.

Limitations:

- Requires a live device connection.
- Generated YAML contains placeholder values (empty strings, zeros) and quoted booleans/integers that must be corrected manually before use.
- Like the pyang skeleton, it does not distinguish mandatory from optional fields.
- Output can be verbose for large subtrees; scoping the path carefully is important.


## Technique 4: Read-Modify-Write

Rather than building a payload from scratch, retrieve the current configuration of the target object, modify only the fields you want to change, and push the result back. This is a natural extension of Technique 2 and works well when you are making incremental changes to an already-configured feature.

NETCONF

The default edit-config operation is merge, meaning the device merges your payload into the existing configuration. You only need to include the fields you want to change, plus any key fields required to identify the list entry.

```bash
# Retrieve current config:
./nc_wrapper.sh <node> --get-config --filter /<path>
```

```bash
# Edit the XML, then push only the changed fields:
./nc_wrapper.sh <node> --edit-config=changes.xml --db=candidate --commit
```

gNMI

The gnmic set command with `--update-path` also performs a merge operation, updating only the specified path while leaving the rest of the configuration intact.

```bash
gnmic --config <node>-gnmic.yml set --update-path /<path> --update-value '{<json>}'
```

Strengths:

- Minimises the risk of accidentally overwriting unrelated configuration.
- Produces very small, focused payloads that are easy to review and audit.
- Merge semantics mean partial payloads are safe for most configuration changes.

Limitations:
- Requires a live device and an existing configuration to read from.
- Not suitable for initial configuration of a feature that does not yet exist on the device.
- When using replace instead of the default merge operation, the full subtree must be included in the payload, or unspecified fields will be deleted.


## Technique 5: Payload Generation from a pyang JSON Driver (jtox)

`pyang` supports a jtox output format that generates a JSON driver file describing the YANG module structure. This driver file can then be used with the `json2xml` tool (part of the `pyang` package) to convert between JSON and XML representations of the same data. This is particularly useful when you want to work in JSON (e.g. when constructing gNMI payloads), but your reference is the XML skeleton from Technique 1.

```bash
# Step 1: Generate the JSON driver file
pyang -f jtox -p <yang-path> -o <module>.jtox <module>.yang
```

```bash
# Step 2: Convert a JSON instance to XML (for NETCONF)
json2xml -t config <module>.jtox <instance>.json > <instance>.xml
```

```bash
# Step 3: Convert an XML instance to JSON (for gNMI)
xml2json <module>.jtox <instance>.xml > <instance>.json
```

Strengths:

- Enables format conversion between XML and JSON using the same YANG model as the source of truth.
- Useful when your team works in JSON but your reference documentation shows XML examples, or vice versa.
- Completely offline — no device needed.

Limitations:
- The jtox workflow is less commonly used and less well-documented than the other techniques.
- `json2xml` and `xml2json` require the `pyang` package and are not always installed by default.
- Does not handle vendor augmentations as cleanly as the live-device techniques.
- The conversion is schema-driven but does not validate content — values must still be correct for the device to accept the payload.


## Comparison Summary

Technique | Best Used When | Protocol | Key Tool
---|---|---|---
pyang skeleton | First exploration of a module | NETCONF (XML) | pyang
CLI read-back | Complex features, native modules | NETCONF / gNMI | nc_wrapper / gnmic
gnmic generate | gNMI payload templates | gNMI (JSON/YAML) | gnmic
Read-modify-write | Incremental changes to existing config | NETCONF / gNMI | nc_wrapper / gnmic
pyang jtox conversion | XML ↔ JSON format translation | Both | pyang / json2xml


## Recommended Workflow

In practice, these techniques are complementary rather than mutually exclusive. A typical workflow for configuring a new feature on a multi-vendor topology looks like this:

- Start with the `pyang` tree (not the skeleton) to understand the module structure and identify which paths are relevant.
- Use the `pyang` skeleton or `gnmic` generate to produce an initial template, depending on whether you are targeting NETCONF or gNMI.
- Configure the feature on one device via CLI and read it back to validate your payload and catch any vendor-specific deviations.
- Use read-modify-write for subsequent changes once the initial configuration is in place.
- Use the jtox conversion if you need to reuse the same payload across both protocols.

Note: No single technique is sufficient for all situations. The CLI read-back approach (Technique 2) is the most reliable for getting a correct payload quickly, but it does not scale to fully automated workflows where no CLI access is available. The pyang-based techniques scale better but require more upfront understanding of the YANG structure.

