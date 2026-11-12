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

## ipc-request-deadline | Request–Reply Deadline and Expired Reply (P1, reviewed)
**Когда:** Поздний IPC/HTTP ответ приходит после timeout, а pending операции не освобождаются.
**Решение:** Задать end-to-end deadline, correlation ID и явные TIMEOUT/CANCELLED; после deadline не применять ответ. Делить общий бюджет между retry/parse/apply.
**Не применять:** Не считать cancellation остановкой remote side-effect; без idempotency повтор опасен.
**Проверка:** Fake late reply, timeout budget, correlation mismatch, no pending leak.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://www.enterpriseintegrationpatterns.com/patterns/messaging/RequestReply.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageExpiration.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/CorrelationIdentifier.html

## ipc-protocol-format-guard | Explicit Protocol Version / Format Indicator (P1, reviewed)
**Когда:** Worker и клиент разной версии иначе толкуют поля, а HELLO не несёт protocol.
**Решение:** Начинать с handshake version и capability flags; обязательные поля валидировать, unknown optional трактовать по контракту; несовместимость = PROTOCOL_VERSION.
**Не применять:** Version match не заменяет строгую проверку payload; optional полям нельзя произвольно ломать compatibility.
**Проверка:** Missing/incorrect protocol, old/new peer, optional fields omitted, correlated ERROR.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://www.enterpriseintegrationpatterns.com/patterns/messaging/FormatIndicator.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/RequestReply.html

## ipc-generation-fence | Generation Fence for Stale Worker Results (P1, reviewed)
**Когда:** Старый worker или source возвращает результаты после reconnect/перезапуска.
**Решение:** Связывать запрос с owner generation и сверять непосредственно перед apply. Для распределённого leader использовать persistent term/fencing у получателя.
**Не применять:** Local counter не равен global consensus; wall-clock timestamp не fencing.
**Проверка:** Old A completes after B, restart, late notify and stale leader term rejected.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://martinfowler.com/articles/patterns-of-distributed-systems/generation-clock.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/CorrelationIdentifier.html

## ipc-invalid-payload-quarantine | Invalid Message Channel / Quarantine (P1, reviewed)
**Когда:** Malformed subscription/IPC packet повторно запускает бесполезный обработчик.
**Решение:** Разделить permanent schema error и transient failure; сохранять bounded redacted diagnostic с code/hash, не автоматически повторять poison payload.
**Не применять:** Не хранить token, raw URL, body, private keys в журнале; broker не нужен для простого sync IPC.
**Проверка:** Malformed/oversized/unknown version, no retry loop, no secret in logs.
**Проекты:** STAYA, Audio Probe, KLIDAN
**Первоисточник:** https://www.enterpriseintegrationpatterns.com/patterns/messaging/InvalidMessageChannel.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html, https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

## bounded-upstream-work-backpressure | Bounded Work Queue and Backpressure (P1, reviewed)
**Когда:** При burst запросов и health probes растут memory, concurrency и задержки.
**Решение:** Задать max in-flight, bounded queue, overflow/reject/coalesce policy и fairness; контролировать queue age и cancelled work.
**Не применять:** Не вводить message broker без потребности; не терять обязательные команды молча.
**Проверка:** 100x burst, queue overflow, bounded memory, cancellation and shutdown.
**Проекты:** STAYA, KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling, https://learn.microsoft.com/en-us/azure/architecture/patterns/rate-limiting-pattern

## staya-active-path-health | Process vs Public Endpoint vs End-to-End Health (P1, reviewed)
**Когда:** systemd active или 200 не доказывает, что публичный URL и реальный egress работают.
**Решение:** Разделить process/listener, local API, public host+path, content и end-to-end; каждому probe свой scope, timeout, права и диагностика.
**Не применять:** 404 legacy/root не равен отказу нужного пути; HTTP 200 не доказывает VPN-транспорт.
**Проверка:** Correct public path, active process with failed route, TLS mismatch, stale output, E2E failure.
**Проекты:** STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring, https://caddyserver.com/docs/api, https://caddyserver.com/docs/caddyfile/matchers

## staya-client-rate-limit | Per-Upstream Rate Limit and Retry-After Budget (P1, reviewed)
**Когда:** Параллельный fetch подписок создаёт 429/503 и шторм повторов.
**Решение:** Устанавливать per-upstream rate/concurrency, bounded attempts и общий deadline; учитывать допустимый Retry-After, добавлять jitter.
**Не применять:** Не retry 400/401/403 или invalid schema; не обходить rate limit обходным host.
**Проверка:** 429 Retry-After, 503 burst, 401 fail closed, retry budget exhaustion.
**Проекты:** STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/rate-limiting-pattern, https://learn.microsoft.com/en-us/azure/architecture/patterns/retry

## staya-failover-hysteresis | Failover Hysteresis and Recovery Probe (P1, reviewed)
**Когда:** Ноды flapping от краткого ping failure; stale health оставляет умерший upstream.
**Решение:** Раздельно readiness/performance, пороги переходов, cooldown, half-open probes и TTL health. Проверить реальную способность текущего алгоритма Xray.
**Не применять:** leastLoad сам по себе не доказывает health-based failover; не принимать решение по одному ping.
**Проверка:** One transient loss, repeated failures, cooldown, recovery and all-down scenario.
**Проекты:** STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker, https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring

