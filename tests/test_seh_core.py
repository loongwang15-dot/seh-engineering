from seh_core import EntityRef, SkillManifest
from seh_validator import ValidationError, require_fields, validate_manifest


def test_entity_ref():
    ref = EntityRef("skill-1", "Skill")
    assert ref.type == "Skill"


def test_skill_manifest_roundtrip():
    manifest = SkillManifest(
        skill_id="example_skill",
        name="Example Skill",
        version="1.0.0",
        dependencies=["core"],
    )
    assert manifest.to_mapping()["skill_id"] == "example_skill"


def test_required_fields():
    require_fields({"skill_id": "x", "version": "1.0.0"}, ["skill_id", "version"])


def test_missing_fields():
    try:
        require_fields({}, ["skill_id"])
    except ValidationError:
        return
    raise AssertionError("ValidationError was not raised")


def test_validate_manifest():
    validate_manifest({"skill_id": "x", "name": "Example", "version": "1.0.0", "dependencies": []})
