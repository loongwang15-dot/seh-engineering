class ValidationError(ValueError):
    pass


def require_fields(payload: dict, fields: list[str]) -> None:
    missing = [name for name in fields if name not in payload]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")


def validate_manifest(manifest: dict) -> None:
    require_fields(manifest, ["skill_id", "name", "version"])
    if not isinstance(manifest.get("dependencies", []), list):
        raise ValidationError("dependencies must be a list")
