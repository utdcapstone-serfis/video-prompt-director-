#!/usr/bin/env python3
"""Synthetic training-data pipeline for the Video Prompt Director.

IMPORTANT: every example here is SYNTHETIC and UNREVIEWED. A teacher model wrote the prompt and
the lint rules filtered it. No video was generated, so nothing proves these prompts work.
Treat the result as format/constraint training data only.

  python3 build_dataset.py generate --n 60     # resumable; appends to data/synthetic/raw.jsonl
  python3 build_dataset.py export              # filter, dedupe, split -> train.jsonl / val.jsonl
  python3 build_dataset.py stats

The locked held-out briefs and the dev briefs are never used: briefs too similar to them are rejected.
"""
import argparse, hashlib, json, random, re, sys, time
from pathlib import Path

import agent  # reuses llm(), parse(), lint(), render(), guidance(), system_prompt()

ROOT = Path(__file__).parent
OUT = ROOT / "data/synthetic"
RAW = OUT / "raw.jsonl"
SHORT_SYSTEM = "You are a Seedance video prompt director. Output JSON only."

PRODUCTS = ["laptop sleeve", "desk lamp", "sunscreen tube", "electric toothbrush", "blender", "tote bag",
            "sunglasses", "skateboard", "camping tent", "acoustic guitar", "sparkling water bottle",
            "granola bar", "hair dryer", "sheet face mask", "memory foam pillow", "running belt",
            "bike helmet", "stand mixer", "hardcover notebook", "air fryer", "hoodie", "beanie",
            "hand cream", "protein shaker", "resistance bands", "electric kettle", "board game",
            "ceramic plant pot", "leather wallet", "beach towel"]
SETTINGS = ["a sunlit kitchen", "a city sidewalk", "a cozy living room", "a park", "a home office",
            "a gym", "a bright studio", "a bedroom", "a cafe", "a rooftop", "a garage", "a beach"]
PEOPLE = [("no people, hands only", 0), ("one person", 1), ("two friends", 2), ("three people", 3)]
STYLES = ["UGC selfie style", "cinematic", "clean product ad", "lifestyle", "documentary feel", "playful and bright"]
ACTIONS = ["uses it for the first time", "shows it to the camera", "unboxes it", "picks it up and examines it",
           "demonstrates how it works", "reacts with a smile after using it"]
EXTRAS = ["The label must stay readable.", "The logo must face the camera.", "Keep the product in frame the whole time.",
          "One slow camera move only.", "Camera stays steady.", "", "", ""]
BANS = [["drone"], ["zoom out"], ["jump cut"], ["drone", "zoom out"], []]
WORDNUM = {2: "two", 3: "three"}


def make_brief(rng, i):
    prod = rng.choice(PRODUCTS)
    ptxt, n = rng.choice(PEOPLE)
    dur = rng.choice([4, 5, 6, 7, 8, 10])
    text = (f"{prod.capitalize()} ad in {rng.choice(SETTINGS)}, {rng.choice(STYLES)}: {ptxt}, "
            f"{rng.choice(ACTIONS)}. {rng.choice(EXTRAS)}").strip()
    must = [prod.split()[-1]] + ([WORDNUM[n]] if n >= 2 else [])
    return {"id": f"s{i:05d}", "brief": text, "duration": dur, "must": must, "ban": rng.choice(BANS)}


def toks(s):
    return set(re.findall(r"[a-z]{3,}", s.lower()))


def jacc(a, b):
    return len(a & b) / max(1, len(a | b))


def blocked_briefs():
    out = []
    for f, key in (("data/heldout_briefs.json", "briefs"), ("data/test_briefs.json", None)):
        d = json.loads((ROOT / f).read_text())
        out += [x["text"] for x in (d[key] if key else d)]
    return [toks(t) for t in out]


def user_msg(b):
    return (f"Brief: {b['brief']}\nPlatform: seedance\nDuration: {b['duration']} seconds\n"
            f"Must-haves: {b['must'] or 'none'}\nBanned: {b['ban'] or 'none'}\nReturn JSON only.")


def teacher(b):
    gblock, used = agent.guidance(b["brief"] + " " + " ".join(b["must"]))
    user = user_msg(b) + gblock
    raw = agent.llm(agent.system_prompt(), user)
    p = agent.parse(raw)
    if isinstance(p, dict):
        p["references"] = []  # text-to-video takes no media
    issues = agent.lint(p, b["duration"], b["ban"])
    repaired = False
    if issues:
        raw2 = agent.llm(agent.system_prompt(), user + "\n\nYour previous draft had these problems, fix them and return full JSON:\n- "
                         + "\n- ".join(issues) + "\nPrevious draft:\n" + (raw if p is None else json.dumps(p)))
        p2 = agent.parse(raw2)
        if isinstance(p2, dict):
            p2["references"] = []
        issues2 = agent.lint(p2, b["duration"], b["ban"])
        if p2 is not None and len(issues2) <= len(issues):
            p, issues, repaired = p2, issues2, True
    return p, issues, repaired, used


