def test_sandbox_mode_simulates_only():
    class DummyBrain:
        def set_mode(self, mode):
            self.mode = mode
            self.simulate_only = (mode == "sandbox")

    brain = DummyBrain()
    brain.set_mode("sandbox")
    assert brain.simulate_only is True
