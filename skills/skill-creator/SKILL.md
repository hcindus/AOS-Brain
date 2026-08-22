---
name: skill-creator
description: Create a reusable skill (SKILL.md) from any transcript, process, or content source. Feed it a transcript, a manual process, or a correction, and it packages it into a markdown skill with frontmatter + steps + rules.
---

# Skill Creator

**Purpose:** Turn any repeatable process, transcript, or correction into a reusable skill — explain it once and never again. This is the "skill-ception" that compounds your capability.

## When to use
- After doing a manual process you'll repeat → capture it as a skill.
- When handed a transcript / course / guide / book chapter → extract the process into a skill.
- When you've corrected the agent on a recurring task → freeze the correction into a skill so it never regresses.

## Process
1. **Input** — receive the source (transcript, process description, or a correction).
2. **Extract the SOP** — pull out the repeatable steps, the rules, and the "when to use" trigger.
3. **Write frontmatter** — `name` (kebab-case) + `description` (a one-liner on *when* to use it).
4. **Write the body** — title, KPI (if measurable), the steps, the rules, and "when to use."
5. **Save** → `skills/<name>/SKILL.md` (create the folder).

## Rules
- One skill = one job-to-be-done. Don't cram multiple processes into one file.
- Keep it under ~200 lines — specific, no fluff.
- The agent should be able to follow it *cold* — no assumed context.
- Name it by the *job*, not the tool (e.g. `viral-hooks`, not `claude-tips`).

## Example output shape

```markdown
---
name: <job-name>
description: <when to use it — one line>
---

# <Title>

**KPI:** <optional measurable outcome>

## Process
1. ...
2. ...

## Rules
- ...
```
