# 🌍 Geo-Explorer

Plataforma de exploração de trilhas de aprendizagem inspirada na DIO — com desafios de código, certificados fictícios e integração nativa com IBM Bob via MCP.

## Visão Geral

O Geo-Explorer oferece três frentes de acesso às mesmas funcionalidades:

| Frente | Como usar | Descrição |
|---|---|---|
| **CLI** | `geo <comando>` | Interface de linha de comando para uso direto no terminal |
| **Slash commands** | `/trilha`, `/desafio`, `/certificado` | Comandos no chat do IBM Bob |
| **Servidor MCP** | `python -m src.mcp.server` | Protocolo MCP para integração com clientes compatíveis |

---

## Pré-requisitos

- Python 3.11+
- pip

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/JorgeJosePereiraOliveira/Geo-Explorer.git
cd Geo-Explorer

# Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Instale as dependências (inclui ferramentas de desenvolvimento)
pip install -e ".[dev]"

# Para habilitar o servidor HTTP futuro (opcional)
pip install -e ".[http]"
```

---

## Uso da CLI

```bash
# Listar todas as trilhas disponíveis
geo listar

# Ver trilha de aprendizagem
geo trilha python
geo trilha java_basico
geo trilha react
geo trilha aws

# Gerar desafio de código
geo desafio python iniciante
geo desafio java intermediario
geo desafio javascript avancado