## staya-subscription-ssrf-boundary | Untrusted Subscription URL / SSRF Boundary (P1, reviewed)
**Когда:** Панель загружает URL внешней подписки, способный вести на loopback, LAN или metadata endpoint.
**Решение:** Разрешать policy schemes/hosts, запрещать private/link-local/metadata targets, контролировать DNS resolution, redirects и egress. Проверять адрес на каждом redirect.
**Не применять:** Строковый prefix или https не доказывают безопасность; не давать fetch доступ к admin socket.
**Проверка:** 127.0.0.1, ::1, link-local, RFC1918, redirect, DNS rebinding, URL userinfo.
**Проекты:** STAYA
**Первоисточник:** https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

## staya-subscription-normalization | Canonical Subscription Merge with Provenance (P1, reviewed)
**Когда:** Внешние и локальные ноды конфликтуют по name/tag/id; результат зависит от порядка.
**Решение:** Нормализовать в каноническую схему с source namespace; задать deterministic collision policy/sorting, validate output. Сохранить отдельные direct fixed-IP и GLOBAL AUTO entries.
**Не применять:** Не отправлять secret URI в logs; не помещать direct nodes в AUTO по умолчанию.
**Проверка:** Source reorder, duplicate ID, malformed tag, empty source, direct retained, client parsing.
**Проекты:** STAYA
**Первоисточник:** https://www.enterpriseintegrationpatterns.com/patterns/messaging/Normalizer.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/CanonicalDataModel.html, https://www.enterpriseintegrationpatterns.com/patterns/messaging/ContentBasedRouter.html

## staya-public-route-contract | Reverse-Proxy Route as Public API Contract (P1, reviewed)
**Когда:** Local /json/ может быть 404, но public /json-global/ корректен; агент объявляет ложный отказ.
**Решение:** Описать exact public host+path, proxy matcher, strip/rewrite, expected status/content. Проверять публичный endpoint без раскрытия токена.
**Не применять:** Не тестировать root вместо target; не расширять matcher до admin API.
**Проверка:** Exact route vs legacy, trailing slash, TLS/host, content validation, no admin exposure.
**Проекты:** STAYA
**Первоисточник:** https://caddyserver.com/docs/caddyfile/matchers, https://caddyserver.com/docs/caddyfile/directives/handle_path, https://caddyserver.com/docs/api

## staya-staged-config-promotion | Preflight–Stage–Promote–Verify–Rollback (P1, reviewed)
**Когда:** Новую конфигурацию публикуют до теста и теряют рабочий Xray/Caddy.
**Решение:** Кандидат + digest + backup, xray run -test preflight, staged update, active listener/public-route/E2E smoke. Отказ → documented per-service rollback and verify.
**Не применять:** Caddy /load rollback не атомарен с Xray/3x-ui; parser PASS не значит REALITY/TLS PASS.
**Проверка:** Invalid candidate, partial deploy, post-restart failure, digest mismatch, rollback probes.
**Проекты:** STAYA
**Первоисточник:** https://github.com/XTLS/Xray-core/blob/c456141815359e1d2c00dfc673f5f26adf22fae2/main/run.go, https://caddyserver.com/docs/api, https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html

## staya-admin-api-isolation | Administrative Control Plane Isolation (P1, reviewed)
**Когда:** Admin API доступен извне из-за wildcard proxy или listener binding.
**Решение:** Отделить data/control plane, loopback/permissioned socket и ACL, независимую авторизацию и запрещающие маршруты.
**Не применять:** Одного URL path недостаточно, когда admin listener уже открыт на публичном интерфейсе.
**Проверка:** External anonymous GET/POST denied, local privileged allowed, firewall/binding verification.
**Проекты:** STAYA
**Первоисточник:** https://caddyserver.com/docs/api, https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html

## staya-secret-lifecycle | Secret Inventory, Rotation and Redaction (P1, reviewed)
**Когда:** Токены, ключи, конфиги попали в Git, logs, backup или stdout.
**Решение:** Вести secret inventory, owner/access scope, rotation/revoke plan, encrypted storage, rights on backup, redact before logging; сохранить действующую SOPS/age policy.
**Не применять:** UI-only mask не защищает stderr/console/history; не вставлять production credential в tests.
**Проверка:** Canary leak scan, rotation rehearsal, permissions, old token revoked, clean report.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html

## security-structured-event-redaction | Structured Security Events without Token Leakage (P1, reviewed)
**Когда:** Отладка требует correlation, но печатает raw subscription URL или secret JSON.
**Решение:** Event code, component, safe ID, phase/status/reason, timestamp; redact sensitive data before sinks, escape newline, control access.
**Не применять:** Не удалять audit trail целиком; не рассчитывать только на post-processing scrub.
**Проверка:** Canary token absent in stdout/stderr/artifacts, newline injection test, useful correlation.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

## secure-deploy-artifact-gate | Trusted Artifact and Protected Deployment Gate (P1, reviewed)
**Когда:** На сервер отправляют бинарник без привязки к source SHA, artifact digest и approval.
**Решение:** Проверять artifact digest и подпись у доверенного независимого источника, фиксировать source commit, preflight, deployment approval и rollback pointer.
**Не применять:** SHA от того же недоверенного источника не authentication; подпись не доказывает отсутствие уязвимостей.
**Проверка:** Tamper, untrusted manifest, incorrect SHA, unauthorized deploy, rollback verification.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html, https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

