---
description: Regenerate README.md from repository-templates.json
---

Regenerate the index README from the JSON source of truth.

Steps:

1. Run the generator:
   ```bash
   python3 scripts/generate_readme.py
   ```
2. Show the user `git diff --stat` and a summary of what changed.
3. If the diff looks correct, stage and commit:
   ```bash
   git add repository-templates.json README.md
   git commit -m "Regenerate README from repository-templates.json"
   git push
   ```

Notes:
- `repository-templates.json` is the source of truth. Never hand-edit README.md — edit the JSON and re-run this command.
- The script alphabetises entries within each section and rewrites the JSON in sorted order.