def cmd_generate(a):
    agent.MODEL = a.model
    OUT.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"] for l in RAW.read_text().splitlines() if l.strip()} if RAW.exists() else set()
    blocked = blocked_briefs()
    rng = random.Random(a.seed)
    made = 0
    i = 0
    while made < a.n:
        b = make_brief(rng, i)
        i += 1
        if b["id"] in done:
            continue
        if any(jacc(toks(b["brief"]), bt) > 0.5 for bt in blocked):
            continue  # too close to a locked or dev brief
        t0 = time.time()
        try:
            p, issues, repaired, used = teacher(b)
        except SystemExit as e:
            print("teacher failed:", e); continue
        row = {**b, "output": p, "lint_issues": issues, "repaired": repaired, "guidance_used": used,
               "teacher": a.model, "system_prompt_sha": hashlib.sha256(agent.system_prompt().encode()).hexdigest()[:12],
               "label": "synthetic_unreviewed", "created": time.strftime("%Y-%m-%d %H:%M")}
        with RAW.open("a") as f:
            f.write(json.dumps(row) + "\n")
        made += 1
        print(f"[{made}/{a.n}] {b['id']} {'ok' if not issues else 'LINT: ' + '; '.join(issues)[:90]} ({time.time() - t0:.0f}s)", flush=True)


def passes(r):
    p = r["output"]
    if r["lint_issues"] or not isinstance(p, dict):
        return False, "lint"
    body = json.dumps(p).lower()
    if not all(m.lower() in body or (m == "two" and "2" in body) or (m == "three" and "3" in body) for m in r["must"]):
        return False, "missing_must"
    if len([n for n in p.get("negatives", []) if str(n).strip()]) > 4:
        return False, "too_many_negatives"
    if len(agent.render(p)) > 1500:
        return False, "too_long"
    if not str(p.get("subject", "")).strip() or not str(p.get("environment", "")).strip():
        return False, "empty_fields"
    return True, ""


def cmd_export(a):
    rows = [json.loads(l) for l in RAW.read_text().splitlines() if l.strip()]
    kept, why, seen = [], {}, []
    for r in rows:
        ok, reason = passes(r)
        if ok:
            sig = toks(" ".join(s.get("action", "") for s in r["output"]["shots"]))
            if any(jacc(sig, s) > 0.85 for s in seen):
                ok, reason = False, "near_duplicate"
            else:
                seen.append(sig)
        if ok:
            kept.append(r)
        else:
            why[reason] = why.get(reason, 0) + 1
    rng = random.Random(0)
    rng.shuffle(kept)
    nval = max(1, len(kept) // 10) if kept else 0
    val, train = kept[:nval], kept[nval:]

    def ex(r):
        return {"messages": [{"role": "system", "content": SHORT_SYSTEM},
                             {"role": "user", "content": user_msg(r)},
                             {"role": "assistant", "content": json.dumps(r["output"])}],
                "meta": {"id": r["id"], "label": r["label"], "teacher": r["teacher"],
                         "system_prompt_sha": r["system_prompt_sha"], "created": r["created"]}}
    for name, rs in (("train", train), ("val", val)):
        (OUT / f"{name}.jsonl").write_text("".join(json.dumps(ex(r)) + "\n" for r in rs))
    print(f"raw: {len(rows)}  kept: {len(kept)} ({len(kept) / max(1, len(rows)):.0%})  train: {len(train)}  val: {len(val)}")
    print("rejected:", why or "none")
    print("All examples are labeled synthetic_unreviewed. Drop the 'meta' column before training.")


def cmd_stats(a):
    rows = [json.loads(l) for l in RAW.read_text().splitlines() if l.strip()]
    print(len(rows), "raw rows;", sum(1 for r in rows if not r["lint_issues"]), "lint-clean;",
          sum(1 for r in rows if r["repaired"]), "needed repair")


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate"); g.add_argument("--n", type=int, default=60)
    g.add_argument("--model", default=agent.MODEL); g.add_argument("--seed", type=int, default=1); g.set_defaults(f=cmd_generate)
    sub.add_parser("export").set_defaults(f=cmd_export)
    sub.add_parser("stats").set_defaults(f=cmd_stats)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
