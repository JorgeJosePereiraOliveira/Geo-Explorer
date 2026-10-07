# Arquitetura do Geo-Explorer

## Visão Geral

O Geo-Explorer é uma ferramenta CLI e servidor MCP construída em Python, organizada em camadas bem definidas, com três frentes de acesso: CLI, Slash Commands (IBM Bob) e Servidor MCP.

## Diagrama de Componentes

```
┌────────────────────────────────────────────────────────────────┐
│                        Pontos de Entrada                        │
│                                                                  │
│  CLI (geo ...)    /slash Bob     MCP stdio     HTTP (futuro)    │
│  src/cli.py      .bob/commands/  src/mcp/      src/mcp/         │
│                  *.md            server.py     http_server.py   │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                      Camada de Comandos                          │
│                                                                  │
│  commands/trilha.py    commands/desafio.py                      │
│  commands/certificado.py                                         │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                       Camada de Dados                            │
│                                                                  │
│  src/data_loader.py  (carregar, buscar, listar)                 │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                      Dados (JSON estático)                       │
│                                                                  │
│  data/trilhas.json (33 trilhas)    data/desafios.json (11)      │
└────────────────────────────────────────────────────────────────┘
```

## Fluxo de um Comando CLI

```
Usuário
  │
  └─► geo trilha java_basico
        │
        ▼
      src/cli.py (click group + command)
        │
        ▼
      src/commands/trilha.py :: exibir_trilha("java_basico")
        │
        ├─► src/data_loader.py :: buscar_trilha("java_basico")
        │     └─► lê data/trilhas.json → filtra por id
        │
        └─► rich.Console → exibe painel + tabela formatada
              (inclui xp_total, badges, promocao, vitalicio, lives)
```

## Fluxo de um Slash Command no IBM Bob

```
Usuário digita no chat do Bob:
  /trilha java_basico
        │
        ▼
      .bob/commands/trilha.md  (lido pelo Bob)
        │  → instrui o Bob a chamar a ferramenta MCP "trilha"
        ▼
      Servidor MCP geo-explorer (stdio)
        │  → src/mcp/server.py :: _handle_call_tool()
        ▼
      _buscar_trilha("java_basico")
        │  → lê data/trilhas.json
        ▼
      JSON retornado ao Bob → formatado em Markdown pelo prompt do slash command
```

## Fluxo do Servidor MCP (stdio)

```
Cliente MCP (Bob / outro)
  │
  └─► JSON-RPC via stdio
        │
        ▼
      src/mcp/server.py
        │
        ├─► tools/list  → _handle_list_tools()  → lista _TOOLS
        │
        └─► tools/call  → _handle_call_tool()
              │
              ├─► "listar_trilhas" → _trilhas()
              ├─► "trilha"         → _buscar_trilha()
              ├─► "desafio"        → _buscar_desafio()
              └─► "certificado"    → _buscar_trilha() + _gerar_codigo()
```

## Fluxo do Servidor HTTP (futuro)

```
Cliente HTTP
  │
  └─► HTTPS + X-API-Key (ou JWT OIDC futuramente)
        │
        ▼
      src/mcp/http_server.py (FastAPI + uvicorn)
        │
        ├─► GET /health              → sem autenticação
        ├─► GET /trilhas             → _trilhas()
        ├─► GET /trilhas/{id}        → _buscar_trilha()
        ├─► GET /desafios/{t}/{n}    → _buscar_desafio()
        └─► GET /certificados/{t}   → _buscar_trilha() + _gerar_codigo()
```

## Decisões de Design

| Decisão | Motivo |
|---|---|
| Dados em JSON estático | Simplicidade — sem banco de dados para projeto educacional |
| `rich` para saída CLI | Experiência visual rica no terminal sem custo de complexidade |
| Código de verificação via SHA-256 | Determinístico e único por combinação nome+trilha+data |
| MCP via stdio (padrão) | Mais simples e compatível com Bob e maioria dos clientes MCP locais |
| `click` para CLI | Geração automática de `--help`, validação de argumentos e subcomandos |
| Slash commands em `.bob/commands/` | Escopo de projeto, sem interferir em outros workspaces |
| API MCP v2 (`add_request_handler`) | Compatível com a versão instalada da biblioteca `mcp` |
| `http_server.py` como esqueleto | Prepara infraestrutura HTTP sem ativar dependências desnecessárias |

## Contratos de Retorno dos Comandos

### `exibir_trilha(tecnologia)` → `dict | None`

```python
{
  "id": "java_basico",
  "nome": "Java para Iniciantes",
  "nivel": "iniciante",
  "carga_horaria": 45,
  "tecnologia": "Java",
  "xp_total": 2200,
  "badges": ["Java Starter", "OOP Fundamentals"],
  "promocao": False,
  "vitalicio": True,
  "lives": 2,
  "modulos": [{"ordem": 1, "titulo": "...", "topicos": ["..."]}]
}
```

### `gerar_certificado(nome, tecnologia, data)` → `dict | None`

```python
{
  "nome": "Maria Lima",
  "trilha_id": "java_basico",
  "trilha_nome": "Java para Iniciantes",
  "nivel": "iniciante",
  "carga_horaria": 45,
  "data_conclusao": "2025-01-15",
  "codigo_verificacao": "31A630220AC1772F"  # SHA-256[:16].upper()
}
```

## Adicionando uma Nova Trilha

1. Edite `data/trilhas.json` — adicione um novo objeto no array `trilhas` com todos os campos obrigatórios (incluindo os novos: `tecnologia`, `xp_total`, `badges`, `promocao`, `vitalicio`, `lives`)
2. Opcionalmente, adicione desafios em `data/desafios.json` com `tecnologia` igual ao ID base da linguagem
3. Nenhum código Python precisa mudar — `data_loader.py` e `mcp/server.py` são genéricos

## Adicionando um Novo Nível de Desafio

1. Adicione o desafio em `data/desafios.json` com o `nivel` desejado
2. Atualize `_NIVEIS_VALIDOS` em `src/commands/desafio.py`
3. Atualize o `enum` do schema MCP em `src/mcp/server.py`

## Adicionando um Novo Slash Command

1. Crie um arquivo `.bob/commands/<nome-do-comando>.md`
2. Adicione frontmatter: `description` e `argument-hint`
3. No corpo, instrua o Bob a chamar a ferramenta MCP adequada e formatar o resultado
4. O comando `/nome-do-comando` aparece automaticamente no chat do IBM Bob

## Estrutura de Testes

```
tests/
├── test_data_loader.py      # Valida contratos JSON, campos novos e buscas
├── test_cli.py              # Testa CLI via CliRunner — cobre src/cli.py (97%)
├── test_mcp_server.py       # Testa funções privadas síncronas do MCP server
├── test_resultados_java.py  # Fluxo completo Java → grava tests/resultados_java.txt
└── commands/
    └── test_commands.py     # Testa funções de negócio diretamente (sem CliRunner)
```

| Arquivo de teste | O que cobre | Cobertura gerada |
|---|---|---|
| `test_data_loader.py` | `src/data_loader.py` | 100% |
| `test_commands.py` | `src/commands/*.py` | 100% |
| `test_cli.py` | `src/cli.py` | 97% |
| `test_mcp_server.py` | `src/mcp/server.py` (funções privadas) | parcial |
| `test_resultados_java.py` | fluxo Java ponta-a-ponta | — |
