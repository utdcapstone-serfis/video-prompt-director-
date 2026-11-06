# Video prompt failure taxonomy (draft v0.1)

Status key: **observed** = confirmed in a real generation, **inferred** = suggested by prompt history, **hypothesis** = plausible, untested. Nothing below is marked observed yet. Update this after reviewing real outputs.

Each failure has a code, a visible symptom, an automatic or human check, and a targeted fix to test.

| Code | Failure | Symptom | Check | Fix to test | Status |
|---|---|---|---|---|---|
| ID | Identity drift | Face, hair, or outfit changes mid-clip | Compare faces/outfits in first, middle, last frames | Character sheet reference; describe each person once, in the same words every time; fewer people | inferred |
| CNT | Wrong count | Wrong number of people or props (one dumbbell instead of two) | Count people and each prop per sampled frame | State counts explicitly; keep props visible and simple; reduce the number of tracked objects | hypothesis |
| REF | Reference leakage | Element from the reference image persists after you tell the model to remove it | Check for the named element in all frames | Edit or regenerate the reference image so the element is absent, instead of instructing removal | inferred |
| TXT | Text or logo fidelity | Letters morph, misspell, or logo geometry changes | Read text in frames; compare logo to reference | Shorter on-screen text; add long text in post; give logo as a reference image with a short lock phrase | inferred |
| CAM | Camera mismatch | Drone move when a static camera was wanted, or a zoom-out that was banned | Describe camera path from frames | One camera move per shot, in plain terms; state the starting frame and the ending frame | hypothesis |
| MOT | Motion or physics | Impossible limbs, passing through objects, poor exercise form | Human review; frame-by-frame for hands and contact | One action per shot; simpler poses; avoid physical contact between a person and a rendered object | inferred |
| TIME | Overstuffed timeline | More events than the duration can show; later beats skipped or rushed | Count beats against seconds | Cap beats by duration (see system prompt); split into separate clips and join | inferred |
| CONT | Continuity break | Scene, lighting, or character differs between cuts or clips | Compare last frame of clip N to first frame of clip N+1 | Use the last frame of one clip as the first-frame reference of the next | hypothesis |
| AUD | Audio mismatch | Voiceover timing or sound effects not aligned to action | Listen with the timeline | Fewer audio cues; keep dialogue short; consider adding audio in post | hypothesis |
| PRM | Prompt-design fault | Contradictions, hype tokens, very long prompt, negatives that name the unwanted thing | Lint the prompt before generating | Remove contradictions; shorten; move constraints to positive phrasing; keep the negatives list short | inferred |

## How this is used
1. The **evaluator** uses the Check column to build yes/no questions per video.
2. The **Director** uses the Fix column to write a targeted revision for a diagnosed failure.
3. Every fix stays a hypothesis until it succeeds on repeated runs. Only then does it move to "verified" in the knowledge base.
