from pathlib import Path


class Tube:
    def __init__(self, func):
        self.func = func

    def __or__(self, other):
        return Tube(
            lambda ryland, context: other.func(ryland, self.func(ryland, context))
        )

    def __ror__(self, other: dict):
        return Tube(lambda ryland, context: self.func(ryland, {**other, **context}))

    def context(self, ryland):
        return self.func(ryland, {})


def tube(func):
    return Tube(func)


def project(keys: list):
    def inner(_, context: dict) -> dict:
        return {k: context[k] for k in keys}

    return Tube(inner)


def path(source_path: Path):
    def inner(_, context: dict) -> dict:
        context = context or {}
        return {
            **context,
            "source_path": source_path,
        }

    return Tube(inner)


def calc_context(calculations: dict):
    def inner(_, context: dict) -> dict:
        result = {}
        for key, func in calculations.items():
            result[key] = func(context)
        return {
            **context,
            **result,
        }

    return Tube(inner)


load = calc_context(
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

    return Tube(inner)