## config-caddy-validate-reload | Caddy Adapt, Validate, Reload and Runtime Verification (P1, reviewed)
**Когда:** При обновлении Caddy конфиг адаптируется без ошибки, но ещё не проверен на provisioning и реальный public route.
**Решение:** Сохранять исходную версию и digest; отдельно выполнять adapt, validate в совместимом окружении, reload через API; затем проверить exact host+path, TLS и ожидаемый ответ.
**Не применять:** Не приравнивать adapt к validate и reload к проверке сетевого маршрута; validate может не пройти из-за ресурсов, занятых работающим инстансом.
**Проверка:** Недопустимый Caddyfile, valid JSON с provisioning failure, ошибочный публичный matcher, rollback после неуспешного reload.
**Проекты:** STAYA
**Первоисточник:** https://caddyserver.com/docs/command-line, https://caddyserver.com/docs/api

## systemd-restart-watchdog | systemd Restart Budget and Service Readiness (P1, reviewed)
**Когда:** Упавшая нода непрерывно перезапускается или systemd показывает active до готовности Xray.
**Решение:** Определить Type, ExecStartPre, Restart/RestartSec, лимиты старта, timeout и при поддержке приложения watchdog/READY notification; проверить состояние listener и transport отдельно.
**Не применять:** Не выставлять Type=notify без реализации sd_notify в приложении; Restart=always не лечит неверную конфигурацию; ExecStartPre не для фоновых daemon.
**Проверка:** Crash loop, invalid config, watchdog missed, manual stop, slow startup, StartLimit, failure recovery.
**Проекты:** STAYA
**Первоисточник:** https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html, https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html

## compose-health-dependency | Compose Dependency Health Gate (P1, reviewed)
**Когда:** Compose запускает приложение до готовности DNS, базы или proxy; зависимый контейнер ошибается сразу после старта.
**Решение:** Настроить healthcheck и depends_on: condition service_healthy только там, где нужна readiness; отдельно проверить recovery после restart и обновления зависимого сервиса.
**Не применять:** Короткий depends_on гарантирует лишь startup order; healthcheck одного контейнера не доказывает end-to-end работу; не добавлять Compose для одного простого systemd daemon.
**Проверка:** Delayed dependency, failed healthcheck, manual restart, container crash, readiness vs liveness.
**Проекты:** STAYA
**Первоисточник:** https://docs.docker.com/compose/how-tos/startup-order, https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks?view=aspnetcore-10.0

## container-immutable-build | Immutable Container Image and Digest Pinning (P1, reviewed)
**Когда:** Деплой повторно скачивает latest, версия меняется без фиксации коммита и откат становится невоспроизводимым.
**Решение:** Использовать доверенный base и pinned digest там, где требуется воспроизводимость; build artifact связывать с source commit, регулярно обновлять pin с тестами; сокращать runtime image и privileges.
**Не применять:** Digest pin не гарантирует отсутствие CVE; нельзя навечно замораживать старый образ; checksum из того же недоверенного источника не удостоверение.
**Проверка:** Rebuild/rollback по exact image digest, malicious tag move, reproducibility, scan and update policy.
**Проекты:** STAYA
**Первоисточник:** https://docs.docker.com/build/building/best-practices/, https://slsa.dev/spec/v1.2/

## sops-multi-recipient-recovery | SOPS/age Multi-Recipient Secret Recovery (P1, reviewed)
**Когда:** Операции с зашифрованным конфигом блокируются после смены ключа/утраты одного получателя или секрет появляется в артефактах.
**Решение:** Описать и сверять SOPS policy/age recipients, тестировать decrypt каждым авторизованным путём, иметь revocation/rotation procedure и offline recovery, без plaintext в Git/QA.
**Не применять:** Наличие второго recipient не заменяет контролируемое хранение private key; ни один PR не должен раскрывать ключи или реальную подписку.
**Проверка:** Synthetic encrypted fixture, lost-key simulation, recipient rotation, rejected unauthorized decrypt, secret scan.
**Проекты:** STAYA
**Первоисточник:** https://github.com/getsops/sops

## observability-context-propagation | Trace Context Across IPC and Deploy Stages (P1, reviewed)
**Когда:** Ошибка проходит через несколько процессов/этапов, а независимые журналы нельзя связать с исходной операцией.
**Решение:** Передавать безопасный trace/correlation context через границы IPC, HTTP, worker и этапы deployment; чётко определять parent/child, retry attempt, generation и security boundary.
**Не применять:** Не включать секретные headers, full subscription URL, personal data или untrusted baggage в spans; не создавать distributed tracing для одномодульного локального действия без пользы.
**Проверка:** Same trace across stages, new span per retry, late reply rejection, no cross-user leak in baggage, missing context fallback.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://opentelemetry.io/docs/concepts/context-propagation/, https://opentelemetry.io/docs/concepts/signals/traces/

## observability-bounded-cardinality | Low-Cardinality Metrics and Defined Units (P1, reviewed)
**Когда:** Теги метрик содержат user ID, device serial или request ID и количество временных рядов растёт.
**Решение:** Определять ограниченные labels с явным смыслом, базовые units, счётчики ошибок и гистограммы latency; идентификаторы операций оставлять в logs/traces, но не metric labels.
**Не применять:** Нельзя ставить токены, endpoint IDs, URL, произвольные исключения и безлимитные значения в labels.
**Проверка:** Unique time series budget, large synthetic ID set, unit correctness, counter/gauge boundaries.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://prometheus.io/docs/practices/naming/, https://opentelemetry.io/docs/concepts/signals/metrics/, https://opentelemetry.io/docs/concepts/semantic-conventions/

