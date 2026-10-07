"""Testes para o módulo data_loader."""
from __future__ import annotations

import pytest

from src.data_loader import (
    buscar_desafio,
    buscar_trilha,
    carregar_desafios,
    carregar_trilhas,
    listar_tecnologias,
)


class TestCarregarTrilhas:
    def test_retorna_lista_nao_vazia(self):
        trilhas = carregar_trilhas()
        assert len(trilhas) > 0

    def test_possui_pelo_menos_30_trilhas(self):
        assert len(carregar_trilhas()) >= 30

    def test_cada_trilha_tem_campos_obrigatorios(self):
        campos = {"id", "nome", "descricao", "nivel", "carga_horaria", "modulos"}
        for trilha in carregar_trilhas():
            assert campos.issubset(trilha.keys()), f"Campos faltando em: {trilha['id']}"

    def test_cada_trilha_tem_campos_novos(self):
        """Valida os campos estendidos adicionados na expansão DIO."""
        campos_novos = {"tecnologia", "xp_total", "badges", "promocao", "vitalicio", "lives"}
        for trilha in carregar_trilhas():
            assert campos_novos.issubset(trilha.keys()), f"Campos novos faltando em: {trilha['id']}"

    def test_xp_total_e_inteiro_positivo(self):
        for trilha in carregar_trilhas():
            assert isinstance(trilha["xp_total"], int) and trilha["xp_total"] > 0

    def test_badges_tem_pelo_menos_um_item(self):
        for trilha in carregar_trilhas():
            assert isinstance(trilha["badges"], list) and len(trilha["badges"]) >= 1

    def test_promocao_e_bool(self):
        for trilha in carregar_trilhas():
            assert isinstance(trilha["promocao"], bool)

    def test_vitalicio_e_bool(self):
        for trilha in carregar_trilhas():
            assert isinstance(trilha["vitalicio"], bool)

    def test_lives_e_inteiro_nao_negativo(self):
        for trilha in carregar_trilhas():
            assert isinstance(trilha["lives"], int) and trilha["lives"] >= 0

    def test_cada_modulo_tem_campos_obrigatorios(self):
        for trilha in carregar_trilhas():
            for modulo in trilha["modulos"]:
                assert {"ordem", "titulo", "topicos"}.issubset(modulo.keys())

    def test_trilhas_java_existem(self):
        ids = {t["id"] for t in carregar_trilhas()}
        assert "java_basico" in ids
        assert "java_intermediario" in ids
        assert "java_avancado" in ids


class TestCarregarDesafios:
    def test_retorna_lista_nao_vazia(self):
        desafios = carregar_desafios()
        assert len(desafios) > 0

    def test_cada_desafio_tem_campos_obrigatorios(self):
        campos = {"tecnologia", "nivel", "titulo", "descricao", "exemplo_entrada", "exemplo_saida"}
        for desafio in carregar_desafios():
            assert campos.issubset(desafio.keys())


class TestBuscarTrilha:
    def test_encontra_trilha_existente(self):
        trilha = buscar_trilha("python")
        assert trilha is not None
        assert trilha["id"] == "python"

    def test_case_insensitive(self):
        assert buscar_trilha("PYTHON") is not None
        assert buscar_trilha("Python") is not None

    def test_retorna_none_para_inexistente(self):
        assert buscar_trilha("cobol") is None

    def test_trilha_python_tem_5_modulos(self):
        trilha = buscar_trilha("python")
        assert trilha is not None
        assert len(trilha["modulos"]) == 5


class TestBuscarDesafio:
    def test_encontra_desafio_existente(self):
        desafio = buscar_desafio("python", "iniciante")
        assert desafio is not None
        assert desafio["tecnologia"] == "python"
        assert desafio["nivel"] == "iniciante"

    def test_case_insensitive(self):
        assert buscar_desafio("PYTHON", "INICIANTE") is not None

    def test_retorna_none_para_combinacao_inexistente(self):
        assert buscar_desafio("python", "ninja") is None

    def test_retorna_none_para_tecnologia_inexistente(self):
        assert buscar_desafio("cobol", "iniciante") is None


class TestListarTecnologias:
    def test_retorna_lista(self):
        techs = listar_tecnologias()
        assert isinstance(techs, list)
        assert len(techs) > 0

    def test_python_esta_na_lista(self):
        assert "python" in listar_tecnologias()
