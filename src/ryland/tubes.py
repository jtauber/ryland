from datetime import datetime
from pathlib import Path
from pprint import pprint
from re import search, DOTALL
from sys import stderr
from typing import Dict, Any, Callable, TypeAlias, TYPE_CHECKING
from urllib.parse import quote_plus

import markdown as md
from markdown.extensions.wikilinks import WikiLinkExtension
import yaml

from .helpers import get_context


if TYPE_CHECKING:
    from .core import Ryland


Context: TypeAlias = Dict[str, Any]
Tube: TypeAlias = Callable[["Ryland", Context], Context]


def project(keys: list[str]) -> Tube:
    def inner(_, context: Context) -> Context:
        return {k: context[k] for k in keys if k in context}

    return inner


def load(source_path: Path) -> Tube:
    def inner(_, context: Context) -> Context:
        return {
            **context,
            "source_path": source_path,
            "source_content": source_path.read_text(),
            "source_modified": datetime.fromtimestamp(source_path.stat().st_mtime),
        }

    return inner


def markdown(frontmatter: bool = False) -> Tube:
    def inner(ryland, context: Context) -> Context:
        if frontmatter:
            if context["source_content"].startswith("---\n"):
                _, frontmatter_block, source_content = context["source_content"].split("---\n", 2)
                extra = {"frontmatter": yaml.safe_load(frontmatter_block)}
            else:
                extra = {"frontmatter": {}}
                source_content = context["source_content"]
        else:
            source_content = context["source_content"]
            extra = {}
        html_content = ryland._markdown.convert(source_content)
        ryland._markdown.reset()
        return {
            **context,
            **extra,
            "content": html_content,
        }

    return inner


def _build_wiki_url(label: str, base: str, end: str) -> str:
    clean_label = quote_plus(label)
    return '{}{}{}'.format(base, clean_label, end)


def obsidian_markdown() -> Tube:
    def inner(_, context: Context) -> Context:
        if context["source_content"].startswith("---\n"):
            _, frontmatter_block, source_content = context["source_content"].split("---\n", 2)
            extra = {"frontmatter": yaml.safe_load(frontmatter_block)}
        else:
            extra = {"frontmatter": {}}
            source_content = context["source_content"]
        html_content = md.markdown(source_content, extensions=[WikiLinkExtension(build_url=_build_wiki_url)])
        return {
            **context,
            **extra,
            "content": html_content,
        }

    return inner


def debug(pretty: bool = True) -> Tube:
    def inner(_, context: Context) -> Context:
        if pretty:
            pprint(context, stream=stderr)
        else:
            print(context, file=stderr)
        return context

    return inner


def excerpt() -> Tube:
    def inner(_, context: Context) -> Context:
        content = get_context("content", "")(context)
        match = search("<p>(.*?)</p>", str(content), DOTALL)
        context["excerpt"] = match.group(1) if match else ""
        return context

    return inner
