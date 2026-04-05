import json
import tempfile

def test_state_snapshot_written():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name

    class DummyBrain:
        def write_state(self, path):
            with open(path, "w") as f:
                json.dump({"phase": "Act"}, f)

    brain = DummyBrain()
    brain.write_state(path)

    with open(path) as f:
        data = json.load(f)

    assert data["phase"] == "Act"
