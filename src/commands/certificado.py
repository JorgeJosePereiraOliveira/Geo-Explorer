"""Comando certificado — gera um certificado fictício para uma trilha concluída."""
from __future__ import annotations

import hashlib
from datetime import date

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.align import Align
from rich.text import Text

from src.data_loader import buscar_trilha, listar_tecnologias

console = Console()


def _gerar_codigo(nome: str, tecnologia: str, data_conclusao: str) -> str:
    """Gera um código único de verificação baseado nos dados do certificado."""
    raw = f"{nome.lower()}|{tecnologia.lower()}|{data_conclusao}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def gerar_certificado(nome: str, tecnologia: str, data_conclusao: str | None = None) -> dict | None:
    """
    Gera e exibe um certificado fictício para o estudante informado.

    Args:
        nome: Nome completo do estudante.
        tecnologia: Identificador da tecnologia/trilha concluída.
        data_conclusao: Data de conclusão no formato YYYY-MM-DD (padrão: hoje).

    Retorna o dicionário do certificado ou None se a trilha não existir.
    """
    trilha = buscar_trilha(tecnologia)

    if trilha is None:
        disponiveis = ", ".join(listar_tecnologias())
        console.print(
            f"[bold red]Trilha '[yellow]{tecnologia}[/yellow]' não encontrada.[/bold red]\n"
            f"Tecnologias disponíveis: [cyan]{disponiveis}[/cyan]"
        )
        return None

    data_str = data_conclusao or date.today().isoformat()
    codigo = _gerar_codigo(nome, tecnologia, data_str)

    # Renderização do certificado
    console.print()
    console.print(Rule("[bold gold1]✨ CERTIFICADO DE CONCLUSÃO ✨[/bold gold1]"))
    console.print()

    titulo = Text("GEO-EXPLORER", style="bold blue", justify="center")
    subtitulo = Text("Plataforma de Trilhas de Aprendizagem", style="dim", justify="center")
    console.print(Align.center(titulo))
    console.print(Align.center(subtitulo))
    console.print()

    conteudo = (
        f"[dim]Certificamos que[/dim]\n\n"
        f"[bold white]  {nome}  [/bold white]\n\n"
        f"[dim]concluiu com êxito a trilha[/dim]\n\n"
        f"[bold cyan]  {trilha['nome']}  [/bold cyan]\n\n"
        f"[dim]Nível:[/dim] [green]{trilha['nivel'].capitalize()}[/green]   "
        f"[dim]Carga horária:[/dim] [green]{trilha['carga_horaria']}h[/green]\n\n"
        f"[dim]Data de conclusão:[/dim] [white]{data_str}[/white]\n"
        f"[dim]Código de verificação:[/dim] [yellow]{codigo}[/yellow]"
    )

    console.print(
        Panel(
            Align.center(conteudo),
            border_style="gold1",
            padding=(1, 4),
        )
    )

    console.print()
    console.print(Rule("[dim]Este é um certificado fictício gerado pelo Geo-Explorer[/dim]"))
    console.print()

    certificado = {
        "nome": nome,
        "trilha_id": tecnologia,
        "trilha_nome": trilha["nome"],
        "nivel": trilha["nivel"],
        "carga_horaria": trilha["carga_horaria"],
        "data_conclusao": data_str,
        "codigo_verificacao": codigo,
    }
    return certificado
