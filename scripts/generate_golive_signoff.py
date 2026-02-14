#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path

TOOLS = [
    "Holz-Tools",
    "Sparrenlängen-Rechner",
    "Laser Entfernungsmesser",
    "BM/HS/DD",
    "Abwicklung Verschnittoptimierung",
    "RestauroMap",
    "Abwicklung Kegelstumpf",
]
MODES = ["Standard", "Strict-Local (?strictLocal=1)"]


def build() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append("# GO_LIVE_SIGNOFF.md")
    lines.append("")
    lines.append(f"Erstellt: {now}")
    lines.append("")
    lines.append("## Sign-Off Metadaten")
    lines.append("")
    lines.append("- Release/Tag: ____________________")
    lines.append("- Umgebung (Domain/Host): ____________________")
    lines.append("- Browser: ____________________")
    lines.append("- Prüfer/in: ____________________")
    lines.append("")
    lines.append("## Tool-Signoff (manuell)")
    lines.append("")
    lines.append("| Tool | Modus | Import | Export | Visualisierung | Hinweise | Freigabe |")
    lines.append("|---|---|---|---|---|---|---|")
    for tool in TOOLS:
        for mode in MODES:
            lines.append(f"| {tool} | {mode} | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail |  | ⬜ |")
    lines.append("")
    lines.append("## Go-Live Entscheidung")
    lines.append("")
    lines.append("- Gesamtstatus: ⬜ FREIGEGEBEN / ⬜ BLOCKIERT")
    lines.append("- Offene Blocker: __________________________________________")
    lines.append("- Entscheidung von: ____________________")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    target = Path("GO_LIVE_SIGNOFF.md")
    target.write_text(build(), encoding="utf-8")
    print(f"generated {target}")


if __name__ == "__main__":
    main()
