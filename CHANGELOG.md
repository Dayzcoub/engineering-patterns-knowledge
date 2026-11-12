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
