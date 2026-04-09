---
description: Add a new template repo to repository-templates.json and regenerate the README
argument-hint: [repo-name] [section]
---

Add a new entry (or entries) to `repository-templates.json`, then regenerate `README.md`.

## Arguments

$ARGUMENTS

If arguments were not supplied, ask the user for:
- The GitHub repo name (e.g. `Claude-Foo-Template`)
- Which section it belongs in (see the `sections` array in `repository-templates.json` — typically "Claude Code Workspace Templates" or "General Starters And Patterns")
- A one-line description (fetch from `gh repo view danielrosehill/<repo> --json description` if the user doesn't supply one)

## Steps

1. Read `repository-templates.json` to see existing sections and entries.
2. For each new repo:
   - Verify it exists and is public: `gh repo view danielrosehill/<repo> --json name,description,visibility`
   - Derive a display name by replacing hyphens with spaces (adjust casing as needed).
   - Append a new entry to the correct section's `entries` array:
     ```json
     {"name": "...", "repo": "...", "description": "..."}
     ```
3. Run `python3 scripts/generate_readme.py` — this sorts entries alphabetically and regenerates `README.md`.
4. Show `git diff --stat` and confirm with the user.
5. Commit and push:
   ```bash
   git add repository-templates.json README.md
   git commit -m "Add <repo-name> to <section>"
   git push
   ```

## Optional: bulk delta check

If the user wants to find all missing templates, use this approach instead:
1. `gh repo list danielrosehill --limit 1000 --visibility public --json name,description,isTemplate` to list public repos.
2. Filter for repos whose name/description contains "template", "starter", "scaffold", or "workspace".
3. Diff against the `repo` fields already in `repository-templates.json`.
4. Present the delta to the user for classification before adding.
