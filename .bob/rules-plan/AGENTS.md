# Project Architecture Rules (Non-Obvious Only)

- **`data_loader.py` não faz cache** — cada função reabre o JSON do disco. A arquitetura atual é adequada para dados estáticos, mas qualquer funcionalidade de alta frequência (ex: API web) precisará de caching explícito.
- **`src/mcp/server.py` viola o princípio de camada única de acesso a dados** — duplica busca/hash em vez de reutilizar `src/data_loader.py` e `src/commands/certificado.py`. Refatoração pendente: extrair para um módulo `src/core.py` compartilhado entre CLI e MCP.
- **O servidor MCP é puramente stateless** — nenhum estado é mantido entre chamadas de ferramentas; o design pressupõe que cada `call_tool` é independente.
- **Não há separação entre camada de apresentação e lógica de negócio nos comandos** — `exibir_trilha()`, `exibir_desafio()` e `gerar_certificado()` fazem rendering com `rich` e retornam dados ao mesmo tempo. Ao evoluir, considere separar em `fetch_X()` + `render_X()`.
- **`pytest` roda com `--cov=src` sempre** (em `pyproject.toml`) — não há como rodar testes sem gerar relatório de cobertura, o que aumenta o tempo de execução.
