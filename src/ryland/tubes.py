from pathlib import Path
from typing import Dict, Any

from .helpers import get_context


def project(keys: list[str]):
    def inner(_, context: Dict[str, Any]) -> Dict[str, Any]:
        return {k: context[k] for k in keys if k in context}

    return inner


def path(source_path: Path):
    def inner(_, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **(context or {}),
            "source_path": source_path,
        }

    return inner


def load():
    return {
        "source_content": lambda context: get_context("source_path")(
            context
        ).read_text(),
    }


def markdown(frontmatter=False):
    def inner(ryland, context: Dict[str, Any]) -> Dict[str, Any]:
        html_content = ryland._markdown.convert(context["source_content"])
        if frontmatter:
            if hasattr(ryland._markdown, "Meta"):
                extra = {"frontmatter": ryland._markdown.Meta}  # type: ignore
            else:
                extra = {"frontmatter": {}}
        else:
            extra = {}
        ryland._markdown.reset()
        return {
            **context,
            **extra,
            "content": html_content,
        }

    return inner
