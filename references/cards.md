# Карточки паттернов

Краткий машинно читаемый оригинал: `data/patterns.json`. Ниже материал для ручного просмотра.

## state-machine | Finite State Machine / State (P0, reviewed)
**Когда:** Состояние объекта влияет на допустимые команды; набор флагов допускает невозможные комбинации.
**Решение:** Задать именованные состояния, переходы, guards, действия входа/выхода и обработку некорректных событий.
**Не применять:** Для 2 простых взаимоисключающих случаев, где достаточно enum/switch; не умножать классы без необходимости.
**Проверка:** Тест матрицы переходов, запрет недопустимых переходов, восстановление после ошибки.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://gameprogrammingpatterns.com/state.html

## command | Command / Explicit Intent (P0, index_only)
**Когда:** Действие оператора должно быть проверяемым, повторяемым или записываемым.
**Решение:** Отделить намерение и данные команды от исполнителя; контракт результата и fingerprint задавать явно.
**Не применять:** Не превращать каждую кнопку в отдельный класс без потребности; не делать команду скрытым событием.
**Проверка:** Тесты конфликта, повторения, сериализации, отмены и границ полномочий.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://gameprogrammingpatterns.com/contents.html

## event-queue | Event Queue / Temporal Decoupling (P0, reviewed)
**Когда:** Производитель не должен ждать обработчик; события приходят в разном темпе.
**Решение:** Отделить отправку от обработки очередью, описать максимальный размер, порядок, coalescing и overflow.
**Не применять:** Не использовать неограниченную очередь для real-time; не обещать ordering между независимыми producer.
**Проверка:** Нагрузка burst, overflow, shutdown, cancellation, ordering, отсутствие утечек.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://gameprogrammingpatterns.com/event-queue.html

## double-buffer | Double Buffer / Atomic Snapshot Publication (P0, reviewed)
**Когда:** Потребитель должен видеть целостную версию параметров или сцены, пока другая версия готовится.
**Решение:** Подготавливать новое состояние вне критического пути, публиковать целую версию атомарно, безопасно управлять lifetime.
**Не применять:** Не считать double buffer заменой SPSC ring buffer; не передавать ссылку на изменяемый объект.
**Проверка:** Тесты torn reads, одновременной публикации, lifetime, проверка задержки.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://gameprogrammingpatterns.com/double-buffer.html

## realtime-callback-boundary | Real-time Callback Boundary (P0, pending_primary_review)
**Когда:** Поток звука имеет жёсткий дедлайн и не должен ждать UI, сеть или файловую систему.
**Решение:** Подготовить данные заранее; в callback делать ограниченную работу без блокирующих операций; передавать управление через bounded buffers/snapshots.
**Не применять:** Не вводить lock, allocation, IO, sleep, логирование в callback без отдельного доказательства безопасности; не считать это уже проверенным текущим кодом.
**Проверка:** Измерять worst-case callback duration, underruns, исключать lifetime race, проверять устойчивость при переподключении.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.rossbencina.com/code/real-time-audio-programming-101-time-waits-for-nothing

## presentation-model | Presentation Model / Humble View (P0, reviewed)
**Когда:** Код XAML/code-behind накапливает состояние, вычисления и логику приложения.
**Решение:** Хранить состояние представления и команды отдельно; view отвечает за отображение и доступность.
**Не применять:** Не переписывать UI на MVVM ради терминологии; сохранить существующие маршруты, DPI, контракты и эффекты.
**Проверка:** VM unit tests, WPF binding/layout tests, DPI 100/125/150%, клавиатура и focus, 1920x1080.
**Проекты:** KLIDAN
**Первоисточник:** https://martinfowler.com/eaaDev/uiArchs.html, https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/

## wpf-mvvm | WPF MVVM / Observable Commands (P0, reviewed)
**Когда:** Одно и то же состояние вручную синхронизируется между несколькими WPF controls.
**Решение:** Явные observable properties, commands и bindings, с контролем потоков UI и жизненного цикла подписок.
**Не применять:** Не добавлять CommunityToolkit, если проект уже имеет эквивалентный контракт; не переносить realtime data на UI thread напрямую.
**Проверка:** Property change tests, commands CanExecute, dispatcher ownership, focus, release build.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/

