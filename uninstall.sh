#!/usr/bin/env bash
# Removes Founder: only the skill folders our installer marked as ours. Nothing you made with it is ever touched.
set -euo pipefail
MARKER=".founder-install"
COMMANDS="board competitors consumer pricing offer cfo marketing brand ops launch plan"   # written by scripts/sync.py from skill.json
removed=0
for base in founder bmac-founder; do
  for name in "$base" $(for s in $COMMANDS; do printf '%s-%s ' "$base" "$s"; done); do
    dir="$HOME/.claude/skills/$name"
    [ -e "$dir" ] || continue
    if [ -f "$dir/$MARKER" ]; then
      rm -rf "$dir"; removed=$((removed + 1))
    else
      printf 'Left %s alone: Founder did not install it.\n' "$dir"
    fi
  done
done
if [ "$removed" -gt 0 ]; then printf 'Removed Founder (%s skill folders).\n' "$removed"; else printf 'Founder was not installed.\n'; fi
