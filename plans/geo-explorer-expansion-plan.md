# Geo-Explorer — Plano de Expansão da Base de Dados e Funcionalidades

## Visão Geral

Expandir o projeto Geo-Explorer em quatro frentes principais:

1. **Base de dados** — substituir as 5 trilhas fictícias por ≥ 30 trilhas DIO com campos estendidos (xp, badges, promoções, vitalício, lives) mantendo retrocompatibilidade.
2. **Slash commands Bob** — criar `/trilha`, `/desafio` e `/certificado` como comandos locais visíveis no chat do IBM Bob.
3. **Testes unitários** — ampliar suite para ≥ 70% de cobertura, exercitar Java, gerar artefatos de desafio/certificado e gravar resultados em `.txt`.
4. **Servidor MCP** — manter/evoluir `src/mcp/server.py` para suportar acesso futuro via HTTPS / SSO / API, documentando o caminho de migração.

**Restrições obrigatórias:**
- Pasta `plans/` criada na raiz (este arquivo está aqui).
- Máximo de 3 arquivos de plano na pasta `plans/`.
- `.bobignore` criado na raiz ignorando: `node_modules/`, `.env`, `data/cache-progresso/`, `docs/certificados-emitidos/`, `*.tmp`.
- Retrocompatibilidade: campos antigos (`id`, `nome`, `descricao`, `nivel`, `carga_horaria`, `modulos`) mantidos em todas as trilhas; novos campos são adicionais.

---

## Sub-Tarefa 1 — Criar `.bobignore` e pasta `plans/`

**Intent:** Preparar a estrutura de controle de contexto e planejamento antes de qualquer mudança de código.

**Expected Outcomes:**
- Arquivo `.bobignore` na raiz filtrando caches, variáveis de ambiente e artefatos temporários.
- Pasta `plans/` já existe (este arquivo está nela).

**Todo List:**
1. Criar `.bobignore` na raiz com as entradas: `node_modules/`, `.env`, `data/cache-progresso/`, `docs/certificados-emitidos/`, `*.tmp`.
2. Confirmar que `plans/` existe (já criada por este arquivo de plano).

**Relevant Context:**
- Nenhum arquivo de código é alterado nesta sub-tarefa.

**Status:** `[ ] pending`

---

## Sub-Tarefa 2 — Expandir `data/trilhas.json` para ≥ 30 trilhas DIO

**Intent:** Substituir as 5 trilhas fictícias por uma base rica e realista simulando o catálogo da DIO, com campos estendidos que habilitam filtragem avançada e exibição mais rica na CLI e no MCP.

**Expected Outcomes:**
- `data/trilhas.json` com ≥ 30 trilhas.
- Cada trilha contém os campos originais + novos: `tecnologia`, `xp_total`, `badges`, `promocao`, `vitalicio`, `lives`.
- As 5 trilhas originais permanecem (com `id` igual) e recebem os novos campos.
- Todos os testes existentes continuam passando (retrocompatibilidade).

**Novos campos por trilha:**

| Campo | Tipo | Descrição |
|---|---|---|
| `tecnologia` | `string` | Família tecnológica (ex: "Java", "Cloud", "Frontend") |
| `xp_total` | `int` | XP total acumulável ao concluir a trilha |
| `badges` | `list[str]` | Nomes dos badges disponíveis na trilha |
| `promocao` | `bool` | Indica se a trilha está em promoção |
| `vitalicio` | `bool` | Indica se o acesso é vitalício |
| `lives` | `int` | Número de lives ao vivo disponíveis |

**Trilhas a incluir (exemplos representativos):**

Tecnologias: Java (básico, intermediário, avançado), Spring Boot, Python, JavaScript, TypeScript, React, Angular, Vue.js, Node.js, SQL, MongoDB, Docker, Kubernetes, AWS, Azure, GCP, Git/GitHub, Linux, C#, .NET, Golang, Rust, Flutter, Kotlin, Machine Learning, Data Science, DevOps, Segurança, Cloud Native, Microserviços, IA Generativa, Power Platform.

**Todo List:**
1. Criar as ≥ 30 trilhas seguindo o contrato JSON existente mais os novos campos.
2. Garantir que trilhas de Java (básico, intermediário, avançado) existam com pelo menos 5 módulos cada — necessário para os testes da Sub-Tarefa 4.
3. Sobrescrever `data/trilhas.json` com a nova versão completa.
4. Executar `pytest tests/test_data_loader.py` — todos os testes devem passar.

