# Geo-Explorer — Guia do Servidor MCP

## Transporte atual: stdio

O servidor MCP padrão usa transporte `stdio` — o protocolo JSON-RPC é trafegado via stdin/stdout,
tornando-o ideal para uso local com IBM Bob e outros clientes MCP compatíveis.

### Como executar

```bash
python -m src.mcp.server
```

### Como registrar no IBM Bob

Adicione ao seu `mcp.json` (global em `~/.bob/mcp.json` ou por workspace em `.bob/mcp.json`):

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

### Ferramentas disponíveis

| Ferramenta | Parâmetros | Descrição |
|---|---|---|
| `listar_trilhas` | — | Lista todas as trilhas com campos completos |
| `trilha` | `tecnologia` (string) | Retorna o plano de estudos de uma trilha |
| `desafio` | `tecnologia`, `nivel` | Retorna um desafio de código |
| `certificado` | `nome`, `tecnologia`, `data_conclusao?` | Gera certificado fictício |

### Exemplo de uso via slash commands

```
/trilha java_basico
/desafio java iniciante
/certificado "Maria Lima" java_basico
```

---

## Transporte futuro: HTTPS / API Key / SSO

O arquivo `src/mcp/http_server.py` contém o esqueleto FastAPI para exposição via HTTP/HTTPS.
Ele **não está ativado por padrão**.

### Instalação das dependências opcionais

```bash
pip install "geo-explorer[http]"
# ou diretamente:
pip install fastapi uvicorn
```

### Configuração

Crie um arquivo `.env` (nunca commite) com as variáveis:

```bash
GEO_API_KEY=seu-token-secreto-aqui
GEO_HOST=0.0.0.0
GEO_PORT=8443
GEO_TLS_CERT=cert.pem
GEO_TLS_KEY=key.pem
```

### Gerar certificado TLS para desenvolvimento

```bash
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/CN=geo-explorer-dev"
```

Para produção, use [Let's Encrypt](https://letsencrypt.org/) ou um certificado corporativo.

### Executar o servidor HTTP

```bash
python -m src.mcp.http_server
```

Acesse a documentação interativa em: `https://localhost:8443/docs`

### Endpoints disponíveis

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| `GET` | `/health` | Não | Health check |
| `GET` | `/trilhas` | API Key | Lista todas as trilhas |
| `GET` | `/trilhas/{tecnologia}` | API Key | Detalhes de uma trilha |
| `GET` | `/desafios/{tecnologia}/{nivel}` | API Key | Desafio de código |
| `GET` | `/certificados/{tecnologia}?nome=...` | API Key | Gera certificado |

### Autenticação via API Key

Inclua o header `X-API-Key: <token>` em todas as requisições autenticadas:

```bash
curl -H "X-API-Key: seu-token" https://localhost:8443/trilhas
```

### Roadmap de autenticação

**Fase 1 (atual) — API Key:**
O header `X-API-Key` é validado contra a variável de ambiente `GEO_API_KEY`.

**Fase 2 (planejado) — OAuth2 / SSO via OIDC:**
Suporte a provedores como Azure AD, Okta e Google Workspace via JWT.
Stub documentado em `src/mcp/http_server.py` na seção `# STUB: OAuth2 / SSO`.

**Fase 3 (futuro) — mTLS:**
Autenticação mútua via certificados de cliente — indicado para ambientes corporativos.

### Migrar o Bob do stdio para HTTP

Quando o servidor HTTP estiver em produção, atualize o `mcp.json` para usar `url`:

```json
{
  "mcpServers": {
    "geo-explorer": {
      "url": "https://seu-servidor:8443/mcp",
      "headers": {
        "X-API-Key": "${env:GEO_API_KEY}"
      }
    }
  }
}
```

> **Nota:** O endpoint `/mcp` no servidor HTTP ainda precisa ser implementado seguindo o
> protocolo MCP Streamable HTTP (substituindo o stdio). O esqueleto atual expõe a API REST
> diretamente — a integração MCP via HTTP é a próxima etapa do roadmap.

---

## Arquitetura de referência

```
┌─────────────────────────────────────────────────────────┐
│                    Clientes                             │
│  IBM Bob (stdio) │ curl/SDK (HTTPS) │ Browser (REST)   │
└────────┬─────────┴────────┬─────────┴────────┬──────────┘
         │                  │                   │
         ▼                  ▼                   ▼
┌────────────────┐  ┌───────────────┐  ┌──────────────────┐
│ src/mcp/       │  │ src/mcp/      │  │ /docs (Swagger)  │
│ server.py      │  │ http_server.py│  │ auto-gerado      │
│ (stdio/JSON-   │  │ (FastAPI +    │  └──────────────────┘
│  RPC)          │  │  uvicorn TLS) │
└────────┬───────┘  └───────┬───────┘
         └────────┬──────────┘
                  ▼
         ┌────────────────┐
         │ data_loader.py │
         │ commands/      │
         └───────┬────────┘
                 ▼
         ┌────────────────┐
         │ data/          │
         │ trilhas.json   │
         │ desafios.json  │
         └────────────────┘
```
