from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "seh_checks.py"
spec = importlib.util.spec_from_file_location("seh_checks", SCRIPT)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class ChecksTest(unittest.TestCase):
    def setUp(self):
        self.workspace = Path.cwd().resolve()
        self.temp = tempfile.TemporaryDirectory(prefix="seh-test-", dir=self.workspace)
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.cleanup)
        self.evidence = self.root / "actual.txt"
        self.evidence.write_text("Observed execution result", encoding="utf-8")

    def cleanup(self):
        if not self.root.is_relative_to(self.workspace) or self.root == self.workspace:
            raise RuntimeError("Temporary cleanup target escaped test workspace")
        self.temp.cleanup()

    def skill(self, name="source"):
        path = self.root / name
        path.mkdir()
        (path / "SKILL.md").write_text("---\nname: example\ndescription: Handle example requests.\n---\n# Example v1.0.0\nDo the task.\n", encoding="utf-8")
        return path

    def record(self, scope="PACKAGE"):
        return {"schema_version": 1, "task_id": "test", "mode": "UPDATE", "profile": "FULL", "scope": scope,
                "checks": [{"id": name, "status": "PASS", "evidence": [{"kind": "command", "path": "actual.txt", "sha256": checks.sha256(self.evidence)}]}
                           for name in sorted(checks.SCOPES[scope])]}

    def test_minimal_skill_requires_no_placeholder_directories(self):
        self.assertEqual(checks.inspect_skill(self.skill())["status"], "PASS")

    def test_missing_entry_fails(self):
        self.assertEqual(checks.inspect_skill(self.root)["status"], "FAIL")

    def test_empty_instructions_fail(self):
        skill = self.skill()
        (skill / "SKILL.md").write_text("---\nname: example\ndescription: Example\n---\n", encoding="utf-8")
        self.assertEqual(checks.inspect_skill(skill)["status"], "FAIL")

    def test_broken_reference_fails(self):
        skill = self.skill()
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("[Guide](missing.md)")
        self.assertEqual(checks.inspect_skill(skill)["status"], "FAIL")

    def test_anchor_is_checked(self):
        skill = self.skill()
        (skill / "guide.md").write_text("# Guide\n## CREATE\n", encoding="utf-8")
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("[Guide](guide.md#create)")
        self.assertEqual(checks.inspect_skill(skill)["status"], "PASS")
        (skill / "guide.md").write_text("# Different\n", encoding="utf-8")
        self.assertEqual(checks.inspect_skill(skill)["status"], "FAIL")

    def test_local_reference_cannot_escape_root(self):
        skill = self.skill()
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("[Outside](../actual.txt)")
        self.assertEqual(checks.inspect_skill(skill)["status"], "FAIL")

    def test_version_mismatch_fails(self):
        skill = self.skill()
        (skill / "VERSION").write_text("1.0.0", encoding="utf-8")
        (skill / "manifest.yaml").write_text("skill_id: example\nversion: 2.0.0\n", encoding="utf-8")
        self.assertEqual(checks.inspect_skill(skill)["status"], "FAIL")

    def test_copy_is_checked_and_platform_extras_are_reported(self):
        source, target = self.skill(), self.skill("target")
        (target / "metadata.txt").write_text("Platform metadata", encoding="utf-8")
        result = checks.compare(source, target)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["target_extras"], ["metadata.txt"])

    def test_changed_or_missing_file_fails_comparison(self):
        source, target = self.skill(), self.skill("target")
        (target / "SKILL.md").write_text("changed", encoding="utf-8")
        self.assertEqual(checks.compare(source, target)["changed"], ["SKILL.md"])
        (target / "SKILL.md").unlink()
        self.assertEqual(checks.compare(source, target)["missing"], ["SKILL.md"])

    def test_empty_canonical_does_not_pass(self):
        source = self.root / "empty"
        source.mkdir()
        self.assertEqual(checks.compare(source, self.skill())["status"], "FAIL")

    def test_valid_scoped_evidence_record_passes(self):
        self.assertEqual(checks.gate(self.record(), self.root)["status"], "PASS")

    def test_missing_required_check_is_blocked(self):
        record = self.record()
        record["checks"].pop()
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_pass_without_evidence_is_unverified(self):
        record = self.record()
        record["checks"][0]["evidence"] = []
        self.assertEqual(checks.gate(record, self.root)["status"], "UNVERIFIED")

    def test_modified_evidence_is_blocked(self):
        record = self.record()
        self.evidence.write_text("Changed since validation", encoding="utf-8")
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_evidence_outside_record_directory_is_blocked(self):
        record = self.record()
        record["checks"][0]["evidence"][0]["path"] = "../actual.txt"
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_missing_evidence_file_is_blocked(self):
        record = self.record()
        self.evidence.unlink()
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_duplicate_check_is_blocked(self):
        record = self.record()
        record["checks"].append(copy.deepcopy(record["checks"][0]))
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_unverified_does_not_become_pass(self):
        record = self.record()
        record["checks"][0].update(status="UNVERIFIED", reason="Not executed")
        self.assertEqual(checks.gate(record, self.root)["status"], "UNVERIFIED")

    def test_fail_is_blocked(self):
        record = self.record()
        record["checks"][0].update(status="FAIL", reason="Observed failure")
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_structural_gate_cannot_be_marked_na(self):
        record = self.record()
        next(c for c in record["checks"] if c["id"] == "structure").update(status="N/A", reason="Skip")
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_new_skill_can_exclude_historical_fidelity(self):
        record = self.record()
        record["mode"] = "CREATE"
        next(c for c in record["checks"] if c["id"] == "fidelity").update(status="N/A", reason="New skill")
        self.assertEqual(checks.gate(record, self.root)["status"], "PASS")

    def test_deployment_requires_runtime_check(self):
        record = self.record("DEPLOYMENT")
        record["checks"] = [c for c in record["checks"] if c["id"] != "deployment"]
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_deployment_na_is_blocked(self):
        record = self.record("DEPLOYMENT")
        next(c for c in record["checks"] if c["id"] == "deployment").update(status="N/A", reason="No app")
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_file_copy_does_not_prove_target_runtime(self):
        self.assertEqual(checks.gate(self.record("DEPLOYMENT"), self.root)["status"], "UNVERIFIED")

    def test_deployment_record_needs_target_app_evidence(self):
        record = self.record("DEPLOYMENT")
        next(c for c in record["checks"] if c["id"] == "deployment")["evidence"][0]["kind"] = "target_app"
        self.assertEqual(checks.gate(record, self.root)["status"], "PASS")

    def test_invalid_schema_is_blocked(self):
        record = self.record()
        record["scope"] = "UNKNOWN"
        self.assertEqual(checks.gate(record, self.root)["status"], "BLOCKED")

    def test_cli_pass_and_unverified_exit_codes(self):
        record = self.record()
        file = self.root / "qa.json"
        file.write_text(json.dumps(record), encoding="utf-8")
        passed = subprocess.run([sys.executable, str(SCRIPT), "gate", str(file)], capture_output=True, text=True)
        self.assertEqual(passed.returncode, 0)
        self.assertEqual(json.loads(passed.stdout)["status"], "PASS")
        record["checks"][0].update(status="UNVERIFIED", reason="Pending")
        file.write_text(json.dumps(record), encoding="utf-8")
        unverified = subprocess.run([sys.executable, str(SCRIPT), "gate", str(file)], capture_output=True, text=True)
        self.assertEqual(unverified.returncode, 2)

    def test_cli_unicode_paths_survive_ascii_stdout_environment(self):
        skill = self.skill()
        (skill / "参考📄.md").write_text("# Guide\n", encoding="utf-8")
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("[参考](参考📄.md)")
        environment = dict(os.environ, PYTHONIOENCODING="ascii")
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(skill)], capture_output=True, encoding="utf-8", env=environment)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["links"][0]["target"], "参考📄.md")


if __name__ == "__main__":
    unittest.main()
