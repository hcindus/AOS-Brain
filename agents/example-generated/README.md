# Example Generated Agent

**Name:** example-generated
**Created:** 2026-07-22T05:30:00

This is a demonstration of the Skill Builder output. This agent was created via natural language conversation.

## How to Create Your Own

Run the skill builder:
```bash
python3 /root/.openclaw/workspace/skills/skill-builder/scripts/skill-builder.py
```

Then follow the interview prompts.

## Generated Files

An agent consists of:
- `{name}_agent.py` - The main Python code
- `{name}.service` - Systemd service definition
- `config.json` - Runtime configuration
- `README.md` - This documentation

## Integration

Agents integrate with:
- BHSI v4 (Binary High-Integrity System)
- AOS Brain v4.5 socket interface
- Society Agent ecosystem
- Keepalive monitoring

## Next Steps

1. Edit the generated `{name}_agent.py`
2. Implement the `execute()` method
3. Test with `python3 {name}_agent.py`
4. Install with the provided systemctl commands
