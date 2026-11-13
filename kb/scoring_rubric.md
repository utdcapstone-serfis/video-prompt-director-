# Scoring rubric and failure codes (v1)

One standard for everyone, so a "3" or a "TXT" means the same thing no matter who wrote it. Use it every time you run `python3 agent.py review`.

Never put brand names, client names or prompt text in this file. Keep it generic so it can live on GitHub.

## 1. Before you score

1. Watch the whole video at normal speed, once, with sound on if audio was requested.
2. Watch again, pausing at the start, the middle and the end. Check people, products, text and camera.
3. Compare against the brief and the prompt, not against what you wish it had asked for.
4. Score only what you actually checked. If you didn't check audio, write `audio not checked`.

## 2. The 1 to 5 score

Score the video against its brief. When two scores seem to fit, pick the lower one.

| Score | Name | Meaning | Test question |
|---|---|---|---|
| 5 | Ship it | Every must-have is present. No defect a normal viewer would notice. | Would you send it to the client as is? |
| 4 | Nearly there | Brief met. One or two small flaws, fixable by trimming, a crop or light post work. | Would you send it after a quick fix? |
| 3 | Mixed | The main idea is there, but a clear defect is visible (one major flaw, or several small ones). Needs another generation or a heavy edit. | Would you regenerate it? |
| 2 | Poor | The brief is only partly met, with several major defects. Useful only as a reference for what to change. | Would you throw it away but learn from it? |
| 1 | Fail | Unusable: wrong subject, broken, distorted, or unsafe. | Is it a waste of the generation? |

**Accepted** means a score of 4 or 5 with no major failure. The dashboard counts "accepted" this way.

## 3. Failure codes

Choose **one primary code**: the single defect that most lowered the score. Use `NONE` only when there is nothing worth fixing, which normally means a 5.

| Code | Name | Use it when | Example symptom |
|---|---|---|---|
| ID | Identity | A person's face, hair or outfit is wrong or changes. | Two characters with the same hairstyle. A face that changes mid-clip. |
| CNT | Count | The number of people or objects is wrong. | Six people where the brief said four. One dumbbell instead of two. |
| PRD | Product fidelity | The product's shape, color, size or design differs from the brief or reference. | A tube that changes shape. A carton that becomes a bottle. |
| REF | Reference use | A reference image or video is ignored, leaks unwanted parts, or is mismatched. | Elements of a reference image appear that were meant to be removed. |
| TXT | Text and logos | Text on products or screen is unreadable, misspelled, invented, or unwanted. | Garbled packaging lettering. Stray fine print in a corner. |
| CAM | Camera | The camera does something the brief did not ask for, or skips what it asked for. | A zoom when zoom was banned. A static shot that pushes in. |
| MOT | Motion and physics | Movement looks wrong or impossible. | Melting hands, objects passing through each other, wrong exercise form. |
| TIME | Timeline | Too much happens for the length, or a beat is missing or rushed. | The last requested action never appears. |
| BRF | Brief miss | A required scene, action or element from the brief is absent, and no other code explains why. | The brief asked for a closing front-on product shot and it never appears. |
| STY | Style and look | Lighting, color, mood or setting does not match the brief. | Dark and moody when the brief said bright and sunny. |
| QLT | Visual quality | The picture is blurry, flickers, has artifacts, or looks low quality. | Smeared faces. Jittering background. |
| CONT | Continuity | Something differs between cuts that should match. | A room that changes color between shots. |
| AUD | Audio | Sound, music or voice-over is wrong, missing or out of sync. | The voice-over says different words than the brief. |
| PRM | Prompt fault | The prompt itself caused the problem: contradictions, overload, or hype words. | Two instructions that conflict. |
| OTHER | Other | None of the above. Explain it in the notes. | |

If two problems matter, put the second one in the notes as `also: CODE`. Do not invent new codes. Propose one in the team chat and add it here.

**Tie-breakers**
- Product wrong → PRD, not ID or REF.
- Wrong text on a product → TXT, not PRD.
- A person's look wrong → ID. A person's count wrong → CNT.
- Something missing that the brief asked for, with no better code → BRF.

## 4. Severity

Add a severity to every defect you list. It tells the next person how much it hurt.

| Severity | Meaning |
|---|---|
| minor | Most viewers won't notice, or a small crop or edit hides it. |
| major | A normal viewer notices and it weakens the ad. |
| blocker | The video cannot be used. |

Severity guides the score: a blocker usually means 1 or 2, a major usually means 3, and only minor flaws leave a 4 or 5. If your score and severity disagree, explain why in the notes.

## 5. How to write the notes

One line per defect, in this shape:

`[CODE, severity] what happened | where (second mark) | how you know`

Then one closing line:

`Settings: model, resolution, duration, audio on/off | Checked: what you watched, what you did not`

Examples (generic):
- `[CNT, minor] six people in one overhead shot, brief said four | 14s | counted in the frame`
- `[TXT, major] packaging lettering is garbled and unreadable | 4s to 7s | zoomed in on the cartons`
- `Settings: seedance-2.0, 480p, 7s, no audio | Checked: 4 frames of 8, audio not checked`

**Rules for notes**
- Describe what you see, not what you think caused it. Write `cause unknown` when you do not know.
- Mark anything you are unsure of with `unconfirmed`.
- No judging words like "bad" or "weird" without a symptom after them.
- Never paste the prompt, the client's name or a product name.

## 6. Quick checklist per video

Answer yes or no. Every "no" becomes a defect line.

1. Is the number of people correct in every shot?
2. Does each person look different from the others, and the same across shots?
3. Is the product correct in shape, color and design?
4. Is all text readable, correct, and only the text that was asked for?
5. Does the camera do what the brief asked, and nothing banned?
6. Does every requested scene and action appear?
7. Does the movement look believable?
8. Does the look match the brief?
9. Is the picture sharp and stable?
10. If audio was requested, does it match the brief?

## 7. Calibration

- Two people should score the same video separately, before comparing.
- A gap of two points or more must be talked through, and the rubric wording fixed if it was unclear.
- Do this on the first five videos, then every tenth video.
- Re-score a video the same way if you score it twice. If you would give it a different score a week later, the rubric needs fixing.

Reference scores so far (generic): a clean video with one wrong people count in a single shot scored 4 with CNT. A video with four clearly different people but unreadable carton text scored 3 with TXT.
