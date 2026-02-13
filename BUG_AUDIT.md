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


3. **P1 UI-Harmonisierung (toolweise, sicher)**
   - Umsetzung aktiv in allen 7 Tool-Seiten (`Holz-Tools.html`, `Sparrenlängen-Rechner V 2.3.html`, `V18.5.2 Laser Entfernungsmesser Tool.html`, `V6.1.18_BM_HS_DD .html`, `V8.2Abwiklung Verschnittoptimierung.html`, `V9_7_RestauroMap_fix.html`, `v2.3.2_Abwicklung Kegelstumpf.html`) via opt-in `body.p1-harmony`.
   - Fokus auf Buttons/Inputs/Cards mit niedriger CSS-Spezifität, damit Berechnungs-/Canvaslogik unberührt bleibt.

## Priorität P2 (mittel)
1. **Dateinamen/Versionen inkonsistent**
   - Risiko: Verlinkungs-/Deploymentfehler.
   - Maßnahme: Umbenennung + Redirect/Link-Mapping.
2. **Große Monolith-HTML-Dateien**
   - Erschwert Review/Regressionstests.
   - Maßnahme: später modularisieren (Styles/Utils/Exports).

## Nächster sicherer Schritt
1. ✅ `vendor/` mit Bibliotheken befüllt (`xlsx`, `jspdf`, `autotable`, `fontawesome`).
2. CDN-Fallback ist jetzt optional abschaltbar via `?strictLocal=1` (Cookie-Policy-Mode).
3. Komponentenweise UI-Harmonisierung (Buttons/Inputs/Cards) in kleinen Commits mit Smoke-Checks.
4. Startseite mit Strict-Local Direktlinks je Tool ergänzt.
5. Startseite prüft jetzt lokale `vendor/*` Dateien (Statusanzeige).
6. Vendor-Status-Prüfung robust gemacht (HEAD mit GET-Fallback).
7. Vendor-Status-Fallback optimiert (Range-GET statt Voll-Download bei großen Dateien).
8. Startseite um globalen Strict-Local Toggle ergänzt (produktiver Privacy-Workflow).
9. Startseite um Go-Live Readiness-Checks erweitert (Tool-Dateien + Vendor-Dateien + JSON-Report-Export).
10. Startseite visuell an Website-CD angenähert (Hero/CTA/Panel-Struktur für einheitliche Unterseiten-Optik).
