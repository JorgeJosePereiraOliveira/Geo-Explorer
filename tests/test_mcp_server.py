"""Testes para as funções privadas do src/mcp/server.py (sem depender do loop asyncio)."""
from __future__ import annotations

from src.mcp.server import (
    _load_json,
    _trilhas,
    _desafios,
    _buscar_trilha,
    _buscar_desafio,
    _gerar_codigo,
)


class TestMCPLoadJson:
    def test_carrega_trilhas_json(self):
        dados = _load_json("trilhas.json")
        assert "trilhas" in dados
        assert len(dados["trilhas"]) >= 30

    def test_carrega_desafios_json(self):
        dados = _load_json("desafios.json")
        assert "desafios" in dados
        assert len(dados["desafios"]) > 0


class TestMCPTrilhas:
    def test_retorna_lista(self):
        trilhas = _trilhas()
        assert isinstance(trilhas, list)
        assert len(trilhas) >= 30

    def test_cada_trilha_tem_id(self):
        for t in _trilhas():
            assert "id" in t


class TestMCPDesafios:
    def test_retorna_lista(self):
        desafios = _desafios()
        assert isinstance(desafios, list)
        assert len(desafios) > 0


class TestMCPBuscarTrilha:
    def test_encontra_python(self):
        trilha = _buscar_trilha("python")
        assert trilha is not None
        assert trilha["id"] == "python"

    def test_encontra_java_basico(self):
        trilha = _buscar_trilha("java_basico")
        assert trilha is not None

    def test_case_insensitive(self):
        assert _buscar_trilha("PYTHON") is not None

    def test_retorna_none_para_inexistente(self):
        assert _buscar_trilha("cobol") is None


class TestMCPBuscarDesafio:
    def test_encontra_java_iniciante(self):
        desafio = _buscar_desafio("java", "iniciante")
        assert desafio is not None
        assert desafio["tecnologia"] == "java"

    def test_retorna_none_para_inexistente(self):
        assert _buscar_desafio("cobol", "iniciante") is None

    def test_case_insensitive(self):
        assert _buscar_desafio("JAVA", "INICIANTE") is not None


class TestMCPGerarCodigo:
    def test_deterministico(self):
        c1 = _gerar_codigo("Ana", "python", "2024-01-01")
        c2 = _gerar_codigo("Ana", "python", "2024-01-01")
        assert c1 == c2

    def test_16_caracteres(self):
        assert len(_gerar_codigo("Ana", "python", "2024-01-01")) == 16

    def test_maiusculo(self):
        codigo = _gerar_codigo("ana", "python", "2024-01-01")
        assert codigo == codigo.upper()

    def test_varia_com_entrada(self):
        c1 = _gerar_codigo("Ana", "python", "2024-01-01")
        c2 = _gerar_codigo("Ana", "java", "2024-01-01")
        assert c1 != c2
