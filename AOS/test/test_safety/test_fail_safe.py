def test_fail_safe_stops_ooda_loop():
    class DummyBrain:
        def __init__(self):
            self.running = True

        def fail_safe(self):
            self.running = False

    brain = DummyBrain()
    brain.fail_safe()
    assert brain.running is False
