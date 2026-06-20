# Carryover

**Never lose context between coding sessions.**

You close Claude Code mid-task. Tomorrow you open it and the AI has forgotten everything — what you were doing, what's half-broken, what *not* to touch. You burn the first 20 minutes rebuilding context, or worse, the model "helpfully" rewrites something that was already working.

Carryover fixes that with two commands:

- **`/wrap`** — run it when you stop. It reads your git state, asks six quick questions (goal, what's broken, the one next move, what surprised you, what *not* to touch, confidence), and writes a handoff file.
- **`/resume`** — run it when you come back. It reads the handoff, flags anything that drifted since, tells you your next move, and **actually starts it** — opens the file, runs the failing test, drafts the first edit. No cold start.

Handoffs are plain Markdown stored per-project under `~/.claude/sessions/`. They're yours, on disk, git-friendly. No account, no cloud, no telemetry.

---

## Install

### As a plugin (recommended)

```
/plugin marketplace add abhilashi/carryover
/plugin install carryover@carryover
```

Commands are namespaced: **`/carryover:wrap`** and **`/carryover:resume`**.

### Manual (bare `/wrap` and `/resume`)

Copy the skill folders into your Claude config:

```bash
git clone https://github.com/abhilashi/carryover
cp -r carryover/skills/wrap carryover/skills/resume ~/.claude/skills/
```

Now `/wrap` and `/resume` work directly (no namespace prefix).

---

## How it works

```
  coding... ──▶  /wrap  ──▶  ~/.claude/sessions/<project>/handoff.md
                              (next move · blockers · do-not-touch · git state)
                                        │
                              ...hours or days pass...
                                        │
  back at it ◀── starts next move ◀── /resume
```

Each `/wrap` overwrites `handoff.md` (the current state) and appends to `history.md` (the running thread across sessions, so you can see how a project evolved).

## What's in a handoff

```markdown
# Handoff — myapp — 2026-06-20 18:40

## ▶ NEXT MOVE (do this first)
Wire the /login POST to the new auth hook; the form already validates.

## Where I left off
Refactoring auth out of the page component into useAuth().

## Broken / unfinished
Token refresh loops on 401 — see api/client.ts.

## ⛔ Do NOT touch (regression guard)
The session cookie code in middleware.ts works — don't "tidy" it.

## Surprised / learned
The 401 loop is the interceptor retrying before the token is set.

## Confidence in next move: 4/5

## Auto-captured state
- Branch: feature/auth-refactor
- Uncommitted: 3 files
- Recent commits: ...
```

## Why two files

- `handoff.md` — the **latest** state. `/resume` reads this.
- `history.md` — **append-only** log of every wrap. Your project's narrative over time.

## Voice mode (optional)

Prefer to *talk* your debrief instead of typing it? Run:

```
/wrap voice      # speaks each question, records your spoken answer, transcribes it
/resume voice    # speaks your next move back to you
```

It's a "call" with **no phone number** — just your local microphone and an API key. Audio never touches the phone network; the mic is captured locally and only the audio for transcription is sent to the speech-to-text API.

**Setup:**

```bash
# one-time: isolated venv for the audio deps (avoids PEP 668 / touching system Python)
python3 -m venv ~/.claude/carryover/venv
~/.claude/carryover/venv/bin/pip install -r ~/.claude/carryover/requirements.txt
export OPENAI_API_KEY=sk-...                           # used for speech-to-text
```

The skills auto-detect `~/.claude/carryover/venv` and use it; if it's absent they fall back to `python3`.

- **Text-to-speech** uses macOS `say` by default (free, offline). Set `CARRYOVER_TTS=openai` to use OpenAI voices instead.
- **Speech-to-text** uses the OpenAI transcription API (`gpt-4o-mini-transcribe` by default; override with `CARRYOVER_STT_MODEL`).
- On first run, grant your terminal **microphone permission** when macOS prompts.
- The recorder auto-stops after a short pause. Tune sensitivity with `CARRYOVER_VAD_THRESHOLD`.

If voice mode isn't set up, `/wrap voice` falls back to a normal typed debrief — nothing breaks.

## Privacy

Everything stays local by default. Carryover writes only to `~/.claude/sessions/` and reads your repo's git metadata — no account, no phone number, no telemetry. The only network call is in **voice mode**, where recorded audio is sent to your configured speech-to-text provider for transcription (and, if you opt into OpenAI TTS, prompts are sent for synthesis). Text mode is fully offline.

## License

MIT — see [LICENSE](LICENSE).
