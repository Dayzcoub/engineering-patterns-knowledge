# Audio Probe: минимальный стабильный профиль устройства

**Статус:** инженерные критерии, основанные на изученных спецификациях API; не доказательство стабильной работы конкретного устройства.
**Версия:** 2026-11-12. Связанные карточки: `wasapi-mode-capability-discovery`, `wasapi-period-lattice`, `wasapi-actual-buffer-readback`, `audio-minimum-stable-profile`, `audio-stream-shutdown-barrier`.

## Цель

Для конкретного **endpoint и режима** выбрать самый малый **эффективный** буфер/период, который прошёл репрезентативные тесты. Возможность открыть stream — только prerequisite, не PASS. Результат зависит от Windows, драйвера, sample rate, формата, направления, нагрузки и версии приложения.

## Порядок (без скрытого fallback)

1. **DISCOVER**: зафиксировать endpoint ID, FriendlyName, capture/render, driver/OS, доступные режимы, input/output channels, rate, sample format, support/error codes. Не переносить свойства render на capture.
2. **CANDIDATES**: для `IAudioClient3` Shared взять default, fundamental, min, max в frames, сгенерировать кандидаты на их пересечении и только кратные fundamental. Для Exclusive/legacy применять их собственные API-ограничения. Поддерживаемое значение не равно стабильному.
3. **INITIALIZE + READBACK**: вызвать Initialize/InitializeSharedAudioStream, прочитать фактический `GetBufferSize`; для exclusive-event alignment error заново активировать client после Release. Сохранять requested/effective отдельно.
4. **QUICK CHECK**: проверить duplex routing и реальные значения frames/packet, убедиться, что корректны capture и render. Результат `UNSUPPORTED`/`OPEN_ERROR` не заменять автоматически ближайшим большим периодом без записи новой попытки.
5. **STABILITY**: упорядочить реально доступные кандидаты по эффективному буферу/целевой суммарной задержке. Для каждого выполнить повторные и длительные тесты с критериями проекта: glitches, underruns/overruns, discontinuities, timing margin/jitter, правильность routing, shutdown/reconnect. Рекомендация в рамках проекта: 60/300/600 секунд под соответствующей нагрузкой; это **не** универсальные нормы Windows.
6. **DECISION**: выбрать минимальный PASS при полностью раскрытых критериях. Если меньший кандидат FAIL, записать причину и перейти к следующему. Если ни один не прошёл — вернуть `NO_STABLE_PROFILE`, а не фиксированные 3, 5 или 10 мс.
7. **PROFILE**: связать результат с endpoint+driver/OS+mode+direction+format+rate+channels+effective frames+test suite version; при смене этих условий помечать профиль `needs-revalidation`.

## Минимальная структура результата

```json
{
  "schemaVersion": 1,
  "deviceId": "endpoint-or-device-key",
  "mode": "wasapi-shared-or-exclusive",
  "capture": {"channels": 1, "rate": 48000, "sampleFormat": "PCM16"},
  "render": {"channels": 2, "rate": 48000, "sampleFormat": "PCM16"},
  "candidates": [
    {"requestedFrames": 240, "effectiveFrames": 240, "status": "NOT_TESTED", "reason": null}
  ],
  "decision": "NOT_TESTED",
  "selectedCandidate": null,
  "testPolicyVersion": "project-defined",
  "hardwareEvidence": null
}
```

Значения в примере **условные**, не результат для DEXP, Bloody, Audient или FLOW 8.

## Отрицательные сценарии

- Unsupported period/rate/format не должен становиться PASS.
- `BUFFER_SIZE_NOT_ALIGNED` должен завершать жизнь старого client перед новой попыткой.
- Прерванный тест или устройство, которое отсоединили, не может выдать PASS.
- При повторном подключении поздний callback/notification не должен менять статус нового поколения.
- Если маршрут mono input → stereo output не поддерживается, нельзя считать duplex проверенным по stereo input → stereo output.
- Приложение не должно утверждать, что `MMCSS=ON` само по себе делает буфер устойчивым.

## Источники и границы доказательств

- WASAPI API: [GetSharedModeEnginePeriod](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-getsharedmodeengineperiod), [InitializeSharedAudioStream](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-initializesharedaudiostream), [Initialize](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-initialize), [GetBufferSize](https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-getbuffersize).
- Scheduling: [MMCSS](https://learn.microsoft.com/en-us/windows/win32/procthread/multimedia-class-scheduler-service); [Exclusive mode](https://learn.microsoft.com/en-us/windows/win32/coreaudio/exclusive-mode-streams).
- Callback: [PortAudio callback constraints](https://files.portaudio.com/docs/v19-doxydocs/writing_a_callback.html).

Эти источники подтверждают **API-контракты**. Они не доказывают, что конкретный ноутбук/драйвер пройдёт тест с 3/5/10 мс. Только физические измерения Audio Probe и KLIDAN могут подтвердить профиль.

## Capture clock evidence

Дополнение: [`audio-capture-clock-contract.md`](audio-capture-clock-contract.md) содержит packet flag, clock frequency, QPC units и epoch после Reset. Не использовать синтетические clock тесты вместо физического профиля.
