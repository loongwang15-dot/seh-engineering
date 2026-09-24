from dataclasses import dataclass, field


@dataclass
class EngineeringTask:
    id: str
    title: str
    dependencies: list[str] = field(default_factory=list)
    status: str = "PENDING"
    assigned_agent: str | None = None


@dataclass
class EngineeringProject:
    id: str
    name: str
    objective: str
    constraints: list[str] = field(default_factory=list)
    tasks: list[EngineeringTask] = field(default_factory=list)
    status: str = "DRAFT"

    def add_task(self, task: EngineeringTask) -> None:
        self.tasks.append(task)

    def ready_tasks(self) -> list[EngineeringTask]:
        completed = {t.id for t in self.tasks if t.status == "COMPLETED"}
        return [
            t for t in self.tasks
            if t.status == "PENDING" and all(dep in completed for dep in t.dependencies)
        ]
