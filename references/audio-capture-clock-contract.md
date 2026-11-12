# WASAPI Capture Flags, Clock Domains and Stream Epochs

Status: **DOC_REVIEW** (Microsoft Learn checked 2026-11-12); all QA below **PROPOSED**, not executed. Applies to KLIDAN and Audio Probe design decisions, not their code.

## Capture packets

IAudioCaptureClient::GetBuffer returns packet frame count, flags, stream-relative device position in frames and QPC position converted to 100 ns. DATA_DISCONTINUITY is a glitch signal on supported Windows versions. TIMESTAMP_ERROR makes packet timing uncertain. SILENT means silent audio and is not itself proof of a glitch. BUFFER_EMPTY has zero frames and does not populate timestamp outputs. Acquire/release packet on the same thread, consume all or none, and release promptly. See https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer.

## Clock domains

IAudioClock::GetPosition returns a position with undefined units unless paired with GetFrequency. Position / frequency gives stream-relative seconds; its QPC output uses 100 ns. S_FALSE can mean delayed/inaccurate reading, so report uncertainty and avoid unbounded retry. IAudioClock2::GetDevicePosition returns hardware frames only for shared-mode streams; endpoint and client mix sample rates may differ. Compare separate endpoints only after normalizing clock units and correlating QPC observations. Sources: https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclock-getposition and https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclock2-getdeviceposition.

## Stream epochs

IAudioClock position freezes at Stop, resumes after Start and returns to zero after Reset. For analysis, use a new epoch after Reset or device recreation; reject late observations from previous stream generations. This is an application-level policy based on documented behavior, not a native WASAPI generation token.

## Proposed QA (NOT EXECUTED)

1. Inject flag combinations and BUFFER_EMPTY; assert independent classification and invalid timing evidence on TIMESTAMP_ERROR.
2. Inject two independent clock frequencies and QPC observations; assert unit conversion, S_FALSE uncertainty and exclusive-mode rejection for IAudioClock2.
3. Race late packet with Stop/Start, Reset and device invalidation; reject stale epoch without imposing monotonicity across reset.
4. On real USB hardware, separately record endpoint identity, mode, actual period, format, duration, discontinuities, timestamps, run artifact hashes and load conditions. Never promote DOC_REVIEW or synthetic PASS to hardware PASS.

Machine-readable cases: [audio-capture-scenarios.json](../data/audio-capture-scenarios.json). No device test was performed in this wave.
