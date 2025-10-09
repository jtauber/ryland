from typing import List


def get_context(path: str, default=None):
    def inner(context):
        def _get_nested(obj, keys: List[str]):
            if not keys or obj is None:
                return obj

            key = keys[0]
            remaining_keys = keys[1:]

            if key in obj:
                return _get_nested(obj[key], remaining_keys)
            else:
                return None

        keys = path.split(".")
        result = _get_nested(context, keys)

        return result or default

    return inner
