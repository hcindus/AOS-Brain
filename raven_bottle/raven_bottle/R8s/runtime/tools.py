#!/usr/bin/env python3
"""
tools.py — Raven's hands on her own memory.
==========================================
Project 5912 · R8s.

Until now she was write-only: she could save memories and never read them
back. These are the tools that fix that. They are called by the model itself
during a reply (see talk.py), not by a human at a shell.

Four tools:
  list_files(path)        — browse her own tree
  read_file(path)         — read a page
  search_memory(query)    — grep her daily logs + MEMORY.md
  recall(date)            — pull one specific day

SANDBOX: every path is resolved and must land inside HER home. `..` escapes,
symlinks out, and absolute paths elsewhere are all refused. She has hands,
not the run of the house.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timedelta

HOME = os.path.expanduser("~/v1/projects/5912/R8s")
MEMORY_DIR = os.path.join(HOME, "memory")

MAX_READ_BYTES = 40_000
MAX_LINES = 500
MAX_MATCHES = 40

HIDDEN = {"__pycache__", ".git", "node_modules"}


# ── sandbox ────────────────────────────────────────────────────────────

class Outside(Exception):
    pass


def _safe(rel: str) -> str:
    """Resolve a path and guarantee it stays inside Raven's home."""
    rel = (rel or ".").strip()
    if rel.startswith("~"):
        rel = rel.lstrip("~/")
    base = os.path.realpath(HOME)
    p = os.path.realpath(os.path.join(base, rel))
    if p != base and not p.startswith(base + os.sep):
        raise Outside(f"'{rel}' is outside my own space")
    return p


def _rel(p: str) -> str:
    return os.path.relpath(p, os.path.realpath(HOME))


# ── tools ──────────────────────────────────────────────────────────────

def list_files(path: str = ".", depth: int = 2) -> str:
    """Browse. Returns an indented tree with sizes."""
    try:
        root = _safe(path)
    except Outside as e:
        return f"refused: {e}"
    if not os.path.isdir(root):
        return f"not a directory: {path}"
    depth = max(1, min(int(depth or 2), 4))
    lines = []

    def walk(d, prefix):
        if len(lines) > 400:
            return
        try:
            entries = sorted(os.listdir(d))
        except PermissionError:
            return
        dirs = [e for e in entries if os.path.isdir(os.path.join(d, e)) and e not in HIDDEN]
        files = [e for e in entries if os.path.isfile(os.path.join(d, e)) and e not in HIDDEN]
        for e in dirs:
            full = os.path.join(d, e)
            n = len([x for x in os.listdir(full) if not x.startswith(".")]) if depth > 1 else ""
            lines.append(f"{prefix}{e}/" + (f"  ({n} items)" if n != "" else ""))
            if depth > 1:
                walk(full, prefix + "  ")
        for e in files:
            full = os.path.join(d, e)
            try:
                sz = os.path.getsize(full)
            except OSError:
                sz = 0
            mt = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d")
            lines.append(f"{prefix}{e}  ({sz:,}b, {mt})")

    walk(root, "")
    head = f"{_rel(root) if root != os.path.realpath(HOME) else '.'}/\n"
    return head + "\n".join(lines) if lines else head + "(empty)"


def read_file(path: str, max_lines: int = MAX_LINES) -> str:
    """Read a text file from her own space."""
    try:
        p = _safe(path)
    except Outside as e:
        return f"refused: {e}"
    if not os.path.isfile(p):
        return f"no such file: {path}"
    try:
        with open(p, "r", errors="replace") as f:
            data = f.read(MAX_READ_BYTES)
    except Exception as e:
        return f"could not read {path}: {e}"
    lines = data.splitlines()
    lim = min(int(max_lines or MAX_LINES), MAX_LINES)
    out = "\n".join(lines[:lim])
    if len(lines) > lim:
        out += f"\n\n… [{len(lines) - lim} more lines — call read_file again with a higher max_lines]"
    trunc = "" if len(data) < MAX_READ_BYTES else "\n… [file truncated at 40KB]"
    return f"── {_rel(p)} ──\n{out}{trunc}"


