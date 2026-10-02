"""CLI principal do Geo-Explorer — ponto de entrada para todos os comandos."""
from __future__ import annotations

import click
from rich.console import Console

from src.commands.trilha import exibir_trilha
from src.commands.desafio import exibir_desafio
from src.commands.certificado import gerar_certificado
from src.data_loader import listar_tecnologias

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="geo-explorer")
def main() -> None:
    """🌍 Geo-Explorer — Explore trilhas de aprendizagem, resolva desafios e conquiste certificados."""


@main.command("trilha")
@click.argument("tecnologia")
def cmd_trilha(tecnologia: str) -> None:
    """Exibe o plano de estudos para a TECNOLOGIA informada.

    \b
    Exemplos:
      geo trilha python
      geo trilha javascript
      geo trilha docker
    """
    exibir_trilha(tecnologia)


@main.command("desafio")
@click.argument("tecnologia")
@click.argument("nivel")
def cmd_desafio(tecnologia: str, nivel: str) -> None:
    """Gera um desafio de código para a TECNOLOGIA e NIVEL informados.

    \b
    Níveis disponíveis: iniciante, intermediario, avancado

    \b
    Exemplos:
      geo desafio python iniciante
      geo desafio javascript intermediario
      geo desafio typescript iniciante
    """
    exibir_desafio(tecnologia, nivel)


@main.command("certificado")
@click.argument("nome")
@click.argument("tecnologia")
@click.option("--data", "data_conclusao", default=None, help="Data de conclusão (YYYY-MM-DD). Padrão: hoje.")
def cmd_certificado(nome: str, tecnologia: str, data_conclusao: str | None) -> None:
    """Gera um certificado fictício para NOME na trilha TECNOLOGIA.

    \b
    Exemplos:
      geo certificado "Ana Silva" python
      geo certificado "João Costa" docker --data 2024-12-01
    """
    gerar_certificado(nome, tecnologia, data_conclusao)


@main.command("listar")
def cmd_listar() -> None:
    """Lista todas as tecnologias disponíveis."""
    techs = listar_tecnologias()
    console.print("[bold cyan]Tecnologias disponíveis:[/bold cyan]")
    for tech in techs:
        console.print(f"  • [green]{tech}[/green]")


if __name__ == "__main__":
    main()
