# KLIDAN WPF: Full HD, DPI, dispatcher и focus

**Версия:** 2026-11-12. **Статус:** документальная рекомендация, не QA-проверка реального интерфейса.

## Область

Приоритетные экраны: Operator Shell, Media Library, Audio Mixer, Audio Editor, Video Mixer, LED Workspace и DataRoot dialogs. Оценивать реальную WorkArea, а не только полное разрешение экрана. В WPF размер макета задаётся в DIP; физические пиксели и DPI нельзя смешивать.

## Матрица визуальных проверок

| Сценарий | Приёмка |
|---|---|
| 1920×1080 при 100%, 125%, 150% | Критические действия видимы, нет перекрытия/обрезки, допустимые области прокручиваются |
| Минимальная разрешённая WorkArea | Window и диалоги внутри экрана, footer и действия доступны |
| Multi-monitor 100% → 150% → 100% | Нет повторного применения DPI scale, окно не остаётся вне экрана |
| Длинные локализованные строки/шрифты | Grid/DockPanel перераспределяют место, подписи не закрывают действия |
| Keyboard-only | Tab order, Enter/Escape и focus scope адекватны модальным окнам |
| Большая медиатека | Виртуализация, reuse-safe selection/expanded state, ограниченные thumbnail decode и memory |
| Late async completion | После Dispose/switch/reconnect старый результат не обновляет UI |

## Запреты и исключения

- `Canvas` имеет смысл для геометрии сцены (LED/video positioning), **не** для компоновки всех форм.
- Не вводить новый набор токенов вместо существующих `KLIDAN.*`.
- Не утверждать, что Release build и WPF unit tests доказывают корректную раскладку при 150%.
- RenderTransform пригоден для визуального перемещения; он не участвует в вычислении места соседних элементов так, как LayoutTransform.
- UI virtualization и data virtualization — разные механизмы.
- Проверить поддержку per-monitor DPI для используемой версии .NET/WPF и Win32-owned окон, а не выводить её из одной настройки manifest.

## Доказательства в PR интеграции

Карта window → screenshot, размеры в DIP, текущий monitor DPI, WPF layout test, требуемые captured states, статистика памяти/scroll, повторные изменения DPI, отдельный тест late reply после Dispose. Доказательства по KLIDAN предоставляются его собственным репозиторием, а не этим справочником.

## Источники

- [WPF layout](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/layout)
- [Automatic layout](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/use-automatic-layout-overview)
- [Windows high DPI](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows)
- [WPF Dispatcher](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/threading-model)
- [WPF controls optimization](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls)
- [Focus overview](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview)
- [Application resources](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-application-resources)
- [2D graphics and imaging](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging)
