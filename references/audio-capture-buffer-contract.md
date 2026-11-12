# WASAPI capture packet lease and packet sizing

Status: **DOC_REVIEW**, 2026-11-12. Source review is not physical QA or production validation.

## Whole-packet ownership

GetBuffer gives a packet whose memory remains valid only until ReleaseBuffer. Consume the full packet and release the acquired frame count, or consume none and release zero; zero makes the next GetBuffer return the same packet. Partial counts are invalid. Avoid delays beyond one processing period. Copy only required data into bounded owned memory before release; avoid UI, disk, network and unbounded queues in the lease window.

## Shared/exclusive mode distinction

GetNextPacketSize is shared-mode only and must run on the same thread as GetBuffer/ReleaseBuffer. Shared capture GetCurrentPadding describes the next packet and matches GetBuffer. Exclusive polling padding is a snapshot and can increase before GetBuffer; use actual returned frames. Exclusive event callback normally processes an entire notified buffer instead of polling padding.

## Proposed QA, not executed

1. Simulate GetBuffer/ReleaseBuffer full/zero/partial, replay, delayed processing, invalidation and cleanup. Assert no use-after-release or unbounded wait.
2. Simulate shared and exclusive polling/event modes, verify only supported size invariants, and enforce same-thread packet handling.
3. On a real capture device, record device identity, requested/effective period, format, event/polling mode, packet count, lease p95/p99/max, discontinuities, timestamps, run duration and artifact digests. Choose the minimum **stable supported** period using transport evidence, never audio amplitude or fixed 3/10 ms thresholds.

See `data/audio-capture-scenarios.json` for machine-readable proposed cases.

## Microsoft primary sources

- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-releasebuffer
- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getnextpacketsize
- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudioclient-getcurrentpadding
- https://learn.microsoft.com/en-us/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer
