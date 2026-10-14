"""SEH offline checks. No model execution, installation, or semantic certification."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

MODES = {"CREATE", "UPDATE", "RECOVER", "AUDIT", "SPLIT", "MERGE", "MIGRATE", "DEPLOY", "DEPRECATE"}
SCOPES = {
    "PACKAGE": {"structure", "fidelity"},
    "BEHAVIOR": {"structure", "fidelity", "behavior", "regression"},
    "DEPLOYMENT": {"structure", "fidelity", "behavior", "regression", "deployment"},
}
KINDS = {"command", "file", "agent_behavior", "target_app", "manual"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(root: Path, target: Path) -> bool:
    return target.resolve().is_relative_to(root.resolve())


def plain_fields(text: str) -> dict[str, str]:
    """Only scalar lines used by this package; not a YAML parser."""
    return {m[1]: m[2].strip().strip('"\'') for m in re.finditer(r"^([a-z_]+):[ \t]*(.*)$", text, re.M)}


def anchors(text: str) -> set[str]:
    found, counts = set(), {}
    fenced = False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            slug = re.sub(r"[^\w\-\s]", "", match[1].lower()).replace(" ", "-")
            number = counts.get(slug, 0)
            counts[slug] = number + 1
            found.add(slug if number == 0 else f"{slug}-{number}")
    return found


def files(root: Path) -> tuple[dict[str, Path], list[str]]:
    collected, issues = {}, []
    if not root.is_dir():
        return {}, [f"Directory not found: {root}"]
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in {"__pycache__", ".git", ".pytest_cache"} for part in relative.parts):
            continue
        if path.is_symlink():
            issues.append(f"Unsupported symbolic link: {relative.as_posix()}")
        elif path.is_file():
            if not contained(root, path):
                issues.append(f"File escapes root: {relative.as_posix()}")
            else:
                collected[relative.as_posix()] = path
    return collected, issues


def inspect_skill(root: Path) -> dict:
    root = root.resolve()
    inventory, issues = files(root)
    entry = inventory.get("SKILL.md")
    if entry is None:
        issues.append("SKILL.md not found")
        return {"status": "FAIL", "scope": "structure", "issues": issues}
    text = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    meta = plain_fields(match[1]) if match else {}
    if not match:
        issues.append("Missing frontmatter")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta.get("name", "")) or len(meta.get("name", "")) > 64:
        issues.append("Invalid or missing scalar name")
    description = meta.get("description", "")
    if not description or len(description) > 1024 or description in {"|", ">"}:
        issues.append("Invalid or unsupported scalar description")
    body = text[match.end():] if match else text
    if not body.strip():
        issues.append("Empty instructions")
    if re.search(r"^\s*\[TODO:[^\n]*\]\s*$", body, re.M):
        issues.append("Unfinished scaffold")
    links = []
    for relative, source in sorted(inventory.items()):
        if source.suffix.lower() != ".md":
            continue
        content = source.read_text(encoding="utf-8")
        for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = source.parent / unquote(parsed.path) if parsed.path else source
            valid = contained(root, destination) and destination.is_file()
            if valid and parsed.fragment:
                valid = unquote(parsed.fragment) in anchors(destination.read_text(encoding="utf-8"))
            links.append({"source": relative, "target": target, "valid": valid})
            if not valid:
                issues.append(f"Invalid local reference: {relative} -> {target}")
    version_path = inventory.get("VERSION")
    version = version_path.read_text(encoding="utf-8").strip() if version_path else None
    if version and not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", version):
        issues.append("Invalid VERSION")
    manifest = inventory.get("manifest.yaml")
    if manifest:
        fields = plain_fields(manifest.read_text(encoding="utf-8"))
        if fields.get("skill_id") != meta.get("name"):
            issues.append("manifest skill_id differs from entry name")
        if version is None or fields.get("version") != version:
            issues.append("manifest version differs from VERSION")
    if version and not re.search(r"\bv" + re.escape(version) + r"\b", body):
        issues.append("Entry does not identify declared version")
    return {"status": "FAIL" if issues else "PASS", "scope": "structure", "name": meta.get("name"),
            "version": version, "entry_sha256": sha256(entry), "files": len(inventory), "links": links, "issues": issues}


def compare(source: Path, target: Path) -> dict:
    expected, source_issues = files(source.resolve())
    actual, target_issues = files(target.resolve())
    issues = source_issues + target_issues
    if "SKILL.md" not in expected:
        issues.append("Canonical SKILL.md not found")
    missing = sorted(set(expected) - set(actual))
    changed = sorted(key for key in expected.keys() & actual.keys() if sha256(expected[key]) != sha256(actual[key]))
    extras = sorted(set(actual) - set(expected))
    return {"status": "FAIL" if issues or missing or changed else "PASS", "scope": "byte_integrity",
            "expected_files": len(expected), "matched_files": len(expected) - len(missing) - len(changed),
            "missing": missing, "changed": changed, "target_extras": extras, "issues": issues,
            "limitation": "Extra files require review; byte integrity is not semantic or runtime validation."}


def gate(report: dict, root: Path) -> dict:
    failures, unknown, observed = [], [], []
    if not isinstance(report, dict):
        return {"status": "BLOCKED", "failures": ["Record must be an object"], "unverified": []}
    if report.get("schema_version") != 1:
        failures.append("schema_version must be 1")
    for key, allowed in (("mode", MODES), ("profile", {"LIGHT", "FULL"}), ("scope", set(SCOPES))):
        if not isinstance(report.get(key), str) or report[key] not in allowed:
            failures.append(f"Invalid {key}")
    if not isinstance(report.get("task_id"), str) or not report["task_id"].strip():
        failures.append("task_id is required")
    checks = report.get("checks")
    if not isinstance(checks, list):
        failures.append("checks must be an array")
        checks = []
    seen = set()
    for item in checks:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            failures.append("Check must have a non-empty string id")
            continue
        check_id, status = item["id"], item.get("status")
        if check_id in seen:
            failures.append(f"Duplicate check: {check_id}")
        seen.add(check_id)
        if status not in {"PASS", "FAIL", "UNVERIFIED", "N/A"}:
            failures.append(f"Invalid status: {check_id}")
            continue
        reason = item.get("reason")
        if status != "PASS" and (not isinstance(reason, str) or not reason.strip()):
            failures.append(f"Reason required: {check_id}")
        if status == "FAIL":
            failures.append(f"Declared failed check: {check_id}")
        elif status == "UNVERIFIED":
            unknown.append(check_id)
        elif status == "N/A" and check_id in SCOPES.get(report.get("scope"), set()):
            allowed_na = (check_id == "fidelity" and report.get("mode") == "CREATE") or (
                check_id == "regression" and (report.get("mode") in {"CREATE", "AUDIT"} or report.get("profile") == "LIGHT"))
            if not allowed_na:
                failures.append(f"Required check cannot be N/A: {check_id}")
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list):
            failures.append(f"evidence must be an array: {check_id}")
            continue
        if status == "PASS" and not evidence:
            unknown.append(f"PASS without evidence: {check_id}")
        for entry in evidence:
            if not isinstance(entry, dict) or entry.get("kind") not in KINDS:
                failures.append(f"Invalid evidence kind: {check_id}")
                continue
            path, digest = entry.get("path"), entry.get("sha256")
            if not isinstance(path, str) or not path or Path(path).is_absolute() or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                failures.append(f"Invalid evidence path/hash: {check_id}")
                continue
            destination = root / path
            if not contained(root, destination) or not destination.is_file():
                failures.append(f"Missing or escaped evidence: {check_id}/{path}")
            elif sha256(destination) != digest.lower():
                failures.append(f"Evidence hash mismatch: {check_id}/{path}")
            else:
                observed.append({"check": check_id, "path": path, "kind": entry["kind"]})
    for check_id in sorted(SCOPES.get(report.get("scope"), set()) - seen):
        failures.append(f"Missing required check: {check_id}")
    deployment = next((c for c in checks if isinstance(c, dict) and c.get("id") == "deployment"), None)
    if deployment and deployment.get("status") == "PASS":
        entries = deployment.get("evidence", [])
        if not isinstance(entries, list) or not any(isinstance(e, dict) and e.get("kind") == "target_app" for e in entries):
            unknown.append("Deployment PASS lacks target_app evidence; file copy is insufficient")
    return {"status": "BLOCKED" if failures else "UNVERIFIED" if unknown else "PASS",
            "scope": report.get("scope"), "failures": failures, "unverified": unknown, "verified_evidence": observed,
            "limitation": "Only record completeness and evidence integrity; evidence claims still require review."}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inspect").add_argument("root", type=Path)
    comparator = sub.add_parser("compare")
    comparator.add_argument("source", type=Path)
    comparator.add_argument("target", type=Path)
    sub.add_parser("gate").add_argument("record", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_skill(args.root)
        elif args.command == "compare":
            result = compare(args.source, args.target)
        else:
            result = gate(json.loads(args.record.read_text(encoding="utf-8-sig")), args.record.parent.resolve())
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        result = {"status": "BLOCKED", "issues": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 2 if result["status"] == "UNVERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
