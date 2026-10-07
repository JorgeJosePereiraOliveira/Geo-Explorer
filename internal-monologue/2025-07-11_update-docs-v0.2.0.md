# 2025-07-11 — Atualização de documentação completa (v0.2.0)

## Contexto
Usuário pediu atualização da documentação com todas as implementações, modificações, prompts, modos de uso, dicas e insights.

## O que foi feito

### README.md
- Introdução reescrita com três frentes de acesso (CLI, Slash Commands, MCP)
- Seção completa de Slash Commands com exemplos de uso para /trilha, /desafio, /certificado
- Tabela completa das 33 trilhas organizada por família tecnológica (Java, Frontend, Python/IA, Cloud, Outras)
- Tabela de campos de trilha (incluindo novos: tecnologia, xp_total, badges, promocao, vitalicio, lives)
- Tabela de desafios disponíveis (11 desafios, 6 tecnologias)
- Seção de Servidor MCP expandida com HTTP futuro e variáveis de ambiente
- Seção de Testes com tabela de cobertura por módulo (81% total)
- Estrutura do projeto atualizada com novos arquivos
- Seção "Dicas de Uso" com trilhas por nível, planos de carreira e desafios progressivos
- Roadmap atualizado e dívidas técnicas revisadas
- Versão bumped para v0.2.0 no rodapé

### CHANGELOG.md
- Nova entrada [0.2.0] — 2025-07-11 com todas as mudanças categorizadas:
  - Base de dados expandida (33 trilhas, 3 desafios Java)
  - Slash commands Bob
  - Testes (51% → 81%)
  - Servidor MCP (API v2, http_server esqueleto, README_MCP)
  - Estrutura e controle (.bobignore, plans/, pyproject.toml)
  - Seção "Alterado" para mudanças em arquivos existentes

### AGENTS.md
- Novo comando pip install -e ".[http]"
- Novo comando para test_resultados_java.py
- Dois novos padrões críticos: API MCP v2, http_server esqueleto não ativo
- Contrato JSON de trilhas expandido com tabela completa de campos (v0.2.0)
- Atenção sobre tecnologia em desafios.json (ID base, não ID de trilha)
- Nova seção "Slash commands (IBM Bob)"
- Nova seção "Testes" com orientações por tipo
- Referência ao README_MCP.md

### docs/arquitetura.md
- Diagrama de componentes atualizado com 4 pontos de entrada (CLI, Slash, MCP stdio, HTTP)
- Fluxo de um Slash Command adicionado
- Fluxo do Servidor MCP atualizado para API v2
- Novo fluxo do Servidor HTTP (esqueleto)
- Decisões de Design com 3 novas entradas (slash commands, API v2, http_server esqueleto)
- Contratos de retorno dos comandos com exemplos reais (java_basico)
- Seção "Adicionando uma Nova Trilha" atualizada com campos novos
- Nova seção "Adicionando um Novo Slash Command"
- Nova seção "Estrutura de Testes" com tabela de cobertura

### .bob/rules-agent/AGENTS.md
- Regra de novos tools MCP atualizada para API v2
- Regra de testes atualizada (test_cli.py com CliRunner)
- 3 novas regras: campos de trilha, slash commands, http_server não ativo

## Arquivos alterados
- README.md
- CHANGELOG.md
- AGENTS.md
- docs/arquitetura.md
- .bob/rules-agent/AGENTS.md
