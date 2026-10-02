"""Comando trilha — exibe o plano de estudos de uma tecnologia."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.data_loader import buscar_trilha, listar_tecnologias

console = Console()


def exibir_trilha(tecnologia: str) -> dict | None:
    """
    Busca e exibe a trilha de aprendizagem da tecnologia informada.

    Retorna o dicionário da trilha ou None se não encontrada.
    """
    trilha = buscar_trilha(tecnologia)

    if trilha is None:
        disponiveis = ", ".join(listar_tecnologias())
        console.print(
            f"[bold red]Trilha '[yellow]{tecnologia}[/yellow]' não encontrada.[/bold red]\n"
            f"Tecnologias disponíveis: [cyan]{disponiveis}[/cyan]"
        )
        return None

    # Cabeçalho
    console.print(
        Panel(
            f"[bold cyan]{trilha['nome']}[/bold cyan]\n"
            f"[white]{trilha['descricao']}[/white]\n\n"
            f"[green]Nível:[/green] {trilha['nivel'].capitalize()}   "
            f"[green]Carga horária:[/green] {trilha['carga_horaria']}h",
            title="[bold blue]📚 Trilha de Aprendizagem[/bold blue]",
            border_style="blue",
        )
    )

    # Tabela de módulos
    tabela = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    tabela.add_column("#", style="dim", width=4, justify="center")
    tabela.add_column("Módulo", style="bold white", min_width=25)
    tabela.add_column("Tópicos", style="cyan")

    for modulo in trilha["modulos"]:
        topicos = " • ".join(modulo["topicos"])
        tabela.add_row(str(modulo["ordem"]), modulo["titulo"], topicos)

    console.print(tabela)
    return trilha
