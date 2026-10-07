# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Comandos

```bash
pip install -e ".[dev]"      # instala tudo; necessário antes de qualquer outra coisa
pip install -e ".[http]"     # dependências opcionais do servidor HTTP (fastapi, uvicorn)
pytest                       # sempre roda com --cov=src (configurado em pyproject.toml, não é opcional)
pytest tests/test_resultados_java.py -v  # executa fluxo Java e grava tests/resultados_java.txt
python -m src.mcp.server     # servidor MCP stdio — deve ser executado como módulo, não como script
python -m src.mcp.http_server  # servidor HTTP (requer [http] instalado e variáveis de ambiente)
ruff check src/ tests/
mypy src/
```

## Padrões críticos

- **`data_loader.py` NÃO faz cache** — cada chamada a `buscar_trilha()` / `buscar_desafio()` reabre e relê o JSON do disco. Considere isso ao adicionar funcionalidades com alta frequência de acesso.
- **`src/mcp/server.py` duplica a lógica de busca** em funções privadas (`_buscar_trilha`, `_buscar_desafio`, `_gerar_codigo`) em vez de importar de `src/data_loader.py` e `src/commands/certificado.py`. Ao corrigir bugs nessa lógica, atualizar os dois lugares.
- **`_NIVEIS_VALIDOS`** em [`src/commands/desafio.py`](src/commands/desafio.py) e o `enum` do schema MCP em [`src/mcp/server.py`](src/mcp/server.py) são listas separadas — devem ser atualizadas juntas manualmente.
- **`jinja2`** está em `dependencies` no `pyproject.toml` mas não é usado em nenhum arquivo do projeto ainda (reservado para certificados HTML/PDF).
- **MCP só pode usar `sys.stderr`** para logging — qualquer `print()` para stdout corrompe o protocolo JSON-RPC do stdio.
- **API MCP v2** — `src/mcp/server.py` usa `server.add_request_handler(method, RequestType, handler)`. Não usar a API v1 com decoradores (`@server.list_tools()`, `@server.call_tool()`), que é incompatível com a versão instalada da biblioteca.
- **`src/mcp/http_server.py` NÃO está ativo por padrão** — é um esqueleto documentado. Nunca incluí-lo no cálculo de cobertura (excluído via `[tool.coverage.run]` omit).

## Estilo de código

- `from __future__ import annotations` é a primeira linha de todo módulo Python do projeto (sem exceção).
- `console = Console()` é sempre declarado em nível de módulo nos arquivos de comando — nunca instanciar dentro de funções.
- Ordem de imports: stdlib → rich → `src.*` (sem seção para third-party intermediária).
- Funções públicas de comando retornam o `dict` processado ou `None` — nunca levantam exceções para entradas inválidas; erros vão para `console.print()`.
- Funções e variáveis privadas de módulo usam prefixo `_` (ex: `_NIVEIS_VALIDOS`, `_gerar_codigo`).

## Estrutura de dados (contratos JSON)

### `data/trilhas.json`
Chave raiz: `"trilhas"`. Campos obrigatórios por item:

| Campo | Tipo | Notas |
|---|---|---|
| `id` | string | snake_case; usado como chave de busca — nunca alterar IDs existentes |
| `nome` | string | Nome exibido |
| `descricao` | string | |
| `nivel` | string | `"iniciante"` / `"intermediario"` / `"avancado"` |
| `carga_horaria` | int | horas |
| `tecnologia` | string | Família (ex: `"Java"`, `"Python"`) — adicionado na v0.2.0 |
| `xp_total` | int | positivo — adicionado na v0.2.0 |
| `badges` | list[str] | mínimo 1 item — adicionado na v0.2.0 |
| `promocao` | bool | adicionado na v0.2.0 |
| `vitalicio` | bool | adicionado na v0.2.0 |
| `lives` | int | ≥ 0 — adicionado na v0.2.0 |
| `modulos` | list | cada item: `ordem` (int), `titulo` (str), `topicos` (list[str] ≥ 3 itens) |

Adicionar trilha = adicionar objeto ao array. Nenhum código Python precisa mudar.

### `data/desafios.json`
Chave raiz: `"desafios"`. Campos obrigatórios: `tecnologia`, `nivel`, `titulo`, `descricao`, `exemplo_entrada`, `exemplo_saida`; `dicas[]` é opcional.

**Atenção:** `tecnologia` deve ser o ID base (ex: `"java"`, não `"java_basico"`) — um desafio cobre todos os níveis de uma linguagem.

## Slash commands (IBM Bob)

Slash commands do projeto ficam em `.bob/commands/`. O nome do arquivo (sem `.md`) vira o comando.
- Frontmatter suportado: `description` (texto no menu), `argument-hint` (hint de parâmetros)
- Argumentos são referenciados como `$1`, `$2`, etc. no corpo do arquivo
- Escopo de projeto: visíveis apenas quando o workspace está aberto no IBM Bob
- Os 3 comandos atuais chamam ferramentas MCP do servidor `geo-explorer`

## Testes

- **Novos campos das trilhas** → testar em `tests/test_data_loader.py` (classe `TestCarregarTrilhas`)
- **Novos comandos CLI** → testar via `click.testing.CliRunner` em `tests/test_cli.py`
- **Novas funções do MCP server** → testar em `tests/test_mcp_server.py` (apenas funções privadas síncronas; handlers assíncronos requerem setup especial)
- **Testes de comando** (`tests/commands/`) testam a função de negócio diretamente (não a CLI click) — manter esse padrão

## Integração MCP (IBM Bob)

```json
{
  "mcpServers": {
    "geo-explorer": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/caminho/absoluto/para/Geo-Explorer"
    }
  }
}
```

Para o servidor HTTP futuro, consulte [`src/mcp/README_MCP.md`](src/mcp/README_MCP.md).
