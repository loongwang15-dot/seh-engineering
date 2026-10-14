from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

POWERSHELL = os.environ.get("SEH_POWERSHELL") or shutil.which("pwsh")
REPO = Path(__file__).resolve().parents[1]
INSTALLER = REPO / "tools" / "install-seh.ps1"
ROLLBACK = REPO / "tools" / "rollback-seh.ps1"


def quoted(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


@unittest.skipUnless(POWERSHELL, "PowerShell 7 is required for real installer recovery tests")
class InstallationTest(unittest.TestCase):
    def setUp(self):
        self.workspace = Path.cwd().resolve()
        self.temp = tempfile.TemporaryDirectory(prefix="seh-install-test-", dir=self.workspace)
        self.root = Path(self.temp.name).resolve()
        self.source, self.target = self.root / "source", self.root / "target"
        self.backup, self.record = self.root / "backup", self.root / "plan.json"
        self.source.mkdir()
        self.target.mkdir()
        self.original = b"Original skill instructions\n"
        self.incoming = b"Revised skill instructions\n"
        (self.target / "SKILL.md").write_bytes(self.original)
        (self.target / "unrelated.txt").write_text("Preserve unrelated data", encoding="utf-8")
        (self.source / "SKILL.md").write_bytes(self.incoming)
        (self.source / "VERSION").write_text("3.0.1\n", encoding="utf-8")
        (self.source / "zz-added.md").write_text("Additional source file", encoding="utf-8")
        self.addCleanup(self.cleanup)

    def cleanup(self):
        if not self.root.is_relative_to(self.workspace) or self.root == self.workspace:
            raise RuntimeError("Refusing cleanup outside the test workspace")
        self.temp.cleanup()

    def run_ps(self, content: str) -> subprocess.CompletedProcess:
        script = self.root / "run.ps1"
        script.write_text("$ErrorActionPreference = 'Stop'\n" + content, encoding="utf-8-sig")
        return subprocess.run([POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(script)],
                              cwd=self.root, capture_output=True, encoding="utf-8", errors="replace", timeout=40)

    def install(self, prelude: str = "") -> subprocess.CompletedProcess:
        return self.run_ps(prelude + "\n& " + quoted(INSTALLER) + " -Source " + quoted(self.source)
                           + " -Target " + quoted(self.target) + " -Backup " + quoted(self.backup)
                           + " -Record " + quoted(self.record))

    def rollback(self) -> subprocess.CompletedProcess:
        return self.run_ps("& " + quoted(ROLLBACK) + " -Record " + quoted(self.record)
                           + " -Target " + quoted(self.target) + " -Backup " + quoted(self.backup))

    def assert_old_restored(self):
        self.assertEqual((self.target / "SKILL.md").read_bytes(), self.original)
        self.assertFalse((self.target / "VERSION").exists())
        self.assertFalse((self.target / "zz-added.md").exists())
        self.assertEqual((self.target / "unrelated.txt").read_text(), "Preserve unrelated data")

    def test_completed_install_and_rollback_preserve_unrelated_files(self):
        installed = self.install()
        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertEqual(json.loads(self.record.read_text())["Status"], "INSTALLED")
        self.assertEqual((self.target / "SKILL.md").read_bytes(), self.incoming)
        restored = self.rollback()
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assert_old_restored()

    def test_interrupted_copy_has_a_durable_usable_recovery_plan(self):
        # Fault injection affects only this test's newly created target directory.
        prelude = "$global:sehWrites = 0\nfunction global:Copy-Item {\n"
        prelude += "param([string]$LiteralPath,[string]$Destination,[switch]$Force)\n"
        prelude += "if ($Destination.StartsWith(" + quoted(str(self.target) + os.sep) + ")) {\n"
        prelude += "  if (-not (Test-Path -LiteralPath " + quoted(self.record) + ")) { throw 'Recovery plan absent before write' }\n"
        prelude += "  $global:sehWrites++\n  if ($global:sehWrites -eq 2) { throw 'Injected interrupted copy' }\n}\n"
        prelude += "Microsoft.PowerShell.Management\\Copy-Item -LiteralPath $LiteralPath -Destination $Destination -Force:$Force\n}\n"
        failed = self.install(prelude)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("Injected interrupted copy", failed.stderr)
        self.assertTrue(self.record.exists())
        plan = json.loads(self.record.read_text())
        self.assertEqual(plan["Status"], "INTERRUPTED")
        self.assertEqual((self.backup / "SKILL.md").read_bytes(), self.original)
        self.assertEqual((self.target / "SKILL.md").read_bytes(), self.incoming)
        restored = self.rollback()
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assert_old_restored()

    def test_later_edit_blocks_all_rollback_mutations(self):
        installed = self.install()
        self.assertEqual(installed.returncode, 0, installed.stderr)
        later = b"A later user edit\n"
        (self.target / "SKILL.md").write_bytes(later)
        restored = self.rollback()
        self.assertNotEqual(restored.returncode, 0)
        self.assertIn("Preserve later change", restored.stderr)
        self.assertEqual((self.target / "SKILL.md").read_bytes(), later)
        self.assertTrue((self.target / "VERSION").exists())
        self.assertTrue((self.target / "zz-added.md").exists())

    def test_interrupted_restore_does_not_truncate_destination(self):
        installed = self.install()
        self.assertEqual(installed.returncode, 0, installed.stderr)
        prelude = "function global:Copy-Item {\nparam([string]$LiteralPath,[string]$Destination,[switch]$Force)\n"
        prelude += "if ($Destination.StartsWith(" + quoted(str(self.target) + os.sep) + ")) {\n"
        prelude += "[IO.File]::WriteAllText($Destination, 'Interrupted staged restore'); throw 'Injected restore failure'\n}\n"
        prelude += "Microsoft.PowerShell.Management\\Copy-Item -LiteralPath $LiteralPath -Destination $Destination -Force:$Force\n}\n"
        failed = self.run_ps(prelude + "& " + quoted(ROLLBACK) + " -Record " + quoted(self.record)
                             + " -Target " + quoted(self.target) + " -Backup " + quoted(self.backup))
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual((self.target / "SKILL.md").read_bytes(), self.incoming)
        restored = self.rollback()
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assert_old_restored()

    def test_changed_backup_blocks_restore_before_mutation(self):
        installed = self.install()
        self.assertEqual(installed.returncode, 0, installed.stderr)
        (self.backup / "SKILL.md").write_bytes(b"Corrupted backup")
        restored = self.rollback()
        self.assertNotEqual(restored.returncode, 0)
        self.assertIn("Backup changed", restored.stderr)
        self.assertEqual((self.target / "SKILL.md").read_bytes(), self.incoming)

    def test_escaped_record_path_is_rejected_before_mutation(self):
        installed = self.install()
        self.assertEqual(installed.returncode, 0, installed.stderr)
        sentinel = self.root / "sentinel.txt"
        sentinel.write_bytes(b"Never modify outside target")
        plan = json.loads(self.record.read_text())
        plan["Entries"][0]["File"] = "../sentinel.txt"
        self.record.write_text(json.dumps(plan), encoding="utf-8")
        restored = self.rollback()
        self.assertNotEqual(restored.returncode, 0)
        self.assertEqual(sentinel.read_bytes(), b"Never modify outside target")
        self.assertEqual((self.target / "SKILL.md").read_bytes(), self.incoming)

    def test_repeated_rollback_is_safe(self):
        installed = self.install()
        self.assertEqual(installed.returncode, 0, installed.stderr)
        first = self.rollback()
        self.assertEqual(first.returncode, 0, first.stderr)
        second = self.rollback()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assert_old_restored()


if __name__ == "__main__":
    unittest.main()
