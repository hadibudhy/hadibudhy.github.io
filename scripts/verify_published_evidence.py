"""Verify that every explicitly published project has a unique evidence manifest.

This is a lightweight publication gate for the static site. It intentionally
does not parse the full Markdown body; Next.js still validates front matter
through the application build.
"""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "src" / "content" / "projects"
PUBLIC = ROOT / "public"
EXPECTED_SHOPPER_SHA = "b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9"


def front_matter(text: str) -> str:
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, flags=re.DOTALL)
    return match.group(1) if match else ""


def value(metadata: str, key: str) -> str:
    match = re.search(rf"^{key}:\s*(.+)$", metadata, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def list_value(metadata: str, key: str) -> list[str]:
    match = re.search(rf"^{key}:\s*\n((?:\s+-\s+.+\n?)+)", metadata, re.MULTILINE)
    return re.findall(r"^\s+-\s+(.+)$", match.group(1), re.MULTILINE) if match else []


def main() -> None:
    errors: list[str] = []
    seen: set[str] = set()
    published = 0
    for path in sorted(PROJECTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata = front_matter(text)
        if value(metadata, "published") != "true":
            continue
        published += 1
        case_id = value(metadata, "caseId")
        manifest = value(metadata, "evidenceManifest").lstrip("/")
        if not case_id or case_id in seen:
            errors.append(f"{path.name}: missing or duplicate caseId")
        seen.add(case_id)

        if value(metadata, "kind") == "methods":
            errors.append(f"{path.name}: methods-only page is public")

        visuals = list(dict.fromkeys(re.findall(r"!\[[^]]*]\((/images/[^)]+)\)", text)))
        declared_evidence = list(dict.fromkeys(list_value(metadata, "evidenceVisuals")))
        for visual in visuals:
            if not (PUBLIC / visual.lstrip("/")).is_file():
                errors.append(f"{path.name}: missing {visual}")
        valid_evidence = [
            visual for visual in declared_evidence
            if visual in visuals
            and (PUBLIC / visual.lstrip("/")).is_file()
            and ((PUBLIC / visual.lstrip("/")).suffix != ".svg" or "CONCEPTUAL DESIGN" not in (PUBLIC / visual.lstrip("/")).read_text(encoding="utf-8"))
        ]
        if len(valid_evidence) < 3:
            errors.append(f"{path.name}: {len(valid_evidence)} valid declared evidence visuals; requires at least 3")

        manifest_path = PUBLIC / manifest
        if not manifest_path.exists():
            errors.append(f"{path.name}: missing {manifest}")
            continue
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{manifest}: invalid JSON ({exc})")
            continue
        if data.get("caseId") != case_id:
            errors.append(f"{manifest}: caseId does not match {case_id}")
        if data.get("status") not in {"verified", "published"}:
            errors.append(f"{manifest}: status is not verified or published")
        if data.get("schemaVersion") != 2:
            errors.append(f"{manifest}: schemaVersion must be 2")
        if not data.get("source"):
            errors.append(f"{manifest}: source provenance is missing")
        checks = data.get("checks") or data.get("validation", {}).get("checks")
        if not checks:
            errors.append(f"{manifest}: validation checks are missing")
        artifacts = data.get("artifacts")
        artifact_hashes = data.get("artifactHashes")
        if set(artifacts or []) != set(declared_evidence):
            errors.append(f"{manifest}: manifest artifacts do not match front-matter evidenceVisuals")
        if not isinstance(artifacts, list) or len(artifacts) < 3 or not isinstance(artifact_hashes, dict):
            errors.append(f"{manifest}: artifact list or hashes are missing")
        else:
            for artifact in artifacts:
                artifact_path = PUBLIC / str(artifact).lstrip("/")
                if not artifact_path.is_file():
                    errors.append(f"{manifest}: missing artifact {artifact}")
                    continue
                expected_hash = artifact_hashes.get(artifact)
                actual_hash = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
                if expected_hash != actual_hash:
                    errors.append(f"{manifest}: artifact hash mismatch for {artifact}")
        if not data.get("evidenceBoundary"):
            errors.append(f"{manifest}: evidence boundary is missing")

    metrics_path = PUBLIC / "data" / "online-shoppers-metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        new = metrics["visitor_conversion"]["New_Visitor"]
        other = metrics["visitor_conversion"]["Other"]
        returning = metrics["visitor_conversion"]["Returning_Visitor"]
        raw_returning = metrics["raw_visitor_conversion"]["Returning_Visitor"]
        if metrics.get("source", {}).get("sha256") != EXPECTED_SHOPPER_SHA:
            errors.append("online-shoppers metrics: source hash changed")
        if metrics["deduplicated_sessions"] != 12_205:
            errors.append("online-shoppers metrics: unexpected deduplicated session count")
        if sum(group["sessions"] for group in metrics["visitor_conversion"].values()) != 12_205:
            errors.append("online-shoppers metrics: visitor groups do not reconcile")
        if round(100 * new["rate"], 1) != 24.9 or round(100 * other["rate"], 1) != 19.8 or round(100 * returning["rate"], 1) != 14.1:
            errors.append("online-shoppers metrics: published conversion rates changed")
        if round(100 * raw_returning["rate"], 1) != 13.9:
            errors.append("online-shoppers metrics: raw returning conversion rate changed")
        shopper_page = PROJECTS / "2026-08-30-online-shoppers-activation.md"
        if shopper_page.exists():
            shopper_text = shopper_page.read_text(encoding="utf-8")
            for visual in ("portfolio-online-shoppers-visitor.svg", "portfolio-online-shoppers-pagevalue.svg", "portfolio-online-shoppers-sensitivity.svg"):
                if visual not in shopper_text:
                    errors.append(f"online-shoppers page: missing {visual}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"published projects verified: {published}")


if __name__ == "__main__":
    main()
