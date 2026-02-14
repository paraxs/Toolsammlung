#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

PREFLIGHT_JSON = Path("GO_LIVE_PREFLIGHT.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run combined go-live release gate (preflight + strict signoff validation)."
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start a temporary local server (python -m http.server) while running checks.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for temporary server and reachability check (default: 8000).",
    )
    parser.add_argument(
        "--allow-open-signoff",
        action="store_true",
        help="Do not fail overall gate when strict signoff still contains template placeholders/fails.",
    )
    return parser.parse_args()


def run_command(cmd: list[str]) -> dict:
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "cmd": " ".join(cmd),
        "code": proc.returncode,
        "durationSec": round(time.time() - started, 2),
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def server_reachable(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=2) as res:
            return 200 <= res.status < 400
    except Exception:
        return False


def safe_load_preflight_summary() -> dict:
    if not PREFLIGHT_JSON.exists():
        return {}

    try:
        payload = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}

    summary = payload.get("summary")
    return summary if isinstance(summary, dict) else {}


def collect_blockers(
    preflight_result: dict,
    signoff_result: dict,
    preflight_summary: dict,
    allow_open_signoff: bool,
) -> list[str]:
    blockers: list[str] = []

    if preflight_result.get("code") != 0:
        blockers.append("Preflight fehlgeschlagen (Vendor/URL-Checks nicht vollständig grün).")

    if preflight_summary:
        vp = preflight_summary.get("vendorPresent")
        vt = preflight_summary.get("vendorTotal")
        uo = preflight_summary.get("urlOk")
        ut = preflight_summary.get("urlTotal")
        if isinstance(vp, int) and isinstance(vt, int) and vp < vt:
            blockers.append(f"Vendor-Checks unvollständig: {vp}/{vt} vorhanden.")
        cp = preflight_summary.get("coreOk")
        ct = preflight_summary.get("coreTotal")
        if isinstance(cp, int) and isinstance(ct, int) and cp < ct:
            blockers.append(f"Core-Checks unvollständig: {cp}/{ct} erreichbar.")
        if isinstance(uo, int) and isinstance(ut, int) and uo < ut:
            blockers.append(f"URL-Checks unvollständig: {uo}/{ut} erreichbar.")

    if signoff_result.get("code") != 0 and not allow_open_signoff:
        blockers.append("Strict-Signoff nicht bestanden (Template/Fails/uneindeutige Entscheidung).")

    for line in signoff_result.get("stdout", "").splitlines():
        if line.strip().startswith("❌"):
            blockers.append(line.strip().lstrip("❌").strip())

    # Deduplizieren bei stabiler Reihenfolge
    dedup: list[str] = []
    for b in blockers:
        if b not in dedup:
            dedup.append(b)
    return dedup


def main() -> int:
    args = parse_args()
    now = datetime.now().isoformat(timespec="seconds")

    server_proc: subprocess.Popen[str] | None = None
    server_started = False

    if args.serve:
        server_proc = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(args.port)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        for _ in range(20):
            if server_reachable(args.port):
                server_started = True
                break
            time.sleep(0.25)

    has_server = server_reachable(args.port)
    preflight_result: dict = {
        "cmd": f"{sys.executable} scripts/run_golive_preflight.py --strict --base-url http://127.0.0.1:{args.port}",
        "code": 2,
        "durationSec": 0,
        "stdout": "",
        "stderr": f"skipped: local server not reachable on port {args.port}",
    }

    if has_server:
        preflight_result = run_command(
            [
                sys.executable,
                "scripts/run_golive_preflight.py",
                "--strict",
                "--base-url",
                f"http://127.0.0.1:{args.port}",
            ]
        )

    signoff_result = run_command([sys.executable, "scripts/validate_golive_signoff.py", "--strict"])
    strict_signoff_ok = signoff_result["code"] == 0

    if args.allow_open_signoff:
        overall_ok = preflight_result["code"] == 0
    else:
        overall_ok = preflight_result["code"] == 0 and strict_signoff_ok

    preflight_summary = safe_load_preflight_summary()
    blockers = collect_blockers(preflight_result, signoff_result, preflight_summary, args.allow_open_signoff)

    summary = {
        "generatedAt": now,
        "flags": {
            "serve": args.serve,
            "allowOpenSignoff": args.allow_open_signoff,
        },
        "server": {
            "port": args.port,
            "reachable": has_server,
            "startedByScript": server_started,
        },
        "checks": {
            "preflight": preflight_result,
            "signoffStrict": signoff_result,
        },
        "preflightSummary": preflight_summary,
        "blockers": blockers,
        "overall": {"ok": overall_ok},
    }

    Path("GO_LIVE_RELEASE_GATE.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md_lines = [
        "# GO_LIVE_RELEASE_GATE.md",
        "",
        f"Erstellt: {now}",
        "",
        "## Ergebnis",
        "",
        f"- Gesamtstatus: {'✅ FREIGABE MÖGLICH' if overall_ok else '❌ NO-GO (Blocker vorhanden)'}",
        f"- Server erreichbar (127.0.0.1:{args.port}): {'✅' if has_server else '❌'}",
        f"- Modus: {'Preflight-gesteuert (Signoff darf offen sein)' if args.allow_open_signoff else 'Strikt (Preflight + Signoff müssen grün sein)'}",
    ]

    if preflight_summary:
        md_lines += [
            f"- Preflight Summary: Vendor {preflight_summary.get('vendorPresent', '?')}/{preflight_summary.get('vendorTotal', '?')}, "
            f"Core {preflight_summary.get('coreOk', '?')}/{preflight_summary.get('coreTotal', '?')}, "
            f"URLs {preflight_summary.get('urlOk', '?')}/{preflight_summary.get('urlTotal', '?')}",
        ]

    if blockers:
        md_lines += ["", "## Konkrete Blocker", ""]
        md_lines.extend(f"- {b}" for b in blockers)

    md_lines += [
        "",
        "## Check-Details",
        "",
        "| Check | Exit-Code | Dauer (s) |",
        "|---|---:|---:|",
        f"| Preflight | {preflight_result['code']} | {preflight_result['durationSec']} |",
        f"| Signoff Strict | {signoff_result['code']} | {signoff_result['durationSec']} |",
        "",
        "## Hinweise",
        "",
        "- Preflight läuft im Strict-Modus über die vom Gate gesetzte Base-URL (default 127.0.0.1:8000 oder `--port`).",
        "- Strikter Modus bricht ab, solange Platzhalter oder Fail-Zeilen in `GO_LIVE_SIGNOFF.md` enthalten sind.",
        "- Für Zwischenstände kann `--allow-open-signoff` genutzt werden, um Infrastruktur-Blocker separat zu beurteilen.",
        "",
    ]

    Path("GO_LIVE_RELEASE_GATE.md").write_text("\n".join(md_lines), encoding="utf-8")

    if server_proc is not None:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_proc.kill()

    print("generated GO_LIVE_RELEASE_GATE.json + GO_LIVE_RELEASE_GATE.md")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