**Relevant Context:**
- Contrato atual: `data/trilhas.json` → chave raiz `"trilhas"`, campos obrigatórios: `id`, `nome`, `descricao`, `nivel`, `carga_horaria`, `modulos[]`.
- `src/data_loader.py` → `buscar_trilha(tecnologia)` busca por `t["id"]` — não mudar o campo `id`.
- `src/commands/trilha.py` → acessa `trilha['nivel']`, `trilha['carga_horaria']`, `trilha['modulos']` — manter esses campos.
- Testes em `tests/test_data_loader.py` → `test_trilha_python_tem_5_modulos` exige exatamente 5 módulos para Python.

**Status:** `[ ] pending`

---

## Sub-Tarefa 3 — Criar Slash Commands do IBM Bob

**Intent:** Registrar `/trilha`, `/desafio` e `/certificado` como slash commands locais do IBM Bob, visíveis e executáveis no chat, armazenados em `.bob/` para escopo de projeto.

**Expected Outcomes:**
- Arquivo `.bob/slash-commands/trilha.md` — ao digitar `/trilha <tecnologia>`, Bob retorna o plano de estudos formatado com os módulos.
- Arquivo `.bob/slash-commands/desafio.md` — ao digitar `/desafio <tecnologia> <nivel>`, Bob gera um desafio de código.
- Arquivo `.bob/slash-commands/certificado.md` — ao digitar `/certificado <nome> <tecnologia>`, Bob gera certificado fictício em Markdown.
- Os três arquivos seguem o schema de slash commands do Bob (`name`, `description`, `content`).

**Todo List:**
1. Criar pasta `.bob/slash-commands/` (se não existir).
2. Criar `.bob/slash-commands/trilha.md` com prompt que instrui Bob a chamar a ferramenta MCP `trilha` e formatar o resultado em Markdown.
3. Criar `.bob/slash-commands/desafio.md` com prompt que instrui Bob a chamar a ferramenta MCP `desafio` e formatar o resultado em Markdown.
4. Criar `.bob/slash-commands/certificado.md` com prompt que instrui Bob a chamar a ferramenta MCP `certificado` e formatar o resultado como certificado Markdown.

**Relevant Context:**
- Slash commands do Bob ficam em `.bob/slash-commands/` (escopo de projeto = visíveis somente neste workspace).
- O servidor MCP `geo-explorer` já expõe `trilha`, `desafio` e `certificado` como ferramentas — os slash commands devem orquestrar essas chamadas.
- O formato do certificado em Markdown deve incluir: nome do usuário, trilha, nível, carga horária, data e código de verificação.

**Status:** `[ ] pending`

---

## Sub-Tarefa 4 — Expandir Testes Unitários para ≥ 70% de Cobertura

**Intent:** Ampliar a suite de testes para cobrir os novos campos das trilhas, exercitar especificamente Java, gerar artefatos de desafio e certificado e gravar resultados em arquivo `.txt`.

**Expected Outcomes:**
- `tests/test_data_loader.py` atualizado para validar os novos campos (`xp_total`, `badges`, `promocao`, `vitalicio`, `lives`).
- `tests/commands/test_commands.py` atualizado com testes de Java.
- Novo arquivo `tests/test_resultados_java.py` que:
  - Consulta trilha de Java.
  - Gera desafio de Java (qualquer nível disponível).
  - Gera certificado para um usuário fixo na trilha de Java.
  - Grava todos os resultados em `tests/resultados_java.txt`.
- `pytest --cov=src` reporta cobertura ≥ 70%.

**Campos novos a validar nos testes:**
- `xp_total` é inteiro positivo.
- `badges` é lista com pelo menos 1 item.
- `promocao` e `vitalicio` são booleanos.
- `lives` é inteiro ≥ 0.

**Todo List:**
1. Atualizar `tests/test_data_loader.py` — adicionar testes para os novos campos de trilha.
2. Atualizar `tests/commands/test_commands.py` — adicionar testes: `exibir_trilha("java")`, `exibir_desafio("java", "iniciante")`, `gerar_certificado("Maria Lima", "java")`.
3. Criar `tests/test_resultados_java.py` — exercitar trilha, desafio e certificado de Java; ao final, gravar resultados em `tests/resultados_java.txt`.
4. Executar `pytest` e confirmar cobertura ≥ 70%.
5. Incluir `tests/resultados_java.txt` no `.gitignore` (artefato gerado, não deve ser versionado).

