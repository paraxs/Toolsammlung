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


## Strict-Local Modus (Cookie/Privacy)

Mit `?strictLocal=1` am Seiten-URL wird der CDN-Fallback blockiert.
Dann funktionieren Exporte nur mit lokal vorhandenen `vendor/*` Dateien.


## Ist-Stand

Die vier Vendor-Dateien sind jetzt im Repository enthalten:
- `vendor/jspdf.umd.min.js`
- `vendor/xlsx.full.min.js`
- `vendor/jspdf.plugin.autotable.min.js`
- `vendor/fontawesome.all.min.js`

Damit funktionieren Exporte/Icons auch im Strict-Local Modus (`?strictLocal=1`) ohne externe Script-Requests.


## Go-Live Check

Auf `index.html` zeigt die Statusbox den Vendor- und Tool-Datei-Status.
Zusätzlich kann ein JSON-Readiness-Report exportiert werden.

Zusätzlich unterstützt das Dashboard jetzt eine „Nur fehlende anzeigen“-Ansicht und einen kopierbaren Kurzstatus für Freigabe-Workflows.

Die Startseite zeigt zusätzlich eine Go-Live Entscheidung (bereit/nicht bereit) inklusive Blocker-Text und Copy-Blocker-Funktion.

Copy-Blocker-Ausgabe enthält jetzt zusätzlich die konkreten fehlenden Vendor-/Tool-Dateien und nutzt einen Clipboard-Fallback für ältere Browser.
