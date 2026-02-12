# abaplint Reference

abaplint is a standalone ABAP code linter that works outside of SAP systems. It checks ABAP code for syntax errors, best practices, and configurable rules.

## Installation

Requires [Node.js](https://nodejs.org) v16+.

```bash
npm install @abaplint/cli -g
```

## Usage

Run in a folder containing ABAP source files:

```bash
abaplint
```

Generate a default config (all rules enabled):

```bash
abaplint -d > abaplint.json
```

## Configuration

Place `abaplint.json` in the repository root. The config has three main sections: `global`, `dependencies`, `syntax`, and `rules`.

### Global Settings

```json
{
  "global": {
    "files": "/src/**/*.*",
    "skipGeneratedFunctionGroups": true
  }
}
```

### Dependencies

Dependencies provide type definitions for standard SAP objects:

- **On-Premise**: Use `https://github.com/abaplint/deps`
- **Steampunk/BTP**: Use version-specific APIs like `https://github.com/abapedia/steampunk-2302-api`

```json
{
  "dependencies": [
    {
      "url": "https://github.com/abaplint/deps",
      "folder": "/deps",
      "files": "/src/**/*.*"
    }
  ]
}
```

### Syntax

```json
{
  "syntax": {
    "version": "v758",
    "errorNamespace": "^(Z|Y|LCL_|TY_|LIF_)"
  }
}
```

- `version`: Target ABAP version (`v702`, `v740sp02`, `v740sp05`, `v740sp08`, `v750`, `v751`, `v752`, `v753`, `v754`, `v755`, `v756`, `v757`, `v758`, `Cloud`)
- `errorNamespace`: Regex for object names that should be fully checked (others get relaxed checking)

### Rules

Full rule reference: https://rules.abaplint.org/

## Starter Configurations

### On-Premise (Syntax Check Only)

Minimal config focusing on syntax correctness. Start here and expand gradually.

```json
{
  "global": {
    "files": "/src/**/*.*",
    "skipGeneratedFunctionGroups": true
  },
  "dependencies": [
    {
      "url": "https://github.com/abaplint/deps",
      "folder": "/deps",
      "files": "/src/**/*.*"
    }
  ],
  "syntax": {
    "version": "v758",
    "errorNamespace": "^(Z|Y|LCL_|TY_|LIF_)"
  },
  "rules": {
    "begin_end_names": true,
    "cds_parser_error": true,
    "check_ddic": true,
    "check_include": true,
    "check_syntax": true,
    "identical_form_names": true,
    "global_class": true,
    "implement_methods": true,
    "method_implemented_twice": true,
    "parser_error": true,
    "superclass_final": true,
    "unknown_types": true,
    "xml_consistency": true
  }
}
```

### Steampunk / BTP (2302)

For SAP BTP ABAP Environment or Steampunk development:

```json
{
  "global": {
    "files": "/src/**/*.*"
  },
  "dependencies": [
    {
      "url": "https://github.com/abapedia/steampunk-2302-api",
      "folder": "/deps",
      "files": "/src/**/*.*"
    }
  ],
  "syntax": {
    "version": "Cloud",
    "errorNamespace": "."
  },
  "rules": {
    "begin_end_names": true,
    "cds_parser_error": true,
    "check_ddic": true,
    "strict_sql": true,
    "sql_escape_host_variables": true,
    "check_include": true,
    "check_syntax": true,
    "cloud_types": true,
    "sy_modification": true,
    "global_class": true,
    "implement_methods": true,
    "method_implemented_twice": true,
    "parser_error": true,
    "superclass_final": true,
    "unknown_types": true,
    "xml_consistency": true
  }
}
```

### HANA Database Compatibility

For checking HANA-specific SQL compliance:

```json
{
  "global": {
    "files": "/src/**/*.*"
  },
  "dependencies": [
    {
      "url": "https://github.com/abaplint/deps",
      "folder": "/deps",
      "files": "/src/**/*.*"
    }
  ],
  "syntax": {
    "version": "v755",
    "errorNamespace": "^(Z|Y|LCL_|TY_|LIF_)"
  },
  "rules": {
    "select_single_full_key": true,
    "select_add_order_by": true,
    "forbidden_void_type": {
      "check": [
        "CL_SQL_STATEMENT",
        "CL_SQL_PREPARED_STATEMENT",
        "CL_SQL_CONNECTION",
        "CX_SQL_EXCEPTION"
      ]
    },
    "dangerous_statement": {
      "execSQL": true
    }
  }
}
```

## IDE Integration

Install the [abaplint VS Code extension](https://marketplace.visualstudio.com/items?itemName=larshp.vscode-abaplint) for real-time linting. The extension uses the same `abaplint.json` configuration and provides IntelliSense for the config file.
