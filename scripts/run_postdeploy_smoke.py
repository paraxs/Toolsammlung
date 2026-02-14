#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run post-deploy smoke checks against a deployment URL.")
    parser.add_argument("--base-url", required=True, help="Deployed base URL, e.g. https://example.com/tools")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any failed smoke check.")
    return parser.parse_args()


def fetch(url: str) -> tuple[int | str, str]:
    try:
        with urllib.request.urlopen(url, timeout=8) as res:
            body = res.read(180000).decode("utf-8", errors="ignore")
            return res.status, body
    except Exception as exc:
        return "ERR", str(exc)


def check_contains(url: str, needle: str) -> dict:
    status, body = fetch(url)
    ok = isinstance(status, int) and 200 <= status < 400 and needle in body
    return {"url": url, "status": status, "needle": needle, "ok": ok}


def main() -> int:
    args = parse_args()
    now = datetime.now().isoformat(timespec="seconds")
    base = args.base_url.rstrip("/")

    checks = []
    checks.append(check_contains(f"{base}/index.html", "tool-link"))
    checks.append(check_contains(f"{base}/index.html", "scripts/index-dashboard.js"))

    for tool in TOOLS:
        encoded = urllib.parse.quote(tool)
        checks.append(check_contains(f"{base}/{encoded}", "<html"))
        checks.append(check_contains(f"{base}/{encoded}?strictLocal=1", "<html"))

    ok_count = sum(1 for row in checks if row["ok"])
    total = len(checks)
    summary = {"ok": ok_count, "total": total}

    payload = {
        "generatedAt": now,
        "baseUrl": base,
        "checks": checks,
        "summary": summary,
    }

    Path("GO_LIVE_POSTDEPLOY_SMOKE.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# GO_LIVE_POSTDEPLOY_SMOKE.md",
        "",
        f"Erstellt: {now}",
        f"Base URL: `{base}`",
        "",
        "## Ergebnis",
        "",
        f"- Smoke Checks OK: **{ok_count}/{total}**",
        "",
        "| URL | Status | Ergebnis |",
        "|---|---:|---|",
    ]
    for row in checks:
        md.append(f"| `{row['url']}` | {row['status']} | {'✅' if row['ok'] else '❌'} |")

    Path("GO_LIVE_POSTDEPLOY_SMOKE.md").write_text("\n".join(md), encoding="utf-8")
    print("generated GO_LIVE_POSTDEPLOY_SMOKE.json + GO_LIVE_POSTDEPLOY_SMOKE.md")

    if args.strict and ok_count != total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
