from dataclasses import dataclass, field
from typing import Any


@dataclass
class EntityRef:
    id: str
    type: str
    version: str = "1.0.0"


@dataclass
class EngineeringResult:
    status: str
    data: Any = None
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillManifest:
    skill_id: str
    name: str
    version: str
    category: str = ""
    author: str = ""
    status: str = "draft"
    created: str | None = None
    updated: str | None = None
    dependencies: list[str] = field(default_factory=list)
    compatibility: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "SkillManifest":
        return cls(
            skill_id=str(payload.get("skill_id", "")),
            name=str(payload.get("name", "")),
            version=str(payload.get("version", "")),
            category=str(payload.get("category", "")),
            author=str(payload.get("author", "")),
            status=str(payload.get("status", "draft")),
            created=payload.get("created"),
            updated=payload.get("updated"),
            dependencies=list(payload.get("dependencies") or []),
            compatibility=dict(payload.get("compatibility") or {}),
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "version": self.version,
            "category": self.category,
            "author": self.author,
            "status": self.status,
            "created": self.created,
            "updated": self.updated,
            "dependencies": list(self.dependencies),
            "compatibility": dict(self.compatibility),
        }
