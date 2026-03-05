# pyang

pyang is a YANG validator, transformator, and code generator written in Python. It can be used to validate YANG modules for correctness, transform them into other formats, and write plugins to generate code from the modules.

Install using:

```bash
pip install pyang
```

## Common Options

| Option | Description |
|---|---|
| `-h, --help` | Print help and exit |
| `-v` | Print version and exit |
| `-f <format>` | Output format (tree, yin, xsd, jstree, etc.) |
| `-o <file>` | Write output to a file |
| `-p <path>` | Add a directory to the YANG module search path |
| `--canonical` | Validate module according to canonical YANG order |
| `--strict` | Force strict YANG compliance |


## Output Formats (`-f`)

pyang can generate a compact tree representation of YANG models for quick visualization, translate YANG models to DSDL schemas for validating XML instance documents, generate UML diagrams, and perform schema-aware translation between XML and JSON.

| Format | Description |
|---|---|
| `tree` | Human-readable ASCII tree view (most popular) |
| `yin` | Convert to YIN (XML equivalent of YANG) |
| `xsd` | Generate W3C XML Schema |
| `jstree` | HTML/JavaScript interactive YANG browser |
| `jtox` | JSON driver file for XML↔JSON conversion |
| `uml` | UML diagram output |
| `dsdl` | Hybrid DSDL schema (RFC 6110) |
| `sample-xml-skeleton` | Skeleton XML instance document |


## Tree-Specific Options

These are some of the most commonly used options in practice:

```bash
pyang -f tree module.yang
```

You can filter the tree output by path and depth, for example:
`pyang module.yang -f tree --tree-path=/bgp/neighbors --tree-depth=4`


| Option | Description |
|---|---|
| `--tree-path=<path>` | Show only the subtree at the given XPath |
| `--tree-depth=<n>` | Limit output to N levels deep |
| `--tree-help` | Print explanation of tree symbols |

**Tree symbols:**
- `+--rw` — read-write node
- `+--ro` — read-only node
- `?` — optional node
- `*` — list (multiple instances)


## Error & Warning Options

You can print a listing of all error codes with `--list-errors`, treat warnings as errors with `-Werror`, suppress all warnings with `-Wnone`, and selectively treat specific error codes as warnings or errors.

| Option | Description |
|---|---|
| `-e, --list-errors` | List all possible error codes and exit |
| `-Werror` | Treat all warnings as errors |
| `-Wnone` | Suppress all warnings |
| `-W <errorcode>` | Treat a specific error as a warning |
| `--max-line-len=<n>` | Warn if any line exceeds N characters |


## Module Resolution Options

| Option | Description |
|---|---|
| `-p <path>` | Add search path for YANG modules |
| `--features <mod:feat>` | Specify active features for a module |
| `--hello` | Parse a NETCONF `<hello>` message as input |

The `--features` option can be used repeatedly — each occurrence defines active (supported) features for one YANG module. If no `--features` option is present for a module, all features defined in that module are considered active.


## Common Usage Examples

```bash
# Validate a YANG module
pyang module.yang

# View as tree
pyang -f tree module.yang

# Convert to YIN (XML)
pyang -f yin -o module.yin module.yang

# Tree with path filter and depth limit
pyang -f tree --tree-path=/interfaces/interface --tree-depth=3 module.yang

# Validate multiple modules
pyang module1.yang module2.yang

# Use a search path for dependencies
pyang -p ./yang-modules -f tree module.yang

# Strict mode validation
pyang --strict module.yang
```

