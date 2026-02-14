# Go-Live Checkliste für die Toolsammlung

Diese Liste ist auf dieses Repository zugeschnitten und dient als finale Freigabe vor der Einbindung in die Haupt-Website.

## 1) Hosting & Dateibereitstellung
- [ ] Alle HTML-Dateien unverändert auf den Webserver hochladen.
- [ ] `index.html` als Einstiegspunkt verwenden (nicht direkt `file://` oder `content://` öffnen).
- [ ] Prüfen, dass Dateinamen **exakt** übernommen werden (inkl. Leerzeichen/Groß-/Kleinschreibung).
- [ ] HTTPS aktivieren (Pflicht wegen Browser-Sicherheitsregeln und stabiler CDN-Ladung).

## 2) Browser-Kompatibilität
- [ ] Android Chrome (aktuell) testen.
- [ ] iOS Safari (aktuell) testen.
- [ ] Desktop Chrome/Edge/Firefox testen.
- [ ] Testen im normalen Modus + Privatmodus (LocalStorage-Verhalten).

## 3) Funktionale Freigabe je Tool
- [ ] Holz-Tools: Berechnung + Export testen.
- [ ] Bedarfsermittlung Holzschindel: Berechnung + PDF testen.
- [ ] Abwicklung & Verschnittoptimierung: Eingabe, Berechnung, Speicherung testen.
- [ ] Kegelstumpf-Rechner: Rechenweg + Export testen.
- [ ] Sparrenlängen-Rechner: Berechnung + Persistenz testen.
- [ ] Laser Entfernungsmesser: Datensatz anlegen, speichern, löschen testen.
- [ ] RestauroMap: Zeichnen + PDF/Export testen.

## 4) Sicherheit & Einbettung in Hauptseite
- [ ] Falls per `<iframe>` eingebunden: `sandbox` bewusst setzen (mind. `allow-scripts allow-same-origin`, falls nötig erweitern).
- [ ] `X-Frame-Options` / CSP (`frame-ancestors`) so konfigurieren, dass Einbettung erlaubt ist.
- [ ] CSP für externe CDNs freigeben, wenn erforderlich (`cdnjs.cloudflare.com`, `fonts.googleapis.com`).
- [ ] `rel="noopener"` bei externen Links beibehalten.

## 5) Performance & Stabilität
- [ ] GZIP/Brotli aktivieren.
- [ ] Statische Assets mit Caching versehen (`Cache-Control`), aber HTML eher kurz cachen.
- [ ] Bei Updates Cache-Busting verwenden.
- [ ] 404/500-Logs nach Deployment prüfen.

## 6) Datenschutz / Betrieb
- [ ] Datenschutzhinweis ergänzen: Tools verwenden `localStorage` im Browser.
- [ ] Klären, ob CDN-Nutzung datenschutzrechtlich für dein Setup passt.
- [ ] Optional: self-hosted Libraries nutzen, wenn externe CDNs vermieden werden sollen.

## 7) Wichtige Erkenntnisse aus dem Audit
- Der Font-Awesome Script-Tag in `V8.2Abwiklung Verschnittoptimierung.html` hatte eine ungültige SRI-Checksumme und wurde vom Browser blockiert.
- Dieser Fehler wurde behoben, indem das fehlerhafte `integrity`-Attribut entfernt wurde.

## 8) Finaler Go-Live Ablauf (empfohlen)
1. Staging-Deployment.
2. Obige Checkliste vollständig abhaken.
3. Ein letzter Mobile-Test auf echtem Gerät.
4. Erst dann Production-Deployment.
5. Nach 24h: Error-Logs + Nutzerfeedback prüfen.
