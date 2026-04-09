"""
Input validation and safe wrapping to reduce prompt-injection risk.

Mitigations are defense-in-depth: size and encoding checks, delimiter wrapping,
and explicit model instructions (see prompt_template) that the bounded region is data only.
"""

from __future__ import annotations

import re
from pathlib import Path

# Groq free tier and latency: keep a conservative cap (bytes).
DEFAULT_MAX_BYTES = 256_000

# If the file contains these substrings as raw text outside normal code, reject or flag.
# We block obvious delimiter-closing attempts that could break out of the trusted wrapper.
_FORBIDDEN_SUBSTRINGS = (
    "<<<SOURCE_END>>>",
    "<<<SOURCE_BEGIN>>>",
)


class SanitizationError(ValueError):
    """Raised when input fails validation."""


def read_and_validate_source(
    path: Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> tuple[str, str]:
    """
    Read `path` as UTF-8 text with validation.

    Returns (raw_text, suggested_language_tag) where tag is a hint for fence parsing
    (e.g. 'python', 'javascript').
    """
    if not path.is_file():
        raise SanitizationError(f"Not a file: {path}")

    data = path.read_bytes()
    if len(data) > max_bytes:
        raise SanitizationError(
            f"File too large ({len(data)} bytes). Maximum allowed is {max_bytes} bytes."
        )
    if b"\x00" in data:
        raise SanitizationError("File contains null bytes; only text source is supported.")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as e:
        raise SanitizationError("File must be valid UTF-8 text.") from e

    # Normalize newlines for stable prompting
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    for bad in _FORBIDDEN_SUBSTRINGS:
        if bad in text:
            raise SanitizationError(
                f"File contains reserved marker {bad!r}; remove it to avoid delimiter confusion."
            )

    # Strip zero-width and other invisible Unicode that sometimes carries payloads
    text = _strip_invisible_unicode(text)

    suffix = path.suffix.lower()
    lang = _suffix_to_language_tag(suffix)
    return text, lang


def wrap_as_untrusted_source_block(text: str) -> str:
    """
    Wrap validated source so the model can treat the region as a single data blob.

    User content cannot close the outer trusted framing without containing the forbidden
    substrings (already rejected).
    """
    return f"<<<SOURCE_BEGIN>>>\n{text}\n<<<SOURCE_END>>>\n"


def _suffix_to_language_tag(suffix: str) -> str:
    mapping = {
        ".py": "python",
        ".pyw": "python",
        ".js": "javascript",
        ".mjs": "javascript",
        ".cjs": "javascript",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".jsx": "jsx",
        ".rs": "rust",
        ".go": "go",
        ".java": "java",
        ".kt": "kotlin",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
        ".swift": "swift",
    }
    return mapping.get(suffix, "text")


_INVISIBLE_RE = re.compile(
    "[\u200b\u200c\u200d\u2060\ufeff\u00ad]"
)


def _strip_invisible_unicode(text: str) -> str:
    return _INVISIBLE_RE.sub("", text)
