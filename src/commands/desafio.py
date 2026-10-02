"""Comando desafio — gera um desafio de código conforme tecnologia e nível."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich import box
from rich.table import Table

from src.data_loader import buscar_desafio, listar_tecnologias

console = Console()

_NIVEIS_VALIDOS = ["iniciante", "intermediario", "avancado"]


def exibir_desafio(tecnologia: str, nivel: str) -> dict | None:
    """
    Busca e exibe um desafio de código para a tecnologia e nível informados.

    Retorna o dicionário do desafio ou None se não encontrado.
    """
    nivel_norm = nivel.lower()
    if nivel_norm not in _NIVEIS_VALIDOS:
        console.print(
            f"[bold red]Nível '[yellow]{nivel}[/yellow]' inválido.[/bold red]\n"
            f"Níveis válidos: [cyan]{', '.join(_NIVEIS_VALIDOS)}[/cyan]"
        )
        return None

    desafio = buscar_desafio(tecnologia, nivel_norm)

    if desafio is None:
        disponiveis = ", ".join(listar_tecnologias())
        console.print(
            f"[bold red]Desafio não encontrado para '[yellow]{tecnologia}[/yellow]' "
            f"— nível '[yellow]{nivel}[/yellow]'.[/bold red]\n"
            f"Tecnologias disponíveis: [cyan]{disponiveis}[/cyan]"
        )
        return None

    # Cabeçalho
    console.print(
        Panel(
            f"[bold yellow]{desafio['titulo']}[/bold yellow]\n\n"
            f"[white]{desafio['descricao']}[/white]",
            title=f"[bold blue]⚡ Desafio — {tecnologia.capitalize()} ({nivel_norm.capitalize()})[/bold blue]",
            border_style="yellow",
        )
    )

    # Exemplo
    console.print(Rule("[bold cyan]Exemplo[/bold cyan]"))
    console.print(f"[green]Entrada:[/green]  [white]{desafio['exemplo_entrada']}[/white]")
    console.print(f"[green]Saída:[/green]    [white]{desafio['exemplo_saida']}[/white]\n")

    # Dicas
    if desafio.get("dicas"):
        tabela = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        tabela.add_column("Dica", style="cyan")
        for dica in desafio["dicas"]:
            tabela.add_row(f"💡 {dica}")
        console.print(Panel(tabela, title="[bold]Dicas[/bold]", border_style="dim"))

    return desafio
