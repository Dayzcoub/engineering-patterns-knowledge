# Contributing

This project grows by **reviewed decisions**, not by importing every pattern article as text.

## Adding or correcting a pattern

1. Check `data/patterns.json` for duplicate concepts and `data/upstream-index.json` for candidate references.
2. Read the primary source and identify the **exact claim** supported by it. Keep a source as `index_only` or `pending_primary_review` when not fully examined.
3. Add or update the source in `data/sources.json` and the card in `data/patterns.json` using an immutable kebab-case `id`.
4. Fill `signals`, `approach`, `avoid`, `verification`, `projects`, `priority`, and `related`. Use project-specific constraints where necessary.
5. Update the human-friendly summary in `references/cards.md`, research priority where applicable, and `CHANGELOG.md`.
6. Run the validator and tests. Open a focused PR that explains alternative solutions and what has actually been checked.

No broad architecture rewrites should be bundled with catalog updates. This repository **does not** grant permissions to copy third-party content or assert compatibility with project production code.

See [detailed rules](references/adding-patterns.md).
