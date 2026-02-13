# GO_LIVE_MANUAL_SCENARIOS.md

Erstellt: 2026-02-13 17:48:27

## Ziel

Kurzer, nachvollziehbarer Fach-Szenario-Durchlauf pro Tool mit Echtdaten-Checkpunkten für **Export / Import / Visualisierung** in **Standard** und **Strict-Local**.

## Durchgeführter Batch in dieser Umgebung

- URL-Erreichbarkeit (lokaler Server): 7 Tools × 2 Modi geprüft.
- Quelltext-Szenario-Hinweise geprüft (Export-/Import-UI, Canvas/SVG-Indikatoren).
- Hinweis: echter Fachklicktest mit Echtdaten (Datei importieren, exportierte Datei öffnen, visuelle Plausibilität bewerten) muss im Zielbrowser erfolgen.

## Matrix

| Tool | Standard URL | Strict-Local URL | Export-Hinweis | Import-Hinweis | Visualisierung-Hinweis | Manuelle Echtdaten-Aktionen |
|---|---|---|---|---|---|---|
| Holz-Tools | ✅ | ✅ | ✅ | ✅ | ✅ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |
| Sparrenlängen-Rechner | ✅ | ✅ | ⚠️ | ✅ | ✅ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |
| Laser Entfernungsmesser | ✅ | ✅ | ✅ | ✅ | ✅ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |
| BM/HS/DD | ✅ | ✅ | ✅ | ✅ | ✅ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |
| Abwicklung Verschnittoptimierung | ✅ | ✅ | ✅ | ✅ | ⚠️ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |
| RestauroMap | ✅ | ✅ | ✅ | ✅ | ✅ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |
| Abwicklung Kegelstumpf | ✅ | ✅ | ✅ | ✅ | ✅ | 1) Eingaben setzen 2) Import durchführen 3) Export erzeugen 4) Visual prüfen |

## Freigabe-Kriterium vor Öffentlichkeit

- Pro Tool je Modus ein erfolgreicher Fachdurchlauf ohne JS-Fehlerbanner und ohne sichtbare Render-Artefakte.
- Exportdatei lässt sich öffnen (PDF/XLSX/JSON je Tool-Fall).
- Importierte Echtdaten sind im UI sichtbar und konsistent gespeichert/verarbeitet.
- Visualisierung (Canvas/SVG) bleibt nach Eingaben/Import plausibel und stabil.

## Ergebnis dieser Runde

- Infrastruktur-/Erreichbarkeits-Teil: dokumentiert und reproduzierbar.
- Fachklick-Teil: mit obiger Matrix klar vorbereitet; letzte manuelle Browser-Abnahme bleibt vor Public Go-Live erforderlich.