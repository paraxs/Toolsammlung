# Bug-Audit mit Prioritäten (Stand: aktuell)

## Ziel
Stabilität erhöhen und UI vereinheitlichen, ohne funktionierende Berechnungslogik zu beschädigen.

## Priorität P0 (kritisch) — abgeschlossen
1. **Zentraler Einstieg für alle 7 Tools**
   - Umsetzung: `index.html` als zentrale Startseite mit Links auf alle Tools.
   - Ergebnis: konsistente Navigation und besseres Einbetten in die Homepage.

## Priorität P1 (hoch) — in Umsetzung
1. **Uneinheitliche Design-Systeme pro Tool**
   - Problem: unterschiedliche Schrift-/Fokus-/Basisstile.
   - Umsetzung: `styles/foundation.css` als Foundation-Layer; zusätzliche Harmonisierung der Fonts (System-/Foundation-Font statt externer Webfont).

2. **Externe CDN-Abhängigkeiten (Cookie/Privacy)**
   - Problem: direkte Drittanbieter-Requests für Kernfunktionen.
   - Umsetzung (dieser Schritt): alle externen Script-Libs auf **lokal-first mit CDN-Fallback** umgestellt.
     - Beispiel: `vendor/jspdf.umd.min.js` → Fallback auf CDN nur wenn lokal fehlt.
   - Ergebnis: Bei lokal abgelegten Vendor-Dateien funktionieren Tools ohne externe Requests.

## Priorität P2 (mittel)
1. **Dateinamen/Versionen inkonsistent**
   - Risiko: Verlinkungs-/Deploymentfehler.
   - Maßnahme: Umbenennung + Redirect/Link-Mapping.
2. **Große Monolith-HTML-Dateien**
   - Erschwert Review/Regressionstests.
   - Maßnahme: später modularisieren (Styles/Utils/Exports).

## Nächster sicherer Schritt
1. `vendor/` mit geprüften Bibliotheken befüllen (`xlsx`, `jspdf`, `autotable`, `fontawesome`).
2. Danach CDN-Fallback optional abschaltbar machen (Cookie-Policy-Mode).
3. Komponentenweise UI-Harmonisierung (Buttons/Inputs/Cards) in kleinen Commits mit Smoke-Checks.
