import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RegistryRecord:
    skill_id: str
    name: str
    version: str
    status: str = "draft"
    metadata: dict = field(default_factory=dict)


class Registry:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path is not None else None
        self.records: dict[str, RegistryRecord] = {}

    def register(self, record: RegistryRecord) -> RegistryRecord:
        self.records[record.skill_id] = record
        if self.path is not None:
            self._persist()
        return record

    def get(self, skill_id: str) -> RegistryRecord | None:
        return self.records.get(skill_id)

    def list(self) -> list[RegistryRecord]:
        return list(self.records.values())

    def _persist(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "seh_version": "1.0.0",
            "skills": [
                {
                    "skill_id": r.skill_id,
                    "name": r.name,
                    "version": r.version,
                    "status": r.status,
                    "metadata": r.metadata,
                }
                for r in self.records.values()
            ],
        }
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Registry":
        registry = cls(path)
        raw_path = Path(path)
        if raw_path.exists():
            payload = json.loads(raw_path.read_text(encoding="utf-8"))
            for item in payload.get("skills", []):
                registry.register(RegistryRecord(**item))
        return registry
