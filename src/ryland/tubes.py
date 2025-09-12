from pathlib import Path


def project(keys: list):
    def inner(_, context: dict) -> dict:
        return {k: context[k] for k in keys}

    return inner


def path(source_path: Path):
    def inner(_, context: dict) -> dict:
        context = context or {}
        return {
            **context,
            "source_path": source_path,
        }

    return inner


def calc_context(calculations: dict):
    def inner(_, context: dict) -> dict:
        result = {}
        for key, func in calculations.items():
            result[key] = func(context)
        return {
            **context,
            **result,
        }

    return inner


load = lambda: calc_context(
    {
        "source_content": lambda context: context["source_path"].read_text(),
    }
)


def markdown(frontmatter=False):
    def inner(ryland, context: dict) -> dict:
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
