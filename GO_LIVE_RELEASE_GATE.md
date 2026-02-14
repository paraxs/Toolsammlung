# GO_LIVE_RELEASE_GATE.md

Erstellt: 2026-02-14T17:05:06

## Ergebnis

- Gesamtstatus: ✅ FREIGABE MÖGLICH
- Server erreichbar (127.0.0.1:8000): ✅
- Modus: Strikt (Preflight + Signoff müssen grün sein)
- Preflight Summary: Vendor 4/4, Core 3/3, URLs 14/14

## Check-Details

| Check | Exit-Code | Dauer (s) |
|---|---:|---:|
| Preflight | 0 | 0.15 |
| Signoff Strict | 0 | 0.05 |

## Hinweise

- Preflight läuft im Strict-Modus über die vom Gate gesetzte Base-URL (default 127.0.0.1:8000 oder `--port`).
- Strikter Modus bricht ab, solange Platzhalter oder Fail-Zeilen in `GO_LIVE_SIGNOFF.md` enthalten sind.
- Für Zwischenstände kann `--allow-open-signoff` genutzt werden, um Infrastruktur-Blocker separat zu beurteilen.
