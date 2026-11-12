# Приоритеты исследования (2026-11-12)

Статусы: **reviewed** = проверена страница первоисточника или содержимое поискового результата; **index_only** = найдена глава/заголовок без полного изучения; **pending_primary_review** = первоисточник недоступен. Эти статусы не означают проверку текущего production-кода.

| Волна | Направление | Паттерны | Проекты | Результат |
|---|---|---|---|---|
| P0 | Управление и состояния | State, Command, Event Queue | KLIDAN, Audio Probe | Transition tables, duplicate-safe commands |
| P0 | Потоки и звук | Real-time boundary, period lattice, actual buffer readback, duplex profiles, worker stop barrier, MMCSS | KLIDAN, Audio Probe | Минимальный стабильный профиль по физическим тестам, а не фиксированные 3/10 мс |
| P0 | WPF и UI | MVVM, constraint-based layout, DPI reconciliation, Dispatcher, generation guard | KLIDAN | Full HD/DPI screenshot matrix, cancellation and focus tests |
| P0 | Хранение и восстановление | SQLite WAL/checkpoint, backup, durability, cross-store intent, recovery | KLIDAN | Fault injection and no-data-loss gates |
| P1 | Взаимодействие компонентов | IPC format/version, deadline, correlation, generation fence, poison payload | KLIDAN, Audio Probe, STAYA | Handshake/late reply tests |
| P1 | Отказоустойчивость | Bounded work, rate limits, readiness layers, failover hysteresis, staged rollback | STAYA | Offline fault injection + live route/egress QA |
| P1 | Безопасность | SSRF, admin isolation, secrets, logging redaction, artifact gates | STAYA, installers | Negative SSRF / leak / access tests |
| P1 | DevOps и обновления | Caddy validate, systemd watchdog, Compose readiness, TUF/Authenticode, update handoff, SLSA | STAYA, KLIDAN, Audio Probe | staged rollout and rollback, trust validation |
| P1 | Операторский UI и доступность | WPF AutomationPeer, critical command identity, keyboard, contrast, localization | KLIDAN | UIA/keyboard evidence, real DPI and assistive technology |
| P1 | Наблюдаемость | OpenTelemetry context, metrics cardinality, actionable alerts, stage journal | STAYA, KLIDAN, Audio Probe | evidence correlation without secret leakage |
| P2 | Производительность | Data Locality, LOH/GC, ArrayPool, cache budgets, preview coalescing | KLIDAN, Audio Probe | Hardware baseline p95/p99 and memory regression |
| P2 | Fault injection и доказательства | Fake clock, I/O crash matrix, late async results, evidence manifest | KLIDAN, Audio Probe, STAYA | Synthetic vs hardware gates, restart recovery |
| P2 | Конкурентный доступ и буферы | Bounded Channels, Pipes, Memory leases, CTS ownership, single-flight cache | KLIDAN, Audio Probe, STAYA | Race/fault injection, bounded memory and shutdown |
| P2 | Комплексные операции | Compensation, Saga | STAYA/new projects | Crash and compensation scenarios |
| P3 | Масштабирование | Cloud, Serverless, Microservices | Future projects | Only on demand |

## Дополнительные направления для следующей версии

- WASAPI/MMCSS contracts: первая документальная волна готова; следующий этап — duplex physical QA, ASIO и адаптация задержек по фактическим устройствам. См. `audio-probe-profile-contract.md`.
- WPF/DPI/UI: первая документальная волна готова; нужны реальные KLIDAN скриншоты/layout QA и аппаратные multi-monitor прогоны. См. `wpf-fullhd-dpi-contract.md`.
- SQLite/DataRoot: первая волна API и crash-recovery контракта готова; нужны физические interruption tests и code audit.
- Обновления/DevOps: документальная P1-волна готова, нужны интеграционные тесты подписей, отката и readiness; см. `devops-release-qa-contract.md`.
- STAYA IPC/reliability/security: документальная P1-волна готова; требуется аудировать точные версии 3x-ui/Xray и провести ограниченные live negative/positive tests. См. `staya-ipc-resilience-security-contract.md`.

## Принцип управления источниками

1. Сначала проверить первоисточник и версию документа.
2. Пересказать принцип своими словами; не копировать чужую книгу в скилл.
3. Указать условия применения, ограничения и цену решения.
4. Привязать сценарий тестирования и метрику.
5. Пометить источник `reviewed`, `index_only` или `pending_primary_review`.
6. Повторно проверять устаревшие технические сведения перед внедрением.

## Волна P0: WASAPI capture clock evidence (2026-11-12)

Три новых паттерна: `audio-capture-discontinuity-evidence`, `audio-clock-domain-reconciliation`, `audio-capture-packet-epoch`. Источники Microsoft Learn reviewed, сценарии proposed. Нет физического теста или production PASS. Следующая тема: проверка callback/ReleaseBuffer lifetime и реального профиля минимального стабильного буфера.

- WASAPI capture packet ownership: API DOC_REVIEW 2026-11-12; two new P0 cards and three proposed cases. Physical lease budget, actual device periods and loss flags remain unverified. See `audio-capture-buffer-contract.md`.
