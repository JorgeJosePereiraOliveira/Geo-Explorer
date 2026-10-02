# 🌍 Geo-Explorer

Plataforma de exploração de trilhas de aprendizagem com desafios de código e certificados fictícios.

## Visão Geral

O Geo-Explorer oferece três comandos principais:

| Comando      | Descrição |
|--------------|-----------|
| `trilha`     | Apresenta um plano de estudos completo para a tecnologia escolhida |
| `desafio`    | Gera um desafio de código conforme a tecnologia e nível informado |
| `certificado`| Cria um certificado fictício para uma trilha concluída |

Além da CLI, o projeto expõe um **Servidor MCP** que permite que ferramentas externas (como o IBM Bob) acessem os recursos diretamente via protocolo MCP.

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

# Instale as dependências
pip install -e ".[dev]"
```

---

## Uso da CLI

```bash
# Listar tecnologias disponíveis
geo listar

# Ver trilha de aprendizagem
geo trilha python
geo trilha javascript
geo trilha docker

# Gerar desafio de código
geo desafio python iniciante
geo desafio javascript intermediario
geo desafio typescript iniciante

# Gerar certificado fictício
geo certificado "Seu Nome" python
geo certificado "Seu Nome" docker --data 2024-12-01
```

### Tecnologias disponíveis

| ID           | Nome                       | Nível          |
|--------------|----------------------------|----------------|
| `python`     | Python para Iniciantes     | Iniciante      |
| `javascript` | JavaScript Moderno         | Intermediário  |
| `typescript` | TypeScript Essencial       | Intermediário  |
| `sql`        | SQL e Bancos de Dados      | Iniciante      |
| `docker`     | Docker e Contêineres       | Intermediário  |

---

## Servidor MCP

O Geo-Explorer expõe suas funcionalidades via **Model Context Protocol (MCP)**, permitindo integração com clientes compatíveis como o IBM Bob.

### Ferramentas disponíveis

| Ferramenta       | Parâmetros                              | Descrição |
|------------------|-----------------------------------------|-----------|
| `listar_trilhas` | —                                       | Lista todas as trilhas disponíveis |
| `trilha`         | `tecnologia`                            | Retorna o plano de estudos completo |
| `desafio`        | `tecnologia`, `nivel`                   | Retorna um desafio de código |
| `certificado`    | `nome`, `tecnologia`, `data_conclusao?` | Gera um certificado fictício |

### Executar o servidor

```bash
python -m src.mcp.server
```

### Integrar com IBM Bob (mcp.json)

```json
{
  "mcpServers": {
    "geo-explorer": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/caminho/para/Geo-Explorer"
    }
  }
}
```

---

## Testes

```bash
# Rodar todos os testes com cobertura
pytest

# Rodar um único arquivo de teste
pytest tests/test_data_loader.py -v

# Rodar um teste específico
pytest tests/test_data_loader.py::TestBuscarTrilha::test_encontra_trilha_existente -v
```

---

## Estrutura do Projeto

```
Geo-Explorer/
├── src/
│   ├── cli.py              # Ponto de entrada da CLI (click)
│   ├── data_loader.py      # Carregamento e busca nos dados JSON
│   ├── commands/
│   │   ├── trilha.py       # Comando trilha
│   │   ├── desafio.py      # Comando desafio
│   │   └── certificado.py  # Comando certificado
│   └── mcp/
│       └── server.py       # Servidor MCP (stdio)
├── data/
│   ├── trilhas.json        # Base de trilhas fictícias
│   └── desafios.json       # Base de desafios de código
├── docs/
│   └── arquitetura.md      # Documentação de arquitetura
├── tests/
│   ├── test_data_loader.py
│   └── commands/
│       └── test_commands.py
├── AGENTS.md               # Guia para agentes de IA
├── pyproject.toml          # Configuração do projeto e dependências
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

## Licença

MIT © Jorge Jose Pereira Oliveira
