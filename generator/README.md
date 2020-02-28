## JQ Commands for getting possible properties

### Types

Get all fields for `domains[].types[]`:

```bash
jq '[.domains[] | select( has("types") ) | .types[] | keys] | flatten | unique' browser_protocol.json js_protocol.json 

[
  "deprecated",
  "description",
  "enum",
  "experimental",
  "id",
  "items",
  "properties",
  "type"
]
[
  "description",
  "experimental",
  "id",
  "properties",
  "type"
]
```

Get all values of `domains[].types[].type`:

```bash
jq '[.domains[] | select( has("types") ) | .types[].type] | unique' browser_protocol.json js_protocol.json 

[
  "array",
  "integer",
  "number",
  "object",
  "string"
]
[
  "integer",
  "number",
  "object",
  "string"
]
```

Get all fields for `domains[].types[type=="object"].properties[]`:

```bash
jq '[.domains[] | select( has("types") ) | .types[] | select(.type == "object") | select( has("properties") ) | .properties[] | keys] | flatten | unique' browser_protocol.json js_protocol.json

[
  "$ref",
  "description",
  "enum",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
[
  "$ref",
  "description",
  "enum",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
```

### Commands

Get all fields for `domains[].commands[]`:

```bash
jq '[.domains[].commands[] | keys ] | flatten | unique' browser_protocol.json js_protocol.json

[
  "deprecated",
  "description",
  "experimental",
  "name",
  "parameters",
  "redirect",
  "returns"
]
[
  "description",
  "experimental",
  "name",
  "parameters",
  "redirect",
  "returns"
]
```

Get all fields for `domains[].commands[].parameters[]`:

```bash
jq '[.domains[].commands[] | select( has("parameters") ) | .parameters[] | keys ] | flatten | unique' browser_protocol.json js_protocol.json

[
  "$ref",
  "deprecated",
  "description",
  "enum",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
[
  "$ref",
  "description",
  "enum",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
```

Get all fields for command `domains[].commands[].returns[]`:

```bash
jq '[.domains[].commands[] | select( has("returns") ) | .returns[] | keys ] | flatten | unique' browser_protocol.json js_protocol.json

[
  "$ref",
  "description",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
[
  "$ref",
  "description",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
```

### Events

Get all fields for `domains[].events[]`:

```bash
jq '[.domains[] | select( has("events") ) | .events[] | keys ] | flatten | unique' browser_protocol.json js_protocol.json

[
  "deprecated",
  "description",
  "experimental",
  "name",
  "parameters"
]
[
  "description",
  "experimental",
  "name",
  "parameters"
]
```

Get all fields for `domains[].events[].parameters[]`:

```bash
jq '[.domains[] | select( has("events") ) | .events[] | select( has("parameters") ) | .parameters[] | keys ] | flatten | unique' browser_protocol.json js_protocol.json

[
  "$ref",
  "deprecated",
  "description",
  "enum",
  "items",
  "name",
  "optional",
  "type"
]
[
  "$ref",
  "description",
  "enum",
  "experimental",
  "items",
  "name",
  "optional",
  "type"
]
```