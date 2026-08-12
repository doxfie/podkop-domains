#!/usr/bin/env python3
"""Подставляет содержимое domains.lst в README между маркерами.

Единственный источник правды — domains.lst. README правится только автоматически,
руками код-блок со списком не трогать.
"""

import pathlib
import re
import sys

START = "<!-- domains:start -->"
END = "<!-- domains:end -->"

root = pathlib.Path(__file__).resolve().parents[1]
readme_path = root / "README.md"

domains = (root / "domains.lst").read_text(encoding="utf-8").strip("\n")
readme = readme_path.read_text(encoding="utf-8")

if START not in readme or END not in readme:
    sys.exit(f"В README.md нет маркеров {START} / {END}")

block = f"{START}\n\n```\n{domains}\n```\n\n{END}"
updated = re.sub(
    re.escape(START) + ".*?" + re.escape(END),
    lambda _: block,
    readme,
    flags=re.S,
)

if updated == readme:
    print("README уже актуален")
    sys.exit(0)

with open(readme_path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(updated)
print("README обновлён")
