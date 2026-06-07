<!-- mcp-name: io.github.CSOAI-ORG/thermal-management-mcp -->
# thermal-management-mcp

[![MCP Scorecard: 26/100](https://img.shields.io/badge/proofof.ai-26%2F100-5b21b6)](https://proofof.ai/scorecard/thermal-management-mcp.html)

**Passive thermal-management physics** — photothermal Marangoni-flow simulation and capillary-cooling heat-load limits for passive (pumpless) actuator and electronics cooling. An MCP server by MEOK AI Labs.

## Tools

| Tool | Description |
|---|---|
| `simulate_marangoni_flow` | Photothermal Marangoni surface-tension flow velocity for passive actuator cooling. |
| `calculate_capillary_limit` | Maximum heat load for a passive capillary cooling layer. |

## Install

```bash
pip install thermal-management-mcp
```

Then run the stdio MCP server:

```bash
python server.py
```

## Scorecard

This server is scored on the [proofof.ai MCP Scorecard](https://proofof.ai/scorecard/thermal-management-mcp.html) (100-point production-readiness rubric). Current: **26/100** — working physics tools, but below the 80 merge gate; a third tool, packaging, CI, and distribution hardening pending.

## License

MIT © MEOK AI Labs
