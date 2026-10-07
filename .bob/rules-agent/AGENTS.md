# Project Coding Rules (Non-Obvious Only)

- **Nunca importe diretamente de `data/`** — use exclusivamente as funções de `src/data_loader.py`. O `src/mcp/server.py` viola essa regra hoje (tem lógica duplicada); não repita esse padrão.
- **`_gerar_codigo()` existe em dois lugares** — `src/commands/certificado.py` (pública via `_gerar_codigo`) e `src/mcp/server.py` (privada). Ao alterar o algoritmo de hash, atualizar ambos.
- **Novos níveis de desafio** exigem alteração em dois arquivos: `_NIVEIS_VALIDOS` em `src/commands/desafio.py` E o `enum` do `inputSchema` do tool `"desafio"` em `src/mcp/server.py`.
- **`jinja2` está instalado mas não usado** — está reservado para geração de certificados em HTML/PDF. Ao implementar, use-o em `src/commands/certificado.py`.
- **Novos comandos CLI** seguem o padrão: função em `src/commands/<nome>.py` + registro em `src/cli.py` como `@main.command("<nome>")`. Não coloque lógica de negócio em `src/cli.py`.
- **Novos tools MCP** devem ser adicionados ao array `_TOOLS` em `src/mcp/server.py` E tratados dentro de `_handle_call_tool()`. A API v1 com decoradores (`@server.list_tools()`) é incompatível com a versão instalada — use `server.add_request_handler()`.
- **`from __future__ import annotations`** deve ser a primeira linha de qualquer novo módulo Python.
- **`console = Console()`** sempre em nível de módulo, nunca dentro de função.
- **Testes de comando** (`tests/commands/`) testam a função de negócio diretamente (não a CLI click). Para testar a CLI, use `tests/test_cli.py` com `click.testing.CliRunner`.
- **Novos campos de trilha** precisam ser validados nos testes de `tests/test_data_loader.py` na classe `TestCarregarTrilhas`.
- **Slash commands** do projeto ficam em `.bob/commands/` (não `slash-commands/`). O nome do arquivo vira o comando.
- **`src/mcp/http_server.py` não está ativo** — é um esqueleto. Não incluir no cálculo de cobertura (excluído em `[tool.coverage.run]` omit no `pyproject.toml`).
