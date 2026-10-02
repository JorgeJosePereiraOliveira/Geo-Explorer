"""Servidor MCP do Geo-Explorer.

Expõe as funcionalidades de trilhas, desafios e certificados como ferramentas
acessíveis por qualquer cliente compatível com o protocolo MCP (Model Context Protocol).

Transporte: stdio (padrão para uso local com Bob e outros clientes MCP).

Uso:
    python -m src.mcp.server
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

# ── Importação da biblioteca MCP ──────────────────────────────────────────────
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp import types as mcp_types
except ImportError:  # pragma: no cover
    print(  # noqa: T201
        "Biblioteca 'mcp' não instalada. Execute: pip install mcp",
        file=sys.stderr,
    )
    sys.exit(1)

# ── Carregamento dos dados ────────────────────────────────────────────────────
_DATA_DIR = Path(__file__).parent.parent.parent / "data"


def _load_json(filename: str) -> dict:
    with open(_DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def _trilhas() -> list[dict]:
    return _load_json("trilhas.json")["trilhas"]


def _desafios() -> list[dict]:
    return _load_json("desafios.json")["desafios"]


def _buscar_trilha(tecnologia: str) -> dict | None:
    return next((t for t in _trilhas() if t["id"] == tecnologia.lower()), None)


def _buscar_desafio(tecnologia: str, nivel: str) -> dict | None:
    return next(
        (d for d in _desafios() if d["tecnologia"] == tecnologia.lower() and d["nivel"] == nivel.lower()),
        None,
    )


def _gerar_codigo(nome: str, tecnologia: str, data_str: str) -> str:
    raw = f"{nome.lower()}|{tecnologia.lower()}|{data_str}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


# ── Servidor MCP ──────────────────────────────────────────────────────────────
server = Server("geo-explorer")


@server.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """Declara as ferramentas disponíveis para clientes MCP."""
    return [
        mcp_types.Tool(
            name="trilha",
            description=(
                "Retorna o plano de estudos completo de uma trilha de aprendizagem. "
                "Inclui nome, descrição, nível, carga horária e todos os módulos com seus tópicos."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "tecnologia": {
                        "type": "string",
                        "description": "Identificador da tecnologia (ex: python, javascript, typescript, sql, docker).",
                    }
                },
                "required": ["tecnologia"],
            },
        ),
        mcp_types.Tool(
            name="desafio",
            description=(
                "Gera um desafio de código para a tecnologia e nível informados. "
                "Retorna título, descrição, exemplo de entrada/saída e dicas."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "tecnologia": {
                        "type": "string",
                        "description": "Identificador da tecnologia (ex: python, javascript, typescript, sql, docker).",
                    },
                    "nivel": {
                        "type": "string",
                        "enum": ["iniciante", "intermediario", "avancado"],
                        "description": "Nível de dificuldade do desafio.",
                    },
                },
                "required": ["tecnologia", "nivel"],
            },
        ),
        mcp_types.Tool(
            name="certificado",
            description=(
                "Gera um certificado fictício de conclusão de trilha para o estudante informado. "
                "Retorna os dados do certificado incluindo um código único de verificação."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "description": "Nome completo do estudante.",
                    },
                    "tecnologia": {
                        "type": "string",
                        "description": "Identificador da trilha concluída (ex: python, docker).",
                    },
                    "data_conclusao": {
                        "type": "string",
                        "description": "Data de conclusão no formato YYYY-MM-DD. Padrão: data atual.",
                    },
                },
                "required": ["nome", "tecnologia"],
            },
        ),
        mcp_types.Tool(
            name="listar_trilhas",
            description="Lista todas as trilhas de aprendizagem disponíveis no Geo-Explorer.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """Despacha a chamada para a ferramenta correta."""

    if name == "listar_trilhas":
        trilhas = _trilhas()
        resultado = [
            {"id": t["id"], "nome": t["nome"], "nivel": t["nivel"], "carga_horaria": t["carga_horaria"]}
            for t in trilhas
        ]
        return [mcp_types.TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    if name == "trilha":
        tecnologia = arguments.get("tecnologia", "")
        trilha = _buscar_trilha(tecnologia)
        if trilha is None:
            ids = [t["id"] for t in _trilhas()]
            return [mcp_types.TextContent(
                type="text",
                text=f"Trilha '{tecnologia}' não encontrada. Disponíveis: {', '.join(ids)}",
            )]
        return [mcp_types.TextContent(type="text", text=json.dumps(trilha, ensure_ascii=False, indent=2))]

    if name == "desafio":
        tecnologia = arguments.get("tecnologia", "")
        nivel = arguments.get("nivel", "")
        desafio = _buscar_desafio(tecnologia, nivel)
        if desafio is None:
            return [mcp_types.TextContent(
                type="text",
                text=f"Desafio não encontrado para '{tecnologia}' — nível '{nivel}'.",
            )]
        return [mcp_types.TextContent(type="text", text=json.dumps(desafio, ensure_ascii=False, indent=2))]

    if name == "certificado":
        nome = arguments.get("nome", "")
        tecnologia = arguments.get("tecnologia", "")
        data_str = arguments.get("data_conclusao") or date.today().isoformat()

        trilha = _buscar_trilha(tecnologia)
        if trilha is None:
            ids = [t["id"] for t in _trilhas()]
            return [mcp_types.TextContent(
                type="text",
                text=f"Trilha '{tecnologia}' não encontrada. Disponíveis: {', '.join(ids)}",
            )]

        codigo = _gerar_codigo(nome, tecnologia, data_str)
        certificado = {
            "nome": nome,
            "trilha_id": tecnologia,
            "trilha_nome": trilha["nome"],
            "nivel": trilha["nivel"],
            "carga_horaria": trilha["carga_horaria"],
            "data_conclusao": data_str,
            "codigo_verificacao": codigo,
        }
        return [mcp_types.TextContent(type="text", text=json.dumps(certificado, ensure_ascii=False, indent=2))]

    return [mcp_types.TextContent(type="text", text=f"Ferramenta '{name}' não reconhecida.")]


async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Ponto de entrada do servidor MCP."""
    import asyncio
    asyncio.run(_run())


if __name__ == "__main__":
    main()
