# Experiment plan (ranked by learning per dollar)

Prices use the account estimate from 2026-11-05: about $0.21/s at 480p, $0.46/s at 720p. Check your balance to confirm. Failed or moderated generations are not charged.

## Free now
1. Run the plain-vs-Director format comparison on the locked held-out briefs (`data/heldout_briefs.json`). Do this once, after you stop tuning the system prompt.
2. Keep adding rules to the pre-flight checks.
3. Write down predictions before any paid test, so you can see afterward whether you were right.

## Paid, in order
| # | Experiment | Why it teaches the most | Settings | Rough cost |
|---|---|---|---|---|
| 1 | Plain-model prompt vs Director prompt for the rooftop brief (run 1 already exists as the Director side) | The first real head-to-head | 6s, 480p, same seed/settings as run 1 if possible | ~$1.25 for one extra run |
| 2 | Same brief at 480p vs the 720p run 1 | Tells you if cheap 480p is a reliable screening tier | 6s, 480p | ~$1.25 |
| 3 | Camera wording: "slow pan right" vs "static wide shot then push-in" | Camera failures were central in Start Again | 4s, 480p | ~$0.82 each |
| 4 | Count/prop constraint phrasing: "two men, each holding one silver dumbbell" vs the same with a repeated count in continuity | Directly tests the CNT failure | 4s, 480p | ~$0.82 each |
| 5 | Held-out comparison: 12 briefs, plain vs Director, 1 generation each | The headline result | 480p, brief's own duration | ~$27 for 24 runs |
| 6 | Re-render only the winners at 720p | Check that 480p findings transfer | 720p | ~$2–4 each |

## Rules
- Change one thing at a time.
- Screen at 480p, confirm at 720p.
- One generation is noisy. A claim needs at least 2 to 3 runs, or a clearly large difference across briefs.
- Rate blind where you can. Ask a friend to score videos without knowing which prompt made them.
- Log every run in `director.db`, including failures.

## Budget scenarios
- Minimum credible result (about $5): experiments 1 and 3.
- Solid pilot (about $30): through experiment 5.
