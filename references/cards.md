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