## observability-actionable-alerts | Symptom-Based Alerts With Runbook Actions (P1, reviewed)
**Когда:** Каждый restart или одиночная 404 создаёт шум, реальная недоступность не выявляется.
**Решение:** Оповещать по измеримому влиянию на пользовательский сценарий, поддерживать уровни warning/critical и runbook со scope, условиями отключения и подтверждением восстановления.
**Не применять:** Не отправлять срочные оповещения по несущественным событиям, не считать 404 legacy route отказом подписки.
**Проверка:** Simulated prolonged outage alerts, transient recovery no page, correct route, alert dedup and runbook link.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://prometheus.io/docs/practices/alerting/, https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks?view=aspnetcore-10.0

## deployment-stage-journal | Immutable Stage Journal and Failure Evidence (P1, reviewed)
**Когда:** Сборка, установка и live smoke выводят PASS без привязки к конкретному source SHA или архивам; поздний этап переписывает статус раннего.
**Решение:** Записывать runId, sourceSha, artifact digest, stage, start/end, exit, structured error и scope каждого перехода. Неизвестный stage при отказе = UNKNOWN/PENDING; не переписывать старые свидетельства.
**Не применять:** Не записывать сырые секреты в journal; единый JSON не гарантирует durable write после power loss; фиксация процесса не равна фактическому smoke.
**Проверка:** Crash midway, missing stage, hash mismatch, partial failure, log redaction, restart readback and immutable run history.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://slsa.dev/spec/v1.2/, https://opentelemetry.io/docs/concepts/semantic-conventions/

## update-tuf-antirollback | Signed Update Metadata and Rollback/Freeze Protection (P0, reviewed)
**Когда:** Клиент доверяет beta.json только по HTTPS и hash, что допускает устаревшую/подменённую метаинформацию при компрометации источника.
**Решение:** Изучить и при необходимости внедрить TUF-подобные роли root/targets/snapshot/timestamp с доверенными ключами, version counters, expiry and rollback protection; идентифицировать target по размеру и digest.
**Не применять:** Не объявлять собственный JSON feed совместимым с TUF без полноценной реализации клиента/репозитория; не считать один SHA от того же канала аутентификацией.
**Проверка:** Old signed metadata replay, expired timestamp, changed target digest, missing trust anchor, key rotation and rollback policy.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://theupdateframework.github.io/specification/latest/, https://docs.sigstore.dev/cosign/verifying/verify/

## update-publisher-signature-policy | Authenticode Publisher and Chain Policy (P0, reviewed)
**Когда:** Установщик подписан self-signed сертификатом, а агент ошибочно объявляет его доверенным для чужой машины.
**Решение:** На Windows проверять WinVerifyTrust/Authenticode по соответствующей политике, доверенную цепочку и ожидаемую идентичность издателя; подписанный test artifact отличать от publicly trusted production signer.
**Не применять:** Хеш SHA-256 и наличие подписи не равны доверенному издателю; отключать SmartScreen/Defender ради PASS нельзя.
**Проверка:** Unsigned, tampered, wrong publisher, expired/revoked chain per policy, self-signed trust failure on clean Windows.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-winverifytrust

## windows-msi-custom-rollback | MSI Deferred Custom Action with Compensating Rollback (P1, reviewed)
**Когда:** Установочный custom action меняет сервисы и внешние файлы, после сбоя Windows Installer не восстанавливает их.
**Решение:** Для MSI custom action, меняющих состояние системы, использовать deferred execution с соответствующими rollback actions и сценариями частичной ошибки, версионированные бэкапы и последующую проверку.
**Не применять:** Это только для Windows Installer/MSI; для Inno Setup/NSIS иной механизм; встроенный rollback MSI не покрывает все сторонние side effects.
**Проверка:** Abort during custom action, rollback disabled, partial filesystem state, service install failure, non-admin account.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/msi/rollback-custom-actions, https://learn.microsoft.com/en-us/windows/win32/msi/deferred-execution-custom-actions, https://learn.microsoft.com/en-us/windows/win32/msi/rollback-installation

## update-worker-handoff | Updater Process Lifetime and File-Promotion Barrier (P0, reviewed)
**Когда:** Updater пытается заменить запущенный бинарник и теряет состояние при отмене/kill; модули продолжают писать в DataRoot.
**Решение:** До замены запретить новые операции, дождаться завершения worker и освобождения файлов, верифицировать candidate; публиковать файлы по правилам Windows API с journal и restart smoke, затем только удалять backup.
**Не применять:** Не считать замену нескольких файлов одной транзакцией; ReplaceFileW имеет ограничения same-volume и error cases, а installer backend может обладать другими возможностями.
**Проверка:** Locked exe, updater crash, partial promotion, failed startup, alternate DataRoot, repeated update and rollback.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew, https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw, https://learn.microsoft.com/en-us/windows/win32/msi/rollback-installation

## supplychain-provenance-verification | Build Provenance and Artifact Identity Verification (P1, reviewed)
**Когда:** Выпущен артефакт с корректным размером и SHA, но нет уверенности, из какого commit и доверенной среды его собрали.
**Решение:** Вести provenance/source reference, identity build environment, immutable artifact digest и проверяемую подпись/attestation при требуемом threat model; отделять test signer от production.
**Не применять:** Не присваивать SLSA Level по одному файлу provenance; аттестацию нужно проверять против доверенной личности сборщика, а не просто хранить.
**Проверка:** Wrong commit/digest, forged attestation, untrusted identity, runtime match and release record.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://slsa.dev/spec/v1.2/, https://docs.sigstore.dev/cosign/verifying/verify/

