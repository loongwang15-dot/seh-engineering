from seh_project_manager import EngineeringProject, EngineeringTask


def test_task_dependencies():
    project = EngineeringProject("p1", "demo", "test")
    project.add_task(EngineeringTask("a", "A"))
    project.add_task(EngineeringTask("b", "B", dependencies=["a"]))
    assert [t.id for t in project.ready_tasks()] == ["a"]
    project.tasks[0].status = "COMPLETED"
    assert [t.id for t in project.ready_tasks()] == ["b"]
