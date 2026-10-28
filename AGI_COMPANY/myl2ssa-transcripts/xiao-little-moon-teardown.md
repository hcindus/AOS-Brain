# Myl2Ssa Transcript — "Little Moon" (Xiao) Companion Robot Teardown

**Logged:** 2026-10-28 (Captain, via Telegram)
**Topic tag:** power — the power system / battery-in-bones reveal
**Source video:** companion-robot teardown (Shenzhen → Pittsburgh robotics lab)

---

## Transcript

On a gray Monday morning in March 2026, a wooden crate the size of a coffin rolled off a truck at a robotics lab outside Pittsburgh. It had come from Shenzhen. It had cost $16,000. And inside, wrapped in foam, folded like she was sleeping, was a woman. Not a woman, a machine built to be one. A Chinese companion robot called Xiao, which means little moon. 5'5, warm to the touch. She can talk, laugh, hold your gaze, and remember your name.

The five American engineers standing around that crate had one plan for her. Take her apart down to the last screw and prove she was cheap junk. Because that is what $16,000 buys you, right? In America, a lifelike humanoid face on a torso gets quoted at $150,000, sometimes $200,000, 10 times the price. So before the lid even came off, the lead engineer made a bet with her team. A month of lunches says this thing is rubber and hype. She lost that bet, because layer by layer what they found inside Little Moon was engineered better than anything America sells at 10 times the price. China did not build a cheap robot. It built a better robot and then made it cheap. And what you are about to see goes much deeper than the price tag.

A skin with a nervous system woven into it. A face that smiles without making a sound. Eyes that were secretly looking back. A battery hidden inside her bones. A memory chip that never stopped listening while they worked. And at the very center of her chest, something none of them expected. Something that made the lead engineer put down her screwdriver and walk out of the room.

[like/subscribe interlude]

Now, you need to meet the people holding the screwdrivers, because what they found only hits as hard as it does once you know who they are. The people who thought they knew.

- **Dana Whitfield** ran the lab. 22 years in robotics. She spent nine of them on a humanoid program at a big American defense contractor, then left to start her own shop. If a robot has a joint, Dana has probably broken one like it.
- **Marcus Reyes** was the actuator guy. Motors, gears, the parts that make a robot move. He keeps a drawer full of burned out servos from every robot he has ever opened. He calls it the graveyard.
- **Priya Natarajan** was the material scientist. Skins, polymers, silicons. She once spent 14 months developing a synthetic skin for an American medical mannequin company. It cost $18,000 per body.
- **Tom Kowalski**, big Tom, handled power. 31 years in electrical engineering. He has pulled apart batteries from cars, drones, forklifts, and one very unlucky golf cart.
- **Jenna Park**, 29, the youngest in the room. Chips and code. If there was a brain inside Little Moon, Jenna would find it.

So why were they doing this at all? Here is where it gets serious. An American elder care company had hired them. It was about to spend $40 million building its own companion robot made in the USA for nursing homes and seniors living alone. Before it signed that check, it wanted one question answered. Is this Chinese robot cheap to make or just cheap to sell? Because those are two very different things. If China was losing money on every unit to grab the market, the American company could wait it out. But…

---

## Key power/hardware signals (for Myl2Ssa.R0s — body)

> **Captain's takeaway (2026-10-28):** *"They turned the body into a battery."* This is the design direction to flag — reference material for **battery + heating**. We specced the spine; they went further and made the *body itself* the energy storage. That's the idea worth stealing.

- **Battery hidden inside her bones** — distributed energy storage woven into the skeleton, not a single central pack. The whole body *is* the battery (structural energy storage), rather than a separate pack bolted on.
- **"At the very center of her chest, something none of them expected"** — a power source / energy system at the thoracic core (note: Myl2Ssa spec places power bus posterior spine, branches C3/T4/T10/L2/L5 — worth cross-referencing against a *chest-centered* power reveal).
- **Skin with a nervous system woven into it** — sensory mesh integrated into the silicone skin.
- **Memory chip that "never stopped listening"** — persistent onboard listening/memory.
- **Price asymmetry:** $16,000 (China) vs $150k–$200k (US humanoid face+torso) — the "engineered better, then made cheap" thesis.
