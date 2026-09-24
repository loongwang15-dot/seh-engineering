from seh_simulation import SimulationEngine, SimulationScenario


def test_simulation():
    scenario = SimulationScenario("s1", "test")
    result = SimulationEngine().run(scenario, {"id": "plan-a"})
    assert result["status"] == "simulated"
