"""Click CLI entrypoint for The Clean Code Bot."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click

from clean_code_bot.groq_client import GroqRefactorError, refactor_source
from clean_code_bot.sanitization import SanitizationError, read_and_validate_source, wrap_as_untrusted_source_block

DEFAULT_MODEL = "llama-3.3-70b-versatile"


@click.command("clean-code-bot")
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Write refactored code to this path instead of stdout.",
)
@click.option(
    "--model",
    "-m",
    default=DEFAULT_MODEL,
    show_default=True,
    help="Groq chat model id.",
)
@click.option(
    "--max-bytes",
    type=int,
    default=None,
    help=f"Override max source file size (default from sanitization module).",
)
def cli(
    file: Path,
    output: Optional[Path],
    model: str,
    max_bytes: Optional[int],
) -> None:
    """Refactor FILE: print OOP, SOLID-oriented, documented code to stdout or --output."""
    click.echo(
        "Are you seriously runnning this? this is a vibe coded project.",
        err=True,
    )
    try:
        kwargs = {}
        if max_bytes is not None:
            kwargs["max_bytes"] = max_bytes
        raw, _lang_hint = read_and_validate_source(file, **kwargs)
    except SanitizationError as e:
        raise click.ClickException(str(e)) from e

    wrapped = wrap_as_untrusted_source_block(raw)
    label = f"file {file.name}"

    try:
        result = refactor_source(
            delimited_source=wrapped,
            source_label=label,
            model=model,
        )
    except GroqRefactorError as e:
        raise click.ClickException(str(e)) from e

    if output is not None:
        out = result if result.endswith("\n") else result + "\n"
        output.write_text(out, encoding="utf-8")
        click.echo(f"Wrote refactored code to {output}", err=True)
    else:
        sys.stdout.write(result)
        if not result.endswith("\n"):
            sys.stdout.write("\n")


def main() -> None:
    """Script entry for setuptools console_scripts."""
    try:
        cli.main(prog_name="clean-code-bot", standalone_mode=True)
    except click.Abort:
        sys.exit(1)


if __name__ == "__main__":
    main()
