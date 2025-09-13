from pathlib import Path
from pprint import pprint
from re import search, DOTALL
from sys import stderr
from typing import Dict, Any, Callable, TypeAlias, TYPE_CHECKING

from .helpers import get_context


if TYPE_CHECKING:
    from .core import Ryland


Tube: TypeAlias = Callable[["Ryland", Dict[str, Any]], Dict[str, Any]]


def project(keys: list[str]) -> Tube:
    def inner(_, context: Dict[str, Any]) -> Dict[str, Any]:
        return {k: context[k] for k in keys if k in context}

    return inner


def load(source_path: Path) -> Tube:
    def inner(_, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **context,
            "source_path": source_path,
            "source_content": source_path.read_text(),
        }

    return inner


def markdown(frontmatter: bool = False) -> Tube:
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


def debug(pretty: bool = True) -> Tube:
    def inner(_, context: Dict[str, Any]) -> Dict[str, Any]:
        if pretty:
            pprint(context, stream=stderr)
        else:
            print(context, file=stderr)
        return context

    return inner


def excerpt() -> Tube:
    def inner(_, context: Dict[str, Any]) -> Dict[str, Any]:
        content = get_context("content", "")(context)
        match = search("<p>(.*?)</p>", str(content), DOTALL)
        context["excerpt"] = match.group(1) if match else ""
        return context

    return inner
