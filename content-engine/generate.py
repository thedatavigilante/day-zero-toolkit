#!/usr/bin/env python3
"""Content engine CLI for The Data Vigilante."""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import click
import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()

console = Console()

PLATFORMS = ["tiktok", "linkedin", "twitter", "github"]
PROMPTS_DIR = Path(__file__).parent / "prompts"
OUTPUT_DIR = Path(__file__).parent / "output"


def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if not path.exists():
        console.print(f"[red]Missing prompt file: {path}[/red]")
        sys.exit(1)
    return path.read_text()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


def save_output(platform: str, topic: str, content: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{platform}_{slugify(topic)}_{timestamp}.md"
    path = OUTPUT_DIR / filename
    path.write_text(f"# {platform.upper()} — {topic}\n\n{content}\n")
    return path


@click.command()
@click.option(
    "--platform",
    "-p",
    required=True,
    type=click.Choice(PLATFORMS, case_sensitive=False),
    help="Target platform: tiktok, linkedin, twitter, github",
)
@click.option(
    "--topic",
    "-t",
    required=True,
    help='Content topic (e.g. "DOGE layoffs and your FEHB rights")',
)
@click.option(
    "--format",
    "-f",
    "content_format",
    default=None,
    help="Platform sub-format (e.g. POST or CAROUSEL for linkedin; README_SECTION or RELEASE_NOTES for github)",
)
@click.option(
    "--model",
    "-m",
    default="claude-sonnet-4-6",
    show_default=True,
    help="Claude model to use",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Optional output filepath (default: auto-saved to output/)",
)
@click.option(
    "--no-save",
    is_flag=True,
    default=False,
    help="Print only, do not save to file",
)
def generate(platform, topic, content_format, model, output, no_save):
    """Generate on-brand social media and GitHub content for The Data Vigilante."""

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print(
            "[red]ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.[/red]"
        )
        sys.exit(1)

    base_persona = load_prompt("base_persona.txt")
    platform_prompt = load_prompt(f"{platform}.txt")

    system = f"{base_persona}\n\n---\n\n{platform_prompt}"

    user_message = f"Topic: {topic}"
    if content_format:
        user_message += f"\nFormat: {content_format.upper()}"

    console.print(
        Panel(
            f"[bold cyan]Platform:[/bold cyan] {platform.upper()}  "
            f"[bold cyan]Topic:[/bold cyan] {topic}"
            + (f"  [bold cyan]Format:[/bold cyan] {content_format.upper()}" if content_format else ""),
            title="[bold]The Data Vigilante — Content Engine[/bold]",
            border_style="cyan",
        )
    )
    console.print("[dim]Generating...[/dim]\n")

    client = anthropic.Anthropic(api_key=api_key)

    with console.status("[bold cyan]Calling Claude...[/bold cyan]"):
        message = client.messages.create(
            model=model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        )

    content = message.content[0].text

    console.print(Markdown(content))

    if not no_save:
        if output:
            save_path = Path(output)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(f"# {platform.upper()} — {topic}\n\n{content}\n")
        else:
            save_path = save_output(platform, topic, content)

        console.print(f"\n[dim]Saved to: {save_path}[/dim]")


if __name__ == "__main__":
    generate()
