#!/usr/bin/env python3
"""Generate README.md from repository-templates.json.

The JSON file is the source of truth. Edit it (or use the /add-template
slash command), then run this script to regenerate README.md.

Usage: python3 scripts/generate_readme.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "repository-templates.json"
README = ROOT / "README.md"

MASTER_BADGE = (
    "[![Master Index]"
    "(https://img.shields.io/badge/Master%20Index-All%20Repositories-purple"
    "?style=for-the-badge&logo=github)]"
    "(https://github.com/danielrosehill/Index)"
)
LICENSE_BADGE = (
    "[![License: CC BY 4.0]"
    "(https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)]"
    "(https://creativecommons.org/licenses/by/4.0/)"
)


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "").replace(",", "")


def view_badge(user: str, repo: str) -> str:
    return (
        f"[![View Repo]"
        f"(https://img.shields.io/badge/View-Repo-blue?style=flat&logo=github)]"
        f"(https://github.com/{user}/{repo})"
    )


def render(data: dict) -> str:
    user = data["github_user"]
    out: list[str] = []
    out.append(f"# {data['title']}")
    out.append("")
    out.append(MASTER_BADGE)
    out.append("")
    out.append(data["description"])
    out.append("")
    out.append(f"**Last Updated:** {data['last_updated']}")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Table of Contents")
    out.append("")
    for section in data["sections"]:
        out.append(f"- [{section['name']}](#{slugify(section['name'])})")
    out.append("")
    out.append("---")
    out.append("")

    for section in data["sections"]:
        out.append(f"## {section['name']}")
        out.append("")
        entries = sorted(section["entries"], key=lambda e: e["name"].lower())
        for entry in entries:
            out.append(f"### {entry['name']}")
            out.append("")
            out.append(entry["description"])
            out.append("")
            out.append(view_badge(user, entry["repo"]))
            out.append("")
        out.append("---")
        out.append("")

    out.append("## License")
    out.append("")
    out.append(LICENSE_BADGE)
    out.append("")
    return "\n".join(out)


def main() -> None:
    data = json.loads(DATA.read_text())
    # Sort entries in-place so JSON stays tidy too.
    for section in data["sections"]:
        section["entries"].sort(key=lambda e: e["name"].lower())
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    README.write_text(render(data))
    total = sum(len(s["entries"]) for s in data["sections"])
    print(f"Wrote {README.relative_to(ROOT)} ({total} entries across "
          f"{len(data['sections'])} sections)")


if __name__ == "__main__":
    main()
