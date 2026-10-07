# Changelog

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [0.2.0] — 2025-07-11

### Adicionado

#### Base de dados expandida
- `data/trilhas.json` — expandido de 5 para **33 trilhas** fictícias inspiradas no catálogo DIO
- Novos campos em todas as trilhas: `tecnologia`, `xp_total`, `badges[]`, `promocao`, `vitalicio`, `lives`
- Novas trilhas adicionadas: `java_basico`, `java_intermediario`, `java_avancado`, `spring_boot`, `microservicos`, `react`, `angular`, `vuejs`, `nodejs`, `mongodb`, `kubernetes`, `aws`, `azure`, `gcp`, `git_github`, `linux`, `csharp_dotnet`, `golang`, `kotlin`, `flutter`, `machine_learning`, `data_science`, `devops`, `seguranca`, `cloud_native`, `ia_generativa`, `power_platform`, `rust`
- `data/desafios.json` — adicionados 3 desafios de Java: `iniciante` (Calculadora de Média), `intermediario` (Sistema de Banco com OOP), `avancado` (Pool de Threads)

#### Slash commands para IBM Bob
- `.bob/commands/trilha.md` — comando `/trilha <tecnologia>` com frontmatter `description` e `argument-hint`
- `.bob/commands/desafio.md` — comando `/desafio <tecnologia> <nivel>`
- `.bob/commands/certificado.md` — comando `/certificado "<nome>" <tecnologia>` com saída em Markdown
- Todos os comandos são escopados ao projeto (visíveis somente neste workspace no IBM Bob)
- Comandos chamam as ferramentas MCP do servidor `geo-explorer` e formatam o resultado em Markdown

#### Testes
- `tests/test_cli.py` — 11 novos testes da CLI via `click.testing.CliRunner` (cobertura de `src/cli.py`: 0% → 97%)
- `tests/test_mcp_server.py` — 20 novos testes das funções privadas do servidor MCP
- `tests/test_resultados_java.py` — 7 testes do fluxo completo Java com gravação em `tests/resultados_java.txt`
- `tests/test_data_loader.py` — 9 novos testes para campos estendidos (`xp_total`, `badges`, `promocao`, `vitalicio`, `lives`) e trilhas Java
- `tests/commands/test_commands.py` — 7 novos testes para Java (trilha, desafio e certificado nos 3 níveis)
- Total: **79 testes, todos passando** | Cobertura: **51% → 81%**

#### Servidor MCP
- `src/mcp/server.py` — reescrito para API MCP v2 (`add_request_handler`) — compatível com a versão atual da biblioteca `mcp`
- `src/mcp/server.py` — ferramenta `listar_trilhas` passa a retornar campos estendidos (`xp_total`, `badges`, `promocao`, `vitalicio`, `lives`)
- `src/mcp/server.py` — ferramenta `certificado` passa a retornar `xp_total`
- `src/mcp/http_server.py` — esqueleto FastAPI com:
  - Autenticação via API Key (`X-API-Key` header)
  - Stub documentado de OAuth2 / SSO via OIDC (Azure AD, Okta, Google Workspace)
  - Suporte a TLS/HTTPS via certificado
  - Endpoints REST: `GET /health`, `GET /trilhas`, `GET /trilhas/{tecnologia}`, `GET /desafios/{tecnologia}/{nivel}`, `GET /certificados/{tecnologia}`
- `src/mcp/README_MCP.md` — guia completo: transporte stdio, esqueleto HTTP, como registrar no Bob, roadmap de migração

#### Estrutura e controle
- `.bobignore` — criado ignorando `node_modules/`, `.env`, `data/cache-progresso/`, `docs/certificados-emitidos/`, `*.tmp`
- `plans/` — pasta criada com `geo-explorer-expansion-plan.md` (plano detalhado das 5 sub-tarefas)
- `pyproject.toml` — grupo de dependências opcionais `[http]` adicionado: `fastapi>=0.110`, `uvicorn[standard]>=0.29`, `python-jose[cryptography]>=3.3`, `httpx>=0.27`
- `pyproject.toml` — `[tool.coverage.run]` configurado para omitir `src/mcp/http_server.py` do cálculo de cobertura
- `.gitignore` — adicionado `tests/resultados_java.txt` (artefato gerado em runtime)

### Alterado

- `data/trilhas.json` — todas as 5 trilhas originais receberam os novos campos sem alteração dos campos anteriores (retrocompatibilidade total)
- `src/mcp/server.py` — migrado da API MCP v1 (decoradores `@server.list_tools()` / `@server.call_tool()`) para a API v2 (`server.add_request_handler()`), corrigindo incompatibilidade com a versão instalada da biblioteca

### Notas técnicas

- A lógica de busca em `src/mcp/server.py` permanece duplicada em relação a `src/data_loader.py` — divergência conhecida, refatoração planejada para v0.3.0
- `src/mcp/http_server.py` é um esqueleto funcional mas não está ativado por padrão — requer instalação do grupo `[http]` e configuração de variáveis de ambiente
- O teste `tests/test_resultados_java.py` grava `tests/resultados_java.txt` em runtime; o arquivo está no `.gitignore`

---

## [0.1.0] — 2026-10-06

### Adicionado

#### Estrutura do projeto
- Estrutura de pastas `src/`, `data/`, `docs/`, `tests/` com separação clara de responsabilidades
- `pyproject.toml` com dependências, scripts de entrada e configuração de `ruff`, `mypy` e `pytest`
- `.gitignore` configurado para Python (ambientes virtuais, cache, cobertura)
- Git configurado globalmente com `credential.helper store` e remote apontando para o repositório GitHub

#### Base de dados fictícias
- `data/trilhas.json` — 5 trilhas de aprendizagem: Python, JavaScript, TypeScript, SQL e Docker
- `data/desafios.json` — 8 desafios de código com níveis iniciante, intermediário e avançado
- `src/data_loader.py` — camada única de acesso aos dados JSON (busca, listagem, filtragem)

#### CLI (`geo`)
- `geo trilha <tecnologia>` — exibe plano de estudos com módulos e tópicos formatados com `rich`
- `geo desafio <tecnologia> <nivel>` — exibe desafio de código com enunciado, exemplo e dicas
- `geo certificado "<nome>" <tecnologia> [--data YYYY-MM-DD]` — gera certificado fictício com código de verificação SHA-256
- `geo listar` — lista todas as tecnologias disponíveis
- Ponto de entrada registrado como `geo` via `[project.scripts]` no `pyproject.toml`

#### Servidor MCP
- `src/mcp/server.py` — servidor MCP via protocolo `stdio`, compatível com IBM Bob e outros clientes MCP
- 4 ferramentas expostas: `listar_trilhas`, `trilha`, `desafio`, `certificado`
- Schema JSON declarado para cada ferramenta com validação de parâmetros

#### Testes
- 29 testes unitários, todos passando (`pytest`)
- Cobertura de 100% nos módulos `data_loader.py` e todos os comandos
- `tests/test_data_loader.py` — testes de carregamento, busca e listagem de dados
- `tests/commands/test_commands.py` — testes dos três comandos principais

#### Documentação
- `README.md` — visão geral, instalação, uso da CLI, ferramentas MCP, estrutura do projeto
- `docs/arquitetura.md` — diagramas de componentes e fluxos, decisões de design
- `AGENTS.md` — guia para agentes de IA com padrões críticos e não-óbvios do projeto
- `.bob/rules-agent/AGENTS.md` — regras de codificação para o modo Agent do IBM Bob
- `.bob/rules-ask/AGENTS.md` — contexto documental para o modo Ask do IBM Bob
- `.bob/rules-plan/AGENTS.md` — restrições arquiteturais para o modo Plan do IBM Bob

### Notas técnicas

- `src/mcp/server.py` contém lógica de busca duplicada em relação a `src/data_loader.py` — divergência conhecida planejada para refatoração futura
- `jinja2` adicionado às dependências para uso futuro em geração de certificados visuais (HTML/PDF)
- Cobertura de `src/cli.py` e `src/mcp/server.py` é 0% por design — testados indiretamente via funções de negócio

---

[0.2.0]: https://github.com/JorgeJosePereiraOliveira/Geo-Explorer/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/JorgeJosePereiraOliveira/Geo-Explorer/releases/tag/v0.1.0