## sqlite-atomic-transaction | Atomic Transaction / Crash Recovery (P0, reviewed)
**Когда:** Изменение нескольких связанных сущностей нельзя оставить наполовину завершённым.
**Решение:** Объединять согласованные изменения в транзакцию; описать границу commit, последующий readback и идемпотентный retry.
**Не применять:** Не считать SQLite-транзакцию транзакцией для файловой системы, сети или другого процесса.
**Проверка:** Fault injection до commit и после commit, повтор операции, crash-restart, инварианты.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/atomiccommit.html

## sqlite-wal | SQLite Write-Ahead Logging (P0, reviewed)
**Когда:** Требуются одновременные читатели и писатель без длительной блокировки чтения.
**Решение:** Проверить, подходит ли WAL для локального хранилища; управлять checkpoint, backup и sidecar-файлами.
**Не применять:** WAL не подходит для обычного общего доступа с разных машин через сетевой FS; не заменяет схему backup.
**Проверка:** Долгие читатели, SQLITE_BUSY, checkpoint, recovery, корректность резервной копии.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/wal.html

## idempotent-receiver | Idempotent Receiver / Duplicate Command Safety (P0, reviewed)
**Когда:** Команда может быть отправлена повторно после timeout, reconnect или retry.
**Решение:** Назначить стабильный request ID/fingerprint, записать обработку и повторно отдавать прежний результат при идентичной команде.
**Не применять:** Не путать тот же ID с изменённым payload; collision должен приводить к конфликту, не к молчаливому успеху.
**Проверка:** Повтор до ответа и после commit, duplicate same payload, conflict changed payload.
**Проекты:** KLIDAN, STAYA
**Первоисточник:** https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html, https://microservices.io/patterns/communication-style/idempotent-consumer.html

## message-correlation | Correlation Identifier / Request-Reply (P1, reviewed)
**Когда:** IPC или network reply приходит поздно, не по порядку или после cancellation.
**Решение:** Передавать request ID через всю цепь, связывать ответ с исходным запросом; отдельно проверять поколение/lifecycle.
**Не применять:** Нельзя считать correlation ID достаточным для защиты от устаревшего состояния, если тот же endpoint переоткрыт.
**Проверка:** Out-of-order replies, duplicates, late replies, cancel/reconnect, timeout.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://www.enterpriseintegrationpatterns.com/patterns/messaging/toc.html

## versioned-value | Versioned Value / Optimistic State Validity (P1, reviewed)
**Когда:** Долгая асинхронная операция может применить результат к уже изменившемуся объекту.
**Решение:** Связать результат с версией исходного состояния; принимать только при совпадении версии и владельца lifecycle.
**Не применять:** Не использовать только wall-clock timestamp; версия должна менятьcя на значимые события.
**Проверка:** Late result, reconnect, dispose, race between check and commit.
**Проекты:** KLIDAN, STAYA
**Первоисточник:** https://martinfowler.com/articles/patterns-of-distributed-systems/versioned-value.html

## retry | Bounded Retry / Backoff (P1, reviewed)
**Когда:** Внешний вызов иногда отказывает временно.
**Решение:** Классифицировать ошибки; ограничить retries и общий deadline; использовать backoff/jitter и учитывать идемпотентность.
**Не применять:** Не повторять необратимую операцию без ключа идемпотентности; не retry постоянно неисправную зависимость.
**Проверка:** Повтор при transient failure, отказ при permanent failure, max attempts/deadline, jitter.
**Проекты:** STAYA, KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/retry

