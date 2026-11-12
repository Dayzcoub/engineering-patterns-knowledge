# STAYA: IPC, subscriptions, resilience and security

Дата: 2026-11-12. Статус: proposal based on inspected primary documentation, not an audit of STAYA production or its exact Xray/3x-ui versions.

## Contract boundaries

1. Separate control plane (admin API), public data plane (subscription path), process health, listener health, and actual transport/egress.
2. Each IPC/HTTP request has protocol version, correlation ID, owner/generation, deadline and explicit cancellation/error status. Late replies must not update a new generation.
3. Treat every upstream subscription as untrusted: allowlist scheme and destination where appropriate; validate IP/DNS and redirects, size, schema and duplicate fields.
4. Normalize inputs into a canonical model with source namespace and deterministic collision rules. Preserve fixed-IP direct nodes apart from GLOBAL AUTO unless explicitly requested.
5. Bound concurrency, work queues and retry budget. Distinguish permanent 4xx or schema errors from transient 429/503 and honor permitted Retry-After.
6. Specify failover with health TTL, failure threshold, cooldown and recovery probes. For STAYA, the GLOBAL AUTO `leastLoad` label alone is not evidence of health-based failover: verify runtime Xray selection semantics, probe configuration and observed node switching separately.
7. Stage deployment as candidate + digest + backup + preflight + promotion + public-route/e2e smoke; rollback and verify per service if a stage fails.
8. Redact secret tokens, URI credentials and private keys before creating logs, stdout, stderr or CI artifacts. Use synthetic secrets for testing.

## Negative QA matrix

| Fault | Required observation |
|---|---|
| IPC missing or incorrect protocol | Typed protocol error, no unsafe payload processing |
| Reply from old generation | Old result rejected without changing current state |
| Subscription redirects to loopback or metadata IP | SSRF rejection, safe diagnostic |
| External subscription 429 Retry-After | Bounded retry, no request storm |
| Duplicate inbound tags or same alias | Deterministic collision behavior and source provenance |
| External source unavailable | Explicit stale/last-known-good/fail-closed policy, no fake freshness |
| Fixed-IP direct and GLOBAL AUTO merged | Both retained; direct does not silently become auto |
| Public subscription path works, legacy root returns 404 | Public path PASS only; wrong path result stays separate |
| Xray syntax accepted but actual transport fails | Preflight PASS / end-to-end FAIL; rollback if required |
| Caddy reload error | Caddy's own rollback checked; no claimed atomic rollback for Xray |
| Process active but listener or egress failed | Degraded health with precise scope |
| Old credentials found in log artifact | Test fails; rotation/revocation and report sanitization required |

## Proof levels

- DOC_REVIEW: source inspected. Does not prove a particular implementation.
- OFFLINE_TEST: mock/model validation using synthetic data. Does not prove live endpoints.
- INTEGRATION_QA: staged service + public path and response checks with redacted evidence.
- LIVE_TRANSPORT_QA: authorized test client verifies egress and reconnect on real deployed versions.
- PROD_PASS requires project-defined scope and evidence for each relevant layer. Do not infer it from a green CI.

## Sources

- Enterprise Integration Patterns: https://www.enterpriseintegrationpatterns.com/patterns/messaging/RequestReply.html and https://www.enterpriseintegrationpatterns.com/patterns/messaging/FormatIndicator.html
- Azure resilience: https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring and https://learn.microsoft.com/en-us/azure/architecture/patterns/rate-limiting-pattern
- OWASP: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html and https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- Caddy: https://caddyserver.com/docs/api and https://caddyserver.com/docs/caddyfile/matchers
- Xray config-test flag in pinned source: https://github.com/XTLS/Xray-core/blob/c456141815359e1d2c00dfc673f5f26adf22fae2/main/run.go

All scenarios are suggested design and QA cases. No live STAYA node, transport, subscription or secret was accessed.
