#!/usr/bin/env python3
"""Replace environment-specific Azure resource IDs with neutral placeholders.

Workbooks exported from the Azure portal frequently carry the author's own
subscription ID, resource group and workspace name in ``fallbackResourceIds``,
``crossComponentResources`` and parameter default values. Those values are
useless to anyone else (the resource does not exist in their tenant) and they
leak details about the environment the workbook was exported from.

This script rewrites every ``/subscriptions/<guid>/...`` path (plain or
URL-encoded) so that:

* the subscription GUID becomes ``00000000-0000-0000-0000-000000000000``
* the resource group name becomes ``placeholder-rg``
* the resource name becomes ``placeholder-workspace`` for Log Analytics
  workspaces and ``placeholder-resource`` for anything else

Provider namespaces and resource types are preserved so the workbook still
knows what kind of resource the parameter expects. Text is edited in place
without re-serialising the JSON, so formatting is untouched.

Usage:
    python scripts/scrub_resource_ids.py            # rewrite files in place
    python scripts/scrub_resource_ids.py --check    # exit 1 if anything would change
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER_SUB = "00000000-0000-0000-0000-000000000000"
PLACEHOLDER_RG = "placeholder-rg"
PLACEHOLDER_WS = "placeholder-workspace"
PLACEHOLDER_RES = "placeholder-resource"

GUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

# Plain form: /subscriptions/<guid>[/resourceGroups/<rg>[/providers/<ns>/<type>/<name>]]
# A segment ends at a slash, quote, backslash (JSON escape), whitespace or
# common delimiters that appear when IDs are embedded in query text.
_SEG = r"[^/\"'\\\s\]\[,;)(&?#%]+"
PLAIN = re.compile(
    rf"/subscriptions/(?P<sub>{GUID})"
    rf"(?:/(?P<rgkey>resourceGroups|resourcegroups)/(?P<rg>{_SEG}))?"
    rf"(?:/(?P<provkey>providers)/(?P<ns>{_SEG})/(?P<type>{_SEG})/(?P<name>{_SEG}))?",
    re.IGNORECASE,
)

# URL-encoded form used inside portal deep links: %2Fsubscriptions%2F<guid>%2F...
_ESEG = r"(?:[^%\"'\\\s&?#]|%(?!2[Ff]|22))+"
ENCODED = re.compile(
    rf"%2[Ff]subscriptions%2[Ff](?P<sub>{GUID})"
    rf"(?:%2[Ff](?P<rgkey>resourceGroups|resourcegroups)%2[Ff](?P<rg>{_ESEG}))?"
    rf"(?:%2[Ff](?P<provkey>providers)%2[Ff](?P<ns>{_ESEG})%2[Ff](?P<type>{_ESEG})%2[Ff](?P<name>{_ESEG}))?",
    re.IGNORECASE,
)

# Personal e-mail addresses that appear as parameter default values.
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:onmicrosoft\.com|ms)\b")
PLACEHOLDER_EMAIL = "user@example.com"


def _rebuild(m: re.Match, sep: str) -> str:
    if m.group("sub").lower() == PLACEHOLDER_SUB:
        return m.group(0)
    out = f"{sep}subscriptions{sep}{PLACEHOLDER_SUB}"
    if m.group("rgkey"):
        out += f"{sep}{m.group('rgkey')}{sep}{PLACEHOLDER_RG}"
    if m.group("provkey"):
        name = PLACEHOLDER_WS if m.group("type").lower() == "workspaces" else PLACEHOLDER_RES
        out += f"{sep}providers{sep}{m.group('ns')}{sep}{m.group('type')}{sep}{name}"
    return out


def scrub_text(text: str) -> str:
    text = PLAIN.sub(lambda m: _rebuild(m, "/"), text)
    text = ENCODED.sub(lambda m: _rebuild(m, "%2F"), text)
    text = EMAIL.sub(PLACEHOLDER_EMAIL, text)
    return text


def workbook_files(root: Path):
    return sorted(p for p in root.rglob("*.workbook") if ".git" not in p.parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="report files that would change and exit 1")
    parser.add_argument("paths", nargs="*", type=Path, help="files or folders to process (default: whole repo)")
    args = parser.parse_args(argv)

    targets: list[Path] = []
    for p in args.paths or [ROOT]:
        targets.extend(workbook_files(p) if p.is_dir() else [p])

    changed = []
    for path in targets:
        original = path.read_text(encoding="utf-8")
        scrubbed = scrub_text(original)
        if scrubbed != original:
            changed.append(path)
            if not args.check:
                path.write_text(scrubbed, encoding="utf-8")

    verb = "would change" if args.check else "scrubbed"
    for path in changed:
        print(f"{verb}: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    print(f"{len(changed)} file(s) {verb}, {len(targets)} scanned")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
