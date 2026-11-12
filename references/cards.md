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

## wasapi-mode-capability-discovery | WASAPI Mode and Format Capability Discovery (P0, reviewed)
**Когда:** Устройство открывается только в части режимов, форматов, частот или схем input/output; неверный формат приводит к ложному выводу о поддержке.
**Решение:** Для каждого направления отдельно перечислять endpoint, shared/exclusive, sample rate, sample type, channels и результаты IsFormatSupported/Initialize. Сохранять ошибки и реальные параметры, не выводить поддержку из названия модели или другого endpoint.
**Не применять:** Не считать общий Windows mix format гарантией exclusive; не подменять поддержку формата результатом успешного открытия других каналов.
**Проверка:** Матрица input/output x shared/exclusive x 44.1/48 kHz x PCM16/24-in-32/Float32; проверки unsupported и device-in-use, readback параметров.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize, https://learn.microsoft.com/en-us/windows-hardware/drivers/audio/low-latency-audio

## wasapi-period-lattice | WASAPI Supported Periods, Not Fixed Milliseconds (P0, reviewed)
**Когда:** Сканер бесконечно тестирует 3 или 10 мс без учёта реальных периодов endpoint; запросы возвращают INVALID_DEVICE_PERIOD.
**Решение:** Для IAudioClient3 shared читать default/fundamental/min/max в audio frames; перечислять только кратные fundamental в допустимом диапазоне. Для legacy/exclusive использовать применимые GetDevicePeriod и фактический результат Initialize; периоды могут зависеть от формата и режима.
**Не применять:** Не переносить IAudioClient3 shared-period lattice на exclusive без оговорок; поддерживаемый period не означает устойчивую работу.
**Проверка:** Unit tests для диапазона, кратности и крайних значений; device matrix c отдельными режимами; исключить hardcoded 3/10 ms и неверные округления frames.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-getsharedmodeengineperiod, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-initializesharedaudiostream, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-getdeviceperiod

## wasapi-actual-buffer-readback | WASAPI Actual Buffer Readback and Alignment (P0, reviewed)
**Когда:** Запрошенная длительность буфера отличается от выделенной; exclusive event mode даёт BUFFER_SIZE_NOT_ALIGNED.
**Решение:** После успешной инициализации читать GetBufferSize в frames; логировать requested vs effective. При exclusive/event alignment error получать aligned frames, освобождать старый IAudioClient, создавать новый и повторять Initialize с выровненным периодом. Конвертацию frames/time выполнять с sample rate.
**Не применять:** Не вызывать повторный Initialize на том же объекте после ошибки; не считать request равным итоговому буферу; не менять формат скрытно.
**Проверка:** Fake HRESULT path для aligned retry, resource release; readback-assert frames, channels, duration, test 44.1/48 kHz.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-getbuffersize

## audio-minimum-stable-profile | Device-Specific Minimum Stable Buffer Selection (P0, reviewed)
**Когда:** Цель сканера — подобрать минимальную подтверждённую задержку конкретного устройства, а не сотни раз проверить один произвольный буфер.
**Решение:** Сначала построить множество подтверждённых поддерживаемых (mode, direction, format, rate, channels, period/buffer). Затем по возрастанию эффективного периода проводить повторяемые duplex и sustained тесты, измерять glitches, overrun/underrun, worst-case jitter и shutdown/reconnect. Выбрать самый малый вариант, который проходит заданный порог надёжности; если ни один не прошёл, вернуть NO_STABLE_PROFILE с причинами, а не фиктивный PASS.
**Не применять:** Не считать открытие stream или один короткий тест стабильностью. Не кодировать 3/5/10 ms как универсальный выбор. Не сравнивать input/output без учёта их раздельной конфигурации.
**Проверка:** Детерминированная таблица кандидатов, тест провала меньшего буфера и выбора следующего PASS, 60/300/600 s под нагрузкой по политике проекта, physical device QA. Порог PASS и длительность должны быть явно заданы, а не объявлены измеренными здесь.
**Проекты:** Audio Probe, KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-getsharedmodeengineperiod, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-getbuffersize, https://learn.microsoft.com/en-us/windows-hardware/drivers/audio/low-latency-audio