## deployment-approval-gate | Environment Approval and Scoped Deployment Secrets (P1, reviewed)
**Когда:** CI job с правом publish запускается из незащищённой ветки или unreviewed PR и получает production secrets.
**Решение:** Использовать GitHub environments, ограничение веток и approvals согласно доступности плана, минимальные permissions, отдельные secrets и staged promotion; проверять фактическую политику.
**Не применять:** Environment без настроенных protection rules не является автоматическим approval; не считать ручной запуск безопасным без проверки actor/branch/artifact.
**Проверка:** Untrusted branch cannot deploy, rejection before secrets, allowed reviewer approval, restart and revoke.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments, https://slsa.dev/spec/v1.2/

## progressive-release-acceptance | Progressive Release and Post-Deploy Acceptance Gate (P1, reviewed)
**Когда:** Один тестовый узел прошёл проверку, затем обновление публикуется всем клиентам без контроля состояния.
**Решение:** Продвигать staging→canary→wider rollout с фиксированными критериями: источник, installed version, update feed, new sessions, critical operations, rollback/stop rules; учитывать размер группы и доступные tester devices.
**Не применять:** Не обещать автоматическую canary процедуру без telemetry и клиентов; PASS из одного process-start не равен release success.
**Проверка:** Canary failure blocks wider release, signed payload mismatch, updater rollback, stale feed, stop condition triggers.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments, https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks?view=aspnetcore-10.0, https://prometheus.io/docs/practices/alerting/

## bounded-channel-overflow-policy | Bounded Channel Overflow Policy (P2, reviewed)
**Когда:** Preview and telemetry producers overrun slower consumers.
**Решение:** Bound capacity; choose Wait/DropNewest/DropOldest/DropWrite only after defining loss, order and backpressure.
**Не применять:** Never drop operator commands, storage commits or audio samples; Wait is not safe inside a realtime callback.
**Проверка:** Burst, overflow, ordering, shutdown, max memory.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/core/extensions/channels

## pooled-buffer-ownership | ArrayPool Buffer Ownership (P2, reviewed)
**Когда:** Frequent byte buffers increase allocations or reuse races.
**Решение:** Rent at least required size, track valid length, Return once to same pool after last consumer completes.
**Не применять:** Never access returned buffer or assume its capacity equals request; pooling does not automatically make callbacks safe.
**Проверка:** Double Return, use-after-return, exception and cancel paths.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1.rent, https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1.return, https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/memory-t-usage-guidelines

## pooled-sensitive-buffer-clearing | Pool Secret Data Clearing (P2, reviewed)
**Когда:** Rented buffer contains data from another user/session.
**Решение:** Clear sensitive bytes under defined policy, return buffers with clearArray where appropriate; ensure downstream no stale data.
**Не применять:** Do not assume Rent returns zeroed memory or that clearing only UI logs protects secrets.
**Проверка:** Canary secret reuse, no stale tail, exception cleanup.
**Проекты:** STAYA, KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1.return, https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1.rent

## large-object-heap-budget | Large Object Heap Pressure Budget (P2, reviewed)
**Когда:** Decoded frames and large arrays cause GC pauses.
**Решение:** Measure allocations, LOH, pause distribution and resident memory on actual runtime; prefer bounded reuse only with a regression baseline.
**Не применять:** Do not assume an LOH threshold or workaround solves every runtime; no premature pooling.
**Проверка:** 1080p frame load, LOH growth, GC pauses, long soak.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/large-object-heap, https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/performance, https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters

## span-memory-lifetime | Span/Memory Ownership and Lifetime (P2, reviewed)
**Когда:** Async decoder uses memory after owner or pool lease ends.
**Решение:** Use Span in synchronous scope; Memory across appropriate async boundaries; track lease and ownership, copy before releasing upstream packet.
**Не применять:** ReadOnlyMemory does not freeze backing store; never retain memory after owner disposal.
**Проверка:** Async delay, lease return, concurrent mutation, slice limits.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/memory-t-usage-guidelines

## pipeline-backpressure-advance | PipeReader Progress and Backpressure (P2, reviewed)
**Когда:** Stream parser retains bytes or grows buffers without bound.
**Решение:** Use PipeReader consumed/examined AdvanceTo correctly; configure pause/resume thresholds, Complete both ends on shutdown.
**Не применять:** Not a substitute for audio ring buffer; avoid complexity for short simple strings.
**Проверка:** Fragmented input, malformed frames, pause, cancellation, bounded memory.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/standard/io/pipelines

## concurrent-getoradd-side-effect | Concurrent GetOrAdd Factory Is Not Once (P2, reviewed)
**Когда:** Concurrent misses start same expensive worker more than once.
**Решение:** Remember GetOrAdd valueFactory can run multiple times outside dictionary locks; separate side effects from insertion.
**Не применять:** Dictionary entry is atomic, delegate execution is not exactly-once.
**Проверка:** Multiple same-key tasks, factory invocations, one stored entry, cancellation.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent.concurrentdictionary-2.getoradd

## cache-single-flight | Per-Key Single-Flight Loader (P2, reviewed)
**Когда:** Duplicate thumbnail metadata loads flood the decoder.
**Решение:** Use shared in-flight load per key with explicit failure eviction and independent caller cancellation rules.
**Не применять:** Do not let one caller cancellation silently abort all users; never apply to non-idempotent commands without contract.
**Проверка:** Ten same-key requests, one load, failures retried, one caller cancels.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent.concurrentdictionary-2.getoradd, https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory

