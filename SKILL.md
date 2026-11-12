---
name: engineering-patterns
description: Evidence-linked engineering patterns for WPF, real-time audio, SQLite, IPC, STAYA, DevOps, performance profiling, bounded queues, caching, concurrency and memory ownership. Use when designing or reviewing modules, diagnosing race/crash/retry failures, or selecting tests for KLIDAN, Audio Probe, STAYA and new projects.
compatibility: Works offline with Python 3 standard library. External links require network only for source re-verification.
metadata:
  version: "0.8.0-preview.1"
  language: "ru"
---

# Engineering Patterns

This is a decision aid, not an instruction to implement every pattern.

## Trigger

Use when a task has a substantial architectural choice, state machine, thread or process boundary, storage/recovery issue, distributed reliability need, UI separation issue, security boundary, or proven performance bottleneck. Do not invoke for trivial formatting or isolated typo fixes.

## Workflow

1. Read project `AGENTS.md`, ADRs and relevant existing code before using this catalog. Project constraints override generic pattern suggestions. In a new project, identify runtime, requirements and failure model first.
2. Search by task symptoms, project or domain. Example: `python scripts/search_patterns.py --project KLIDAN "reconnect late response"` or `python scripts/search_patterns.py --domain audio`.
3. Inspect 1-3 candidate entries in `data/patterns.json` and their `source_urls`; review `references/priorities.md` for study status.
4. Choose the simplest adequate solution. Explicitly compare it with **doing nothing** or a simpler local fix. Prefer compatible changes; don't use a pattern to justify a needless refactor.
5. State: evidence in this codebase, proposed pattern, why it fits, why alternatives do not, tradeoffs, failure modes, and specific tests.
6. For concurrency, record ownership, lifetime, ordering, queue bounds, cancellation and recovery. For WPF, check 1920×1080, DPI 100/125/150%, keyboard/focus and existing design tokens. For audio, measure callback timing and never assume a queue or double-buffer is real-time safe.
7. Для WPF проверить WorkArea/DIP/per-monitor DPI, Dispatcher ownership, late async completion, focus/keyboard, virtualization, design tokens и скриншоты. См. `references/wpf-fullhd-dpi-contract.md`.
8. Для SQLite/DataRoot разграничивать atomic DB transaction и операции файловой системы, сохранять pending intent до readback и проверять состояние WAL/backup/RootId. См. `references/sqlite-dataroot-recovery-contract.md`.
9. Для STAYA исследовать `references/staya-ipc-resilience-security-contract.md` и сценарии из `data/staya-scenarios.json`. Проверять раздельно process, public route, egress, SSRF, retry budget, secrets, staged rollback. Не объявлять LIVE PASS по config parse.
10. Для release/updater и DevOps проверить source identity, trust policy, metadata freshness, MSI vs non-MSI, staging/rollback, health scope, readiness и telemetry limits. См. `references/devops-release-qa-contract.md` и `data/devops-scenarios.json`.
11. Для performance/cache/concurrency обязательно проверить profiling baseline, bounded queue, pool owner/lifetime, cache revision/TTL, cancellation join и реальную политику потери кадров. См. `references/performance-memory-contract.md` и `data/performance-scenarios.json`.
12. Для QA/fault injection разделять синтетические, интеграционные и физические доказательства; тестировать fake-clock deadlines и crash at every write boundary. См. `references/qa-fault-injection-contract.md`.
13. Для Audio Probe разделять capability discovery, requested/effective periods и физическую стабильность; не фиксировать 3/5/10 ms как универсальную цель. См. `references/audio-probe-profile-contract.md`.
14. If primary source is `index_only` or `pending_primary_review`, say so. Verify externally before treating it as authoritative, and do not claim current implementation is compliant without code/tests.
15. If implementing: keep change scoped; run project-defined builds, tests, and regression checks. Report PASS/FAIL with exact evidence.

## Answer contract for agents

- **Problem and evidence**: one short paragraph identifying symptoms, code locations and invariants.
- **Choice**: exact pattern IDs (or `none`) and cited primary URLs.
- **Why / cost**: expected value and new complexity.
- **Verification**: named automated and physical tests, plus observed results.
- **Decision status**: proposed / proven / rejected. Never mix proposal with production proof.

## Anti-overengineering rules

- Avoid introducing a microservice, message broker, CQRS or Saga when a local method/transaction is enough.
- Keep strict real-time audio and UI threading boundaries. Do not apply an arbitrary backend pattern inside an audio callback.
- `Double Buffer` is not synonymous with an SPSC audio ring buffer.
- Do not retry non-idempotent actions without an explicit duplicate-protection contract.
- Do not infer design-system compliance from build success alone.
- Source catalogs contain ideas, not mandatory coding standards.

## Knowledge organization

- `data/patterns.json`: original machine-readable pattern cards.
- `data/sources.json`: primary URLs and review status.
- `data/upstream-index.json`: 115 unreviewed upstream bibliography URLs (122 occurrences) for future research; NEVER cite as reviewed.
- `references/priorities.md`: study waves and project mapping.
- `references/adding-patterns.md`: expansion rules.
- `references/qa-fault-injection-contract.md`: deterministic timing, I/O failure matrix and evidence levels.
- `data/qa-scenarios.json`: proposed fault-injection cases, not executed tests.
- `references/performance-memory-contract.md`: profiling, buffer ownership, caching and bounded queue QA.
- `data/performance-scenarios.json`: eight proposed synthetic QA cases, not measured performance.
- `references/devops-release-qa-contract.md`: versioned release and rollback, config validation, observability acceptance matrix.
- `data/devops-scenarios.json`: synthetic proposed DevOps/update decisions (not executed QA).
- `references/staya-ipc-resilience-security-contract.md`: STAYA IPC, resilience, security boundaries.
- `data/staya-scenarios.json`: synthetic QA decision scenarios, not executed tests.
- `references/sqlite-dataroot-recovery-contract.md`: транзакции, файлы, WAL и fault injection.
- `references/wpf-fullhd-dpi-contract.md`: операторский интерфейс WPF, DPI и проверка UI.
- `references/audio-probe-profile-contract.md`: WASAPI discovery, minimum stable profile decision and physical QA boundary.
- `scripts/search_patterns.py`: local retrieval (no network).
- `scripts/validate.py`: integrity checks for updated catalog.

## Reuse in ChatGPT and coding agents

Agent reads the local skill when mounted in its skill path; repository instructions can point to it. ChatGPT in a new conversation does not automatically know local files or this archive: attach the skill or provide it through a shared Project/connector context. No hidden automatic synchronization is assumed.
