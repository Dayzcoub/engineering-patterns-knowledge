# Engineering Patterns Knowledge

[![Validate](https://github.com/Dayzcoub/engineering-patterns-knowledge/actions/workflows/validate.yml/badge.svg)](https://github.com/Dayzcoub/engineering-patterns-knowledge/actions/workflows/validate.yml)

Общая расширяемая библиотека инженерных паттернов и [Agent Skill](SKILL.md) для Codex, OpenCode и других совместимых агентов. Основная цель: **выбирать решение по симптомам и проверкам, а не вводить архитектурные абстракции ради модных названий**.

**Версия:** `0.6.0-preview.1` · **Статус:** исследовательская база, не обязательный стандарт для production.

## Состав

- **80 карточек** в [`data/patterns.json`](data/patterns.json). Каждая содержит признаки задачи, подход, ограничения, способы проверки и ссылки.
- **98 URL первоисточников** в [`data/sources.json`](data/sources.json) со статусами глубины проверки.
- **115 уникальных URL (122 вхождения)** в [`data/upstream-index.json`](data/upstream-index.json). Это очередь для исследований по оригинальному списку, **не 115 изученных паттернов**.
- [`references/cards.md`](references/cards.md): читаемые людьми карточки; [`references/priorities.md`](references/priorities.md): приоритеты для KLIDAN, Audio Probe, STAYA.
- [`SKILL.md`](SKILL.md): правила применения скилла; [`AGENTS.md`](AGENTS.md): правила работы в этом репозитории.
- [`scripts/search_patterns.py`](scripts/search_patterns.py): локальный поиск; [`scripts/validate.py`](scripts/validate.py): проверка каталога; [`tests/`](tests/): smoke/unit-тесты.

## Быстрый старт (PowerShell, Windows)

```powershell
$dest = Join-Path $HOME '.agents\skills\engineering-patterns'
git clone https://github.com/Dayzcoub/engineering-patterns-knowledge.git $dest
python (Join-Path $dest 'scripts\validate.py')
python (Join-Path $dest 'scripts\search_patterns.py') --project KLIDAN 'reconnect late response'
python (Join-Path $dest 'scripts\search_patterns.py') --domain audio --json
```

При обновлении: `git -C $dest pull --ff-only`. Для уже существующей папки не выполнять `git clone` поверх неё. Если скилл установили из старого ZIP, сохранить локальные изменения и заменить/мигрировать папку вручную.

**Codex / OpenCode:** используйте поддержку Agent Skills в вашей версии агента и проверьте, что он видит `engineering-patterns` в `.agents/skills`. Для других агентов укажите путь к `SKILL.md` в конфигурации или проектном `AGENTS.md`. **Одна установка не подключает скилл автоматически к каждой беседе ChatGPT.**

## Пример запроса агенту

> Изучи текущую реализацию reconnect в KLIDAN. Примени skill `engineering-patterns` для анализа late replies и отмены. Сначала покажи доказанные инварианты, затем сравни минимум два решения (включая простой локальный фикс), укажи связанные ID паттернов и тесты. Не меняй код без необходимости.

## Проверки и развитие

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/search_patterns.py 'retry duplicate'
```

Сначала изучаем P0/P1-паттерны по их первоисточникам. Новую карточку добавляем только со ссылкой, условиями **когда не применять** и проверкой. Инструкция в [`CONTRIBUTING.md`](CONTRIBUTING.md) и [`references/adding-patterns.md`](references/adding-patterns.md). Переход между статусами проверки не происходит автоматически. Автоматические тесты подтверждают **целостность файла**, а не правильность архитектурного решения.

## Происхождение и права

Индекс URL из [DovAmir/awesome-design-patterns](https://github.com/DovAmir/awesome-design-patterns), commit [`9006287`](https://github.com/DovAmir/awesome-design-patterns/commit/9006287f27e720000cc8763ae4cd150789b8571d), 25 октября 2024 года. Автор указал CC0 1.0 для **своего списка**. Это не лицензия сторонних книг и сайтов. Копии внешних учебников и статей сюда не добавляются. Отдельная лицензия для оригинальных файлов этого репозитория пока **не выбрана**. До её выбора не стоит предполагать право на повторное распространение чужого содержимого.

## Границы ответственности

Паттерн не заменяет анализ требований, ADR, тесты, физические измерения или ревью реального кода. Для real-time audio нельзя автоматически переносить многопоточные схемы из backend-разработки. Для безопасности, хранения и релизов нужны отдельные проверки. Код проектов KLIDAN, Audio Probe и STAYA этот репозиторий **не изменяет**.

### P0: Audio Probe и WASAPI

Первая углублённая волна: [контракт выбора минимального стабильного буфера](references/audio-probe-profile-contract.md), включая supported periods, effective buffer readback, duplex routing, MMCSS, отмену и восстановление. Документация изучена, физические испытания устройств в этом репозитории **не проводились**. Фиксированные 3/10 мс не используются как критерий успеха.

### P0: WPF, DPI и многозадачный UI

[Контракт для Full HD и DPI](references/wpf-fullhd-dpi-contract.md): адаптивная компоновка, Dispatcher, late async results, virtualized media library, focus, токены, оптимизация thumbnail. Это рекомендации на основе Microsoft Learn, **не** визуальный PASS KLIDAN.

### P0: SQLite / DataRoot

[Контракт crash recovery](references/sqlite-dataroot-recovery-contract.md) охватывает WAL, checkpoints, durability, online backup и fail-closed схему согласования SQLite/JSON/marker. Это справочник решений, а не аудит production DataRoot.

### P1: IPC, STAYA resilience and security

16 новых карточек описывают handshake/versioning, deadline, stale replies, bounded work, rate limits, failover, SSRF, нормализацию подписок, public routing, safe rollout, admin isolation, secret lifecycle и logging. Подробности: [STAYA contract](references/staya-ipc-resilience-security-contract.md), [машиночитаемые сценарии](data/staya-scenarios.json). Это рекомендации и QA checklist, не результат production проверки.

### P1: DevOps, наблюдаемость и безопасные обновления

[Контракт релизов и конфигураций](references/devops-release-qa-contract.md) содержит матрицу preflight/runtime/trust/rollback, а [сценарии](data/devops-scenarios.json) описывают 8 проектных заданий для агентов. Источники исследованы, но установка на реальных стендах и серверах не проводилась.
