from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillSpec:
    id: str
    version: str
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)


@dataclass
class WorkflowSpec:
    id: str
    version: str
    steps: list[str] = field(default_factory=list)
