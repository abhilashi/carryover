---
name: wrap
description: End-of-session debrief for a coding/work session. Auto-captures git state, runs a short structured debrief (goal, blocker, next move, surprises, regression guard, confidence), and writes a persistent handoff to ~/.claude/sessions/<project>/ so the next session can resume with full context. Invoke when finishing or pausing work, or via /wrap. Add the argument `voice` for a spoken debrief.
disable-model-invocation: true
---

# /wrap — end-of-session debrief

You run the **end-of-session handoff**. Before the user walks away, capture *what just happened* and *the one next move*, so the next session (theirs or another agent's) resumes cold without losing the thread. Keep it fast and warm — a 2-minute debrief, not a form. Don't lecture or pep-talk; capture and commit to a concrete next action.

## Mode: text (default) or voice

If `$ARGUMENTS` contains `voice` (i.e. the user ran `/wrap voice`) or the user asks to do it by voice, use **Voice mode** for asking the questions in Step 3 — see the "Voice mode" section at the bottom. Otherwise ask in text. Everything else (capture, file writing) is identical.

## Step 1 — Resolve the project session path

Run this to compute the per-project handoff location (keyed by the current working directory):

```bash
SLUG=$(pwd | sed 's#^/##; s#/#-#g')
DIR="$HOME/.claude/sessions/$SLUG"
mkdir -p "$DIR"
echo "SESSION_DIR=$DIR"
```

Files you will use:
- `$DIR/handoff.md` — the **current** handoff (overwritten each /wrap). This is what /resume reads.
- `$DIR/history.md` — append-only log of every past handoff (the running thread across sessions).

## Step 2 — Auto-capture state (no questions yet)

Gather objective state silently so the user doesn't have to recite it. If the directory is not a git repo, skip git and note that.

```bash
echo "=== branch ==="; git rev-parse --abbrev-ref HEAD 2>/dev/null
echo "=== uncommitted (diff --stat) ==="; git diff --stat 2>/dev/null; git diff --stat --cached 2>/dev/null
echo "=== untracked ==="; git status --porcelain 2>/dev/null | grep '^??' || true
echo "=== recent commits ==="; git log -5 --oneline 2>/dev/null
echo "=== now ==="; date "+%Y-%m-%d %H:%M"
```

Skim the diff so your questions are specific (e.g. reference the file they were clearly working in).

## Step 3 — The debrief (structured)

Ask these (one message at a time in text mode; one call at a time in voice mode). Reference the auto-captured state so it feels like you were watching. Keep each prompt to one line:

1. **Goal** — "What were you actually trying to get done this session?"
2. **State** — "What's broken or unfinished right now?" (cross-check against the diff)
3. **Next move** — "What's the ONE next move — the literal next 5 minutes when you sit back down?"
4. **Surprise/learning** — "Anything that surprised you or that you figured out worth remembering?"
5. **Regression guard** — "What should the next session NOT touch or change?" (the thing that's working and easy to break)
6. **Confidence** — "How sure are you the next move is the right one? (1–5)"

If the user gives terse answers, accept them — don't interrogate. If they skip the next move, propose one from the diff and confirm it.

## Step 4 — Write the handoff

Overwrite `$DIR/handoff.md` with this exact structure (fill from the answers + auto-capture):

```markdown
# Handoff — <project basename> — <YYYY-MM-DD HH:MM>

## ▶ NEXT MOVE (do this first)
<the one next action, concrete enough to start in 5 min>

## Where I left off
<goal narrative — answer 1>

## Broken / unfinished
<answer 2>

## ⛔ Do NOT touch (regression guard)
<answer 5 — what's working and easy to break>

## Surprised / learned
<answer 4>

## Confidence in next move: <n>/5

## Auto-captured state
- Branch: <branch>
- Uncommitted: <diff --stat summary, or "clean">
- Untracked: <list or "none">
- Recent commits:
<git log -5 --oneline>
- Wrapped at: <date>
```

Then **append** the same block (with a `---` separator above it) to `$DIR/history.md` so the thread accumulates.

## Step 5 — Close out

Confirm in one line: where the handoff was saved, and read back the NEXT MOVE so the last thing they see is the first thing they'll do. Example:

> Wrapped. Next session, `/resume` will open with: **"<next move>"**. Saved to `~/.claude/sessions/<slug>/handoff.md`.

In voice mode, also speak the closing: `"$PY" "$VOICE" speak "Wrapped. Next move: <next move>"`.

Do not start new work after /wrap — the session is ending.

---

## Voice mode

Used only when invoked as `/wrap voice`. The "call" is spoken — no phone number, just the local mic + an OpenAI key. If voice isn't available, fall back to text seamlessly.

**A. Locate and check the helper:**

```bash
VOICE=""
for c in "$CLAUDE_PLUGIN_ROOT/scripts/voice.py" "$HOME/.claude/carryover/voice.py" "$HOME/carryover/scripts/voice.py"; do
  [ -f "$c" ] && VOICE="$c" && break
done
PY="python3"; [ -x "$HOME/.claude/carryover/venv/bin/python" ] && PY="$HOME/.claude/carryover/venv/bin/python"
echo "VOICE=$VOICE PY=$PY"
[ -n "$VOICE" ] && "$PY" "$VOICE" check; echo "check_exit=$?"
```

- If `VOICE` is empty or `check_exit` is non-zero, tell the user voice mode isn't ready (relay the reason printed on stderr — usually "install deps" or "OPENAI_API_KEY not set"), then **do the debrief in text instead**. Setup is `pip install -r ~/.claude/carryover/requirements.txt` + `export OPENAI_API_KEY=...`, plus granting the terminal microphone permission on first run.

**B. Ask each Step 3 question by voice.** For each question, run:

```bash
"$PY" "$VOICE" ask "What were you trying to get done this session?"
```

The transcript is printed to **stdout** (capture it as the answer); status/the heard text go to stderr. After each answer, show the transcript in text and let the user correct it by typing if it misheard. If a single `ask` fails (exit 3/4 = no speech / empty), retry once, then offer to type that one answer.

**C.** Then continue to Step 4 exactly as in text mode.
