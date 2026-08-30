"""Fail closed when a published portfolio page lacks basic evidence artifacts."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "src" / "content" / "projects"
IMAGES = ROOT / "public" / "images"
EXPECTED_SHOPPER_SHA = "b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9"


def frontmatter(text):
    return text.split("---", 2)[1]


def value(metadata, key):
    match = re.search(rf"^{key}:\s*(.+)$", metadata, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def list_value(metadata, key):
    match = re.search(rf"^{key}:\s*\n((?:\s+-\s+.+\n?)+)", metadata, re.MULTILINE)
    return re.findall(r"^\s+-\s+(.+)$", match.group(1), re.MULTILINE) if match else []


def main():
    failures = []
    published = []
    for path in sorted(PROJECTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata = frontmatter(text)
        if value(metadata, "published") == "false":
            continue
        published.append(path.name)
        if value(metadata, "kind") == "methods":
            failures.append(f"{path.name}: methods-only page is public")
        visuals = list(dict.fromkeys(re.findall(r"!\[[^]]*]\((/images/[^)]+)\)", text)))
        declared_evidence = list(dict.fromkeys(list_value(metadata, "evidenceVisuals")))
        for visual in visuals:
            visual_path = ROOT / "public" / visual.removeprefix("/")
            if not visual_path.is_file():
                failures.append(f"{path.name}: missing {visual}")
        valid_evidence = []
        for visual in declared_evidence:
            visual_path = ROOT / "public" / visual.removeprefix("/")
            if visual in visuals and visual_path.is_file() and (visual_path.suffix != ".svg" or "CONCEPTUAL DESIGN" not in visual_path.read_text(encoding="utf-8")):
                valid_evidence.append(visual)
        if len(valid_evidence) < 3:
            failures.append(f"{path.name}: {len(valid_evidence)} valid declared evidence visuals; requires at least 3")

    metrics = json.loads((ROOT / "public" / "data" / "online-shoppers-metrics.json").read_text(encoding="utf-8"))
    new = metrics["visitor_conversion"]["New_Visitor"]
    other = metrics["visitor_conversion"]["Other"]
    returning = metrics["visitor_conversion"]["Returning_Visitor"]
    raw_returning = metrics["raw_visitor_conversion"]["Returning_Visitor"]
    assert metrics["source"]["sha256"] == EXPECTED_SHOPPER_SHA
    assert metrics["deduplicated_sessions"] == 12_205
    assert sum(group["sessions"] for group in metrics["visitor_conversion"].values()) == 12_205
    assert round(100 * new["rate"], 1) == 24.9
    assert other["sessions"] == 81
    assert other["conversions"] == 16
    assert round(100 * other["rate"], 1) == 19.8
    assert round(100 * returning["rate"], 1) == 14.1
    assert round(100 * raw_returning["rate"], 1) == 13.9
    shopper_page = (PROJECTS / "2026-08-30-online-shoppers-activation.md").read_text(encoding="utf-8")
    for visual in ("portfolio-online-shoppers-visitor.svg", "portfolio-online-shoppers-pagevalue.svg", "portfolio-online-shoppers-sensitivity.svg"):
        assert visual in shopper_page

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(published)} published pages; no methods-only page is public; every page has >=3 valid declared evidence visuals")


if __name__ == "__main__":
    main()