## wasapi-event-driven-io | Event-Driven Audio Buffer Service (P0, reviewed)
**Когда:** Сервис потока основан на таймере/sleep, получает нерегулярное расписание, underruns и плохую воспроизводимость.
**Решение:** Когда режим и драйвер поддерживают event callback, связать stream с event handle, обслуживать пакеты после сигнала, контролировать Start/Stop и использовать GetCurrentPadding/свободные frames для render. Правила размера пакета и period зависят от shared/exclusive.
**Не применять:** Не выдавать polling за event-driven; не применять sleep в высокоприоритетном callback; не предполагать одинаковые размер и правила в shared/exclusive.
**Проверка:** Тест последовательности SetEventHandle/Start/Stop, правильных frames per event, no buffer overrun, timeout/shutdown и сопоставление underruns с timer mode.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/coreaudio/exclusive-mode-streams, https://learn.microsoft.com/en-us/windows/win32/coreaudio/rendering-a-stream, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize

## wasapi-invalid-device-recovery | WASAPI Invalidated Endpoint Recovery (P0, reviewed)
**Когда:** USB-устройство отключили/поменяли формат; клиент продолжает читать старый endpoint или зависает при пересоздании.
**Решение:** Обрабатывать AUDCLNT_E_DEVICE_INVALIDATED, остановить операции на старом поколении, отпустить интерфейсы и заново активировать default или выбранный endpoint в зависимости от политики. Асинхронные OnSessionDisconnected уведомления не должны воскресить старый stream.
**Не применять:** Не переключать принудительно явно выбранное устройство на default без соглашения с пользователем. Не освобождать COM-ресурсы, пока рабочий поток ещё ими владеет.
**Проверка:** Disconnect/reconnect, смена default, изменение sample rate, device-in-use, stale notification, отказ активации и cleanup без утечек.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/coreaudio/recovering-from-an-invalid-device-error, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize

## mmcss-audio-thread-scope | MMCSS Scheduling with Thread-Scoped Cleanup (P0, reviewed)
**Когда:** Буферный поток не получает CPU своевременно; бездумно повышают приоритет всему процессу или забывают откатить MMCSS.
**Решение:** Регистрация конкретного audio-worker через AvSetMmThreadCharacteristics с обоснованным task (Audio/Pro Audio), обработка неуспеха, AvRevertMmThreadCharacteristics на том же потоке. Сравнить реальную производительность до/после; регистрировать на время задачи.
**Не применять:** Не считать MMCSS гарантией glitch-free; не менять registry task profile без отдельного решения; не регистрировать UI thread ради ускорения аудио.
**Проверка:** MMCSS ON/OFF A/B under CPU load, thread identity + handle lifetime, revert on all exit paths, latency/glitch counters.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/procthread/multimedia-class-scheduler-service, https://learn.microsoft.com/en-us/windows/win32/api/avrt/nf-avrt-avrevertmmthreadcharacteristics, https://learn.microsoft.com/en-us/windows/win32/coreaudio/exclusive-mode-streams

## wasapi-capture-packet-lifetime | WASAPI Capture Packet Ownership (P0, reviewed)
**Когда:** Данные захвата теряются, перемешиваются, частично копируются или используются после ReleaseBuffer.
**Решение:** Читать GetNextPacketSize/ GetBuffer, обрабатывать весь пакет или не обрабатывать, учитывать SILENT и DATA_DISCONTINUITY, копировать нужные данные в собственный ограниченный буфер до ReleaseBuffer. Вызовы GetBuffer/ReleaseBuffer выполняются парно одним потоком.
**Не применять:** Не держать указатель на WASAPI packet после ReleaseBuffer; не трактовать число frames как bytes; не делать тяжёлую обработку между GetBuffer/ReleaseBuffer.
**Проверка:** Тест длины пакета и same-thread pairing, silent/data-discontinuity, buffer empty, varying packet size, overflow policy.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/coreaudio/capturing-a-stream, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer

## audio-format-channel-map | Audio Sample Container and Channel Routing Contract (P0, reviewed)
**Когда:** На многоканальном устройстве путают mono/stereo или 24-in-32; ошибочные channel indices ведут к тишине или неверному источнику.
**Решение:** В профиле хранить отдельно capture и render channels/rates/format; валидировать container bits, valid bits, SubFormat, channel mask и block align. Маршруты описывать явно и документировать единый 0-based индекс; реальные аппаратные подписи не выводить автоматически из speaker mask.
**Не применять:** Не предполагать, что 7/8 всегда stereo на любом устройстве; не считать 24 valid bits 3-byte container при 32-bit упаковке; не использовать speaker mask как подтверждение физической коммутации.
**Проверка:** PCM16, PCM24 packed, PCM24-in-32, Float32; mono input/stereo output и stereo/stereo; boundary indices, 6+2 routing и физическая проверка каналов.
**Проекты:** Audio Probe, KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/mmreg/ns-mmreg-waveformatextensible, https://learn.microsoft.com/en-us/windows/win32/coreaudio/capturing-a-stream, https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize

## audio-stream-shutdown-barrier | Audio Worker Lifecycle and Shutdown Barrier (P0, reviewed)
**Когда:** Stop/Dispose завершается до конца callback; предыдущий поток пишет после нового старта или cleanup гоняется с IPC.
**Решение:** Явно управлять состояниями Open/Running/Stopping/Stopped/Disposed; вначале запретить новые операции, затем остановить stream и дождаться прекращения доступа worker, после этого освободить callback state/COM/IPC. Любые поздние результаты сверять с generation id.
**Не применять:** Не считать установку cancellation flag достаточным join; не освобождать память, когда callback ещё может обращаться к ней; не делать ожидание в самом callback.
**Проверка:** Fake callbacks blocked at stop, late completions, repeated Start/Stop, Stop while buffer active, cleanup exception, process exit + IPC shutdown sequence.
**Проекты:** Audio Probe, KLIDAN
**Первоисточник:** https://portaudio.com/docs/v19-doxydocs/start_stop_abort.html, https://learn.microsoft.com/en-us/windows/win32/coreaudio/recovering-from-an-invalid-device-error

