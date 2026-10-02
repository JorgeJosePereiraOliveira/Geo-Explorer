"""Carregador de dados para trilhas e desafios."""
from __future__ import annotations

import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"


def carregar_trilhas() -> list[dict]:
    """Retorna a lista de todas as trilhas disponíveis."""
    with open(_DATA_DIR / "trilhas.json", encoding="utf-8") as f:
        return json.load(f)["trilhas"]


def carregar_desafios() -> list[dict]:
    """Retorna a lista de todos os desafios disponíveis."""
    with open(_DATA_DIR / "desafios.json", encoding="utf-8") as f:
        return json.load(f)["desafios"]


def buscar_trilha(tecnologia: str) -> dict | None:
    """Busca uma trilha pelo id de tecnologia (case-insensitive)."""
    tecnologia = tecnologia.lower()
    return next((t for t in carregar_trilhas() if t["id"] == tecnologia), None)


def buscar_desafio(tecnologia: str, nivel: str) -> dict | None:
    """Busca um desafio pela tecnologia e nível (case-insensitive)."""
    tecnologia = tecnologia.lower()
    nivel = nivel.lower()
    return next(
        (d for d in carregar_desafios() if d["tecnologia"] == tecnologia and d["nivel"] == nivel),
        None,
    )


def listar_tecnologias() -> list[str]:
    """Retorna os ids de todas as tecnologias disponíveis."""
    return [t["id"] for t in carregar_trilhas()]
