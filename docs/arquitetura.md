# Arquitetura do Geo-Explorer

## Visão Geral

O Geo-Explorer é uma ferramenta CLI e servidor MCP construída em Python, organizada em camadas bem definidas.

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                     Pontos de Entrada                    │
│                                                          │
│   CLI (geo ...)              MCP (stdio)                 │
│   src/cli.py                 src/mcp/server.py           │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                     Camada de Comandos                    │
│                                                          │
│   commands/trilha.py    commands/desafio.py              │
│   commands/certificado.py                                │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                    Camada de Dados                        │
│                                                          │
│   src/data_loader.py                                     │
│   (carregar, buscar, listar)                             │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                   Dados (JSON estático)                   │
│                                                          │
│   data/trilhas.json         data/desafios.json           │
└─────────────────────────────────────────────────────────┘
```

## Fluxo de um Comando CLI

```
Usuário
  │
  └─► geo trilha python
        │
        ▼
      src/cli.py (click group + command)
        │
        ▼
      src/commands/trilha.py :: exibir_trilha("python")
        │
        ├─► src/data_loader.py :: buscar_trilha("python")
        │     └─► lê data/trilhas.json → filtra por id
        │
        └─► rich.Console → exibe tabela formatada no terminal
```

## Fluxo do Servidor MCP

```
Cliente MCP (Bob / outro)
  │
  └─► JSON-RPC via stdio
        │
        ▼
      src/mcp/server.py
        │
        ├─► list_tools()  → declara ferramentas disponíveis
        │
        └─► call_tool(name, args)
              │
              ├─► "trilha"        → buscar_trilha()
              ├─► "desafio"       → buscar_desafio()
              ├─► "certificado"   → gerar código SHA-256 + montar dict
              └─► "listar_trilhas"→ carregar_trilhas()
```

## Decisões de Design

| Decisão | Motivo |
|---------|--------|
| Dados em JSON estático | Simplicidade — sem banco de dados para um projeto educacional |
| `rich` para saída | Experiência visual rica no terminal sem custo de complexidade |
| Código de verificação via SHA-256 | Determinístico e único por combinação nome+trilha+data |
| MCP via stdio | Padrão mais simples e compatível com Bob e a maioria dos clientes MCP locais |
| `click` para CLI | Geração automática de `--help`, validação de argumentos e subcomandos |

## Adicionando uma Nova Trilha

1. Edite `data/trilhas.json` — adicione um novo objeto no array `trilhas`
2. Edite `data/desafios.json` — adicione desafios para a nova tecnologia
3. Não é necessário alterar código — `data_loader.py` é genérico

## Adicionando um Novo Nível de Desafio

1. Adicione o desafio em `data/desafios.json` com o `nivel` desejado
2. Atualize `_NIVEIS_VALIDOS` em `src/commands/desafio.py`
3. Atualize o `enum` do schema MCP em `src/mcp/server.py`
