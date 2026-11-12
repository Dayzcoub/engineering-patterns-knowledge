# Fault injection, deterministic QA and evidence contract

Version: 0.8.0-preview.1. Date: 2026-11-12. Status: DOC_REVIEW / PROPOSED_QA. No device or production tests executed.

## Evidence levels

- SYNTHETIC: fake time, stubbed IPC, mock I/O, virtual state. Does not imply physical reliability.
- INTEGRATION: real component on controlled isolated test root. Does not imply power-loss durability.
- HARDWARE: target device and driver tested at stated format, channels, period and load.
- LIVE_NETWORK: authorized public route and transport tested; excludes unrelated admin endpoints.
- PROD_PASS only for explicitly supported scope with real evidence, not from source review.

## Procedure

1. State invariant and an expected result before injecting a fault.
2. Build fault matrix covering steps before and after write, commit, readback, publish and cleanup. Do not modify production paths.
3. For time-dependent logic use controllable TimeProvider or existing project clock; timers and deadlines tested at exact boundaries.
4. For concurrency control the order of Await/Stop/reconnect/callback using gates and explicit synchronization rather than Sleep.
5. For crash recovery terminate isolated child process, then reopen the state in a fresh process and check RootId/journal and data integrity.
6. For cancellation distinguish requested, acknowledged, worker-exited and resources-released. Cancellation is cooperative.
7. Capture run ID, repo/source SHA, artifact hash, OS/runtime, evidence level, fixture, injected failure point, expected/observed results, PASS/FAIL/UNKNOWN and redacted evidence paths.
8. Run synthetic CI and hardware/device QA as separate gates. Never promote synthetic PASS to physical PASS.

## Matrix

| Injected fault | Expected evidence |
|---|---|
| Late reply after reconnect | Old generation rejected; new state unchanged |
| Timeout at deadline - 1 tick / + 1 tick | Deterministic state transition without wall time |
| Disk full before canonical write | Recoverable old root; no false commit |
| Crash between canonical and readback | Fresh process reconciles pending intent, no blank database |
| Repeated cancellation during callback | No early resource free, bounded join or explicit BLOCKED |
| Fake WASAPI reports 5 ms support | SYNTHETIC only; no claim of physical stability |
| Parallel CI uses same resources | Isolated run roots and no state contamination |
| Missing or expired evidence artifact | UNKNOWN/NO_EVIDENCE, never automatic PASS |

## Sources

- https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview
- https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.time.testing.faketimeprovider.advance?view=net-10.0-pp
- https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
- https://www.sqlite.org/testing.html
- https://www.sqlite.org/atomiccommit.html
- https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/task-cancellation
- https://learn.microsoft.com/en-us/windows/win32/coreaudio/recovering-from-an-invalid-device-error
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts

The catalog and scenarios are documentation. No KLIDAN, Audio Probe or STAYA production code is changed.