# Gerar certificado fictício (exibido no terminal)
geo certificado "Seu Nome" java_basico
geo certificado "Seu Nome" python --data 2024-12-01
```

---

## Slash Commands no IBM Bob

Os slash commands estão armazenados em `.bob/commands/` e são visíveis apenas neste projeto.

> **Pré-requisito:** o servidor MCP `geo-explorer` deve estar registrado no IBM Bob (veja seção [Servidor MCP](#servidor-mcp)).

### `/trilha <tecnologia>`

Retorna o plano de estudos completo formatado em Markdown.

```
/trilha java_basico
/trilha react
/trilha machine_learning
```

**O que é exibido:** nome, nível, carga horária, XP total, badges, promoção, acesso vitalício, lives ao vivo e todos os módulos com tópicos.

---

### `/desafio <tecnologia> <nivel>`

Gera um desafio de código para a tecnologia e nível escolhidos.

```
/desafio java iniciante
/desafio python avancado
/desafio javascript intermediario
```

**Níveis válidos:** `iniciante` | `intermediario` | `avancado`

**O que é exibido:** título, enunciado completo, exemplo de entrada/saída e dicas de implementação.

---

### `/certificado "<nome completo>" <tecnologia>`

Gera um certificado fictício de conclusão formatado em Markdown.

```
/certificado "Maria Lima" java_basico
/certificado "João Costa" python
/certificado "Ana Souza" react
```

**O que é exibido:** certificado oficial com nome do estudante, trilha, nível, carga horária, XP conquistado, data de conclusão e código de verificação único (SHA-256).

---

## Base de Dados — Trilhas Disponíveis

O projeto conta com **33 trilhas** organizadas por família tecnológica:

### Java
| ID | Nome | Nível | XP |
|---|---|---|---|
| `java_basico` | Java para Iniciantes | Iniciante | 2.200 |
| `java_intermediario` | Java Intermediário | Intermediário | 2.800 |
| `java_avancado` | Java Avançado | Avançado | 3.500 |
| `spring_boot` | Spring Boot | Intermediário | 3.000 |
| `microservicos` | Microsserviços com Java | Avançado | 3.700 |

### Frontend / JavaScript
| ID | Nome | Nível | XP |
|---|---|---|---|
| `javascript` | JavaScript Moderno | Intermediário | 2.500 |
| `typescript` | TypeScript Essencial | Intermediário | 1.800 |
| `react` | React | Intermediário | 2.500 |
| `angular` | Angular | Avançado | 3.200 |
| `vuejs` | Vue.js | Intermediário | 2.300 |
| `nodejs` | Node.js | Intermediário | 2.700 |

### Python / IA / Data
| ID | Nome | Nível | XP |
|---|---|---|---|
| `python` | Python para Iniciantes | Iniciante | 2.000 |
| `machine_learning` | Machine Learning | Intermediário | 3.200 |
| `data_science` | Data Science | Iniciante | 2.500 |
| `ia_generativa` | IA Generativa | Intermediário | 2.300 |

### Cloud & DevOps
| ID | Nome | Nível | XP |
|---|---|---|---|
| `docker` | Docker e Contêineres | Intermediário | 1.500 |
| `kubernetes` | Kubernetes | Avançado | 3.000 |
| `aws` | AWS Cloud | Iniciante | 2.000 |
| `azure` | Azure | Iniciante | 1.800 |
| `gcp` | Google Cloud | Iniciante | 1.800 |
| `devops` | DevOps | Avançado | 3.500 |
| `cloud_native` | Cloud Native | Avançado | 3.200 |

### Outras Tecnologias
| ID | Nome | Nível | XP |
|---|---|---|---|
| `sql` | SQL e Bancos de Dados | Iniciante | 1.500 |
| `mongodb` | MongoDB | Iniciante | 1.500 |
| `csharp_dotnet` | C# e .NET | Intermediário | 2.700 |
| `golang` | Golang | Intermediário | 2.500 |
| `kotlin` | Kotlin | Intermediário | 2.500 |
| `flutter` | Flutter | Intermediário | 2.700 |
| `rust` | Rust | Avançado | 3.500 |
| `git_github` | Git e GitHub | Iniciante | 1.000 |
| `linux` | Linux | Iniciante | 1.500 |
| `seguranca` | Segurança da Informação | Intermediário | 2.200 |
| `power_platform` | Power Platform | Iniciante | 1.700 |

### Campos de cada trilha

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | Identificador único (snake_case) |
| `nome` | string | Nome exibido da trilha |
| `descricao` | string | Descrição resumida |
| `nivel` | string | `iniciante` / `intermediario` / `avancado` |
| `carga_horaria` | int | Horas de dedicação estimadas |
| `tecnologia` | string | Família tecnológica (ex: "Java", "Python") |
| `xp_total` | int | XP acumulável ao concluir a trilha |
| `badges` | list | Nomes dos badges disponíveis |
| `promocao` | bool | Indica se a trilha está em promoção |
| `vitalicio` | bool | Indica se o acesso é vitalício |
| `lives` | int | Quantidade de lives ao vivo disponíveis |
| `modulos` | list | Lista de módulos com `ordem`, `titulo` e `topicos[]` |

---

## Desafios Disponíveis

| Tecnologia | Iniciante | Intermediário | Avançado |
|---|---|---|---|
| Python | Calculadora de IMC | Analisador de Texto | Decorador de Cache |
| Java | Calculadora de Média | Sistema de Banco (OOP) | Pool de Threads |
| JavaScript | FizzBuzz Funcional | Debounce | — |
| TypeScript | Generic Stack | — | — |
| SQL | Top 3 Vendedores | — | — |
| Docker | Containerize um App | — | — |

---

## Servidor MCP

O Geo-Explorer expõe suas funcionalidades via **Model Context Protocol (MCP)**, permitindo integração com clientes compatíveis como o IBM Bob.

### Ferramentas disponíveis

| Ferramenta | Parâmetros | Descrição |
|---|---|---|
| `listar_trilhas` | — | Lista todas as 33 trilhas com campos completos |
| `trilha` | `tecnologia` | Retorna o plano de estudos completo |
| `desafio` | `tecnologia`, `nivel` | Retorna um desafio de código |
| `certificado` | `nome`, `tecnologia`, `data_conclusao?` | Gera certificado com código SHA-256 |

### Executar o servidor (transporte stdio)

```bash
python -m src.mcp.server
```

### Registrar no IBM Bob

Adicione ao seu `mcp.json` (global `~/.bob/mcp.json` ou por projeto `.bob/mcp.json`):

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

### Servidor HTTP (futuro — esqueleto disponível)

O arquivo `src/mcp/http_server.py` contém o esqueleto FastAPI com:
- Autenticação via **API Key** (`X-API-Key` header)
- Stub de **OAuth2 / SSO via OIDC** (Azure AD, Okta, Google)
- Suporte a **TLS/HTTPS** via certificado

```bash
# Instalar dependências HTTP
pip install -e ".[http]"