## wpf-responsive-layout | WPF Constraint-Based Responsive Workspace (P0, reviewed)
**Когда:** На 1920×1080 и при масштабировании часть панели обрезается, действия уходят за край или прокрутка возникает в неправильной области.
**Решение:** Применить Grid/DockPanel с Auto/*, ограничениями Min/Max и отдельным scrolling для длинного контента. Контейнеры меняют плотность компоновки по фактическому доступному пространству в DIP. При нехватке ширины вторичные блоки сворачиваются, но критические кнопки остаются видимыми.
**Не применять:** Не рассчитывать размеры элементов из физического разрешения монитора; не оборачивать весь Operator workspace в бесконечно большой ScrollViewer. Canvas допустим для истинных координат сцены, но не как основа формы.
**Проверка:** WPF layout/screenshot матрица 1920×1080 при DPI 100/125/150%; минимальный WorkArea; контроль пересечений, видимости TAKE/Program, scroll containment, клавиатуры.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/layout, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/use-automatic-layout-overview

## wpf-per-monitor-dpi | Per-Monitor DPI and WorkArea Reconciliation (P0, reviewed)
**Когда:** Перемещение окна между мониторами меняет DPI; координаты окна или модальные диалоги оказываются вне видимой рабочей области.
**Решение:** Разделять физические пиксели и WPF DIP, учитывать активную DPI-awareness модель приложения и изменения DPI в жизненном цикле окна; размещать top-level окна относительно соответствующего monitor work area и перепроверять размеры после изменения DPI.
**Не применять:** Не считать установку manifest/per-monitor flag достаточной для всей WPF/Win32 интеграции. Не применять к геометрии сцены коэффициенты DPI повторно, если она уже задана в DIP.
**Проверка:** Перенос между 100/150% мониторами, смена primary monitor, taskbar/work area, окно после перезапуска, диалоги и owned windows, проверка координат без двойного масштаба.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/layout

## wpf-layout-pass-budget | Avoid Unnecessary Measure/Arrange Passes (P1, reviewed)
**Когда:** Перетаскивание фейдера, масштаба или панели вызывает заметные зависания при частых UpdateLayout/size changes.
**Решение:** Разделять изменения геометрии и визуального смещения. Предпочитать изменение существующего RenderTransform для частого перемещения, минимизировать LayoutTransform/UpdateLayout и глубокие повторные перестройки дерева. Измерять реальные layout passes до рефакторинга.
**Не применять:** Не заменять LayoutTransform на RenderTransform там, где новое геометрическое место необходимо окружающим элементам; не преждевременно оптимизировать простое дерево.
**Проверка:** Frame-time, layout/measure counts, drag responsiveness и visual regression на FHD/DPI; сравнение до/после.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-layout-and-design, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/layout

## wpf-dispatcher-ownership | Dispatcher Ownership and UI Thread Isolation (P0, reviewed)
**Когда:** Фоновые ADB, media discovery, device scans или audio telemetry напрямую изменяют WPF controls либо блокируют ввод.
**Решение:** Сохранять WPF DispatcherObject на UI owner thread, выполнять тяжёлую/блокирующую работу вне Dispatcher, отправлять краткие обновления через InvokeAsync, связывать lifetime операций с окном и источником. Не блокировать UI ожиданием Task.
**Не применять:** Не вызывать Task.Wait/Result на UI thread для DispatcherOperation; не выполнять real-time audio callback через UI Dispatcher; не создавать отдельный Dispatcher без необходимости.
**Проверка:** Thread-affinity assertions, fake slow backend, UI responsiveness, window close before completion, deadlock watchdog, source disconnect during queued notification.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/threading-model

## wpf-async-generation-guard | WPF Latest-Request-Wins with Generation Guard (P0, reviewed)
**Когда:** Поздний результат старого поиска/сканирования/USB-poll перезаписывает новое состояние после reconnect, выбора вкладки или Dispose.
**Решение:** Каждой операции присваивать монотонную версию, привязанную к owner/source; после await и непосредственно перед UI apply сверять generation, cancellation и disposed state. Отменять старую операцию, но не считать cancellation достаточной защитой от late completion.
**Не применять:** Не применять latest-wins для обязательных событий, где нужна последовательная обработка всех команд. Не подавлять ошибки как 'stale' до фиксации диагностической причины.
**Проверка:** Fake delayed operation A завершается после B; switch source, Dispose, dispatcher queued late delivery, повторный reconnect и соблюдение UI thread ownership.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/threading-model, https://martinfowler.com/articles/patterns-of-distributed-systems/versioned-value.html

## wpf-virtualized-list | WPF Virtualized Items and Recycling-Safe State (P1, reviewed)
**Когда:** Медиатека с тысячами элементов долго открывается, растёт память и теряется состояние раскрытых карточек при прокрутке.
**Решение:** Для подходящих ItemsControl активировать UI virtualization/recycling, не создавать контейнеры вручную, хранить item-specific state в VM/model, а не в переиспользуемом ListViewItem. Отдельно планировать data paging/virtualization, поскольку UI virtualization не загружает данные порциями.
**Не применять:** Не считать ScrollViewer вокруг ItemsControl бесплатным; не использовать UI virtualization как замену запросам по страницам; не применять без тестов к нестандартным панелям и двунаправленным спискам.
**Проверка:** Число созданных visual containers, memory/load/scroll budget на 1k/10k items, сохранение selection/expanded state, page reload, thumbnail decode.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-data-binding

## wpf-focus-scope | WPF Focus Scope and Keyboard Navigation (P1, reviewed)
**Когда:** В модальных окнах, вкладках и Operator shell теряется фокус, Tab перескакивает на скрытые элементы, hotkey срабатывает в TextBox.
**Решение:** Различать keyboard vs logical focus, явно определять focus scopes, tab order и допустимые горячие клавиши; при смене workspace восстанавливать фокус после Loaded/visibility transition и проверять реальный Keyboard.FocusedElement.
**Не применять:** Не устанавливать фокус до появления элемента в visual tree; не перехватывать клавиши глобально, когда ввод находится в редактируемом поле; не использовать IsTabStop=false как замену доступности.
**Проверка:** Tab/Shift+Tab, Enter/Escape, keyboard-only operation, focus return from dialogs, hidden/disabled controls, hotkeys while editing.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview

## wpf-shared-design-resources | WPF Shared Design Tokens and Dynamic Theme Boundaries (P1, reviewed)
**Когда:** Те же кнопки/кисти отличаются на разных экранах; изменение темы не доходит до экземпляров или создаёт множество копий тяжёлых brushes.
**Решение:** Определять общие размеры, typography, Brushes, templates на уровне Application/Window/theme dictionaries; выбирать StaticResource по умолчанию, DynamicResource только когда ресурс действительно меняется во время работы. Сохранять стабильные KLIDAN.* keys.
**Не применять:** Не переводить все ссылки на DynamicResource без измерения; не дублировать Brush в каждой карточке; не заменять существующие токены новым параллельным набором.
**Проверка:** Theme switch light/dark, runtime resource replacement, отсутствие missing resource keys, память на повторённых карточках, DPI/layout screenshots.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-application-resources

## wpf-thumbnail-decode-budget | WPF Thumbnail Decode to Display Size (P1, reviewed)
**Когда:** Медиатека декодирует полные кадры ради маленьких превью, расходует память и замедляет scroll.
**Решение:** Декодировать изображения с целевым pixel budget/DecodePixelWidth/Height по display size и DPI, ограничить конкурентное декодирование, использовать cancellation/generation guard для late thumbnails; сохранять качество для Program output отдельно.
**Не применять:** Не понижать качество Program/Preview видеосигнала ради скорости UI thumbnails; не использовать thumbnail cache без понятного лимита и инвалидизации по ревизии файла.
**Проверка:** RSS/working set, первая загрузка и быстрый scroll, смена media revision, late render after navigation, сравнение thumbnail и source pixel sizes.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging

## sqlite-cross-store-intent | Crash-Recoverable Intent Across SQLite and Filesystem (P0, reviewed)
**Когда:** DataRoot/SQLite/JSON marker должны соответствовать одному RootId после ошибки между записью файлов и обновлением БД.
**Решение:** Определить одну каноническую конфигурацию, сохранять pending intent с уникальным target RootId, готовить destination, проверять запись/readback, переключать canonical pointer, затем подтверждать повторным readback. При старте reconcile pending/canonical/DB marker по явным правилам; повторение должно быть идемпотентно.
**Не применять:** Не называть несколько операций по SQLite+JSON одной атомарной транзакцией. Не удалять старый root до проверки нового. Не считать ReplaceFileW надёжным cross-volume commit; его собственные ограничения и ошибки обрабатывать отдельно.
**Проверка:** Fault injection до и после каждого шага, zero-byte/temp/permission denied, cross-volume, inconsistent marker, retry after crash, non-admin operator, recovery without data loss.
**Проекты:** KLIDAN
**Первоисточник:** https://www.sqlite.org/atomiccommit.html, https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew, https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw

## sqlite-wal-checkpoint-control | SQLite WAL Checkpoint and Long Reader Lifecycle (P0, reviewed)
**Когда:** Файл -wal растёт, хотя изменения небольшие; медиатека держит активную read transaction и блокирует завершение checkpoint.
**Решение:** Отслеживать длительность readers, размер WAL и checkpoint progress. Проверять результат checkpoint и BUSY; планировать обслуживающую операцию вне UI критического пути. Не делать TRUNCATE при активных readers без временного бюджета и политики обработки busy.
**Не применять:** Не считать WAL бесконечно быстрым или запись действительно параллельной; в WAL одновременно один writer; не применять WAL на network filesystem без подтверждённой поддержки.
**Проверка:** Long-lived reader + writes, PASSIVE incomplete, FULL/TRUNCATE busy, release reader then successful checkpoint, UI remains responsive.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/wal.html, https://www.sqlite.org/c3ref/wal_checkpoint_v2.html

## sqlite-wal-durability-policy | WAL synchronous Mode vs Power-Loss Durability (P0, reviewed)
**Когда:** Разработчик считает любой COMMIT гарантированно сохранённым после отключения питания независимо от PRAGMA synchronous.
**Решение:** Для каждой критичности данных зафиксировать journal_mode и synchronous; WAL+FULL обеспечивает более сильную гарантию durability при power loss, чем WAL+NORMAL. Разделять приложение crash, OS crash и power loss. Readback через соединение не равнозначен физически durable commit.
**Не применять:** Не менять GLOBAL/connection PRAGMA на OFF ради ускорения без принятого риска потерь; не описывать WAL+NORMAL как защиту от потери последнего commit при power loss.
**Проверка:** Readback journal/synchronous на реальном соединении, test recovery after process termination, fault/power-loss test on controlled hardware, результат и лимиты документировать.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/pragma.html, https://www.sqlite.org/wal.html

## sqlite-online-backup | Online SQLite Backup Instead of Bare File Copy (P0, reviewed)
**Когда:** Резервная копия SQLite создаётся копированием .db при открытом WAL и потом не восстанавливается или теряет данные.
**Решение:** Для live database использовать SQLite Online Backup API или документированную альтернативу VACUUM INTO. Копию проверить отдельно: open, integrity_check, RootId, schema version, и восстановить на временном стенде; сохранять provenance и версию.
**Не применять:** Не копировать только файл .db из работающей WAL базы и не считать успешный File.Copy достаточной проверкой. Не заменять существующую активную базу без остановки клиентов и rollback plan.
**Проверка:** Backup while writer active, reopen destination, quick_check/integrity_check, restore on clean host, simulated interruption and insufficient disk.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/backup.html, https://www.sqlite.org/wal.html, https://www.sqlite.org/pragma.html

## sqlite-write-contention | SQLite Single-Writer Contention and Bounded Retry (P0, reviewed)
**Когда:** Два процесса/модуля пишут одновременно, виден SQLITE_BUSY, бесконечный retry в UI или зависшая транзакция.
**Решение:** Уточнить boundary ownership и BEGIN DEFERRED/IMMEDIATE, использовать ограниченный busy_timeout/backoff с cancellation вне UI, корректно откатывать и повторять полную идемпотентную операцию. Диагностировать долгие readers, writers и locks.
**Не применять:** Не считать WAL многопишущим; не повторять частично выполненную side-effect операцию без idempotency key; не держать write transaction во время сети/длинного сканирования.
**Проверка:** Two concurrent writers, busy on BEGIN IMMEDIATE, timeout→recoverable error, cancellation, retry duplicate fingerprint, no UI freeze.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/lang_transaction.html, https://www.sqlite.org/rescode.html, https://www.sqlite.org/wal.html

## sqlite-foreign-keys-per-connection | Foreign Key Enforcement Per SQLite Connection (P1, reviewed)
**Когда:** Схема содержит FOREIGN KEY, но дочерние записи-сироты появляются через новый connection pool/тестовый процесс.
**Решение:** На каждом новом соединении включить PRAGMA foreign_keys=ON вне активной транзакции, прочитать back, проверять foreign_key_check при миграциях; считать настройку connection-scoped.
**Не применять:** Не предполагать, что наличие FOREIGN KEY в DDL гарантирует runtime enforcement; не переключать PRAGMA после BEGIN в надежде немедленно включить.
**Проверка:** Новый pooled/non-pooled connection, insert orphan must fail, migration creates no orphan, foreign_key_check empty.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/foreignkeys.html, https://www.sqlite.org/pragma.html

## sqlite-integrity-recovery-gate | SQLite Integrity and Recovery Gate Before Promotion (P0, reviewed)
**Когда:** После копирования/аварии найден файл БД, но приложение сразу назначает его рабочим без верификации.
**Решение:** Перед признанием нового DataRoot/backup рабочим проверить открытие, PRAGMA quick_check/integrity_check, отдельно foreign_key_check и прикладной RootId/schema marker. При ошибке сохранить старое состояние и предоставить диагностируемый режим recovery.
**Не применять:** Не считать quick_check полным эквивалентом integrity_check; integrity_check не выявляет FK errors. Не выполнять тяжёлую проверку в UI Dispatcher.
**Проверка:** Known corrupt file, broken FK, mismatched RootId, clean backup, fault at readback, untrusted path and access denied; no silent overwrite.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/pragma.html, https://www.sqlite.org/backup.html

## sqlite-savepoint-nested-work | SQLite SAVEPOINT Scope Is Not an Independent Commit (P1, reviewed)
**Когда:** Внутренний сервис делает RELEASE savepoint, а затем внешняя операция откатывает всю транзакцию, хотя сервис считал изменения надёжно сохранёнными.
**Решение:** Использовать SAVEPOINT для локального отката фрагмента внутри одной транзакции; считать надёжным завершением только внешний COMMIT. Документировать владельца transaction и границы state/lifetime.
**Не применять:** Не выдавать RELEASE внутреннего savepoint за durable commit, не смешивать с отдельными filesystem mutations без recovery protocol.
**Проверка:** Inner RELEASE then outer ROLLBACK, nested retry, ROLLBACK TO continuation and COMMIT, injected exception across service boundaries.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://www.sqlite.org/lang_savepoint.html, https://www.sqlite.org/lang_transaction.html

