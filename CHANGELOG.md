## 0.9.0-preview.1 (2026-11-12)

- 7 P1 карточек WPF: AutomationPeer, critical operator semantics, keyboard navigation, system contrast, text readability, localization and accessibility evidence.
- Добавлены `references/wpf-accessibility-qa-contract.md` и 6 proposed QA scenarios.
- Версии QA файлов и validator синхронизированы; реальные испытания KLIDAN не проводились.

## 0.8.0-preview.1 (2026-11-12)

- 8 новых QA-карточек: fake time, deterministic ordering, I/O/crash fault injection, cancellation lifecycle, physical evidence separation, evidence manifest и CI isolation.
- Добавлены контракт `references/qa-fault-injection-contract.md` и 6 proposed сценариев `data/qa-scenarios.json`.
- Синхронизированы версии каталогов сценариев, расширены CI и офлайн-проверки.
- Рабочие приложения и серверы не менялись; physical/live QA не проводилось.

## 0.7.0-preview.1 (2026-11-12)

- Добавлено 13 карточек P0/P2 по System.Threading.Channels, ArrayPool, LOH/GC, Span/Memory, Pipelines, GetOrAdd, кешированию, ReaderWriterLockSlim, CancellationTokenSource и preview coalescing.
- Добавлены `references/performance-memory-contract.md` и 8 сценариев `data/performance-scenarios.json` для KLIDAN/Audio Probe/STAYA.
- Синхронизированы версии уже существующих сценариев; тесты расширены на источники, ссылки и границы доказательств.
- Реальных замеров и изменений production-кода нет.

## 0.6.0-preview.1 (2026-11-12)

- Добавлены 16 P0/P1 карточек по Caddy validate/reload, systemd, Compose readiness, immutable images, SOPS, OpenTelemetry/Prometheus, TUF, Authenticode, MSI rollback, updater handoff, SLSA и release approvals.
- Подготовлены `references/devops-release-qa-contract.md` и 8 machine-readable сценариев; ни один не помечен как выполненная production QA.
- Расширена валидация сценариев и offline tests. STAYA scenarios синхронизированы с текущей версией каталога.
- Никакие приложения и рабочие сервисы не менялись.

## 0.5.0-preview.1 (2026-11-12)

- Добавлены 16 карточек P1 по IPC, асинхронным ответам, rate limits, health, failover, SSRF, canonical subscription merge, public routing, safe deploy, admin isolation, secrets, logging и provenance.
- Добавлен контракт STAYA и 6 machine-readable сценариев для review и QA.
- Добавлены регрессионные проверки сценариев и статуса первоисточников.
- Код STAYA/Xray/Caddy, рабочие ноды и пользовательские подписки не изменялись; live PASS не заявлен.

## 0.4.0-preview.1 (2026-11-12)

- Добавлено 8 SQLite/DataRoot карточек: cross-store intent, checkpoint control, synchronous durability, live backup, single-writer retries, FK enforcement, integrity gate, nested savepoints.
- Добавлен контракт восстановления и fault-injection matrix, с разделением SQLite API guarantees и project design proposal.
- Запрещены false claims о power loss durability, cross-volume atomic rename и простом .db copy при active WAL.
- Нет изменений production KLIDAN; нет физического crash-test PASS.

## 0.3.0-preview.1 (2026-11-12)

- Добавлено 9 P0/P1 карточек по responsive WPF, per-monitor DPI, layout pass budget, dispatcher, stale async results, virtualization, focus, shared resource tokens и thumbnail decode.
- Добавлена проверяемая Full HD/DPI QA matrix с разграничением рекомендаций и результатов приложения.
- Дополнены unit checks на WPF карточки и provenance.
- Не менялись исходники KLIDAN, не заявлен UI layout PASS.

## 0.2.0-preview.1 (2026-11-12)

- Добавлены 10 P0-карточек по WASAPI, period discovery, actual buffer readback, minimum stable profile, packet lifetime, channel mapping, MMCSS, device recovery и shutdown barrier.
- Real-time callback boundary подтверждён доступным PortAudio-первоисточником; ссылка Ross Bencina по-прежнему pending (502), её статус не повышен.
- Добавлены первоисточники Microsoft/PortAudio, контракт physical QA и проверка инвариантов каталога.
- Production код KLIDAN/Audio Probe не менялся; реальные профили устройств не заявлены проверенными.

# Changelog

## 0.1.0-preview.2 (2026-11-11)

- Initialized standalone GitHub skill repository with root `SKILL.md` and agent guidance.
- Imported all ten files from the initial `0.1.0-preview.1` package.
- Added complete upstream bibliography snapshot (115 URLs, 122 occurrences) as **unreviewed research backlog**.
- Added stronger offline integrity validation, unit/smoke tests and GitHub Actions CI.
- Added contribution workflow, provenance guidance, and reproducible Windows installation.
- No production repository files changed; no new pattern has been certified by these packaging changes.

## 0.1.0-preview.1 (2026-11-11)

- Added curated P0-P2 card collection and source provenance.
- Added a project priority matrix, offline search, and validator.
- Preserved pending review for real-time primary source and Command chapter.
- No production repository files changed.
