# Empfohlene VS Code-Erweiterungen für Melody Mind Nuxt

Für die optimale Entwicklungserfahrung mit diesem Projekt empfehlen wir die Installation der folgenden VS Code-Erweiterungen:

## Notwendige Erweiterungen

### ESLint

- **ID**: `dbaeumer.vscode-eslint`
- **Beschreibung**: Integriert ESLint in VS Code für Echtzeit-Linting und automatische Fehlerbehebung.
- **Installation**: `code --install-extension dbaeumer.vscode-eslint`

### Prettier - Code formatter

- **ID**: `esbenp.prettier-vscode`
- **Beschreibung**: Integriert Prettier in VS Code für konsistente Codeformatierung.
- **Installation**: `code --install-extension esbenp.prettier-vscode`

### Vue Language Features (Volar)

- **ID**: `Vue.volar`
- **Beschreibung**: Bietet erweiterte Unterstützung für Vue 3, einschließlich Syntax-Highlighting, IntelliSense und Debugging.
- **Installation**: `code --install-extension Vue.volar`

## Empfohlene Erweiterungen

### Tailwind CSS IntelliSense

- **ID**: `bradlc.vscode-tailwindcss`
- **Beschreibung**: Bietet Autovervollständigung und Linting für Tailwind CSS-Klassen.
- **Installation**: `code --install-extension bradlc.vscode-tailwindcss`

### i18n Ally

- **ID**: `lokalise.i18n-ally`
- **Beschreibung**: Hilft bei der Verwaltung von Übersetzungen in mehrsprachigen Projekten.
- **Installation**: `code --install-extension lokalise.i18n-ally`

### Iconify IntelliSense

- **ID**: `antfu.iconify`
- **Beschreibung**: Bietet IntelliSense für Iconify-Icons, die mit nuxt-icon verwendet werden.
- **Installation**: `code --install-extension antfu.iconify`

### Markdown Preview Enhanced

- **ID**: `shd101wyy.markdown-preview-enhanced`
- **Beschreibung**: Verbesserte Markdown-Vorschau für Dokumentationsdateien.
- **Installation**: `code --install-extension shd101wyy.markdown-preview-enhanced`

## Installation aller Erweiterungen

Du kannst alle Erweiterungen auf einmal mit dem folgenden Befehl installieren:

```bash
code --install-extension dbaeumer.vscode-eslint && \
code --install-extension esbenp.prettier-vscode && \
code --install-extension Vue.volar && \
code --install-extension bradlc.vscode-tailwindcss && \
code --install-extension lokalise.i18n-ally && \
code --install-extension antfu.iconify && \
code --install-extension shd101wyy.markdown-preview-enhanced
```

## Konfiguration

Die Konfiguration für diese Erweiterungen wurde bereits in der `.vscode/settings.json`-Datei eingerichtet. Diese Einstellungen sorgen für:

- Automatische Formatierung beim Speichern
- ESLint-Integration mit Flat Config
- Prettier als Standard-Formatierer
- Spezifische Einstellungen für verschiedene Dateitypen
