# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Stack

- **Python 3.11+** — sem Node.js no ambiente
- **CLI:** `click` + `rich` (formatação no terminal)
- **MCP Server:** biblioteca `mcp` via `stdio`
- **Testes:** `pytest` + `pytest-cov`
- **Linting/Tipos:** `ruff`, `mypy`
- **Pacote:** `pyproject.toml` com `setuptools`

## Comandos essenciais

```bash
pip install -e ".[dev]"            # instala dependências incluindo dev
geo trilha python                  # CLI principal
geo desafio python iniciante
geo certificado "Nome" python
python -m src.mcp.server           # inicia servidor MCP (stdio)
pytest                             # todos os testes com cobertura
pytest tests/test_data_loader.py::TestBuscarTrilha::test_encontra_trilha_existente -v  # teste único
ruff check src/ tests/             # lint
mypy src/                          # tipos
```

## Padrões críticos

- **`data_loader.py` é a única fonte de dados** — comandos e servidor MCP nunca leem JSON diretamente; sempre usam `buscar_trilha()`, `buscar_desafio()`, `carregar_trilhas()`, `listar_tecnologias()` de `src/data_loader.py`.
- **Adicionar trilha/desafio = só editar JSON** — `data_loader.py` é genérico; nenhum código precisa mudar ao adicionar conteúdo em `data/trilhas.json` ou `data/desafios.json`.
- **Níveis válidos** estão hardcoded em `src/commands/desafio.py::_NIVEIS_VALIDOS` e no `enum` do schema MCP em `src/mcp/server.py` — ambos devem ser atualizados juntos.
- **Código de verificação** do certificado é SHA-256 dos campos `nome|tecnologia|data` (16 chars, uppercase) — deterministico; mesmos dados sempre geram o mesmo código.
- **MCP usa `console.error` / `sys.stderr`** para logs — nunca `print()` para stdout, pois o canal stdio é reservado ao protocolo JSON-RPC.
- **Servidor MCP** está em `src/mcp/server.py` e é executado com `python -m src.mcp.server` (não há script separado).

## Estrutura de dados

- `data/trilhas.json` — campos obrigatórios: `id`, `nome`, `descricao`, `nivel`, `carga_horaria`, `modulos[]`
- `data/desafios.json` — campos obrigatórios: `tecnologia`, `nivel`, `titulo`, `descricao`, `exemplo_entrada`, `exemplo_saida`; `dicas[]` é opcional

## Integração MCP com IBM Bob

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

## Git

- Remote: `https://github.com/JorgeJosePereiraOliveira/Geo-Explorer.git`
- `credential.helper store` configurado globalmente (credenciais persistidas fora do projeto)
