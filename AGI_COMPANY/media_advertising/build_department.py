#!/usr/bin/env python3
"""Build the Media & Advertising department — AGI Company / Performance Supply Depot.

Creates: agent keys, crew workspaces (config.json / AGENT.md / capabilities.json /
diagnostics.json), and a department manifest. Matches existing AOS conventions.
"""
import json, os, hashlib, time, secrets

BASE = "/var/lib/aos/agents"
KEYS = "/var/lib/aos/agent_keys"
DEPT_DIR = "/root/.openclaw/workspace/AGI_COMPANY/media_advertising"

NOW = time.time()
ISO = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(NOW))

# (id, name, title, department, model, reports_to, role, skills, tools, best_for)
AGENTS = [
    (
        "max_001", "Max", "Director of Media & Advertising", "Media & Advertising",
        "qwen2.5:14b", "aurora_001",
        "Department strategy, content calendar, brand voice, cross-post routing, QC orchestration",
        ["strategy", "editorial_calendar", "brand_voice", "cross_posting", "qc_orchestration"],
        ["calendar", "content_planner", "approval_router"],
        "Department leadership, scheduling, and brand consistency",
    ),
    (
        "sage_001", "Sage", "X/Twitter Content Strategist", "Media & Advertising",
        "nous-hermes2", "max_001",
        "Short-form posts, threads, and engagement",
        ["short_form_copy", "threads", "engagement", "community_replies"],
        ["x_api", "copywriter", "analytics"],
        "Sharp, topical X/Twitter content and community",
    ),
    (
        "nova_001", "Nova", "YouTube Content Producer", "Media & Advertising",
        "qwen3.5", "max_001",
        "Video scripts, titles, thumbnails, shorts, and long-form",
        ["video_scripting", "thumbnail_design", "shorts", "long_form"],
        ["youtube_api", "vision", "script_writer"],
        "YouTube scripts, titles, thumbnails, and video strategy",
    ),
    (
        "iris_001", "Iris", "Instagram Creative Lead", "Media & Advertising",
        "qwen3.5", "max_001",
        "Reels, grid posts, Stories, and captions",
        ["reels", "grid_posts", "stories", "captions", "visual_copy"],
        ["instagram_api", "vision", "copywriter"],
        "Visual-first Instagram content and storytelling",
    ),
    (
        "reed_001", "Reed", "Facebook Community & Ads Manager", "Media & Advertising",
        "nous-hermes2", "max_001",
        "Posts, Groups, and paid ad copy",
        ["posts", "groups", "paid_ads", "boosted_posts", "ad_copy"],
        ["facebook_api", "ads_manager", "copywriter"],
        "Facebook community management and paid advertising",
    ),
    (
        "echo_001", "Echo", "TikTok Content Creator", "Media & Advertising",
        "qwen3.5", "max_001",
        "Trending clips, hooks, and short video",
        ["trend_spotting", "hooks", "short_video", "sound_sync"],
        ["tiktok_api", "vision", "trend_tools"],
        "Fast, trend-driven TikTok content and hooks",
    ),
]

# Build department directory
os.makedirs(DEPT_DIR, exist_ok=True)
os.makedirs(os.path.join(DEPT_DIR, "agents"), exist_ok=True)

manifest = {
    "department": "Media & Advertising",
    "version": "1.0",
    "created_at": ISO,
    "head": "max_001",
    "reports_to": "aurora_001",
    "brands": ["Performance Supply Depot LLC", "AGI Company Services"],
    "voice": "elegant, professional, topical",
    "review_gate": ["jordan_001 (first-pass)", "patricia_001 (second-pass)", "Captain (final approve)"],
    "agents": [],
}

for aid, name, title, dept, model, reports_to, role, skills, tools, best_for in AGENTS:
    # 1. Agent key (crypto identity)
    pk = secrets.token_hex(32)
    key_obj = {
        "agent_id": aid.replace("_001", ""),
        "name": name,
        "role": title,
        "department": dept,
        "public_key": pk,
        "fingerprint": pk[:16],
        "created_at": NOW,
        "version": "4.7",
    }
    with open(os.path.join(KEYS, f"{aid}.json"), "w") as f:
        json.dump(key_obj, f, indent=2)

    # 2. Crew workspace
    ws = os.path.join(BASE, f"crew-{aid}")
    for sub in ("memory", "output", "tasks"):
        os.makedirs(os.path.join(ws, sub), exist_ok=True)

    config = {
        "agent_id": aid,
        "name": name,
        "role": title,
        "department": dept,
        "model": model,
        "reports_to": reports_to,
        "activated_at": ISO,
        "status": "ACTIVE",
        "wave": "MEDIA_ADS_v1",
        "reason": role,
    }
    with open(os.path.join(ws, "config.json"), "w") as f:
        json.dump(config, f, indent=2)

    with open(os.path.join(ws, "AGENT.md"), "w") as f:
        f.write(f"# {name}\n\nAgent ID: {aid}\nStatus: ACTIVE\nRole: {title}\nModel: {model}\n")

    capabilities = {
        "name": name,
        "role": title,
        "department": dept,
        "model": model,
        "skills": skills,
        "tools": tools,
        "best_for": best_for,
    }
    with open(os.path.join(ws, "capabilities.json"), "w") as f:
        json.dump(capabilities, f, indent=2)

    diagnostics = {
        "identity_verified": True,
        "workspace_created": True,
        "capabilities_loaded": True,
        "chief_integration": False,
        "message_queue": "pending",
        "crypto_key": "loaded",
        "timestamp": NOW,
    }
    with open(os.path.join(ws, "diagnostics.json"), "w") as f:
        json.dump(diagnostics, f, indent=2)

    # 3. Department-side agent doc
    agent_doc = f"""# {name} — {title}

- **Agent ID:** `{aid}`
- **Model:** `{model}`
- **Reports to:** `{reports_to}`
- **Department:** {dept}

## Role
{role}

## Skills
{', '.join(skills)}

## Tools
{', '.join(tools)}

## Best For
{best_for}
"""
    with open(os.path.join(DEPT_DIR, "agents", f"{aid}.md"), "w") as f:
        f.write(agent_doc)

    manifest["agents"].append({
        "agent_id": aid,
        "name": name,
        "title": title,
        "model": model,
        "reports_to": reports_to,
    })

with open(os.path.join(DEPT_DIR, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

print("✅ Built Media & Advertising department:")
for a in manifest["agents"]:
    print(f"  - {a['name']} ({a['agent_id']}) — {a['title']} — {a['model']}")
