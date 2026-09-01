#!/usr/bin/env python3
"""Validate every ``*.workbook`` file in the repository.

Checks performed on each file:

* parses as UTF-8 JSON without a byte-order mark or leading comment lines
  (the Azure portal's Advanced Editor rejects both)
* top-level value is an object with ``"version": "Notebook/1.0"`` and an
  ``items`` array, which is the minimum the Gallery Template editor needs
* no environment-specific ``/subscriptions/<guid>/...`` resource IDs are left
  in the file (see ``scrub_resource_ids.py``)
* the file lives inside a category folder, not at the repository root

Exit status is non-zero when any error is found, so the script doubles as
the CI gate in ``.github/workflows/validate.yml``.

Usage:
    python scripts/validate_workbooks.py            # whole repository
    python scripts/validate_workbooks.py path/a.workbook "Networking/"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_VERSION = "Notebook/1.0"
PLACEHOLDER_SUB = "00000000-0000-0000-0000-000000000000"
GUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
SUBSCRIPTION_PATH = re.compile(rf"(?:/|%2[Ff])subscriptions(?:/|%2[Ff])({GUID})", re.IGNORECASE)


def workbook_files(root: Path):
    return sorted(p for p in root.rglob("*.workbook") if ".git" not in p.parts)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_bytes()

    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("file starts with a UTF-8 byte-order mark")
        raw = raw[3:]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return errors + [f"not valid UTF-8: {exc}"]

    if text.lstrip().startswith("//"):
        errors.append("file starts with a // comment; JSON does not allow comments")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return errors + [f"invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})"]

    if not isinstance(data, dict):
        return errors + ["top-level JSON value must be an object"]

    version = data.get("version")
    if version != EXPECTED_VERSION:
        errors.append(f'"version" is {version!r}, expected {EXPECTED_VERSION!r}')
    if not isinstance(data.get("items"), list):
        errors.append('"items" must be an array')

    leaked = sorted({m.group(1).lower() for m in SUBSCRIPTION_PATH.finditer(text)} - {PLACEHOLDER_SUB})
    if leaked:
        errors.append(
            "contains environment-specific subscription IDs "
            f"({', '.join(leaked)}); run scripts/scrub_resource_ids.py"
        )

    try:
        rel = path.resolve().relative_to(ROOT)
        if len(rel.parts) < 2:
            errors.append("workbook must live inside a category folder, not the repository root")
    except ValueError:
        pass

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="*", type=Path, help="files or folders to validate (default: whole repo)")
    args = parser.parse_args(argv)

    targets: list[Path] = []
    for p in args.paths or [ROOT]:
        targets.extend(workbook_files(p) if p.is_dir() else [p])

    failed = 0
    for path in targets:
        problems = validate(path)
        if problems:
            failed += 1
            shown = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
            print(f"FAIL {shown}")
            for problem in problems:
                print(f"     - {problem}")

    print(f"{len(targets) - failed} passed, {failed} failed, {len(targets)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
