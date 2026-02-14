# GO_LIVE_RELEASE_GATE.md

Erstellt: 2026-02-14T08:52:31

## Ergebnis

- Gesamtstatus: ❌ NO-GO (Blocker vorhanden)
- Server erreichbar (127.0.0.1:8000): ✅
- Modus: Strikt (Preflight + Signoff müssen grün sein)
- Preflight Summary: Vendor 4/4, URLs 14/14

## Check-Details

| Check | Exit-Code | Dauer (s) |
|---|---:|---:|
| Preflight | 0 | 0.16 |
| Signoff Strict | 1 | 0.06 |

## Hinweise

- Preflight benötigt einen erreichbaren lokalen Server (default Port 8000, alternativ `--port`).
- Strikter Modus bricht ab, solange Platzhalter oder Fail-Zeilen in `GO_LIVE_SIGNOFF.md` enthalten sind.
- Für Zwischenstände kann `--allow-open-signoff` genutzt werden, um Infrastruktur-Blocker separat zu beurteilen.
