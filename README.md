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

## Privacy

Everything stays local. Carryover writes only to `~/.claude/sessions/` and reads your repo's git metadata. No network calls, no account, no phone number, nothing leaves your machine.

## License

MIT — see [LICENSE](LICENSE).
