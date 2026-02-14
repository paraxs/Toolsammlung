# GO_LIVE_120MIN.md

## Ziel
Schneller, sicherer Go-Live-Durchlauf in 120 Minuten ohne neue Features.

## 0) Freeze (T-120 bis T-110)
- Keine neuen Features mehr.
- Nur Blocker-Fixes.
- Branch/Commit für Release markieren.

## 1) Infrastruktur-Check (T-110 bis T-90)
- `python3 scripts/run_golive_preflight.py` ausführen (liefert Preflight-Report).
- `index.html` laden.
- Go-Live Cockpit prüfen (Vendor + Tool-Status).
- Standard + `?strictLocal=1` für mindestens 1 Tool smoke-testen.

## 2) Fachcheck Standard (T-90 bis T-50)
Für alle 7 Tools:
- 1x Eingaben
- 1x Import (wenn vorhanden)
- 1x Export (PDF/XLSX/JSON je Tool)
- 1x Visualisierung prüfen

Ergebnis in `GO_LIVE_MANUAL_SCENARIOS.md`/Signoff notieren.

## 3) Fachcheck Strict-Local (T-50 bis T-20)
Für alle 7 Tools mit `?strictLocal=1`:
- Gleiche 4 Checks wie oben.
- Besonders Export/Icon prüfen.

## 4) Sign-Off (T-20 bis T-10)
- `python3 scripts/generate_golive_signoff.py`
- `GO_LIVE_SIGNOFF.md` ausfüllen (Pass/Fail je Tool/Modus).
- Go/No-Go Entscheidung dokumentieren.

## 5) Live-Schaltung + Smoke (T-10 bis T+10)
- Deployment ausrollen.
- 3 schnelle Live-Smokes:
  - Startseite / Tool öffnen
  - Export läuft
  - Keine kritischen JS-Fehler in Konsole

## Hard Stop Kriterien (nicht live gehen)
- Kritischer Exportpfad defekt.
- Import zerstört Daten oder UI.
- Visualisierung offensichtlich falsch/instabil.
- Strict-Local bricht in produktrelevanten Tools.
