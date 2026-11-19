# Validated surfaces

The [CLI manifest](cli/manifest.json) records the binary version, source commit and capture date. [Command discovery](cli/commands.json) includes required flags, safety metadata and endpoint mappings.

The [native MCP capture](mcp/tools-list.json) records the tools and input schemas returned by the authenticated endpoint on the stated date. The [documentation extract](mcp/documented-surface.json) records transport, authentication and connector rollout. Runtime discovery determines what a particular client can call.

Refresh the CLI from a release build. Supply the full source commit used to build it.

```sh
python3 scripts/refresh_validated_surfaces.py --cli-bin /path/to/af --cli-commit "$CLI_COMMIT"
```

Refresh MCP from a complete JSON-RPC response saved after initialization. The capture file should contain only the tools/list envelope.

```sh
python3 scripts/refresh_validated_surfaces.py --skip-cli --mcp-capture /path/to/tools-list-response.json
```

Each invocation updates only the selected interfaces. Maintain the documentation extract from the official MCP documentation.
