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
        "cmd": "python3 scripts/run_golive_preflight.py",
        "code": 2,
        "durationSec": 0,
        "stdout": "",
        "stderr": "skipped: local server not reachable on port {}".format(args.port),
    }

    if has_server:
        preflight_result = run_command([sys.executable, "scripts/run_golive_preflight.py"])

    signoff_result = run_command([sys.executable, "scripts/validate_golive_signoff.py", "--strict"])

    summary = {
        "generatedAt": now,
        "server": {
            "port": args.port,
            "reachable": has_server,
            "startedByScript": server_started,
            "serveFlag": args.serve,
        },
        "checks": {
            "preflight": preflight_result,
            "signoffStrict": signoff_result,
        },
    }

    overall_ok = preflight_result["code"] == 0 and signoff_result["code"] == 0
    summary["overall"] = {"ok": overall_ok}

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
        "- Preflight benötigt einen erreichbaren lokalen Server auf Port 8000 (oder `--port`).",
        "- Strict-Signoff schlägt fehl, solange Platzhalter oder Fail-Zeilen in `GO_LIVE_SIGNOFF.md` enthalten sind.",
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
