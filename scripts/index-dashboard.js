const vendorFiles = [
      'vendor/jspdf.umd.min.js',
      'vendor/xlsx.full.min.js',
      'vendor/jspdf.plugin.autotable.min.js',
      'vendor/fontawesome.all.min.js'
    ];

    const toolFiles = [
      'Holz-Tools.html',
      'Sparrenlängen-Rechner%20V%202.3.html',
      'V18.5.2%20Laser%20Entfernungsmesser%20Tool.html',
      'V6.1.18_BM_HS_DD%20.html',
      'V8.2Abwiklung%20Verschnittoptimierung.html',
      'V9_7_RestauroMap_fix.html',
      'v2.3.2_Abwicklung%20Kegelstumpf.html'
    ];

    async function probePath(path, method = 'HEAD') {
      const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
      const timeoutId = controller ? setTimeout(() => controller.abort(), 4500) : null;
      try {
        const resp = await fetch(path, method === 'HEAD'
          ? { method: 'HEAD', cache: 'no-store', signal: controller?.signal }
          : { method: 'GET', cache: 'no-store', headers: { Range: 'bytes=0-0' }, signal: controller?.signal }
        );
        return { ok: (resp.ok || resp.status === 206), status: resp.status, path, method };
      } catch (_) {
        return { ok: false, status: 0, path, method };
      } finally {
        if (timeoutId) clearTimeout(timeoutId);
      }
    }

    function candidatePaths(file) {
      const base = new URL('.', window.location.href).pathname;
      const normalized = file.replace(/^\/+/, '');
      return [
        normalized,
        './' + normalized,
        (base.endsWith('/') ? base : base + '/') + normalized
      ].filter((v, i, arr) => arr.indexOf(v) === i);
    }

    async function fileExists(file) {
      const candidates = candidatePaths(file);
      for (const c of candidates) {
        const head = await probePath(c, 'HEAD');
        if (head.ok) return head;
        const get = await probePath(c, 'GET');
        if (get.ok) return get;

        // hosts/proxies sometimes fail first probe sporadically (status 0) -> one cache-busted retry
        if ((head.status === 0 || get.status === 0)) {
          const bust = withCacheBuster(c);
          const retryHead = await probePath(bust, 'HEAD');
          if (retryHead.ok) return { ...retryHead, path: c };
          const retryGet = await probePath(bust, 'GET');
          if (retryGet.ok) return { ...retryGet, path: c };
        }
      }
      return { ok: false, status: 0, path: candidates[0], method: 'HEAD' };
    }

    function prettyPath(p) {
      try { return decodeURIComponent(String(p || '')); } catch (_) { return String(p || ''); }
    }

    function withCacheBuster(path) {
      const sep = String(path).includes('?') ? '&' : '?';
      return `${path}${sep}rlz=${Date.now()}`;
    }

    async function renderStatus(listId, summaryId, files, labelOk) {
      const list = document.getElementById(listId);
      const summary = document.getElementById(summaryId);
      if (!list || !summary) return { okCount: 0, total: files.length, checks: [] };

      const checks = await Promise.all(files.map(async (file) => { const r = await fileExists(file); return { file, ...r }; }));
      const okCount = checks.filter(x => x.ok).length;
      const allOk = okCount === checks.length;

      summary.innerHTML = allOk
        ? `<span class="status-ok">${labelOk}:</span> alles vorhanden.`
        : `<span class="status-miss">Unvollständig:</span> ${checks.length - okCount} Datei(en) fehlen.`;

      const onlyMissing = document.getElementById('showMissingOnly')?.checked;
      const visible = onlyMissing ? checks.filter(x => !x.ok) : checks;

      list.innerHTML = visible.map(({ file, ok, method, status, path }) =>
        `<li><code>${file}</code>: <span class="${ok ? 'status-ok' : 'status-miss'}">${ok ? 'vorhanden' : 'fehlt'}</span> <span class="diag">(${method} ${status || 'ERR'} • ${prettyPath(path)})</span></li>`
      ).join('') || '<li><span class="status-ok">Keine fehlenden Dateien.</span></li>';

      return { okCount, total: checks.length, checks };
    }

    function setGlobalStrictLocal(enabled) {
      const links = document.querySelectorAll('.tool-link');
      links.forEach((a) => {
        const base = a.dataset.base || a.getAttribute('href').split('?')[0];
        a.href = enabled ? `${base}?strictLocal=1` : base;
      });
      const state = document.getElementById('strictLocalState');
      if (state) state.textContent = enabled ? 'Strict-Local global aktiv (alle Öffnen-Links nutzen ?strictLocal=1).' : 'Standardmodus aktiv.';
      localStorage.setItem('strictLocalGlobal', enabled ? '1' : '0');
    }

    async function runReadinessChecks() {
      const vendor = await renderStatus('vendor-status', 'vendor-summary', vendorFiles, 'Strict-Local bereit');
      const tools = await renderStatus('tool-status', 'tool-summary', toolFiles, 'Go-Live bereit');
      const generatedAt = new Date().toISOString();
      const basePath = new URL('.', window.location.href).pathname;

      const missingVendor = vendor.checks.filter((x) => !x.ok).map((x) => x.file);
      const missingTools = tools.checks.filter((x) => !x.ok).map((x) => x.file);
      const blockers = [];
      if (missingVendor.length) blockers.push(`Vendor-Dateien fehlen: ${missingVendor.length}`);
      if (missingTools.length) blockers.push(`Tool-Dateien fehlen: ${missingTools.length}`);
      const recommendedGoLive = blockers.length === 0;

      window.__readinessReport = {
        generatedAt,
        strictLocalGlobal: localStorage.getItem('strictLocalGlobal') === '1',
        onlyMissingView: document.getElementById('showMissingOnly')?.checked || false,
        basePath,
        vendor,
        tools,
        blockers,
        missingVendor,
        missingTools,
        recommendedGoLive
      };

      const ts = document.getElementById('lastCheckAt');
      if (ts) ts.textContent = `Letzter Check: ${new Date(generatedAt).toLocaleString('de-DE')}`;
      const bp = document.getElementById('basePathLabel');
      if (bp) bp.textContent = basePath;

      const box = document.getElementById('overallStatus');
      const summary = document.getElementById('overallSummary');
      const blockerText = document.getElementById('overallBlockers');
      const missingFilesText = document.getElementById('overallMissingFiles');
      if (box && summary && blockerText && missingFilesText) {
        box.classList.toggle('ok', recommendedGoLive);
        box.classList.toggle('bad', !recommendedGoLive);
        box.querySelector('h4').textContent = recommendedGoLive
          ? 'Go-Live Entscheidung: bereit ✅'
          : 'Go-Live Entscheidung: noch nicht bereit ⚠️';
        summary.textContent = recommendedGoLive
          ? 'Alle geprüften Dateien sind vorhanden. Release-Freigabe ist technisch möglich.'
          : 'Es bestehen noch Blocker. Bitte vor Veröffentlichung beheben.';
        blockerText.textContent = blockers.length ? `Blocker: ${blockers.join(' | ')}` : 'Keine Blocker erkannt.';

        const missingList = [...missingVendor, ...missingTools];
        missingFilesText.textContent = missingList.length
          ? `Fehlende Dateien: ${missingList.slice(0, 6).join(' | ')}${missingList.length > 6 ? ' …' : ''}`
          : 'Fehlende Dateien: keine.';
      }
    }

    const strictToggle = document.getElementById('strictLocalToggle');
    if (strictToggle) {
      const urlStrict = new URLSearchParams(location.search).get('strictLocal') === '1';
      const stored = localStorage.getItem('strictLocalGlobal') === '1';
      strictToggle.checked = urlStrict || stored;
      setGlobalStrictLocal(strictToggle.checked);
      strictToggle.addEventListener('change', () => setGlobalStrictLocal(strictToggle.checked));
    }

    document.getElementById('exportReadinessBtn')?.addEventListener('click', () => {
      const data = window.__readinessReport || { generatedAt: new Date().toISOString(), info: 'Noch keine Checks ausgeführt' };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `toolsammlung-readiness-${new Date().toISOString().slice(0,10)}.json`;
      a.click();
      URL.revokeObjectURL(a.href);
    });



    const showMissingOnly = document.getElementById('showMissingOnly');
    if (showMissingOnly) {
      showMissingOnly.checked = localStorage.getItem('readinessShowMissingOnly') === '1';
      showMissingOnly.addEventListener('change', async () => {
        localStorage.setItem('readinessShowMissingOnly', showMissingOnly.checked ? '1' : '0');
        await runReadinessChecks();
      });
    }

    document.getElementById('copySummaryBtn')?.addEventListener('click', async () => {
      const r = window.__readinessReport;
      const text = r
        ? `Go-Live Check ${r.generatedAt}
BasePath: ${r.basePath}
Vendor: ${r.vendor.okCount}/${r.vendor.total}
Tools: ${r.tools.okCount}/${r.tools.total}`
        : 'Noch kein Readiness-Report vorhanden.';
      const ok = await copyText(text);
      alert(ok ? 'Kurzstatus in Zwischenablage kopiert.' : 'Kopieren nicht möglich.');
    });

    async function copyText(text) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (_) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        const ok = document.execCommand('copy');
        document.body.removeChild(ta);
        return ok;
      }
    }

    document.getElementById('copyBlockersBtn')?.addEventListener('click', async () => {
      const r = window.__readinessReport;
      const parts = [];
      if (r?.blockers?.length) parts.push('Blocker:', ...r.blockers.map((x) => `- ${x}`));
      if (r?.missingVendor?.length) parts.push('', 'Fehlende Vendor-Dateien:', ...r.missingVendor.map((x) => `- ${x}`));
      if (r?.missingTools?.length) parts.push('', 'Fehlende Tool-Dateien:', ...r.missingTools.map((x) => `- ${x}`));
      const text = r
        ? (parts.length ? parts.join('\n') : 'Keine Blocker erkannt.')
        : 'Noch kein Readiness-Report vorhanden.';
      const ok = await copyText(text);
      alert(ok ? 'Blocker in Zwischenablage kopiert.' : 'Kopieren nicht möglich.');
    });

    document.getElementById('refreshChecksBtn')?.addEventListener('click', async () => {
      const btn = document.getElementById('refreshChecksBtn');
      if (btn) { btn.disabled = true; btn.textContent = 'Prüfe …'; }
      try { await runReadinessChecks(); }
      finally { if (btn) { btn.disabled = false; btn.textContent = 'Checks neu laden'; } }
    });

    runReadinessChecks();
