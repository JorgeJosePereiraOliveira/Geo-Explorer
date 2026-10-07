"""Exercita trilha, desafio e certificado de Java e grava resultados em tests/resultados_java.txt."""
from __future__ import annotations

import json
from pathlib import Path

from src.data_loader import buscar_trilha, buscar_desafio
from src.commands.certificado import gerar_certificado, _gerar_codigo

_RESULTADOS_PATH = Path(__file__).parent / "resultados_java.txt"
_USUARIO = "Maria Lima"
_DATA = "2025-01-15"


def _gravar_resultados(trilha: dict, desafios: list[dict], certificado: dict) -> None:
    """Grava os resultados dos três comandos Java no arquivo de texto."""
    linhas: list[str] = [
        "=" * 70,
        "RESULTADOS DOS TESTES JAVA — GEO-EXPLORER",
        "=" * 70,
        "",
        ">>> TRILHA: java_basico",
        "-" * 40,
        json.dumps(trilha, ensure_ascii=False, indent=2),
        "",
        ">>> DESAFIOS DE JAVA",
        "-" * 40,
    ]
    for desafio in desafios:
        linhas.append(f"[{desafio['nivel'].upper()}] {desafio['titulo']}")
        linhas.append(desafio["descricao"])
        linhas.append("")

    linhas += [
        ">>> CERTIFICADO",
        "-" * 40,
        json.dumps(certificado, ensure_ascii=False, indent=2),
        "",
        "=" * 70,
    ]
    _RESULTADOS_PATH.write_text("\n".join(linhas), encoding="utf-8")


class TestResultadosJava:
    """Exercita o fluxo completo de Java e persiste resultados em arquivo .txt."""

    def test_trilha_java_basico_existe(self):
        trilha = buscar_trilha("java_basico")
        assert trilha is not None, "Trilha java_basico deve existir"
        assert trilha["id"] == "java_basico"
        assert len(trilha["modulos"]) >= 5

    def test_desafio_java_iniciante_existe(self):
        desafio = buscar_desafio("java", "iniciante")
        assert desafio is not None
        assert desafio["tecnologia"] == "java"

    def test_desafio_java_intermediario_existe(self):
        desafio = buscar_desafio("java", "intermediario")
        assert desafio is not None

    def test_desafio_java_avancado_existe(self):
        desafio = buscar_desafio("java", "avancado")
        assert desafio is not None

    def test_certificado_java_valido(self):
        cert = gerar_certificado(_USUARIO, "java_basico", _DATA)
        assert cert is not None
        assert cert["nome"] == _USUARIO
        assert cert["trilha_id"] == "java_basico"
        assert len(cert["codigo_verificacao"]) == 16

    def test_codigo_verificacao_java_deterministico(self):
        c1 = _gerar_codigo(_USUARIO, "java_basico", _DATA)
        c2 = _gerar_codigo(_USUARIO, "java_basico", _DATA)
        assert c1 == c2

    def test_grava_resultados_em_arquivo(self):
        """Executa o fluxo completo e grava em tests/resultados_java.txt."""
        trilha = buscar_trilha("java_basico")
        assert trilha is not None

        niveis = ["iniciante", "intermediario", "avancado"]
        desafios = [buscar_desafio("java", n) for n in niveis]
        desafios_validos = [d for d in desafios if d is not None]
        assert len(desafios_validos) == 3, "Devem existir desafios de Java nos 3 níveis"

        cert = gerar_certificado(_USUARIO, "java_basico", _DATA)
        assert cert is not None

        _gravar_resultados(trilha, desafios_validos, cert)

        assert _RESULTADOS_PATH.exists(), "Arquivo resultados_java.txt deve ser criado"
        conteudo = _RESULTADOS_PATH.read_text(encoding="utf-8")
        assert "java_basico" in conteudo
        assert _USUARIO in conteudo
        assert cert["codigo_verificacao"] in conteudo
