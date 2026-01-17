from pathlib import Path
from shutil import copy
from typing import List

from PIL import Image


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


def resize_and_copy(path: Path, out_path: Path, max_size: tuple[int, int]) -> None:
    try:
        if out_path.exists() and out_path.stat().st_mtime >= path.stat().st_mtime:
            return
    except OSError:
        pass
    ext = path.suffix.lower()
    if ext in (".svg"):
        copy(path, out_path)
    else:
        try:
            with Image.open(path) as im:
                mode = "RGBA" if "A" in im.getbands() else "RGB"
                if im.mode != mode:
                    im = im.convert(mode)
                im.thumbnail(max_size, Image.Resampling.LANCZOS)
                if ext in (".jpg", ".jpeg") and im.mode == "RGBA":
                    im = im.convert("RGB")
                im.save(out_path)
        except Exception:
            copy(path, out_path)
