# WASAPI Capture Worker Lifecycle (2026-11-12)

**Evidence:** Microsoft API documentation reviewed. This document is DOC_REVIEW, not production or physical PASS.

## Shutdown and Reset

- Signal cancellation and wake the capture worker; stop new acquisition, settle any active GetBuffer/ReleaseBuffer lease on its owning thread, and join before disposing the client.
- Stop freezes the stream clock; Start resumes it. Reset requires a stopped stream, flushes pending data, resets position to zero, and can fail with `AUDCLNT_E_BUFFER_OPERATION_PENDING` if buffer I/O is active.
- Record exact HRESULT, stream generation and shutdown duration. A bounded join timeout is a failure, not permission to free an in-use interface.

## Invalidation

- Treat `AUDCLNT_E_DEVICE_INVALIDATED`, `AUDCLNT_E_RESOURCES_INVALIDATED`, `AUDCLNT_E_SERVICE_NOT_RUNNING` as terminal for the current measurement epoch.
- In exclusive capture, `AUDCLNT_E_BUFFER_ERROR` may mean no packet is available. Wait until the next pass; count repeats and use controlled shutdown/reinitialization rather than a busy loop.
- Preserve device identity, requested/effective period, mode, packet-loss flags and artifacts for any physical qualification. Never infer PASS from signal amplitude.

## Proposed QA

See `data/audio-capture-scenarios.json`: `capture-stop-reset-lease-barrier`, `capture-unplug-error-matrix`, `capture-worker-shutdown-repetition`. Synthetic fault injection and hardware unplug are separate evidence levels; none executed here.

## Primary sources

- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-stop
- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-reset
- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer
- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-releasebuffer
