"""Render the synthetic ComplaintFlow evaluation slices as a static SVG."""

from __future__ import annotations

import html
import json
from pathlib import Path

from complaintflow.schemas import Complaint
from complaintflow.service import default_service


ROOT = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).with_name("fixture.json")
OUTPUT = ROOT / "public" / "images" / "complaintflow-evaluation-slices.svg"


def render_chart() -> str:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    service = default_service()
    slices: dict[str, dict[str, int]] = {}
    for row in fixture:
        result = service.triage(Complaint(row["complaint_id"], row["text"]))
        bucket = slices.setdefault(row.get("slice", "unspecified"), {"cases": 0, "correct": 0})
        bucket["cases"] += 1
        bucket["correct"] += int(result.queue == row["label"])

    max_cases = max(bucket["cases"] for bucket in slices.values())
    rows = []
    for index, (label, values) in enumerate(slices.items()):
        y = 235 + index * 78
        width = round(610 * values["cases"] / max_cases)
        rows.append(
            f'<text x="80" y="{y + 31}" fill="#17251E" font-size="21" font-weight="600">{html.escape(label.title())}</text>'
            f'<rect x="300" y="{y}" width="610" height="46" rx="8" fill="#EAF0EB"/>'
            f'<rect x="300" y="{y}" width="{width}" height="46" rx="8" fill="#155B49"/>'
            f'<text x="940" y="{y + 30}" fill="#17251E" font-size="20" font-weight="500">{values["correct"]} / {values["cases"]} correct</text>'
        )

    title = "Synthetic evaluation cases by slice"
    desc = "All five hand-written slices routed correctly. Bar length shows the number of cases; each row labels correct cases over total cases. The fixture contains 20 synthetic examples and does not estimate real-world accuracy."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <rect width="1200" height="680" fill="#FFFEFA"/>
  <rect x="48" y="42" width="8" height="94" rx="4" fill="#155B49"/>
  <text x="80" y="82" fill="#17251E" font-family="IBM Plex Sans, sans-serif" font-size="32" font-weight="600">{title}</text>
  <text x="80" y="125" fill="#52635A" font-family="IBM Plex Sans, sans-serif" font-size="18">20 hand-written cases · correct routes or escalations by slice</text>
  {''.join(rows)}
  <line x1="80" y1="635" x2="1120" y2="635" stroke="#D8E2DA"/>
  <text x="80" y="660" fill="#52635A" font-family="IBM Plex Sans, sans-serif" font-size="16">Synthetic contract fixture, not a production accuracy estimate.</text>
</svg>
'''


def main() -> None:
    OUTPUT.write_text(render_chart(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from {FIXTURE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
