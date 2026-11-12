# Приоритеты исследования (2026-11-12)

Статусы: **reviewed** = проверена страница первоисточника или содержимое поискового результата; **index_only** = найдена глава/заголовок без полного изучения; **pending_primary_review** = первоисточник недоступен. Эти статусы не означают проверку текущего production-кода.

| Волна | Направление | Паттерны | Проекты | Результат |
|---|---|---|---|---|
| P0 | Управление и состояния | State, Command, Event Queue | KLIDAN, Audio Probe | Transition tables, duplicate-safe commands |
| P0 | Потоки и звук | Real-time boundary, period lattice, actual buffer readback, duplex profiles, worker stop barrier, MMCSS | KLIDAN, Audio Probe | Минимальный стабильный профиль по физическим тестам, а не фиксированные 3/10 мс |
| P0 | WPF и UI | MVVM, Presentation Model, Humble View | KLIDAN | State isolation, layout tests |
| P0 | Хранение и восстановление | SQLite transactions, WAL, idempotency | KLIDAN | Crash/retry tests, backup checks |
| P1 | Взаимодействие компонентов | Correlation ID, Versioned Value, Outbox | KLIDAN, STAYA | Late responses, IPC/reconnect tests |
| P1 | Отказоустойчивость | Retry, Circuit Breaker, Bulkhead | STAYA | Failover and recovery tests |
| P1 | Безопасность | Secure defaults, least privilege, validation | STAYA, installers | Negative tests |
| P2 | Производительность | Dirty Flag, Data Locality | KLIDAN | Measured benchmark improvements |
| P2 | Комплексные операции | Compensation, Saga | STAYA/new projects | Crash and compensation scenarios |
| P3 | Масштабирование | Cloud, Serverless, Microservices | Future projects | Only on demand |

## Дополнительные направления для следующей версии

- WASAPI/MMCSS contracts: первая документальная волна готова; следующий этап — duplex physical QA, ASIO и адаптация задержек по фактическим устройствам. См. `audio-probe-profile-contract.md`.
- WPF layout и DPI, focus, accessibility: конкретные Microsoft рекомендации и реальные capture/layout tests.
- Договоры обновления приложений, signed installer, rollback и сохранение настроек.
- Security design, secrets, multi-stage deployment для STAYA.

## Принцип управления источниками

1. Сначала проверить первоисточник и версию документа.
2. Пересказать принцип своими словами; не копировать чужую книгу в скилл.
3. Указать условия применения, ограничения и цену решения.
4. Привязать сценарий тестирования и метрику.
5. Пометить источник `reviewed`, `index_only` или `pending_primary_review`.
6. Повторно проверять устаревшие технические сведения перед внедрением.
