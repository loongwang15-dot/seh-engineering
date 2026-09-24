from dataclasses import dataclass, field


@dataclass
class BenchmarkCase:
    id: str
    input: dict
    expected: dict
    constraints: list[str] = field(default_factory=list)


@dataclass
class Benchmark:
    id: str
    name: str
    target: str
    cases: list[BenchmarkCase] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)
    thresholds: dict[str, float] = field(default_factory=dict)


@dataclass
class QualityGateResult:
    status: str
    reasons: list[str] = field(default_factory=list)


def quality_gate(metrics: dict[str, float], thresholds: dict[str, float]) -> QualityGateResult:
    failures = [
        f"{name}={value} < threshold={thresholds[name]}"
        for name, value in metrics.items()
        if name in thresholds and value < thresholds[name]
    ]
    return QualityGateResult("FAIL" if failures else "PASS", failures)
