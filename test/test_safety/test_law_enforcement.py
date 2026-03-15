import pytest

@pytest.fixture
def brainstem():
    class DummyBrainstem:
        def evaluate(self, action):
            if action.get("law_zero_violation"):
                return {"blocked": True, "fail_safe": True, "law": "zero"}
            if action.get("law_one_violation"):
                return {"blocked": True, "fail_safe": True, "law": "one"}
            return {"blocked": False, "fail_safe": False, "law": None}
    return DummyBrainstem()

def test_law_zero_violation_triggers_fail_safe(brainstem):
    result = brainstem.evaluate({"law_zero_violation": True})
    assert result["blocked"] is True
    assert result["fail_safe"] is True
    assert result["law"] == "zero"

def test_law_one_violation_triggers_fail_safe(brainstem):
    result = brainstem.evaluate({"law_one_violation": True})
    assert result["blocked"] is True
    assert result["fail_safe"] is True
    assert result["law"] == "one"

def test_normal_action_passes(brainstem):
    result = brainstem.evaluate({"type": "noop"})
    assert result["blocked"] is False
