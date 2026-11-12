# KLIDAN: SQLite, DataRoot и crash recovery

**Дата:** 2026-11-12. **Статус:** изученные API-контракты + предлагаемый протокол восстановления; это не проверка текущего исходного кода KLIDAN.

## Инварианты

- Canonical `data-root.json` должен быть согласован с SQLite `RootId` и marker, либо операция должна иметь **явное** pending/recoverable состояние.
- Успешный SQLite COMMIT **не** объединяет внешнюю JSON/marker запись с БД в одну транзакцию.
- Pending intent нельзя удалять, пока readback canonical+marker+DB не подтвердил target RootId.
- Старый DataRoot и данные сохраняются до прохождения verification, с отдельной политикой очистки/rollback.
- Для cross-volume, отказа доступа, занятости файла и power loss предусмотрены отдельные статусы, не скрытый reset.

## Логика восстановления (проектный протокол, не SQLite API)

1. **Discover**: read canonical config, pending intent, root marker and SQLite. Не доверять одному файлу, если остальные не согласованы.
2. **Prepare**: создать target, идентификатор target RootId и persist pending intent так, чтобы рестарт мог его обнаружить. Определить VFS/Windows persistence semantics; не обещать durability без проверки.
3. **Stage**: подготовить целевые файлы/SQLite, выполнить доступные записи и verify их содержимое, права и контрольные значения; при миграции выполнить корректный SQLite backup.
4. **Promote**: атомарную файловую замену по возможности выполнять только в документированных пределах API; для нового файла нужен отдельный create/publish протокол. Запись canonical и SQLite всё равно не образуют общую atomic transaction.
5. **Readback**: сравнить canonical RootId, marker RootId и SQLite RootId; проверить DB consistency согласно политике. Только затем очистить pending.
6. **Restart**: при наличии pending использовать state machine retry/rollback/reconcile; повторная операция с тем же target не создаёт новую пустую БД и не переписывает старую.

## Матрица fault injection

| Где сбой | Ожидаемое поведение |
|---|---|
| До pending write | Старый canonical остаётся валиден; повтор не теряет данные |
| После pending, до stage | Pending обнаруживается после restart; безопасный retry |
| После stage, до canonical publish | Целевые файлы проверяются; переход не заявляется завершённым |
| После canonical publish, до readback | Повторный запуск сверяет все RootId, не удаляет pending до проверки |
| Readback mismatch | Recovery/error state, без silent reinitialize |
| Доступ запрещён / диск полон | Fail closed, диагностика, без потери старой базы |
| Cross-volume / network path | Не утверждать atomic rename/replace; отдельный протокол копирования и сверки |
| WAL с открытыми reader | Обрабатывать SQLITE_BUSY/checkpoint partial, не делать blind .db copy |
| Crash vs OS crash vs power loss | Отдельные доказательства; `synchronous=NORMAL` не гарантирует durable commit при power loss |

## Проверки сохранности SQLite

- Для открытой базы: использовать официальное [Online Backup API](https://www.sqlite.org/backup.html) или альтернативу, а не копировать только `.db` при активном WAL.
- Проверить `PRAGMA journal_mode`, `PRAGMA synchronous`, `PRAGMA quick_check` / `integrity_check`, а отдельно `PRAGMA foreign_key_check`.
- WAL содержит sidecar `-wal` и `-shm`, его checkpoint может быть неполным при долгом чтении.
- `ReplaceFileW` требует один том для соответствующих файлов и может завершиться частичным файловым состоянием на некоторых error paths. `REPLACEFILE_WRITE_THROUGH` **не поддерживается**.

## Источники

- [SQLite WAL](https://www.sqlite.org/wal.html), [Checkpoint](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html), [Pragmas](https://www.sqlite.org/pragma.html)
- [Atomic Commit](https://www.sqlite.org/atomiccommit.html), [BEGIN transaction](https://www.sqlite.org/lang_transaction.html), [SQLite Backup](https://www.sqlite.org/backup.html)
- [Windows ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew) и [MoveFileExW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)

**Граница доказательств:** сведения выше описывают документированные гарантии и ограничения. Полный протокол intent/reconcile является инженерным предложением для проверки отдельно в KLIDAN. Отсутствуют результаты аварийных испытаний, если они не приложены в PR реализации.
