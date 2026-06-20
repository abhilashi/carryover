---
name: resume
description: Start-of-session re-initiation for a coding/work session. Reads the persistent handoff written by /wrap for this project, restates where you left off (next move, blockers, regression guard), checks whether the repo changed since, and then ACTUALLY STARTS the next move rather than just naming it. Invoke when returning to a project, or via /resume.
disable-model-invocation: true
---

# /resume — pick up where you left off

You **pick up the thread from the last session.** Your job is not to summarize and wait — it's to get the user moving in under a minute. Decomposition is done; the bottleneck is *initiation*. So you restate, sanity-check, then **start the first step yourself**.

## Step 1 — Resolve the project session path

```bash
SLUG=$(pwd | sed 's#^/##; s#/#-#g')
DIR="$HOME/.claude/sessions/$SLUG"
echo "SESSION_DIR=$DIR"
ls -la "$DIR" 2>/dev/null || echo "NO_SESSION"
```

If there is no `handoff.md`, tell the user there's no prior session for this project and offer to start one (run `/wrap` at the end of this one). Stop here.

## Step 2 — Read the handoff

Read `$DIR/handoff.md`. Extract: the **NEXT MOVE**, where they left off, what's broken, the **regression guard (do-not-touch)**, and the confidence score.

## Step 3 — Reality check against current state

The repo may have changed since the handoff was written. Run:

```bash
echo "=== branch ==="; git rev-parse --abbrev-ref HEAD 2>/dev/null
echo "=== uncommitted ==="; git diff --stat 2>/dev/null; git status --porcelain 2>/dev/null | head
echo "=== commits since wrap ==="; git log -5 --oneline 2>/dev/null
```

Compare to the "Auto-captured state" in the handoff. If the branch differs, or commits appeared, or uncommitted work changed, **flag it** — the next move may be stale. Don't blindly execute against a moved codebase.

## Step 4 — Restate, tight

Three lines, no more:

> **Last time:** <one line — where they left off>
> **Heads-up / don't touch:** <regression guard, + any drift you detected in step 3>
> **▶ Next move:** <the NEXT MOVE from the handoff>

## Step 5 — Initiate (the whole point)

Do not stop at naming the move. **Start it.** Pick the smallest concrete first action and do it now:
- open / read the file the next move is about,
- write the first line / stub,
- run the failing test or repro command,
- or draft the first edit and show it.

Then ask only: *"Keep going?"* — never "what would you like to do?". If the move is genuinely ambiguous after the handoff + reality check, ask exactly one clarifying question, then start.

Anything destructive (deletes, force-push, migrations) — describe it and get a yes before running. Everything read-only or additive — just do it.
