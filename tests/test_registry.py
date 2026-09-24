from seh_registry import Registry, RegistryRecord


def test_registry_register() -> None:
    registry = Registry()
    record = RegistryRecord("skill-1", "Skill One", "1.0.0")
    registry.register(record)
    assert registry.get("skill-1").skill_id == "skill-1"
    assert len(registry.list()) == 1
