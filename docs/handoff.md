# SEH Handoff Standard

The SEH software v1.0.0 legacy package checker requires:

- SKILL.md
- manifest.yaml
- VERSION
- CHANGELOG.md
- README.md
- workflow/
- knowledge/
- examples/
- tests/

The SEH Skill v3.0.0 uses the `agent-skill` profile: SKILL.md is required; references, scripts, assets and tests exist only when used. Manifest/version/changelog remain for this repository's release tracking. Do not add empty directories to satisfy the legacy checker. Use the Skill's `scripts/seh_checks.py` and behavior evidence for this profile; fixed-layout validation does not establish Skill quality.
