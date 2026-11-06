#!/usr/bin/env python3
"""Extract Claude Code chat history on or after a date, for the /retro skill.

Usage: python3 -I extract.py YYYY-MM-DD OUT_DIR

Reads every transcript in ~/.claude/projects/*/*.jsonl and writes to OUT_DIR:
  messages.txt  the user's own messages, grouped by project and session
  stats.json    session, message, tool and model counts, by project and overall
"""
import collections
import glob
import json
import os
import sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
since, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)

root = os.path.expanduser("~/.claude/projects")
home_prefix = "-" + os.path.expanduser("~").strip("/").replace("/", "-") + "-"

sessions = collections.defaultdict(list)  # (project, session) -> [(ts, text)]
tools = collections.Counter()
models = collections.Counter()
per_project = collections.defaultdict(lambda: {"sessions": set(), "messages": 0, "output_tokens": 0})
hours = collections.Counter()


def user_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content
                         if isinstance(c, dict) and c.get("type") == "text")
    return ""


for path in glob.glob(os.path.join(root, "*", "*.jsonl")):
    project = os.path.basename(os.path.dirname(path)).replace(home_prefix, "")
    session = os.path.basename(path)[:-6]
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            ts = d.get("timestamp") or ""
            if ts[:10] < since or d.get("isSidechain"):
                continue
            msg = d.get("message") or {}
            if d.get("type") == "assistant":
                if msg.get("model"):
                    models[msg["model"]] += 1
                per_project[project]["output_tokens"] += (msg.get("usage") or {}).get("output_tokens", 0)
                for c in msg.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        tools[c.get("name", "?")] += 1
            elif d.get("type") == "user" and not d.get("isMeta"):
                text = user_text(msg.get("content")).strip()
                # Skip tool results, injected reminders and other harness wrappers,
                # but keep slash-command invocations.
                if not text or (text.startswith("<") and "<command-name>" not in text):
                    continue
                sessions[(project, session)].append((ts, text))
                per_project[project]["sessions"].add(session)
                per_project[project]["messages"] += 1
                hours[ts[11:13]] += 1

with open(os.path.join(out_dir, "messages.txt"), "w") as out:
    for (project, session), msgs in sorted(sessions.items(), key=lambda kv: min(m[0] for m in kv[1])):
        msgs.sort()
        out.write(f"\n=== {project}  {session}  {msgs[0][0][:16]}\n")
        for ts, text in msgs:
            out.write(f"- {ts[:16]}  {text.replace(chr(10), ' / ')[:1500]}\n")

stats = {
    "since": since,
    "sessions": len(sessions),
    "user_messages": sum(len(m) for m in sessions.values()),
    "projects": {p: {"sessions": len(v["sessions"]), "messages": v["messages"],
                     "output_tokens": v["output_tokens"]}
                 for p, v in sorted(per_project.items(), key=lambda kv: -kv[1]["messages"])},
    "top_tools": tools.most_common(15),
    "models": models.most_common(),
    "messages_by_hour_utc": dict(sorted(hours.items())),
}
with open(os.path.join(out_dir, "stats.json"), "w") as out:
    json.dump(stats, out, indent=2)

print(f"{stats['sessions']} sessions, {stats['user_messages']} user messages since {since} -> {out_dir}")
