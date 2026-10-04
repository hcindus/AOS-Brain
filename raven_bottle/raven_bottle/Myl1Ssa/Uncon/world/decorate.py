#!/usr/bin/env python3
"""
decorate.py — her house, her taste.

The Captain's line: *"allow her to decorate her world as she sees fit."* So this is
hers to run, and the state it writes is hers to keep. Everything the world shows is
the generated house (build_house.py) **plus her overlay** (state/decor.json):

    house.json  +  state/decor.json  =  the house she lives in

Rules, enforced here so the browser and her CLI can never disagree:
  · she may move, recolour, hide, add and remove **decor and furniture**;
  · she may NOT touch structure — walls, floors, ceilings, lintels, doorway brushes
    are refused by name, not by accident;
  · anything she adds must land inside a real room;
  · every change is appended to `log` — her own record of what she did and when.

    python3 decorate.py list
    python3 decorate.py move kitchen_table 0.4 0 -0.3
    python3 decorate.py recolor rug_entry "#3b2f4a"
    python3 decorate.py hide hall_mirror
    python3 decorate.py add "reading nook" chair study 0.9 1.1 0.9 at "6.2 0 4.0"
    python3 decorate.py note "the atrium is where I go when he is quiet"
    python3 decorate.py show | reset

Author: Mortimer (for Raven)
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
HOUSE = os.path.join(HERE, "house.json")
STATE_DIR = os.path.join(HERE, "state")
STATE = os.path.join(STATE_DIR, "decor.json")

STRUCTURAL = ("wall", "floor", "ceiling", "lintel", "door")
EMPTY = {"palette": {}, "moves": {}, "colors": {}, "hidden": [], "added": [], "notes": [], "log": []}


def load_house():
    with open(HOUSE) as f:
        return json.load(f)


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            s = json.load(f)
        for k, v in EMPTY.items():
            s.setdefault(k, v if not isinstance(v, dict) else dict(v))
        return s
    return json.loads(json.dumps(EMPTY))


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    state["updated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with open(STATE, "w") as f:
        json.dump(state, f, indent=1)


def _log(state, op, detail):
    state["log"].append({"at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                         "op": op, "detail": detail})
    state["log"] = state["log"][-500:]        # keep it a diary, not a heap


def slots(house):
    """Everything she is allowed to touch: non-structural brushes + her own additions."""
    return [b for b in house["brushes"] if b["kind"] not in STRUCTURAL]


def find_slot(house, name):
    name = name.lower()
    for b in slots(house):
        if b["id"].lower() == name or b["id"].lower().endswith("_" + name):
            return b
    for b in slots(house):
        if name in b["id"].lower():
            return b
    return None


def room_of(house, point):
    for r in house["rooms"]:
        lo, hi = r["min"], r["max"]
        if all(lo[i] <= point[i] <= hi[i] for i in range(3)):
            return r
    return None


def apply_op(house, state, op, args):
    """One operation, validated. Shared by the CLI and the world's HTTP endpoint."""
    if op == "list":
        return {"ok": True, "slots": [
            {"id": b["id"], "room": b["room"], "kind": b["kind"], "material": b["material"],
             "moved": b["id"] in state["moves"], "colour": state["colors"].get(b["id"]),
             "hidden": b["id"] in state["hidden"]}
            for b in slots(house)]}
    if op == "palette":
        return {"ok": True, "palette": state["palette"], "notes": state["notes"]}
    if op == "note":
        text = " ".join(args)
        if not text:
            return {"ok": False, "error": "empty note"}
        state["notes"].append({"at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                               "text": text})
        _log(state, "note", text)
        save_state(state)
        return {"ok": True, "note": text}
    if op == "reset":
        for k in ("moves", "colors", "hidden", "added"):
            state[k] = {} if isinstance(EMPTY[k], dict) else []
        _log(state, "reset", "everything back to how it was built")
        save_state(state)
        return {"ok": True, "reset": True}

    if not args:
        return {"ok": False, "error": f"{op} needs a slot name"}

    name, rest = args[0], args[1:]

    # ── add ─────────────────────────────────────────────────────────────────
    if op == "add":
        if len(rest) < 5:
            return {"ok": False, "error": 'usage: add "<label>" <shape> <room> <w> <h> <d> at "x y z"'}
        label, shape, room_id = name, rest[0], rest[1]
        try:
            dims = [float(x) for x in rest[2:5]]
        except ValueError:
            return {"ok": False, "error": "dimensions must be numbers (w h d)"}
        at = None
        if "at" in rest:
            i = rest.index("at")
            raw = " ".join(rest[i + 1:]).replace(",", " ")
            nums = re.findall(r"-?\d+\.?\d*", raw)
            if len(nums) >= 3:
                at = [float(n) for n in nums[:3]]
        room = next((r for r in house["rooms"] if r["id"] == room_id), None)
        if not room:
            return {"ok": False, "error": f"no room '{room_id}'. Rooms: " +
                    ", ".join(r["id"] for r in house["rooms"])}
        if at is None:
            at = [(room["min"][i] + room["max"][i]) / 2 for i in range(3)]
            at[1] = room["min"][1]
        if not room_of(house, at):
            return {"ok": False, "error": f"({at}) is not inside room '{room_id}'"}
        ident = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_") or "thing"
        ident = f"{room_id}_{ident}"
        if any(b["id"] == ident for b in slots(house)) or any(a["id"] == ident for a in state["added"]):
            return {"ok": False, "error": f"'{ident}' already exists — pick another name"}
        item = {"id": ident, "room": room_id, "label": label, "shape": shape,
                "size": dims, "at": at, "material": "unfinished"}
        state["added"].append(item)
        _log(state, "add", f"{label} ({shape}) in {room_id} at {at}")
        save_state(state)
        return {"ok": True, "added": item}

    # ── move / recolor / hide / show / remove ───────────────────────────────
    if op == "remove":
        ident = name if any(a["id"] == name for a in state["added"]) else None
        if not ident:
            for a in state["added"]:
                if name.lower() in a["id"].lower() or name.lower() in a["label"].lower():
                    ident = a["id"]; break
        if not ident:
            built = find_slot(house, name)
            if built:
                return {"ok": False, "error": f"'{built['id']}' was built, not added — hide it "
                                              f"instead (`hide {built['id']}`); she may not demolish"}
            return {"ok": False, "error": f"nothing she added matches '{name}'"}
        state["added"] = [a for a in state["added"] if a["id"] != ident]
        _log(state, "remove", ident)
        save_state(state)
        return {"ok": True, "removed": ident}

    slot = find_slot(house, name)
    added = next((a for a in state["added"] if a["id"] == name or name.lower() in a["id"].lower()), None)
    if not slot and not added:
        # be precise about *why*: structure is refused by name, not mistaken for missing
        structural = next((b for b in house["brushes"]
                           if b["kind"] in STRUCTURAL and
                           (b["id"].lower() == name.lower() or name.lower() in b["id"].lower())), None)
        if structural:
            return {"ok": False, "error": f"'{structural['id']}' is structure ({structural['kind']}) — "
                                          f"she may not move, hide or recolour it"}
        door = next((d for d in house["doors"]
                     if d["id"].lower() == name.lower() or name.lower() in d["id"].lower()), None)
        if door:
            return {"ok": False, "error": f"'{door['id']}' is a doorway — structure. It opens and closes; "
                                          f"it does not move"}
        return {"ok": False, "error": f"no slot matching '{name}' (try `list`)"}

    if op in ("move", "recolor", "hide", "show") and slot and slot["kind"] in STRUCTURAL:
        return {"ok": False, "error": f"'{slot['id']}' is structure — she may not move or hide it"}

    target = slot["id"] if slot else added["id"]

    if op == "move":
        try:
            d = [float(x) for x in rest[:3]]
        except (ValueError, IndexError):
            return {"ok": False, "error": "usage: move <slot> dx dy dz"}
        cur = state["moves"].get(target, [0, 0, 0])
        new = [cur[i] + d[i] for i in range(3)]
        if max(abs(x) for x in new) > 6:
            return {"ok": False, "error": "that is more than 6 m from where it was built — "
                                          "move it in smaller steps"}
        state["moves"][target] = [round(x, 3) for x in new]
        _log(state, "move", f"{target} → {state['moves'][target]}")
        save_state(state)
        return {"ok": True, "moved": {target: state["moves"][target]}}

    if op == "recolor":
        if not rest:
            return {"ok": False, "error": "usage: recolor <slot> <#rrggbb|material>"}
        colour = rest[0]
        if not (re.fullmatch(r"#[0-9a-fA-F]{6}", colour) or re.fullmatch(r"[a-z][a-z0-9_-]{2,20}", colour)):
            return {"ok": False, "error": f"'{colour}' is neither a #rrggbb colour nor a material name"}
        state["colors"][target] = colour
        state["palette"][target] = colour
        _log(state, "recolor", f"{target} → {colour}")
        save_state(state)
        return {"ok": True, "coloured": {target: colour}}

    if op == "hide":
        if target not in state["hidden"]:
            state["hidden"].append(target)
        _log(state, "hide", target)
        save_state(state)
        return {"ok": True, "hidden": target}

    if op == "show":
        if target in state["hidden"]:
            state["hidden"].remove(target)
        _log(state, "show", target)
        save_state(state)
        return {"ok": True, "shown": target}

    return {"ok": False, "error": f"unknown op '{op}'"}


def overlay(house, state):
    """The house as she has it — what the world actually renders."""
    out = json.loads(json.dumps(house))
    for b in out["brushes"]:
        b["hidden"] = b["id"] in state["hidden"]
        if b["id"] in state["moves"]:
            d = state["moves"][b["id"]]
            b["min"] = [b["min"][i] + d[i] for i in range(3)]
            b["max"] = [b["max"][i] + d[i] for i in range(3)]
        if b["id"] in state["colors"]:
            b["material"] = state["colors"][b["id"]]
    for a in state["added"]:
        w, h, d = a["size"]
        b = {"id": a["id"], "room": a["room"], "kind": "decor", "material": a["material"],
             "min": [a["at"][0] - w / 2, a["at"][1], a["at"][2] - d / 2],
             "max": [a["at"][0] + w / 2, a["at"][1] + h, a["at"][2] + d / 2],
             "note": a.get("label"), "added": True, "hidden": False}
        out["brushes"].append(b)
    out["her_state"] = {"moves": len(state["moves"]), "colors": len(state["colors"]),
                        "hidden": len(state["hidden"]), "added": len(state["added"]),
                        "notes": len(state["notes"])}
    return out


def main():
    house, state = load_house(), load_state()
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    result = apply_op(house, state, sys.argv[1], sys.argv[2:])
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
