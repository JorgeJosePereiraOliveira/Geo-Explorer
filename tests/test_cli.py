"""Testes da CLI via click.testing.CliRunner para ampliar cobertura de src/cli.py."""
from __future__ import annotations

from click.testing import CliRunner

from src.cli import main


class TestCLITrilha:
    """Testa o comando `geo trilha` via CliRunner."""

    def test_trilha_java_basico(self):
        runner = CliRunner()
        result = runner.invoke(main, ["trilha", "java_basico"])
        assert result.exit_code == 0

    def test_trilha_python(self):
        runner = CliRunner()
        result = runner.invoke(main, ["trilha", "python"])
        assert result.exit_code == 0

    def test_trilha_inexistente(self):
        runner = CliRunner()
        result = runner.invoke(main, ["trilha", "cobol"])
        assert result.exit_code == 0  # comando não levanta exceção, só imprime erro


class TestCLIDesafio:
    """Testa o comando `geo desafio` via CliRunner."""

    def test_desafio_java_iniciante(self):
        runner = CliRunner()
        result = runner.invoke(main, ["desafio", "java", "iniciante"])
        assert result.exit_code == 0

    def test_desafio_python_intermediario(self):
        runner = CliRunner()
        result = runner.invoke(main, ["desafio", "python", "intermediario"])
        assert result.exit_code == 0

    def test_desafio_nivel_invalido(self):
        runner = CliRunner()
        result = runner.invoke(main, ["desafio", "python", "ninja"])
        assert result.exit_code == 0


class TestCLICertificado:
    """Testa o comando `geo certificado` via CliRunner."""

    def test_certificado_java(self):
        runner = CliRunner()
        result = runner.invoke(main, ["certificado", "Maria Lima", "java_basico"])
        assert result.exit_code == 0

    def test_certificado_com_data(self):
        runner = CliRunner()
        result = runner.invoke(main, ["certificado", "Pedro Costa", "python", "--data", "2024-06-01"])
        assert result.exit_code == 0

    def test_certificado_trilha_invalida(self):
        runner = CliRunner()
        result = runner.invoke(main, ["certificado", "Ana", "cobol"])
        assert result.exit_code == 0


class TestCLIListar:
    """Testa o comando `geo listar` via CliRunner."""

    def test_listar_retorna_tecnologias(self):
        runner = CliRunner()
        result = runner.invoke(main, ["listar"])
        assert result.exit_code == 0

    def test_versao(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
