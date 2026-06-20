# Carryover — demo recording script

A tight ~40-second screen capture for the README header, Show HN, and the PH gallery.
Record with [asciinema](https://asciinema.org) (`asciinema rec carryover.cast`) or any
screen recorder, then convert to GIF with [agg](https://github.com/asciinema/agg)
(`agg carryover.cast carryover.gif`).

## Setup before recording
- A small real repo with an obvious half-finished task (e.g. a failing test).
- Clean terminal, large font, short prompt.
- If showing voice mode, have `OPENAI_API_KEY` set and mic permission granted.

## Beat sheet (keep it under a minute)

```
# 1. You've been coding. You're about to stop.
$ git diff --stat        # show there's real uncommitted work

# 2. Wrap the session
/wrap
#   → it auto-reads git state, then asks the 6 questions.
#   → answer them fast (one line each). Show the handoff being written.
$ cat ~/.claude/sessions/<project>/handoff.md   # show the saved handoff

# 3. (Simulate time passing — new terminal / next day)

# 4. Come back and resume
/resume
#   → it restates: "Last time… / Don't touch… / ▶ Next move…"
#   → then it STARTS the move (opens the file / runs the failing test).
#      THIS is the money shot — capture the "it just started working" moment.
```

## Optional voice beat (separate 15s clip)
```
/wrap voice
#   → "🔊 SPEAKING" cue + the question is spoken aloud
#   → "Tink" beep + "🎙 LISTENING — speak now" cue
#   → you answer out loud; "Pop" beep + "✓ HEARD: ..." cue
```

## Caption to overlay / post with the GIF
> Stop with `/wrap`. Come back to `/resume`. It remembers what you were doing —
> and starts your next move.
