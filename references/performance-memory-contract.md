# KLIDAN: performance, memory and concurrency contract

Дата: 2026-11-12. Статус DOC_REVIEW/PROPOSED_QA. Это не benchmark и не real-time certification.

## Safe default

1. Profile first. Save OS/runtime, CPU/GPU, resolution, DPI, input dataset, warmup, duration, p50/p95/p99 latency, allocations, LOH and GC pauses before changing code.
2. For UI thumbnails/replaceable preview select explicit bounded queue and drop/coalescing policy. Never silently drop audio samples, operator commands, archive data or Program output.
3. ArrayPool is a lease: Rent may return larger or uncleared array. Track actual valid length. Return exactly once to the same pool after *last* reader, including callback/cancel paths. A returned array must never be used.
4. Memory/ReadOnlyMemory ownership does not make backing storage immutable. A producer may replace mutable content; capture lifetime must be shorter than owner release.
5. ConcurrentDictionary GetOrAdd factory may run more than once. Exactly-once loads require a separate per-key single-flight contract and failure invalidation.
6. Cache requires size budget and defined units, TTL, revision keys, eviction and miss fallback. Do not key on raw untrusted subscription URLs or sensitive tokens.
7. ReaderWriterLockSlim may block and has thread ownership; do not place it in real-time callback or hold across await. Test writer progress and cleanup.
8. CancellationTokenSource Dispose does not Cancel. Request cancellation, wait for worker termination, then Dispose. Old generation results cannot apply.
9. Pipelines require correct AdvanceTo consumed/examined plus Complete and bounded buffering; they are not equivalent to an SPSC audio ring buffer.

## Acceptance matrix

| Scenario | Required evidence |
|---|---|
| 10k Media Library items | Bounded thumbnail cache, memory/GC evidence, correct reuse and invalidation |
| 60→30 fps preview | Bounded queue, frame sequence/ownership, Program/audio policy unaffected |
| 10 concurrent same-key requests | No duplicate active side effect; cancel/failure handled per key |
| ArrayPool double Return/use-after-return | Negative tests reject or expose bug; no stale data leaking to next owner |
| CTS Dispose before async worker ends | Fault injection reproduces and repair guarantees join order |
| Fragmented IPC PipeReader packet | Correct AdvanceTo and cleanup under failure |
| Full HD mixer frame-time regression | Baseline p50/p95/p99 and representative memory/GC on target hardware |

## Verified documentation

- Microsoft Channels: https://learn.microsoft.com/en-us/dotnet/core/extensions/channels
- Microsoft ArrayPool Return: https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1.return
- Microsoft Span/Memory lifetime: https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/memory-t-usage-guidelines
- Microsoft GetOrAdd: https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent.concurrentdictionary-2.getoradd
- Microsoft IO pipelines: https://learn.microsoft.com/en-us/dotnet/standard/io/pipelines
- Microsoft GC troubleshooting: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/performance

The patterns are decision guides. Their source review does not establish measured KLIDAN or Audio Probe performance.