# Configurar variáveis de ambiente
GEO_API_KEY=seu-token
GEO_PORT=8443
GEO_TLS_CERT=cert.pem
GEO_TLS_KEY=key.pem

# Executar
python -m src.mcp.http_server
```

Consulte [`src/mcp/README_MCP.md`](src/mcp/README_MCP.md) para o guia completo de migração stdio → HTTPS.

---

## Testes

```bash
# Rodar todos os testes com cobertura (resultado: 81%)
pytest

# Arquivos de teste específicos
pytest tests/test_data_loader.py -v       # Dados e data_loader
pytest tests/commands/test_commands.py -v # Comandos (trilha, desafio, certificado)
pytest tests/test_cli.py -v               # CLI via CliRunner
pytest tests/test_mcp_server.py -v        # Funções privadas do servidor MCP
pytest tests/test_resultados_java.py -v   # Fluxo completo Java + grava .txt

# Teste único
pytest tests/commands/test_commands.py::TestComandoCertificado::test_codigo_e_deterministico -v
```

### Resultados em arquivo

O teste `tests/test_resultados_java.py` grava automaticamente em `tests/resultados_java.txt` o resultado completo do fluxo Java: trilha + desafios (3 níveis) + certificado.

### Cobertura

| Módulo | Cobertura |
|---|---|
| `src/data_loader.py` | 100% |
| `src/commands/trilha.py` | 100% |
| `src/commands/desafio.py` | 100% |
| `src/commands/certificado.py` | 100% |
| `src/cli.py` | 97% |
| `src/mcp/server.py` | 46% |
| **Total** | **81%** |

---

## Estrutura do Projeto

```
Geo-Explorer/
├── .bob/
│   ├── commands/
│   │   ├── trilha.md           # Slash command /trilha
│   │   ├── desafio.md          # Slash command /desafio
│   │   └── certificado.md      # Slash command /certificado
│   ├── rules/
│   │   └── basic_rules.md
│   ├── rules-agent/
│   │   └── AGENTS.md
│   └── skills/
│       └── changelog-entry/
│           └── SKILL.md
├── data/
│   ├── trilhas.json            # 33 trilhas fictícias DIO (campos estendidos)
│   └── desafios.json           # 11 desafios de código
├── docs/
│   └── arquitetura.md          # Diagramas de componentes e decisões de design
├── plans/
│   └── geo-explorer-expansion-plan.md  # Plano de expansão v0.2.0
├── src/
│   ├── cli.py                  # Ponto de entrada da CLI (click)
│   ├── data_loader.py          # Camada de acesso aos dados JSON
│   ├── commands/
│   │   ├── trilha.py           # Comando trilha
│   │   ├── desafio.py          # Comando desafio
│   │   └── certificado.py      # Comando certificado
│   └── mcp/
│       ├── server.py           # Servidor MCP stdio (API v2)
│       ├── http_server.py      # Esqueleto HTTP/HTTPS (FastAPI)
│       └── README_MCP.md       # Guia do servidor MCP
├── tests/
│   ├── test_data_loader.py     # Testes de dados e busca
│   ├── test_cli.py             # Testes da CLI via CliRunner
│   ├── test_mcp_server.py      # Testes das funções privadas do MCP
│   ├── test_resultados_java.py # Fluxo Java + grava resultados_java.txt
│   └── commands/
│       └── test_commands.py    # Testes dos comandos de negócio
├── .bobignore                  # Ignora node_modules, .env, caches, *.tmp
├── AGENTS.md                   # Guia para agentes de IA
├── CHANGELOG.md                # Histórico de mudanças
├── pyproject.toml              # Configuração do projeto e dependências
└── README.md
```

---

## Desenvolvimento

```bash
# Verificar estilo de código
ruff check src/ tests/