## cache-size-revision-budget | Cache Size, TTL and Revision Keys (P2, reviewed)
**Когда:** Cache consumes unbounded memory or shows stale thumbnails.
**Решение:** Use identity+revision key, size budget with defined unit, TTL/eviction and authoritative fallback; invalidate on media revision.
**Не применять:** Do not assume IMemoryCache self-limits under system memory pressure; avoid arbitrary unbounded URL keys.
**Проверка:** 10k unique entries bounded, file revision, expiry, fallback.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging

## reader-writer-critical-section | Reader/Writer Critical-Section Ownership (P2, reviewed)
**Когда:** Shared mutable model blocks readers or writer progress.
**Решение:** Measure contention; use short read/write scopes and correct upgrade/thread ownership where justified.
**Не применять:** Never await while holding ReaderWriterLockSlim; never lock realtime audio callback.
**Проверка:** Concurrent readers/writer, upgrade tests, exception cleanup, writer progress.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-threading-readerwriterlockslim

## cancellation-source-lifecycle | Cancel/Join/Dispose Lifetime Barrier (P0, reviewed)
**Когда:** CTS disposed while worker still reads token or publishes late result.
**Решение:** Signal cooperative cancellation, await worker/join, then dispose source; use generation guard at apply boundary.
**Не применять:** Dispose is not Cancel, and Cancel alone does not join running worker.
**Проверка:** Cancel during I/O, Dispose race, late results, repeat shutdown.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/api/system.threading.cancellationtokensource, https://learn.microsoft.com/en-us/dotnet/api/system.threading.cancellationtokensource.dispose

## performance-baseline-budget | Profiling Before Optimization Budget (P2, reviewed)
**Когда:** Memory or latency optimization made without measured baseline.
**Решение:** Record hardware/runtime/workload and latency percentiles, allocation, GC/LOH and memory; compare before/after under same conditions.
**Не применять:** Microbenchmark or CI pass is not proof of real audio/video latency or UX.
**Проверка:** Warmup, repeated runs, regression threshold, release build hardware.
**Проекты:** KLIDAN, Audio Probe
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters, https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace, https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/performance

## latest-frame-coalescing | Latest-Frame Coalescing for Replaceable Preview (P2, reviewed)
**Когда:** Preview backlog grows and displayed frame lags source.
**Решение:** For replaceable preview only, retain latest sequence/generation and dispose superseded frames; recording and Program output require explicit separate policy.
**Не применять:** Never silently discard audio samples, operator TAKE or lossless evidence.
**Проверка:** 60 fps decoder/30 fps render, bounded backlog, A/V sync, disposal, stale frame.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/core/extensions/channels, https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/memory-t-usage-guidelines, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging

## qa-controllable-time | Controllable Clock and Deadline Replay (P1, reviewed)
**Когда:** Тест timeout зависит от Sleep, wall-clock и скорости CI и периодически падает.
**Решение:** Ввести TimeProvider либо минимальный clock abstraction в нужных границах; управлять FakeTimeProvider в тесте, отдельно сохранять monotonic duration и UTC timestamps.
**Не применять:** Не подменять физический таймер аудиоустройства и не считать fake clock доказательством реального deadline; не добавлять новый пакет, если проект уже имеет проверяемый clock.
**Проверка:** Deadline just before/after boundary, timer advance, cancellation, no real sleeps, no wall-clock dependence.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview, https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.time.testing.faketimeprovider.advance?view=net-10.0-pp

## qa-scheduled-interleavings | Deterministic Async Interleaving Test (P1, reviewed)
**Когда:** Race между reconnect, Stop и поздним callback проявляется только иногда.
**Решение:** На границе I/O/IPC/worker поставить контролируемые barriers и завершать операции в заданном порядке A→B, B→A, Cancel→late reply; проверять generation и ownership.
**Не применять:** Не заменять управляемым тестом нагрузочные race/physical тесты; избегать задержек на случайном Thread.Sleep вместо сигнала готовности.
**Проверка:** Late A after B, simultaneous dispose/apply, no deadlock, all tasks join, repeatable ordering across CI.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices, https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/task-cancellation

## qa-io-fault-matrix | Fault Injection at Every Durable I/O Boundary (P1, reviewed)
**Когда:** Миграция/установка или backup проходят happy path, но падают посередине commit/readback.
**Решение:** Перечислить операции I/O, на каждой точке подставлять permission denied, short write, disk full, corrupted readback и проверять rollback/retry invariants. Отдельно проверять отказ в recovery path.
**Не применять:** Не утверждать, что симулятор I/O точно моделирует отключение питания и порядок fsync на конкретном носителе.
**Проверка:** Fail before/after stage, write, rename, commit, readback; no silent reset, no data loss; recovery idempotent.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://www.sqlite.org/testing.html, https://www.sqlite.org/atomiccommit.html

## qa-process-crash-recovery | Process-Crash Boundary and Restart Verification (P0, reviewed)
**Когда:** Приложение после аварии на стадии установки или DataRoot использует неполный журнал.
**Решение:** Запускать тест в дочернем процессе с подготовленным workspace, убивать в контролируемой точке, потом открывать state свежим процессом и сверять persisted intent/RootId/статус.
**Не применять:** Kill дочернего процесса не моделирует потерю питания или отказ OS; не запускать crash injection на production DataRoot.
**Проверка:** Crash before/after canonical write, restart, check journal, match IDs, repeat safe retry, no corrupt DB.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://www.sqlite.org/testing.html, https://www.sqlite.org/atomiccommit.html

