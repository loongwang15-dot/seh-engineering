from seh_benchmark import quality_gate


def test_quality_gate_pass():
    result = quality_gate({"quality": 0.95}, {"quality": 0.90})
    assert result.status == "PASS"


def test_quality_gate_fail():
    result = quality_gate({"quality": 0.80}, {"quality": 0.90})
    assert result.status == "FAIL"
