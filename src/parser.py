"""Command parser with environment variable expansion."""

import os
import re

ENV_VAR_PATTERN = r'\$\{([^}]+)\}|\$([A-Za-z_]\w*)'


def expand_env_vars(text: str) -> str:
    """Expand environment variables like $VAR and ${VAR}."""

    def _replace(match: re.Match) -> str:
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, "")

    return re.sub(ENV_VAR_PATTERN, _replace, text)


def _is_quote(char: str) -> bool:
    """Return True if character is a quote mark."""
    return char in ('"', "'")


def _handle_in_quote(
    char: str,
    in_quote: str | None,
    current: list[str],
) -> str | None:
    """Process character when inside quotes."""
    if char == in_quote:
        return None
    current.append(char)
    return in_quote


def _handle_outside_quote(
    char: str,
    tokens: list[str],
    current: list[str],
) -> str | None:
    """Process character outside quotes."""
    if _is_quote(char):
        return char
    if char == ' ':
        if current:
            tokens.append("".join(current))
            current.clear()
        return None
    current.append(char)
    return None


def _tokenize(text: str) -> list[str]:
    """Split text into tokens respecting quoted arguments."""
    tokens: list[str] = []
    current: list[str] = []
    in_quote: str | None = None

    for char in text:
        if in_quote is not None:
            in_quote = _handle_in_quote(char, in_quote, current)
        else:
            in_quote = _handle_outside_quote(
                char, tokens, current
            )

    if current:
        tokens.append("".join(current))

    return tokens


def parse_command(line: str) -> tuple[str, list[str]]:
    """Parse input line into command name and arguments."""
    expanded = expand_env_vars(line)
    tokens = _tokenize(expanded)

    if not tokens:
        return "", []

    return tokens[0], tokens[1:]