# Formatação automática
ruff format src/ tests/

# Verificação de tipos
mypy src/
```

---

## Dicas de Uso

### Navegar pelas trilhas disponíveis
```bash
geo listar                    # Lista todos os IDs
geo trilha git_github         # Ideal para iniciantes absolutos
geo trilha ia_generativa      # Tendência do mercado
```

### Escolher pelo nível
- **Iniciante:** `python`, `sql`, `aws`, `git_github`, `linux`, `mongodb`, `data_science`
- **Intermediário:** `javascript`, `typescript`, `react`, `nodejs`, `java_intermediario`, `golang`
- **Avançado:** `java_avancado`, `microservicos`, `kubernetes`, `devops`, `rust`, `angular`

### Gerar plano de carreira completo
```bash
# Trilha de backend Java completa
geo trilha java_basico
geo trilha java_intermediario
geo trilha java_avancado
geo trilha spring_boot
geo trilha microservicos

# Trilha fullstack JavaScript
geo trilha javascript
geo trilha nodejs
geo trilha react
```

### Praticar com desafios progressivos
```bash
# Começar com Python
geo desafio python iniciante
geo desafio python intermediario
geo desafio python avancado

# Progredir para Java
geo desafio java iniciante
geo desafio java intermediario
geo desafio java avancado
```

### Emitir certificados em lote
```bash
geo certificado "Maria Lima" java_basico
geo certificado "Maria Lima" java_intermediario
geo certificado "Maria Lima" spring_boot
```

---

## Roadmap

### 🔴 Próximo — Certificado Visual (HTML)

Gerar arquivo `.html` do certificado usando `jinja2` (já instalado):
- Flag `--formato html` no comando `geo certificado`
- Template em `src/templates/certificado.html.j2`
- Saída em `docs/certificados-emitidos/`

### 🟡 Seguinte

- Desafios para as novas tecnologias (React, Docker avançado, Kubernetes)
- Exportação para PDF (`weasyprint`)
- Ativar servidor HTTP/HTTPS (`src/mcp/http_server.py`)
- Refatorar lógica duplicada entre `src/data_loader.py` e `src/mcp/server.py`

### 🟢 Futuro

- Comando `geo ranking` — placar de desafios resolvidos
- Modo interativo (`geo play`)
- Integração SSO/OAuth2 no servidor HTTP
- Suporte a `geo trilha --filtro tecnologia=Java nivel=avancado`

---

## Dívidas Técnicas Conhecidas

| # | Descrição | Localização |
|---|---|---|
| 1 | `src/mcp/server.py` duplica lógica de busca de `src/data_loader.py` | `src/mcp/server.py` |
| 2 | `jinja2` instalado mas ainda não utilizado | `pyproject.toml` |
| 3 | Desafios apenas para Python, Java, JavaScript, TypeScript, SQL e Docker | `data/desafios.json` |
| 4 | Servidor HTTP (`http_server.py`) é esqueleto — não ativado em produção | `src/mcp/http_server.py` |
| 5 | `src/mcp/server.py` tem 46% de cobertura — handlers assíncronos não testados | `tests/test_mcp_server.py` |

---

## Licença

MIT © Jorge Jose Pereira Oliveira

> Geo-Explorer — v0.2.0 | 33 trilhas · 11 desafios · 79 testes · 81% de cobertura
