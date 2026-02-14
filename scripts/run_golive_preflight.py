#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

TOOLS = [
    "Holz-Tools.html",
    "Sparrenlängen-Rechner V 2.3.html",
    "V18.5.2 Laser Entfernungsmesser Tool.html",
    "V6.1.18_BM_HS_DD .html",
    "V8.2Abwiklung Verschnittoptimierung.html",
    "V9_7_RestauroMap_fix.html",
    "v2.3.2_Abwicklung Kegelstumpf.html",
]
VENDOR = [
    "vendor/jspdf.umd.min.js",
    "vendor/xlsx.full.min.js",
    "vendor/jspdf.plugin.autotable.min.js",
    "vendor/fontawesome.all.min.js",
]


def check_url(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=6) as res:
            return {"ok": 200 <= res.status < 400, "status": res.status, "url": url}
    except Exception as exc:
        return {"ok": False, "status": "ERR", "url": url, "error": str(exc)}


def main() -> None:
    now = datetime.now().isoformat(timespec="seconds")

    vendor_rows = []
    for file in VENDOR:
        p = Path(file)
        vendor_rows.append({"file": file, "exists": p.exists(), "size": p.stat().st_size if p.exists() else 0})

    url_rows = []
    for file in TOOLS:
        encoded = urllib.parse.quote(file)
        url_rows.append(check_url(f"http://127.0.0.1:8000/{encoded}"))
        url_rows.append(check_url(f"http://127.0.0.1:8000/{encoded}?strictLocal=1"))

    report = {
        "generatedAt": now,
        "vendor": vendor_rows,
        "urlChecks": url_rows,
        "summary": {
            "vendorPresent": sum(1 for r in vendor_rows if r["exists"]),
            "vendorTotal": len(vendor_rows),
            "urlOk": sum(1 for r in url_rows if r["ok"]),
            "urlTotal": len(url_rows),
        },
    }

    Path("GO_LIVE_PREFLIGHT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# GO_LIVE_PREFLIGHT.md",
        "",
        f"Erstellt: {now}",
        "",
        "## Zusammenfassung",
        "",
        f"- Vendor vorhanden: **{report['summary']['vendorPresent']}/{report['summary']['vendorTotal']}**",
        f"- URL Checks OK: **{report['summary']['urlOk']}/{report['summary']['urlTotal']}**",
        "",
        "## Vendor-Dateien",
        "",
        "| Datei | Vorhanden | Größe (Bytes) |",
        "|---|---|---:|",
    ]
    for r in vendor_rows:
        lines.append(f"| `{r['file']}` | {'✅' if r['exists'] else '❌'} | {r['size']} |")

    lines += [
        "",
        "## URL-Checks (Standard + Strict-Local)",
        "",
        "| URL | Status | Ergebnis |",
        "|---|---:|---|",
    ]
    for r in url_rows:
        lines.append(f"| `{r['url']}` | {r['status']} | {'✅' if r['ok'] else '❌'} |")

    Path("GO_LIVE_PREFLIGHT.md").write_text("\n".join(lines), encoding="utf-8")
    print("generated GO_LIVE_PREFLIGHT.json + GO_LIVE_PREFLIGHT.md")


if __name__ == "__main__":
    main()