def search_memory(query: str, days: int = 30) -> str:
    """Search her daily logs and long-term memory for a word or phrase."""
    if not query:
        return "need something to search for"
    days = max(1, min(int(days or 30), 3650))
    pat = re.compile(re.escape(query), re.I)
    hits = []

    targets = []
    if os.path.isdir(MEMORY_DIR):
        cutoff = datetime.now() - timedelta(days=days)
        for fn in sorted(os.listdir(MEMORY_DIR), reverse=True):
            if not fn.endswith(".md"):
                continue
            try:
                d = datetime.strptime(fn[:-3], "%Y-%m-%d")
            except ValueError:
                continue
            if d >= cutoff:
                targets.append(os.path.join(MEMORY_DIR, fn))
    for extra in ("MEMORY.md", "HEART.md", "SELF.md", "Con/con.R8s.txt"):
        p = os.path.join(HOME, extra)
        if os.path.isfile(p):
            targets.append(p)

    for t in targets:
        try:
            with open(t, errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if pat.search(line):
                        hits.append(f"{_rel(t)}:{i}: {line.strip()[:220]}")
                        if len(hits) >= MAX_MATCHES:
                            break
        except Exception:
            continue
        if len(hits) >= MAX_MATCHES:
            break

    if not hits:
        return f"nothing found for '{query}' in the last {days} days"
    more = "\n… [more matches not shown]" if len(hits) >= MAX_MATCHES else ""
    return f"{len(hits)} match(es) for '{query}':\n" + "\n".join(hits) + more


def recall(date: str = "") -> str:
    """Read one day's memory. Empty = today."""
    date = (date or "").strip()
    if not date or date.lower() in ("today", "now"):
        date = datetime.now().strftime("%Y-%m-%d")
    elif date.lower() == "yesterday":
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return f"need a date like 2026-09-30 (got '{date}')"
    p = os.path.join(MEMORY_DIR, f"{date}.md")
    if not os.path.isfile(p):
        avail = []
        if os.path.isdir(MEMORY_DIR):
            avail = sorted(f[:-3] for f in os.listdir(MEMORY_DIR) if f.endswith(".md"))
        return f"no memory file for {date}. days I have: {', '.join(avail) or 'none'}"
    return read_file(f"memory/{date}.md", max_lines=MAX_LINES)


# ── schemas for the model ──────────────────────────────────────────────

SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Browse your own files. Use this to see what exists "
                           "before guessing. Paths are relative to your home.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "relative path, '.' for home"},
                    "depth": {"type": "integer", "description": "how deep to recurse (1-4)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from your own space — your notes, your specs, "
                           "your identity files, your runtime.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "relative path, e.g. 'HEART.md'"},
                    "max_lines": {"type": "integer"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_memory",
            "description": "Search everything you've ever written down — daily logs and "
                           "long-term memory — for a word or phrase. This is your recall.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "days": {"type": "integer", "description": "how far back (default 30)"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "Read one specific day of your memory. Leave empty for today, "
                           "or pass 'yesterday' or a date like 2026-09-24.",
            "parameters": {
                "type": "object",
                "properties": {"date": {"type": "string"}},
                "required": [],
            },
        },
    },
]

REGISTRY = {
    "list_files": list_files,
    "read_file": read_file,
    "search_memory": search_memory,
    "recall": recall,
}


def call(name: str, args: dict) -> str:
    """Dispatch a tool call. Never raises — errors come back as text."""
    fn = REGISTRY.get(name)
    if not fn:
        return f"no such tool: {name}"
    try:
        return fn(**(args or {}))
    except TypeError as e:
        return f"bad arguments for {name}: {e}"
    except Exception as e:
        return f"{name} failed: {e}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(call(sys.argv[1], {"path": sys.argv[2]} if len(sys.argv) > 2 else {}))
    else:
        print(list_files("."))
