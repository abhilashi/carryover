# Carryover — launch copy

Ready-to-post promotional copy. Repo: https://github.com/abhilashi/carryover
Positioning in one line: **Carryover ends your coding session with a 2-minute debrief and starts the next one for you — so Claude Code never forgets where you were.**

The core hook everywhere: *you* already know the cold-start pain (close the AI mid-task, come back tomorrow, burn 20 minutes rebuilding context — or worse, it "helpfully" rewrites something that worked). Carryover kills it with two commands.

---

## Show HN

**Title:**
`Show HN: Carryover – /wrap and /resume so Claude Code never forgets your session`

**Body:**
```
I kept losing context between Claude Code sessions. I'd stop mid-task, come back
the next day, and the model had forgotten everything — what I was doing, what was
half-broken, what NOT to touch. I'd burn the first 20 minutes rebuilding context,
or it would confidently rewrite something that already worked.

Carryover is two slash commands:

- /wrap — run it when you stop. It reads your git state, asks six quick questions
  (goal, what's broken, the one next move, what surprised you, what NOT to touch,
  confidence), and writes a handoff file.
- /resume — run it when you come back. It reads the handoff, flags anything that
  drifted since, tells you your next move, and actually STARTS it (opens the file,
  runs the failing test, drafts the first edit). No cold start.

Handoffs are plain Markdown under ~/.claude/sessions/ — yours, on disk, git-friendly.
No account, no cloud, no telemetry. There's an optional voice mode (/wrap voice) that
talks the debrief — local mic + speech-to-text, no phone number, all on your machine.

It's an open-source Claude Code plugin (MIT). Install:
  /plugin marketplace add abhilashi/carryover
  /plugin install carryover@carryover

I built it because the handoff doc I was writing by hand every evening was begging to
be automated. Would love feedback on the debrief questions and the resume->initiate step.
```

---

## r/ClaudeAI (and r/vibecoding)

**Title:**
`I built a Claude Code plugin that debriefs your session and starts the next one for you`

**Body:**
```
The thing that kills me about long projects in Claude Code: every new session starts
cold. The model forgot what I was doing, what's broken, and what's working-but-fragile.

So I made Carryover — two commands:

🔹 /wrap (when you stop): reads your git diff + asks 6 fast questions (goal, blocker,
   the ONE next move, surprises, what-not-to-touch, confidence) → saves a handoff.
🔹 /resume (when you're back): reads it, checks what changed in the repo since, tells
   you your next move, and *starts it* instead of just naming it.

Everything's local Markdown in ~/.claude/sessions/. No account, no telemetry. MIT.
Optional voice mode (/wrap voice) lets you just talk the debrief — no phone number,
mic + speech-to-text on your machine.

Install:
  /plugin marketplace add abhilashi/carryover
  /plugin install carryover@carryover

GitHub: https://github.com/abhilashi/carryover
What questions would YOU want a session debrief to ask?
```

---

## X / Twitter thread

```
1/ Every Claude Code session starts cold.

You stop mid-task. Come back tomorrow. The AI forgot what you were doing, what's
broken, and what NOT to touch — so it rewrites the one thing that worked.

I built Carryover to fix it. Two commands. 🧵

2/ /wrap — run it when you stop.

It reads your git state and asks 6 fast questions:
• what were you doing
• what's broken
• the ONE next move
• what surprised you
• what NOT to touch
• confidence

→ saves a handoff file.

3/ /resume — run it when you're back.

It reads the handoff, flags what changed in the repo since, tells you your next move…
and then STARTS it. Opens the file. Runs the failing test. Drafts the first edit.

No 20-minute cold start. You're moving in under a minute.

4/ It's all local. Plain Markdown in ~/.claude/sessions/. Your data, on disk,
git-friendly. No account. No cloud. No telemetry.

5/ Bonus: voice mode. `/wrap voice` talks the debrief to you and records your answers —
local mic + speech-to-text, no phone number, nothing leaves your machine.

6/ Open source, MIT, a Claude Code plugin:

  /plugin marketplace add abhilashi/carryover
  /plugin install carryover@carryover

https://github.com/abhilashi/carryover

Tell me what your end-of-session debrief should ask. ⬇️
```

---

## Product Hunt

**Name:** Carryover
**Tagline:** `Never lose context between coding sessions`
**Description:**
```
Carryover is an open-source Claude Code plugin with two commands. /wrap ends a session:
it reads your git state, runs a 2-minute debrief, and saves a handoff (next move, blockers,
what-not-to-touch). /resume starts the next one: it reads the handoff, flags what changed,
and actually begins your next move instead of just naming it. All local Markdown — no account,
no telemetry. Optional voice mode debriefs you out loud with no phone number.
```
**First comment (maker):**
```
Hey PH 👋 I built this because I was hand-writing a "where I left off" note at the end of
every coding session and re-reading it the next morning. Carryover automates both ends —
the debrief AND the cold-start. It's MIT and fully local. The most opinionated bit is that
/resume doesn't summarize-and-wait; it starts your next move. Curious whether that crosses
the line for you or saves you the friction. Feedback very welcome.
```

---

## One-paragraph blurb (for newsletters / DMs / awesome-lists)

```
Carryover is a free, MIT-licensed Claude Code plugin that stops you losing context between
sessions. /wrap runs a quick end-of-session debrief and saves a Markdown handoff; /resume
reads it back, checks what changed in the repo, and starts your next move. Fully local —
no account, no telemetry — with an optional no-phone-number voice mode.
github.com/abhilashi/carryover
```
