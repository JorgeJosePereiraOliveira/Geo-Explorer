"""Testes para os comandos trilha, desafio e certificado."""
from __future__ import annotations

import pytest
from rich.console import Console

from src.commands.trilha import exibir_trilha
from src.commands.desafio import exibir_desafio
from src.commands.certificado import gerar_certificado, _gerar_codigo


class TestComandoTrilha:
    def test_retorna_trilha_valida(self, capsys):
        resultado = exibir_trilha("python")
        assert resultado is not None
        assert resultado["id"] == "python"

    def test_retorna_none_para_tecnologia_invalida(self, capsys):
        resultado = exibir_trilha("cobol")
        assert resultado is None

    def test_exibe_todos_os_tecnologias(self, capsys):
        for tech in ["python", "javascript", "typescript", "sql", "docker"]:
            resultado = exibir_trilha(tech)
            assert resultado is not None, f"Trilha '{tech}' deveria existir"

    def test_trilha_java_basico(self):
        resultado = exibir_trilha("java_basico")
        assert resultado is not None
        assert resultado["id"] == "java_basico"

    def test_trilha_java_intermediario(self):
        resultado = exibir_trilha("java_intermediario")
        assert resultado is not None

    def test_trilha_java_avancado(self):
        resultado = exibir_trilha("java_avancado")
        assert resultado is not None

    def test_trilha_retorna_campos_novos(self):
        resultado = exibir_trilha("java_basico")
        assert resultado is not None
        assert "xp_total" in resultado
        assert "badges" in resultado
        assert "promocao" in resultado
        assert "vitalicio" in resultado
        assert "lives" in resultado


class TestComandoDesafio:
    def test_retorna_desafio_valido(self):
        resultado = exibir_desafio("python", "iniciante")
        assert resultado is not None
        assert resultado["tecnologia"] == "python"
        assert resultado["nivel"] == "iniciante"

    def test_retorna_none_para_nivel_invalido(self):
        resultado = exibir_desafio("python", "ninja")
        assert resultado is None

    def test_retorna_none_para_tecnologia_invalida(self):
        resultado = exibir_desafio("cobol", "iniciante")
        assert resultado is None

    def test_desafio_python_avancado_existe(self):
        resultado = exibir_desafio("python", "avancado")
        assert resultado is not None

    def test_desafio_java_iniciante(self):
        resultado = exibir_desafio("java", "iniciante")
        assert resultado is not None
        assert resultado["tecnologia"] == "java"
        assert resultado["nivel"] == "iniciante"

    def test_desafio_java_intermediario(self):
        resultado = exibir_desafio("java", "intermediario")
        assert resultado is not None

    def test_desafio_java_avancado(self):
        resultado = exibir_desafio("java", "avancado")
        assert resultado is not None


class TestComandoCertificado:
    def test_retorna_certificado_valido(self):
        cert = gerar_certificado("Ana Silva", "python")
        assert cert is not None
        assert cert["nome"] == "Ana Silva"
        assert cert["trilha_id"] == "python"
        assert len(cert["codigo_verificacao"]) == 16

    def test_retorna_none_para_trilha_invalida(self):
        cert = gerar_certificado("João", "cobol")
        assert cert is None

    def test_data_padrao_e_hoje(self):
        from datetime import date
        cert = gerar_certificado("Maria", "docker")
        assert cert is not None
        assert cert["data_conclusao"] == date.today().isoformat()

    def test_data_customizada(self):
        cert = gerar_certificado("Pedro", "python", "2024-01-15")
        assert cert is not None
        assert cert["data_conclusao"] == "2024-01-15"

    def test_codigo_e_deterministico(self):
        codigo1 = _gerar_codigo("Ana", "python", "2024-01-01")
        codigo2 = _gerar_codigo("Ana", "python", "2024-01-01")
        assert codigo1 == codigo2

    def test_codigo_muda_com_dados_diferentes(self):
        codigo1 = _gerar_codigo("Ana", "python", "2024-01-01")
        codigo2 = _gerar_codigo("Ana", "javascript", "2024-01-01")
        assert codigo1 != codigo2

    def test_codigo_tem_16_caracteres(self):
        codigo = _gerar_codigo("Ana", "python", "2024-01-01")
        assert len(codigo) == 16

    def test_certificado_java(self):
        cert = gerar_certificado("Maria Lima", "java_basico")
        assert cert is not None
        assert cert["nome"] == "Maria Lima"
        assert cert["trilha_id"] == "java_basico"
        assert len(cert["codigo_verificacao"]) == 16
