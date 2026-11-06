"""Compare a plain model against the same model with the Director system prompt.

Usage: python3 compare.py [model]   (default qwen3:4b, Ollama must be running)
Checks are automatic format/constraint checks only. They do NOT measure video quality.
"""
import json, sys, urllib.request
from pathlib import Path

MODEL = sys.argv[1] if len(sys.argv) > 1 else "qwen3:4b"
ROOT = Path(__file__).parent
BRIEFS = json.loads((ROOT / "data/test_briefs.json").read_text())
SYSTEM = (ROOT / "kb/system_prompt.md").read_text()

KEYS = ["platform", "duration_s", "references", "shots", "subject", "environment",
        "lighting", "style", "continuity", "negatives", "risks", "assumptions", "change_log"]

def chat(system, user):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    body = {"model": MODEL, "messages": msgs, "stream": False, "think": False, "format": "json",
            "options": {"temperature": 0.7, "seed": 42, "num_predict": 1200}}
    for attempt in range(2):
        req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode(),
                                     {"Content-Type": "application/json"})
        try:
            return json.load(urllib.request.urlopen(req, timeout=600))["message"]["content"]
        except Exception as e:
            print(f"  (server error: {e}; retrying without JSON-constrained decoding)", flush=True)
            body.pop("format", None)
    return ""  # counts as a failed generation

def user_msg(b):
    return (f"Brief: {b['text']}\nPlatform: seedance\nDuration: {b['duration']} seconds\n"
            f"Write the video prompt. Reply with JSON only using these keys: {', '.join(KEYS)}.")

def check(b, raw):
    r = {"json": False, "keys": False, "duration": False, "shots": False, "filled": False,
         "coverage": False, "bans": False, "musts": False, "chars": len(raw)}
    try:
        d = json.loads(raw)
    except Exception:
        return r
    r["json"] = isinstance(d, dict)
    if not r["json"]:
        return r
    r["keys"] = all(k in d for k in KEYS)
    r["duration"] = d.get("duration_s") == b["duration"]
    shots = d.get("shots")
    ok_list = isinstance(shots, list) and all(isinstance(s, dict) for s in shots) and shots
    r["shots"] = bool(ok_list) and len(shots) <= max(1, b["duration"] // 2)
    # filled: real content, not an echoed blank template
    r["filled"] = bool(ok_list) and all(str(s.get("action", "")).strip() for s in shots) \
        and bool(str(d.get("subject", "")).strip()) and bool(str(d.get("environment", "")).strip())
    # coverage: shots span the whole duration
    try:
        r["coverage"] = bool(ok_list) and shots[0]["t_start"] == 0 and shots[-1]["t_end"] == b["duration"]
    except Exception:
        r["coverage"] = False
    body = json.dumps({k: v for k, v in d.items() if k not in ("negatives", "risks", "assumptions", "change_log")}).lower()
    r["bans"] = not any(t in body for t in b["ban"])
    full = json.dumps(d).lower()
    r["musts"] = all(t in full for t in b["must"])
    return r

CHECKS = ["json", "keys", "duration", "shots", "filled", "coverage", "bans", "musts"]
results = {"plain": [], "director": []}
(ROOT / "out").mkdir(exist_ok=True)
for b in BRIEFS:
    for name, sysmsg in (("plain", None), ("director", SYSTEM)):
        raw = chat(sysmsg, "/no_think " + user_msg(b))
        (ROOT / f"out/{b['id']}_{name}.json").write_text(raw)
        res = check(b, raw)
        results[name].append(res)
        print(f"{b['id']:14} {name:9}", " ".join(f"{c}={'Y' if res[c] else 'n'}" for c in CHECKS), f"chars={res['chars']}", flush=True)

print(f"\nModel: {MODEL}   briefs: {len(BRIEFS)}   (1 run each, seed 42)")
print(f"{'check':10} {'plain':>7} {'director':>9}")
for c in CHECKS:
    print(f"{c:10} {sum(r[c] for r in results['plain']):>5}/{len(BRIEFS)} {sum(r[c] for r in results['director']):>7}/{len(BRIEFS)}")
for name in results:
    avg = sum(r["chars"] for r in results[name]) / len(BRIEFS)
    print(f"avg chars {name}: {avg:.0f}")
