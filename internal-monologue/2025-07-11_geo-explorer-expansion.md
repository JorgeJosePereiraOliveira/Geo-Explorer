# 2025-07-11 — Expansão Geo-Explorer: 30+ trilhas DIO, slash commands, testes e MCP HTTP

## Contexto
Usuário solicitou expansão completa do projeto Geo-Explorer em 5 frentes.

## O que foi feito

### Sub-Tarefa 1 — .bobignore e plans/
- Criado `.bobignore` ignorando `node_modules/`, `.env`, `data/cache-progresso/`, `docs/certificados-emitidos/`, `*.tmp`.
- Pasta `plans/` criada com `geo-explorer-expansion-plan.md`.

### Sub-Tarefa 2 — 32 trilhas DIO + desafios Java
- `data/trilhas.json` expandido de 5 para 32 trilhas fictícias com campos novos: `tecnologia`, `xp_total`, `badges`, `promocao`, `vitalicio`, `lives`.
- 5 trilhas originais mantidas com retrocompatibilidade total.
- Trilhas Java em 3 níveis: `java_basico`, `java_intermediario`, `java_avancado`.
- `data/desafios.json` recebeu 3 desafios de Java (iniciante, intermediário, avançado).

### Sub-Tarefa 3 — Slash commands Bob
- Criados em `.bob/commands/` (local ao projeto):
  - `trilha.md` → `/trilha <tecnologia>`
  - `desafio.md` → `/desafio <tecnologia> <nivel>`
  - `certificado.md` → `/certificado "<nome>" <tecnologia>`
- Todos usam frontmatter com `description` e `argument-hint`.
- Chamam as ferramentas MCP do servidor `geo-explorer`.

### Sub-Tarefa 4 — Testes ≥ 70% (resultado: 81%)
- `tests/test_data_loader.py` — 9 testes novos para campos estendidos e trilhas Java.
- `tests/commands/test_commands.py` — 7 testes novos (Java nos 3 níveis + certificado).
- `tests/test_cli.py` — NOVO: 11 testes de CLI via `click.testing.CliRunner` cobrindo `src/cli.py` (0% → 97%).
- `tests/test_mcp_server.py` — NOVO: 20 testes das funções privadas do MCP server.
- `tests/test_resultados_java.py` — NOVO: 7 testes + gravação em `tests/resultados_java.txt`.
- Total: 79 testes, todos passando, cobertura 81%.
- `src/mcp/server.py` reescrito para API MCP v2 (`add_request_handler`).

### Sub-Tarefa 5 — MCP HTTP/SSO
- `src/mcp/server.py` atualizado com API v2 e campos `xp_total` em `listar_trilhas` e `certificado`.
- `src/mcp/http_server.py` NOVO: esqueleto FastAPI com autenticação API Key + stub OAuth2/SSO/OIDC + mTLS documentado.
- `src/mcp/README_MCP.md` NOVO: documentação dos dois transportes e roadmap de migração.
- `pyproject.toml` — dependências opcionais `[http]` adicionadas.

## Arquivos alterados/criados
- `.bobignore` (novo)
- `plans/geo-explorer-expansion-plan.md` (novo)
- `data/trilhas.json` (expansão: 5 → 32 trilhas)
- `data/desafios.json` (+3 desafios Java)
- `.bob/commands/trilha.md`, `desafio.md`, `certificado.md` (novos)
- `tests/test_data_loader.py` (atualizado)
- `tests/commands/test_commands.py` (atualizado)
- `tests/test_cli.py` (novo)
- `tests/test_mcp_server.py` (novo)
- `tests/test_resultados_java.py` (novo)
- `src/mcp/server.py` (reescrito para API v2)
- `src/mcp/http_server.py` (novo — esqueleto)
- `src/mcp/README_MCP.md` (novo)
- `pyproject.toml` (deps opcionais http + omit coverage)
- `.gitignore` (+tests/resultados_java.txt)
