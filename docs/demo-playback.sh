#!/usr/bin/env bash
# Scripted reproduction of a Carryover /wrap -> /resume session, used only to
# render the demo GIF (docs/carryover.gif). Not interactive — it replays a
# realistic session with typewriter timing. Regenerate the GIF with:
#   asciinema rec --command "bash docs/demo-playback.sh" --overwrite docs/carryover.cast
#   agg --font-size 20 --theme asciinema docs/carryover.cast docs/carryover.gif
#   gifsicle -O3 --lossy=60 docs/carryover.gif -o docs/carryover.gif
set -u
g(){ printf '\033[%sm' "$1"; }
R=$(g 0); DIM=$(g 90); CY=$(g 36); GR=$(g 32); YE=$(g 33); BO=$(g 1); MG=$(g 35)
sp(){ sleep "$1"; }
tw(){ local s=$1; shift; local t="$*" i; for((i=0;i<${#t};i++)); do printf '%s' "${t:$i:1}"; sleep "$s"; done; printf '\n'; }
prompt(){ printf "%s❯%s " "$CY" "$R"; }
q(){ printf "  %s?%s %s\n" "$YE" "$R" "$1"; sp 0.25; printf "    %s%s%s\n\n" "$GR" "$2" "$R"; sp 0.45; }

clear; sp 0.6

# --- real work in progress ---
prompt; tw 0.045 "git diff --stat"; sp 0.2
printf "%s src/auth.ts        | 24 +++++++++---\n test/auth.test.ts  |  8 ++++\n 2 files changed, 29 insertions(+), 3 deletions(-)%s\n" "$DIM" "$R"
sp 0.9

# --- wrap ---
prompt; tw 0.06 "/wrap"; sp 0.4
printf "%s%s  Carryover — end-of-session debrief%s\n" "$BO" "$MG" "$R"; sp 0.3
printf "%s  auto-captured: branch feature/auth-refactor · 2 files changed%s\n\n" "$DIM" "$R"; sp 0.5
q "What were you trying to get done?"   "Move auth into a useAuth() hook"
q "What's broken or unfinished?"        "Token refresh loops on 401"
q "The ONE next move?"                  "Fix the interceptor retry in api/client.ts"
q "Anything surprising?"                "401 loop = interceptor retries before the token is set"
q "What should NOT be touched?"         "session cookie code in middleware.ts — it works"
q "Confidence (1-5)?"                   "4"
printf "  %s✓ handoff saved%s  %s~/.claude/sessions/myapp/handoff.md%s\n" "$GR" "$R" "$DIM" "$R"
sp 1.3

# --- time passes ---
printf "\n%s        … next day, fresh session, zero memory …%s\n\n" "$DIM" "$R"; sp 1.1

# --- resume ---
prompt; tw 0.06 "/resume"; sp 0.4
printf "%s%s  Carryover — picking up where you left off%s\n\n" "$BO" "$MG" "$R"; sp 0.4
printf "  %sLast time:%s    moved auth into useAuth(); 401 refresh loop still open\n" "$BO" "$R"; sp 0.5
printf "  %s%s⛔ Don't touch:%s middleware.ts session cookie (it works)\n" "$BO" "$YE" "$R"; sp 0.5
printf "  %s%s▶ Next move:%s   fix the interceptor retry in api/client.ts\n\n" "$BO" "$GR" "$R"; sp 0.8
printf "  %sstarting it for you…%s\n" "$DIM" "$R"; sp 0.6
prompt; tw 0.03 "open api/client.ts  ·  npm test -- auth"; sp 0.5
printf "%s  ● running auth.test.ts …%s\n" "$YE" "$R"; sp 1.0
printf "%s  ✓ auth.test.ts — 3 passing%s\n" "$GR" "$R"; sp 0.8
printf "\n  %sYou're already moving.%s\n" "$BO" "$R"; sp 1.8
