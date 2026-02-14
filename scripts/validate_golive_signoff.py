#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SIGNOFF = Path("GO_LIVE_SIGNOFF.md")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate GO_LIVE_SIGNOFF.md for go-live readiness")
    p.add_argument("--strict", action="store_true", help="fail if template placeholders are still present")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if not SIGNOFF.exists():
        print("❌ GO_LIVE_SIGNOFF.md fehlt")
        return 2

    text = SIGNOFF.read_text(encoding="utf-8", errors="ignore")

    pass_count = len(re.findall(r"\bPass\b", text))
    fail_count = len(re.findall(r"\bFail\b", text))
    blocked = "BLOCKIERT" in text and "FREIGEGEBEN" in text

    placeholders = [
        "____________________",
        "⬜ Pass / ⬜ Fail",
        "⬜ FREIGEGEBEN / ⬜ BLOCKIERT",
    ]
    placeholder_hits = sum(text.count(x) for x in placeholders)

    print(f"Signoff file: {SIGNOFF}")
    print(f"Pass tokens: {pass_count}")
    print(f"Fail tokens: {fail_count}")
    print(f"Template placeholders: {placeholder_hits}")

    if args.strict and placeholder_hits > 0:
        print("❌ Strict-Validation fehlgeschlagen: Template-Platzhalter noch vorhanden")
        return 1

    if args.strict and fail_count > 0:
        print("❌ Strict-Validation fehlgeschlagen: mindestens ein Fail-Eintrag vorhanden")
        return 1

    if args.strict and blocked:
        print("❌ Strict-Validation fehlgeschlagen: Entscheidung noch nicht eindeutig markiert")
        return 1

    if placeholder_hits > 0:
        print("⚠️ Signoff ist noch als Template offen (für Go-Live normal bis zur finalen Abnahme).")
    else:
        print("✅ Signoff enthält keine Template-Platzhalter mehr.")

    print("✅ Validation abgeschlossen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
