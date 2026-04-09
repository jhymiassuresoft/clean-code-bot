"""Groq Cloud chat completion client for refactor responses."""

from __future__ import annotations

import os
import re
from typing import Optional

from groq import Groq

from clean_code_bot.prompt_template import build_chat_messages


class GroqRefactorError(RuntimeError):
    """API or parsing failure."""


def _extract_fenced_code(assistant_text: str) -> str:
    """
    Take the model reply and return inner code from the first fenced block if present;
    otherwise return stripped full text.
    """
    text = assistant_text.strip()
    fence = re.search(
        r"```(?:[\w+-]+)?\s*\n([\s\S]*?)\n```",
        text,
    )
    if fence:
        return fence.group(1).rstrip("\n")
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
        while lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).rstrip("\n")
    return text


def refactor_source(
    *,
    delimited_source: str,
    source_label: str,
    model: str,
    api_key: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """
    Call Groq chat completions and return refactored source (code body only).
    """
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise GroqRefactorError(
            "Missing API key. Set GROQ_API_KEY in the environment or pass api_key=."
        )

    client = Groq(api_key=key)
    messages = build_chat_messages(
        delimited_source=delimited_source,
        source_label=source_label,
    )

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=16_384,
        )
    except Exception as e:
        raise GroqRefactorError(f"Groq API request failed: {e}") from e

    choice = completion.choices[0] if completion.choices else None
    if not choice or not choice.message or not choice.message.content:
        raise GroqRefactorError("Empty response from Groq.")

    return _extract_fenced_code(choice.message.content)
