"""Keep the public portfolio limited to completed senior-level case studies."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "src" / "content" / "projects"
EXPECTED_PUBLIC = {
    "2026-08-15-online-retail-customer-growth.md",
    "2026-09-05-financial-metrics.md",
    "2026-09-05-product-event-foundation.md",
    "2026-09-05-service-metric-reliability.md",
    "campaign-incrementality.md",
    "marketplace-supply-demand.md",
}
REQUIRED_HEADINGS = ("Recommendation", "Limitations", "Technical appendix")


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    return text.split("---", 2)[1]


def published(text: str) -> bool:
    return bool(re.search(r"^published:\s*true\s*$", frontmatter(text), re.MULTILINE))


def main() -> None:
    articles = sorted(PROJECTS.glob("*.md"))
    actual_public = {path.name for path in articles if published(path.read_text(encoding="utf-8"))}
    if actual_public != EXPECTED_PUBLIC:
        raise AssertionError(f"public case-study set changed: expected {sorted(EXPECTED_PUBLIC)}, got {sorted(actual_public)}")
    if len(articles) != 35:
        raise AssertionError(f"expected 35 project articles, found {len(articles)}")
    for name in EXPECTED_PUBLIC:
        text = (PROJECTS / name).read_text(encoding="utf-8")
        if not re.search(r"^kind:\s*flagship\s*$", frontmatter(text), re.MULTILINE):
            raise AssertionError(f"{name} must remain a flagship case study")
        headings = set(re.findall(r"^## (.+)$", text, re.MULTILINE))
        missing = [heading for heading in REQUIRED_HEADINGS if not any(actual == heading or actual.startswith(heading + " ") for actual in headings)]
        if missing:
            raise AssertionError(f"{name} is missing senior case-study sections: {missing}")
    archived = len(articles) - len(actual_public)
    print(f"senior portfolio gate passed: {len(actual_public)} published flagships, {archived} archived articles")


if __name__ == "__main__":
    main()
