# Netlify-Einbindung: Tools-Seite ohne Geschwindigkeitsverlust

## Kurzantwort (empfohlen)
Für **beste Performance deiner Hauptseite**:
1. Tools auf **eigener URL/Subdomain** betreiben (z. B. `tools.deinedomain.de`).
2. Auf der Hauptseite nur **leichtgewichtig verlinken** (CTA/Button).
3. Optional nur bei Bedarf per `iframe` laden (lazy), nicht sofort beim Seitenstart.

Damit bleibt die Hauptseite schnell, und die Tools laden erst, wenn Nutzer sie wirklich brauchen.

---

## Warum nicht direkt hart einbetten?
Deine Tools bestehen aus mehreren umfangreichen HTML-Apps mit JS, Tabellen, Exports, Canvas/PDF etc.
Wenn du diese direkt auf der Startseite mitlädst, passieren meist:
- mehr JavaScript beim Initial-Load,
- schlechtere Core Web Vitals (LCP/INP),
- höhere CPU/Memory-Last auf Mobile.

**Fazit:** Direkte Einbettung auf jeder Seite ist nur sinnvoll, wenn ein Tool zentraler Bestandteil genau dieser Seite ist.

---

## Empfohlene Architektur

### Option A (Best Practice): Subdomain + Link
- Deploy dieses Repo als eigene Netlify-Site (oder Domain-Alias) unter z. B. `tools.deinedomain.de`.
- Hauptseite verlinkt auf die Tools-Landingpage (`index.html`).
- Vorteil: völlige Entkopplung von Performance und Stabilität.

### Option B (Hybrid): Lazy `iframe` nur nach Klick
- Hauptseite zeigt erst Vorschau/Karte/CTA.
- Erst bei Klick wird `iframe.src` gesetzt.
- Vorteil: Tool wirkt „eingebettet“, aber ohne Initial-Load-Strafe.

### Option C (Nicht empfohlen): Sofortige Full-Embed
- `iframe`/App beim Initial-Render laden.
- Nur sinnvoll für sehr kleine Tools (hier eher nicht).

---

## Konkrete Umsetzung auf Netlify

### 1) Deployment
- Repo wie gehabt deployen.
- Primärdomain/Subdomain auf Tools-Site zeigen lassen.
- HTTPS aktiv (Netlify standardmäßig).

### 2) Hauptseite verlinken
```html
<a href="https://tools.deinedomain.de" target="_blank" rel="noopener">
  Zu den Profi-Tools
</a>
```

### 3) Optional: Lazy-Embed nach Klick
```html
<button id="openTools">Tools öffnen</button>
<iframe id="toolsFrame" title="Tools" loading="lazy" style="width:100%;height:80vh;border:0"></iframe>
<script>
  document.getElementById('openTools').addEventListener('click', () => {
    const f = document.getElementById('toolsFrame');
    if (!f.src) f.src = 'https://tools.deinedomain.de';
  });
</script>
```

---

## SEO/UX Empfehlung
- Für Marketing-/SEO-Seiten: **Link statt Embed**.
- Für Anwendungsseiten im Kundenportal: **lazy Embed** okay.
- Mobile zuerst testen (Android Chrome + iOS Safari).

---

## Entscheidungsmatrix
- **Maximale Geschwindigkeit Hauptseite:** Option A.
- **Gute Mischung aus UX + Performance:** Option B.
- **Einbettung um jeden Preis:** Option C (nur wenn unvermeidbar).

**Empfehlung für deinen Fall:** **Option A** (eigene URL/Subdomain) und von der Homepage prominent verlinken.
