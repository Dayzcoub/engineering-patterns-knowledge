# Instructions for coding agents

This repository is an **offline knowledge skill**. The curated JSON is not a mandatory design system.

1. Read `SKILL.md` and `references/adding-patterns.md` before changing pattern content.
2. Keep stable `id` values and preserve existing `source_urls` / review statuses unless newly substantiated by primary-source research.
3. Keep `data/upstream-index.json` separate from `data/sources.json`: an unreviewed index is not a primary-source audit.
4. Do not copy full proprietary articles, books, or other third-party content here. Paraphrase briefly, cite original URLs, respect source licenses.
5. For any new pattern, document: signal, approach, when **not** to use, validation/failure modes, project impact, `source_review`, and related IDs.
6. Avoid promising real-time, safety, security or performance properties without measurements and applicable tests.
7. Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` before PR/commit.
8. Do not modify KLIDAN/Audio Probe/STAYA sources from this repository. Integration belongs to the respective project PR.
9. Never claim that automated JSON validation proves the pattern's architectural suitability.
10. Для STAYA использовать placeholder вместо адресов, токенов, приватных ключей и production subscription URL. Evidence всегда redacted.
11. Разделять document review, offline model checks, staged integration checks и live transport evidence.
12. Update-паттерны: определить реальный тип установщика (MSI/Inno/NSIS), ожидаемую цепочку доверия и модель update feed до предложения изменений.
13. Отличать проверку конфигурации от проверки реального network/rollback/release; status DOC_REVIEW не является PROD_PASS.
