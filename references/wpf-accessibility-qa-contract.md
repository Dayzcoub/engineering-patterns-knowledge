# KLIDAN WPF Operator Accessibility: QA contract

Version: 0.9.0-preview.1; DOC_REVIEW / PROPOSED_QA. No production UI was modified or tested here.

## Matrix

| Surface | Required proof |
|---|---|
| Operator TAKE / Program / Preview | Unique AutomationProperties.Name, correct Invoke/CanExecute, no wrong target |
| Mixer fader | Appropriate range/control automation pattern, keyboard change and visible value |
| LED joystick | Arrow control on focused target; text editor keys unaffected |
| DataRoot/Settings dialogs | Tab order, Enter/Escape, focus restore, no hidden target |
| Media library | Selection state, keyboard navigation, accessibility identity of virtualized rows |
| Every relevant surface | 1920x1080 100%,125%,150% DPI, Windows contrast, actual UIA tree |

## Constraints

- WPF AutomationPeer/AutomationProperties is for Windows Presentation Foundation. Do not reuse WinUI ThemeDictionaries in WPF.
- SystemParameters.HighContrast and DynamicResource SystemColors brush keys are WPF-compatible. Keep KLIDAN.* tokens and adapt them rather than creating a parallel style system.
- Keyboard focus is different from logical focus. A call to Focus is not proof that the requested target got focus.
- Avoid global shortcuts that intercept edit controls or Input Method Editors.
- UIA unit tests, screenshot tests and real assistive-technology checks have separate evidence levels.
- No false claim of WCAG/ADA or overall accessibility compliance without a complete requirements and user test process.

## Sources
- https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control
- https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/accessibility-best-practices
- https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview
- https://learn.microsoft.com/dotnet/desktop/wpf/advanced/input-overview
- https://learn.microsoft.com/en-us/dotnet/api/system.windows.systemparameters.highcontrast?view=windowsdesktop-10.0
- https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/how-to-paint-an-area-with-a-system-brush
- https://learn.microsoft.com/en-us/dotnet/framework/wpf/advanced/wpf-globalization-and-localization-overview
- https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessible-text-requirements

