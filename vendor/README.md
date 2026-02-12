# Vendor-Bibliotheken (lokal)

Für eine möglichst externe-abhängigkeitsfreie Nutzung (Cookie/Privacy) können die folgenden Dateien lokal abgelegt werden:

- `vendor/jspdf.umd.min.js`
- `vendor/xlsx.full.min.js`
- `vendor/jspdf.plugin.autotable.min.js`
- `vendor/fontawesome.all.min.js`

Die HTML-Tools sind auf **lokal-first** konfiguriert:
- Zuerst wird die lokale Datei geladen.
- Nur wenn sie fehlt, wird automatisch auf CDN zurückgefallen.

Sobald alle Vendor-Dateien lokal vorliegen, funktionieren die Export-/Icon-Funktionen ohne externe Script-Requests.
