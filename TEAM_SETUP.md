# Team setup: Video Prompt Director

Everyone runs their own copy on their own laptop. Your results go into **your own log files**, so nobody's work overwrites anyone else's.

> Status: tested on one Mac only. Windows and Linux steps below are untested.

## 1. Install (once)

| Tool | Where | Check |
|---|---|---|
| Git | git-scm.com (Mac: `git --version` offers to install) | `git --version` |
| Python 3.10+ | python.org | `python3 --version` (Windows: `python --version`) |
| Ollama | ollama.com | `ollama --version` |

No Python packages are needed. The agent uses only the standard library.

## 2. Get the code

```bash
git clone -b video-prompt-director https://github.com/utdcapstone-serfis/video-prompt-director-.git
cd video-prompt-director-
```

`main` is empty on GitHub, so the `-b video-prompt-director` part is required. The repo is private: sign in with your GitHub login, or with a personal access token as the password. Never paste a token into chat or commit it.

## 3. Download the model (about 2.5 GB)

```bash
ollama pull qwen3:4b
```

Keep Ollama running while you use the agent. If your laptop has less than 8 GB of memory or cannot run Ollama, you can still use everything except drafting: see "No local model" below.

## 4. Tell the agent who you are

```bash
python3 agent.py config --person "yourname" --hf-script "/full/path/to/hf.py"
```

- `--person` names your log folder. Use a short name with no spaces.
- `--hf-script` is only needed to generate videos. It is the Higgsfield `hf.py` script from the Higgsfield skill.
- This saves to `settings.local.json`, which is gitignored and stays on your machine.
- Run `python3 agent.py config` with no options any time to see the settings in use.

Your Higgsfield key goes in your own shell profile, never in a file in this repo:

```bash
export HF_KEY="your-key-id:your-secret"
```

Create your own key at console.higgsfield.ai. Do not reuse anyone else's. Generating videos spends your prepaid API balance, so `generate` does a dry run unless you add `--yes`.

## 5. Check it works (free)

```bash
python3 agent.py draft "Candle ad on a wooden shelf" --duration 4 --must candle
python3 agent.py list
```

## Daily use

```bash
python3 agent.py draft "<brief>" --duration 6 --must <words> --ban <words>
python3 agent.py estimate <run>                    # price check, free
python3 agent.py generate <run> --yes --resolution 480p
python3 agent.py review <run> --score 1-5 --failure CODE --notes "what happened"
python3 agent.py revise <run>
python3 agent.py import --prompt-file p.txt --video v.mp4 --brief "..." --duration 30   # log a video made elsewhere
python3 agent.py dashboard                         # writes reports/dashboard.html
```

Failure codes are in `kb/failure_taxonomy.md`. Use `NONE` when nothing went wrong.

## How logs work (and what is shared)

- Your working database is `director.db`. It is private to your machine and gitignored.
- After every command the agent also writes `logs/<yourname>/runs.jsonl` and `lessons.jsonl`. Only you edit those files, so they never conflict with a teammate's.
- `python3 agent.py team` lists everyone whose logs your machine can see. `report` and `dashboard` combine all of them. Teammates' videos are not on your machine, so their rows show no video.
- Lessons stay per person. A teammate's lesson never changes your drafts. Shared knowledge goes through `kb/guidance.jsonl` instead (below).

### Serfis material stays out of GitHub

`director.db`, `logs/`, `reports/`, `videos/` and `settings.local.json` are gitignored on purpose, because prompts and videos for Serfis are client material. Do not remove them from `.gitignore`. To share logs, use a private shared folder the whole team can reach, such as a Google Drive folder:

1. Make a shared folder, for example `director-logs`, and sync it to every laptop (Drive for desktop).
2. Each person points their own logs at it and tells the agent to read it:

```bash
python3 agent.py config --log-dir "/path/to/director-logs" --add-team-dir "/path/to/director-logs"
```

Each person then writes only to their own subfolder (`director-logs/<yourname>/`), so the sync has nothing to merge. Sync can lag by a few minutes. Not tested yet with real Drive sync.

## Shared knowledge (code review required)

`kb/system_prompt.md` and `kb/guidance.jsonl` change how every draft is written. Edit them on a branch and open a pull request. Do not edit them directly on `main`. Guidance starts as `unverified` and only reaches the model after it is promoted with evidence from a run.

`data/heldout_briefs.json` is locked for the final comparison. Nobody tunes on it.

## No local model

Teammates whose laptop cannot run Ollama can:
- review videos and log scores,
- import videos made elsewhere,
- read the shared logs and dashboard.

Drafting needs a model. Options once the team decides: a shared hosted model API (costs money per draft), or a rented GPU. Neither is built yet.

## Using another model

```bash
ollama pull <model>
python3 agent.py config --model <model>
```

The model choice is unproven: qwen3:4b was picked for convenience, not because it beat the others.

## Troubleshooting

| Problem | Fix |
|---|---|
| "The model failed twice. Is Ollama running?" | Start the Ollama app, then retry. |
| `generate` says it cannot find hf.py | Set `--hf-script` (step 4). |
| `generate` fails and says no charge | Your Higgsfield API balance is probably too low. |
| Teammate's runs are missing | Run `python3 agent.py team` and check the folders it lists. |
| `git pull` deleted my `director.db` | An old commit tracked it. Restore it from your Trash or start fresh. |
