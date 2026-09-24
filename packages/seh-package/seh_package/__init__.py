from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from seh_core import SkillManifest


@dataclass
class SkillPackage:
    root: str | Path
    manifest: SkillManifest | None = None

    REQUIRED_FILES = {
        "SKILL.md",
        "manifest.yaml",
        "VERSION",
        "CHANGELOG.md",
        "README.md",
        "workflow",
        "knowledge",
        "examples",
        "tests",
    }

    @property
    def path(self) -> Path:
        return Path(self.root)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.path.exists():
            return ["Package root does not exist"]
        for item in self.REQUIRED_FILES:
            target = self.path / item
            if not target.exists():
                issues.append(f"Missing required package item: {item}")
        if self.manifest is not None:
            if not self.manifest.skill_id:
                issues.append("Manifest skill_id is required")
            if not self.manifest.name:
                issues.append("Manifest name is required")
            if not self.manifest.version:
                issues.append("Manifest version is required")
        return issues
