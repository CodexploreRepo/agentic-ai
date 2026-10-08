---
title: Model Context Protocol
description: One protocol between agents and the systems they use.
---

# Model Context Protocol

:::note[Outline]
This page is an outline with its sources identified. The prose lands with Module 07. The headings below are what it will contain -- useful already if you are deciding what to study next.
:::

*Covered in **Module 07**.*

## What this page will cover

- The problem MCP solves: N agents times M integrations, each written twice
- Primitives: tools, resources, and prompts -- and which of the three people actually use
- Transports: stdio for local servers, HTTP for remote
- Writing a server: what belongs in one, and what is better as an in-process tool
- Consuming servers from an agent, and the trust boundary that creates
- Security: a third-party MCP server is third-party code with your credentials. Tool poisoning and shadowing
- Where Agent Skills fit alongside it

## Sources

- Model Context Protocol specification
- Anthropic engineering, *Equipping agents for the real world with Agent Skills*
- Koenigstein, *AI Agents* -- ch. 5

---

*See [attribution and originality policy](/references/attribution). All prose here is
original; the sources above are credited for the ideas, not reproduced.*
