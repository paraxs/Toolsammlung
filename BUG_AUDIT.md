# Bug-Audit mit Prioritäten (Stand: aktuell)

## Ziel
Stabilität erhöhen und UI vereinheitlichen, ohne funktionierende Berechnungslogik zu beschädigen.

## Priorität P0 (kritisch) — **gestartet**
1. **Kein zentraler Einstieg für alle 7 Tools**
   - Risiko: Veraltete Direktlinks, unklare Navigation.
   - **Umgesetzt:** `index.html` als zentrale Startseite mit Links auf alle Tools.
   - Nächster Schritt: optionaler Einbettungsmodus (`iframe`) für Homepage-Integration.

## Priorität P1 (hoch)
1. **Uneinheitliche Design-Systeme pro Tool**
   - Unterschiedliche Farben, Radius, Typografie, Fokuszustände.
   - Maßnahme: `styles/foundation.css` als gemeinsames Foundation-Layer (aktiv).
2. **Externe CDN-Abhängigkeiten**
   - XLSX/jsPDF/AutoTable/FontAwesome (CDN) + zuvor Google Fonts.
   - **Umgesetzt:** Google-Fonts entfernt (Systemschrift), CDN-Skripte mit `onerror`-Warnungen abgesichert.
   - Nächster Schritt: lokale Vendor-Dateien einchecken und CDN vollständig ersetzen.

## Priorität P2 (mittel)
1. **Dateinamen/Versionen inkonsistent**
   - Risiko: Verlinkungs-/Deploymentfehler.
   - Maßnahme: Umbenennung + Redirect/Link-Mapping.
2. **Große Monolith-HTML-Dateien**
   - Erschwert Review/Regressionstests.
   - Maßnahme: später modularisieren (Styles/Utils/Exports).

## Harmonisierung (schrittweise, regressionsarm)
1. **Phase 1:** Foundation-Layer (done).
2. **Phase 2:** zentrales Start-UI (P0 started, done via `index.html`).
3. **Phase 3:** komponentenweise Vereinheitlichung in kleinen Commits inkl. Smoke-Checks.