## circuit-breaker | Circuit Breaker (P1, reviewed)
**Когда:** Сломанный backend вызывает каскадные ошибки или чрезмерную очередь ожидания.
**Решение:** Ввести Closed/Open/Half-Open, критерии переходов и fallback с наблюдаемыми метриками.
**Не применять:** Не применять в локальном быстром обработчике, где простая обработка ошибок достаточна.
**Проверка:** Отказ backend, recover, half-open probe, защита исправных endpoints.
**Проекты:** STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker

## bulkhead | Bulkhead / Failure Isolation (P1, reviewed)
**Когда:** Отказ или перегрузка одного компонента отнимает ресурсы у остальных.
**Решение:** Разделить ограниченные ресурсы по критичным доменам (pool, worker, queue, process).
**Не применять:** Не плодить процессы/пулы без измеримого риска; разделение расходует ресурсы.
**Проверка:** Перегрузить один домен и подтвердить работу остальных, метрики saturation.
**Проекты:** STAYA, KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead

## transactional-outbox | Transactional Outbox (P1, reviewed)
**Когда:** Изменение БД и отправка события должны быть согласованы, а broker вне транзакции БД.
**Решение:** В одной транзакции писать доменные данные и запись outbox; отдельный sender доставляет запись.
**Не применять:** Не нужен, если нет атомарной связи БД и внешней доставки; возможны дубли доставки.
**Проверка:** Crash до/после commit и publish, повтор relay, порядок событий, consumer idempotency.
**Проекты:** STAYA, KLIDAN
**Первоисточник:** https://microservices.io/patterns/data/transactional-outbox.html

## compensating-transaction | Compensating Transaction (P2, reviewed)
**Когда:** Операция изменяет несколько внешних систем без общей ACID-транзакции.
**Решение:** Определить пошаговые обратные действия и устойчивый журнал прогресса, учитывать параллельные изменения.
**Не применять:** Это не автоматический rollback; нельзя просто переписать текущее состояние старым snapshot.
**Проверка:** Отказ на каждом шаге, повтор компенсации, конкурентное изменение, operator recovery.
**Проекты:** STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction

## dirty-flag | Dirty Flag / Deferred Recompute (P2, reviewed)
**Когда:** Дорогой derived state пересчитывается при каждом изменении, хотя нужен реже.
**Решение:** При обновлении исходных данных отмечать stale; пересчитывать только при чтении, кэшировать до следующего изменения.
**Не применять:** Не делать это, если дешёвый инкрементальный update уже возможен или актуальность нужна всегда.
**Проверка:** Изменение parent/dependency, тест invalidation, benchmark, memory overhead.
**Проекты:** KLIDAN
**Первоисточник:** https://gameprogrammingpatterns.com/dirty-flag.html

## data-locality | Data Locality / Cache-Friendly Layout (P2, reviewed)
**Когда:** Большой hot loop упирается в память/cache misses.
**Решение:** После profiling рассмотреть последовательные массивы/буферы и уменьшение pointer chasing.
**Не применять:** Не делать premature SoA rewrite; профилировать на целевом железе и сравнивать.
**Проверка:** Performance benchmark, correctness compare, cache/memory regression.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://gameprogrammingpatterns.com/data-locality.html

## least-privilege | Least Privilege / Secure Defaults (P1, reviewed)
**Когда:** Инсталлятор, daemon или внешний endpoint получает больше прав, чем требуется.
**Решение:** Минимизировать права и поверхность атаки, fail-closed при сбое в проверке конфигурации.
**Не применять:** Не заменять проверку входов наличием авторизации; не хранить секреты в логах.
**Проверка:** Негативные тесты авторизации, privilege matrix, secret scan, rollback path.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html

## input-validation | Input Validation at Trust Boundary (P1, reviewed)
**Когда:** Данные поступают из JSON, IPC, UI, сети, конфигурации или миграций.
**Решение:** На границе проверять тип, длину, значения и сочетания полей; использовать SQL parameters и bounds.
**Не применять:** Не считать проверку UI достаточной; SQL parameterization не заменяется string validation.
**Проверка:** Fuzz/invalid inputs, min/max, nested data, path traversal, fail-closed error handling.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html