## qa-cancel-is-not-stop | Cancellation Request Is Not Stop/Join Proof (P1, reviewed)
**Когда:** Stop помечен PASS сразу после Cancel, хотя worker продолжает писать в память или IPC.
**Решение:** Фиксировать отдельные состояния cancel requested, worker acknowledged, worker exited и resources released; проверять wait/join, cancellation response и поздние результаты.
**Не применять:** Не считать Task status Canceled обязательным, если delegate нормально завершился; не освобождать интерфейсы до остановки владельца.
**Проверка:** Cancel returns before worker, late completion, noncooperative task, bounded shutdown, dispose after join.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/task-cancellation, https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices

## qa-physical-evidence-separation | Synthetic, Integration and Hardware QA Scope (P1, reviewed)
**Когда:** Фейковые устройства и мок-сервер успешно проходят тест, а итоговый отчёт заявляет physical PASS.
**Решение:** В результатах хранить evidenceLevel, target runtime/OS, реальные endpoint IDs в защищённых локальных отчётах, проверенную операцию и критерии; синтетические результаты маркировать отдельно от physical hardware/network.
**Не применять:** Не выводить device stability из mocked WASAPI; не считать HTTP 200 доказательством VPN egress; не включать чувствительные идентификаторы в публичную карточку.
**Проверка:** Fake-only shows SYNTHETIC, hardware test required for PHYSICAL, exact source and device, no false promotion.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://learn.microsoft.com/en-us/windows/win32/coreaudio/recovering-from-an-invalid-device-error, https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices

## qa-evidence-provenance-manifest | Reproducible Evidence Manifest and Retention (P1, reviewed)
**Когда:** Скриншоты, JSON и CI-log нельзя связать с точной сборкой или идентификатором теста.
**Решение:** Сохранять run ID, source SHA, artifact digest, OS/runtime, test policy, timestamp, outcome, evidence paths/hashes; задавать retention и redaction; исключать secret-bearing raw logs.
**Не применять:** Подписанный manifest не делает сфабрикованный результат реальным; отсутствие артефакта означает отсутствие доказательства, а не PASS.
**Проверка:** Artifact mismatched hash, missing file, expired retention, wrong source SHA, sensitive canary leak.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts, https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices

## qa-ci-isolation-and-concurrency | CI Concurrency Group and Isolated Test Matrix (P1, reviewed)
**Когда:** Параллельные тесты используют общий каталог/устройство и портят друг другу состояние, новый run отменяет нужный deploy.
**Решение:** Изолировать temp/data roots на run, определить parallel-safe группы; для GitHub Actions использовать точные concurrency groups и политику cancel-in-progress только если отмена безопасна.
**Не применять:** Не включать cancel-in-progress для stateful deploy без восстановительного протокола; не считать green CI воспроизводимостью hardware сценария.
**Проверка:** Two PR runs, shared resource collision, matrix OS/runtime coverage, queued/cancel semantics and cleanup.
**Проекты:** KLIDAN, Audio Probe, STAYA
**Первоисточник:** https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency, https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices

## wpf-custom-automation-peer | UI Automation Peer for Custom Operator Controls (P1, reviewed)
**Когда:** Custom fader, joystick, TAKE/Program widget is drawn but inaccessible to screen reader/automation tools.
**Решение:** Expose appropriate AutomationPeer, control type, Name, supported patterns (Invoke/RangeValue as applicable) and property changed events. Use built-in WPF controls where feasible.
**Не применять:** Do not create a Custom control type when a standard type describes behavior. AutomationPeer tests are not proof that every screen reader works.
**Проверка:** UIA tree Name/control type/pattern; Invoke or range control; value update event; detached/hidden elements.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control, https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/accessibility-best-practices

## wpf-semantic-critical-actions | Operator-Critical Action Identity and State (P1, reviewed)
**Когда:** Visual TAKE, Program, Preview and Stop buttons have ambiguous names or disabled state is unclear for keyboard/screen-reader use.
**Решение:** Name every critical action by intent and current state, expose enabled/disabled, avoid relying on color alone, keep semantic command binding and visual label in sync.
**Не применять:** Do not assign the same accessible name to Program and Preview; do not make a decorative status lamp act as a hidden command.
**Проверка:** AutomationProperties.Name/HelpText, CanExecute/disabled, program state event, keyboard activation and wrong-target negative tests.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/accessibility-best-practices, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control

## wpf-keyboard-navigation-matrix | Keyboard Navigation and Focus Scope Matrix (P1, reviewed)
**Когда:** Tab cycles through hidden items; Enter/Escape in dialogs, joystick and mixer hotkeys conflict with TextBox editing.
**Решение:** Map Tab/Shift-Tab and directional navigation by workspace, use WPF focus scopes/KeyboardNavigation intentionally, restore focus to visible enabled target after modal close.
**Не применять:** Do not intercept text input and IME globally; focus request before Loaded may fail; existing screen-specific bindings take precedence.
**Проверка:** Tab order, arrows, Escape/Enter, modal focus return, TextBox caret, screen at 100/125/150% DPI.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview, https://learn.microsoft.com/dotnet/desktop/wpf/advanced/input-overview

## wpf-system-contrast-resources | System High-Contrast Resource Adaptation (P1, reviewed)
**Когда:** Custom dark-theme panel fixes text/brush colors and loses important contrast in Windows contrast mode.
**Решение:** Detect WPF SystemParameters.HighContrast where relevant; use dynamic SystemColors brush keys for system-derived values; preserve semantic roles and visible state in custom templates.
**Не применять:** Do not copy WinUI ThemeDictionaries API into WPF; do not assume dark theme equals Windows high contrast; never convey alert with color alone.
**Проверка:** Windows contrast mode switch while app open; selected/disabled/hover, focus border, text readability and theme-switch regression.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/api/system.windows.systemparameters.highcontrast?view=windowsdesktop-10.0, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/how-to-paint-an-area-with-a-system-brush, https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/accessibility-best-practices

