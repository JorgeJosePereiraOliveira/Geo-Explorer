# Project Documentation Rules (Non-Obvious Only)

- **`docs/arquitetura.md`** é a referência canônica de fluxos e decisões de design — consulte antes de responder perguntas sobre "por que X foi feito assim".
- **`src/mcp/server.py` não usa `src/data_loader.py`** apesar de ser o padrão do resto do projeto — tem lógica de busca interna duplicada. Isso é uma divergência técnica conhecida, não um padrão intencional.
- **`jinja2` aparece nas dependências** mas não existe nenhum template `.html` ou `.j2` no projeto — a biblioteca foi adicionada para uso futuro em certificados visuais.
- **A CLI é exposta como `geo`** (não `geo-explorer`, não `python -m src.cli`) — definido em `[project.scripts]` no `pyproject.toml`.
- **Cobertura de testes:** `src/cli.py` e `src/mcp/server.py` têm 0% de cobertura (excluídos por design — a CLI testa as funções de negócio direto, o servidor MCP requer cliente assíncrono).
