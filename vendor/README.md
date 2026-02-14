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

Dashboard-Filter „Nur fehlende anzeigen“ wird jetzt gespeichert; Probe-Logik nutzt bei Netzwerkfehlern (Status 0) einen zusätzlichen Retry mit Cache-Buster.

Für den finalen Release-Check liegt ein Batch-Report unter `GO_LIVE_GATE.md` (Standard + Strict-Local je Tool).

Zusätzlich liegt eine manuelle Go-Live-Fachcheckliste unter `GO_LIVE_MANUAL_SCENARIOS.md` (Export/Import/Visualisierung je Tool) vor.

Für den finalen Releaseentscheid steht `GO_LIVE_SIGNOFF.md` bereit (neu generierbar mit `python3 scripts/generate_golive_signoff.py`).

Für zeitkritische Releases gibt es zusätzlich `GO_LIVE_120MIN.md` als kompaktes operatives Runbook.

Schneller Vorab-Check: `python3 scripts/run_golive_preflight.py --strict --base-url http://127.0.0.1:8000` erzeugt `GO_LIVE_PREFLIGHT.md` und `GO_LIVE_PREFLIGHT.json` (non-zero bei Blockern).

Der Preflight prüft jetzt zusätzlich die Core-Dateien der Startseite (`index.html`, `scripts/index-dashboard.js`, `styles/foundation.css`), damit Deployments mit fehlenden Basis-Dateien früh stoppen.

Sign-Off-Qualität prüfen: `python3 scripts/validate_golive_signoff.py` (oder `--strict` für harte Freigabeprüfung).

Schneller End-to-End Gate-Check: `python3 scripts/run_release_gate.py --serve` erzeugt `GO_LIVE_RELEASE_GATE.md` und `GO_LIVE_RELEASE_GATE.json` (Preflight + Strict-Signoff in einem Lauf, listet jetzt auch konkrete Blocker).
Zwischenstand ohne finalen Signoff-Block: `python3 scripts/run_release_gate.py --serve --allow-open-signoff`.

Post-Deploy Smoke (Live-URL): `python3 scripts/run_postdeploy_smoke.py --base-url https://<deine-domain>/<pfad> --strict` erzeugt `GO_LIVE_POSTDEPLOY_SMOKE.md` und `GO_LIVE_POSTDEPLOY_SMOKE.json`.