## wpf-label-contrast-baseline | Accessible Text Contrast and Zoom Baseline (P1, reviewed)
**Когда:** Tiny captions, meter labels and disabled/secondary text become unreadable at FHD/DPI or custom theme.
**Решение:** Check foreground/background contrast of functional text, keep important labels text rather than only graphics, verify readability after display scaling and with font settings.
**Не применять:** Do not rely on high-contrast mode to fix weak default palette; avoid hardcoded WCAG claims from screenshot-only comparison.
**Проверка:** Contrast samples from actual theme, 1920x1080 100/125/150%, long labels, selected row and error text.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessible-text-requirements, https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/accessibility-best-practices

## wpf-operator-localization-expansion | Long Localized Text and Culture-Aware Layout (P1, reviewed)
**Когда:** Russian labels get clipped; localized number formats and custom fonts change control width or rendering.
**Решение:** Prefer auto/relative layout, TextWrapping when appropriate, correct XML lang/culture for formatting, maintain stable resource keys and protect critical actions from clipping.
**Не применять:** Do not fix every translated string with fixed pixel widths. LocBaml on .NET Framework is not automatically compatible with modern .NET WPF.
**Проверка:** Pseudo-long strings, RU/EN resource length, decimal separator, text overlap, focus and keyboard operation at FHD/DPI.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/framework/wpf/advanced/wpf-globalization-and-localization-overview

## wpf-accessibility-evidence-gate | Accessibility Evidence Across Custom Workspaces (P1, reviewed)
**Когда:** Screenshots and build PASS are accepted as proof of keyboard and assistive automation usability.
**Решение:** For each workspace capture scope-specific visual evidence plus UIA tree, keyboard-only navigation and real focus state, including modal and program display transitions.
**Не применять:** Do not treat AutomationPeer unit test or screenshot as complete physical accessibility certification; record test environment and remaining manual gaps.
**Проверка:** Operator shell, mixer, LED joystick, media library, dialogs; Tab/Enter/Escape/UIA patterns, system contrast, 100/125/150% DPI.
**Проекты:** KLIDAN
**Первоисточник:** https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/accessibility-best-practices, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control, https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview


## WASAPI capture and clock (2026-11-12)

### audio-capture-discontinuity-evidence

**Signals:** Capture packets contain DATA_DISCONTINUITY, TIMESTAMP_ERROR or SILENT; a stream appears stable despite uncertain packet timing.

**Approach:** Record flag bitmask, packet frame count, stream-relative device position and QPC time (100 ns) per packet. Treat discontinuity as a glitch indicator, timestamp error as invalid timing evidence and SILENT as silence rather than automatically a glitch. Distinguish BUFFER_EMPTY from successful nonempty packets. Keep GetBuffer/ReleaseBuffer ordered on one thread and release promptly.

**Avoid:** Do not treat SILENT as data loss, accept invalid timestamps as latency PASS, assume a missing flag proves glitch-free hardware, or delay ReleaseBuffer for expensive logging.

**Verification:** Proposed synthetic flag-combination and empty/error-code matrix; separate physical endpoint run with load, reconnect and raw artifact provenance. Assert timestamp-uncertain packets cannot establish timing PASS.

**Review:** DOC_REVIEW (primary sources reviewed; physical QA not executed). [Sources](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer)

### audio-clock-domain-reconciliation

**Signals:** Duplex capture/render clocks drift or a sample-position comparison gives impossible latency because units or rates differ.

**Approach:** For IAudioClock position, obtain GetFrequency and normalize position/frequency; compare each endpoint using correlated QPC in 100 ns units. For shared mode only, IAudioClock2 hardware frame position is an alternative, but endpoint sample rate can differ from client mix rate. Record mode, endpoint, frequency, epoch, clock method and confidence.

**Avoid:** Do not compare raw positions from distinct clocks, equate endpoint and mix sample rates, call IAudioClock2 for exclusive mode, or treat S_FALSE delayed readings as equally accurate S_OK. Do not retry S_FALSE indefinitely.

**Verification:** Proposed synthetic independent-clock rate and delayed-read matrix, QPC unit normalization, shared/exclusive negative cases; physical two-USB-endpoint drift evidence required before hardware claim.

**Review:** DOC_REVIEW (primary sources reviewed; physical QA not executed). [Sources](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclock-getposition)

### audio-capture-packet-epoch

**Signals:** A late capture packet or clock observation from an invalidated stream updates a newly started measurement; position resets to zero.

**Approach:** Assign a generation to each initialized capture stream and to all packet metadata; reject late observations from previous generations. Stop freezes IAudioClock position; subsequent Start resumes; Reset while stopped sets position to zero, so begin a new analysis epoch after Reset or stream recreation. Preserve raw error/status and cleanup ordering.

**Avoid:** Do not require position monotonicity across Reset or device recreation, reuse old QPC correlations after invalidation, or treat generation fencing as proof of actual hardware stability.

**Verification:** Proposed deterministic late-packet, Stop/Start, Reset and DEVICE_INVALIDATED cases; assert no old generation contributes to new stability result. Physical reconnect evidence remains separate.

**Review:** DOC_REVIEW (primary sources reviewed; physical QA not executed). [Sources](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer)
