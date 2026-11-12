# DevOps and secure releases: operating contract (v0.6 preview)

Дата: 2026-11-12. Статус: DOC_REVIEW + PROPOSED_QA. Нет production rollout или физических проверок устройств.

## Рекомендуемые отдельные доказательства

1. **Config preflight**: immutable candidate digest, exact tool/version, parse and validate result. Для Caddy `adapt` и `validate` не одно и то же; `reload` проверять отдельно.
2. **Runtime readiness**: process active != listener ready != public path healthy != actual end-to-end connection. Для Compose short `depends_on` не гарантирует readiness; `condition: service_healthy` требует healthcheck.
3. **Update trust**: SHA-256 проверяет совпадение байтов, но не подлинность издателя, если digest из того же недоверенного источника. Для Windows отдельно проверить WinVerifyTrust и ожидаемую цепочку; тестовый self-signed != публично доверенная подпись.
4. **Metadata freshness**: TUF spec описывает подписанные роли metadata, target digest/size, timestamp expiry и rollback detection. Простая собственная beta.json не становится TUF после добавления signature.
5. **Installer backend**: MSI rollback custom actions относятся к Windows Installer. Для Inno Setup/NSIS механизмы и этапы иные; сначала определить фактический установщик проекта.
6. **Process handoff**: закрыть новые операции, дождаться worker, снять locks, stage verified files и выполнить readback после рестарта. Откат бинарника и миграция DataRoot не образуют одну транзакцию.
7. **Structured evidence**: run ID, source SHA, artifact digest, installed version, stage, status, error and timestamps; синтетические IDs вместо токенов и private URLs.
8. **Observability**: метрики с bounded labels и единицами измерения; traces для причинной связи; alert только если есть действие и наблюдаемое влияние. Не передавать secrets в span attributes и metric labels.
9. **Release gate**: staging → canary → wider release только после подтверждения exact artifact identity, scoped smoke, rollback readiness и заданных stop rules.

## Acceptance matrix

| Сбой | Ожидаемая реакция |
|---|---|
| `caddy adapt` PASS / `caddy validate` FAIL | Блокируется промоут, текущий runtime не меняется |
| Docker container started, dependency not ready | Readiness FAIL, приложение не объявляется готовым |
| systemd crash loop | Bounded restart и диагностируемый failure, без бесконечной нагрузки |
| Signed test installer with untrusted chain | TRUST_FAIL по политике production, не ложный PASS |
| SHA совпал, но publisher не совпал | UPDATE_REJECT, без выполнения candidate |
| Старый signed feed с истёкшим timestamp | UPDATE_REJECT по документированной freshness policy |
| Бинарник занят, worker ещё работает | Обновление ждёт/отменяется до file replacement |
| MSI deferred action меняет внешнее состояние и затем FAIL | Соответствующий rollback action проверен; только если backend MSI |
| Metrics labels включают request ID | Test FAIL из-за unbounded cardinality, ID остаётся в traces/logs |
| Canary не прошла e2e smoke | Продвижение блокируется, rollback предусмотрен |

## Источники

- Caddy: https://caddyserver.com/docs/command-line
- Docker Compose: https://docs.docker.com/compose/how-tos/startup-order
- systemd: https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
- TUF v1.0.37 (8 October 2026): https://theupdateframework.github.io/specification/latest/
- Windows Authenticode: https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-winverifytrust
- Windows Installer rollback custom action: https://learn.microsoft.com/en-us/windows/win32/msi/rollback-custom-actions
- OpenTelemetry context: https://opentelemetry.io/docs/concepts/context-propagation/
- Prometheus metric labels: https://prometheus.io/docs/practices/naming/
- SLSA v1.2: https://slsa.dev/spec/v1.2/

В этом репозитории изменяется только база знаний. Для каждого проекта требуется отдельный PR с реальными тестами и указанием доверенной версии инструментов.