**Relevant Context:**
- `pyproject.toml` → `addopts = "--cov=src --cov-report=term-missing"` — cobertura é sempre gerada.
- `data/desafios.json` pode precisar de desafio de Java adicionado para o teste funcionar (verificar se já existe).
- `src/commands/certificado.py` → `gerar_certificado(nome, tecnologia, data_conclusao)` — retrona `dict | None`.

**Status:** `[ ] pending`

---

## Sub-Tarefa 5 — Evoluir o Servidor MCP para Suporte a HTTPS / SSO / API

**Intent:** Manter o servidor stdio atual funcionando e documentar/preparar a estrutura para migração futura a transporte HTTP com autenticação, organizando o código na pasta `src/mcp/`.

**Expected Outcomes:**
- `src/mcp/server.py` atualizado para expor as novas trilhas e campos (sem quebrar contratos existentes).
- Ferramenta MCP `listar_trilhas` passa a retornar também `xp_total`, `badges`, `promocao`, `vitalicio`, `lives`.
- Novo arquivo `src/mcp/http_server.py` (esqueleto comentado) com estrutura FastAPI + autenticação via API Key / OAuth2 / SSO — preparado mas não ativado por padrão.
- `src/mcp/README_MCP.md` documentando: transporte stdio atual, esqueleto HTTP, como registrar no Bob, como expor via HTTPS futuramente.

**Todo List:**
1. Atualizar `src/mcp/server.py` — ferramenta `listar_trilhas` deve incluir novos campos no JSON de resposta.
2. Criar `src/mcp/http_server.py` — esqueleto FastAPI com comentários explicando como habilitar transport HTTP, autenticação via `X-API-Key` e stub de OAuth2/SSO.
3. Criar `src/mcp/README_MCP.md` — documentar os dois modos de transporte e como migrar do stdio para HTTPS.
4. Executar `python -m src.mcp.server` para confirmar que o servidor stdio ainda inicializa sem erros.

**Relevant Context:**
- `AGENTS.md` → "MCP só pode usar `sys.stderr` para logging — qualquer `print()` para stdout corrompe o protocolo JSON-RPC do stdio."
- `AGENTS.md` → "`src/mcp/server.py` duplica lógica de busca" — manter esse padrão por ora (refatoração está fora do escopo).
- `pyproject.toml` → `mcp>=1.0.0` já está nas dependências; adicionar `fastapi` e `uvicorn` como opcionais (`[project.optional-dependencies]` → `http`).

**Status:** `[ ] pending`

---

## Ordem de Execução

```
Sub-Tarefa 1 → Sub-Tarefa 2 → Sub-Tarefa 3 → Sub-Tarefa 4 → Sub-Tarefa 5
```

- **1** deve ser executada primeiro (cria estrutura de controle).
- **2** deve ser executada antes de **4** (testes dependem dos dados de Java).
- **3** pode ser executada em paralelo com **2**, mas é lógico fazer após **2** (slash commands referenciam tecnologias novas).
- **5** deve ser executada após **2** (server precisa dos novos campos).

---

## Arquivos Alterados / Criados

| Arquivo | Operação | Sub-Tarefa |
|---|---|---|
| `.bobignore` | Criar | 1 |
| `data/trilhas.json` | Substituir (≥ 30 trilhas) | 2 |
| `.bob/slash-commands/trilha.md` | Criar | 3 |
| `.bob/slash-commands/desafio.md` | Criar | 3 |
| `.bob/slash-commands/certificado.md` | Criar | 3 |
| `tests/test_data_loader.py` | Atualizar | 4 |
| `tests/commands/test_commands.py` | Atualizar | 4 |
| `tests/test_resultados_java.py` | Criar | 4 |
| `tests/resultados_java.txt` | Gerado em runtime | 4 |
| `src/mcp/server.py` | Atualizar (listar_trilhas) | 5 |
| `src/mcp/http_server.py` | Criar (esqueleto) | 5 |
| `src/mcp/README_MCP.md` | Criar | 5 |
| `.gitignore` | Atualizar (resultados_java.txt) | 4 |
| `pyproject.toml` | Atualizar (deps opcionais http) | 5 |
