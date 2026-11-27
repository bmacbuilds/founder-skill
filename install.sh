#!/usr/bin/env bash
# Installs Founder: /founder and each of its commands as its own, one folder each in ~/.claude/skills/,
# and nothing else on the computer.
#
#   bash install.sh                           the latest release
#   bash install.sh --from PATH               a release folder (or its founder/ folder) or .tar.gz on this computer
#   bash install.sh --update                  replace an earlier Founder without asking
#   bash install.sh --name bmac-founder    install as /bmac-founder, and its commands as /bmac-founder-...
#   bash install.sh --replace                 move someone else's skills with our names aside (kept as backups)
#
# It never deletes anything that is not ours, never leaves half an installation, and asks before it changes
# anything that is already there. Uninstall with uninstall.sh.
set -euo pipefail

NAME="founder"
FALLBACK="bmac-founder"
RELEASE_URL="${FOUNDER_RELEASE_URL:-https://github.com/bmacbuilds/founder-skill/archive/refs/tags/v1.0.0.tar.gz}"
MARKER=".founder-install"
COMMANDS="board competitors consumer pricing offer cfo marketing brand ops launch plan"   # written by scripts/sync.py from skill.json
FROM="" UPDATE=0 REPLACE=0 ASSUME_YES=0

say() { printf '%s\n' "$*"; }
fail() { printf 'Founder was not installed: %s\n' "$*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --from) FROM="${2:?--from needs a folder or a .tar.gz}"; shift 2 ;;
    --update) UPDATE=1; shift ;;
    --replace) REPLACE=1; shift ;;
    --name) NAME="${2:?--name needs a name}"; shift 2 ;;
    --yes) ASSUME_YES=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) fail "unknown option $1 (try --help)" ;;
  esac
done
case "$NAME" in founder|"$FALLBACK") ;; *) fail "the name is /founder or /$FALLBACK" ;; esac

ask() {  # ask "question" -> 0 for yes. With no one to ask (no terminal), the answer is no, unless --yes.
  [ "$ASSUME_YES" = 1 ] && return 0
  local answer=""
  if [ -t 0 ]; then
    printf '%s [y/N] ' "$1"; read -r answer || return 1
  elif [ -z "${FOUNDER_NO_PROMPT:-}" ] && { : </dev/tty; } 2>/dev/null; then   # run as curl ... | bash
    printf '%s [y/N] ' "$1" >/dev/tty; read -r answer </dev/tty || return 1
  else
    return 1
  fi
  case "$answer" in y|Y|yes|Yes) return 0 ;; *) return 1 ;; esac
}

SKILLS="$HOME/.claude/skills"
# Staging and backups live beside the skills folder, never in it: Claude Code makes a command of every folder there.
# Same disk as the skills folder, so every move into place is a rename.
WORK="$HOME/.claude/.founder"
RUN="$WORK/run.$$"
STAMP="$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="$WORK/backups/$STAMP"
FOLDERS="$NAME"; for s in $COMMANDS; do FOLDERS="$FOLDERS $NAME-$s"; done   # the skill, then each command's own
STAGE="$(mktemp -d "${TMPDIR:-/tmp}/founder.XXXXXX")"
PLACED="" BACKUPS="" DONE=0
cleanup() {   # not finished: take out what this run put in, and put back what was there, folder by folder
  rm -rf "$STAGE"
  if [ "$DONE" != 1 ]; then
    for f in $PLACED; do rm -rf "${SKILLS:?}/$f"; done
    for f in $FOLDERS; do
      if [ -d "$RUN/old/$f" ] && [ ! -e "$SKILLS/$f" ]; then mv "$RUN/old/$f" "$SKILLS/$f"; fi
    done
    for f in $BACKUPS; do
      if [ ! -e "$SKILLS/$f" ] && [ -d "$BACKUP_DIR/$f" ]; then mv "$BACKUP_DIR/$f" "$SKILLS/$f"; say "Your earlier /$f skill was put back."; fi
    done
    rmdir "$BACKUP_DIR" 2>/dev/null || true
  fi
  rm -rf "$RUN"
  rmdir "$WORK/backups" "$WORK" 2>/dev/null || true
  return 0
}
trap cleanup EXIT

# 1. Claude Code. The files are harmless without it, so a missing Claude Code is a note, not a stop.
if ! command -v claude >/dev/null 2>&1; then
  say "Note: Claude Code was not found on this computer. Founder runs inside it: install Claude Code from"
  say "      https://code.claude.com, then type /$NAME in it."
fi

# 2. The release, staged in a temporary folder.
if [ -z "$FROM" ]; then
  command -v curl >/dev/null 2>&1 || fail "curl is needed to download the release"
  curl -fsSL "$RELEASE_URL" -o "$STAGE/release.tar.gz" || fail "the download failed ($RELEASE_URL)"
  FROM="$STAGE/release.tar.gz"
fi
if [ -d "$FROM" ]; then
  ROOT="$FROM"; [ -f "$FROM/SKILL.md" ] && [ "$(basename "$FROM")" = founder ] && ROOT="$(dirname "$FROM")"
elif [ -f "$FROM" ]; then
  mkdir "$STAGE/unpacked" && tar -xzf "$FROM" -C "$STAGE/unpacked" || fail "$FROM is not a readable release"
  found="$(find "$STAGE/unpacked" -mindepth 1 -maxdepth 2 -type d -name founder | head -n 2)"   # GitHub wraps it in one folder
  [ -n "$found" ] && [ "$(printf '%s\n' "$found" | wc -l | tr -d ' ')" = 1 ] || fail "$FROM has no single founder/ folder"
  ROOT="$(dirname "$found")"
else
  fail "$FROM was not found"
fi
[ -d "$ROOT/founder" ] || fail "$FROM has no founder/ folder"
mkdir "$STAGE/pkg"
cp -R "$ROOT/founder" "$STAGE/pkg/$NAME"
for s in $COMMANDS; do
  [ -f "$ROOT/founder-$s/SKILL.md" ] || fail "the release is missing the /founder-$s command"
  cp -R "$ROOT/founder-$s" "$STAGE/pkg/$NAME-$s"
done
PKG="$STAGE/pkg/$NAME"

# 3. Every required file, before anything is touched.
for f in SKILL.md NOTICE VERSION; do [ -f "$PKG/$f" ] || fail "the release is missing $f"; done
for s in $COMMANDS; do [ -f "$PKG/commands/$s/COMMAND.md" ] || fail "the release is missing the $s command's instructions"; done
grep -q '^name: founder$' "$PKG/SKILL.md" || fail "the release's SKILL.md is not Founder"
VERSION="$(head -n 1 "$PKG/VERSION")"
for f in $FOLDERS; do
  skill="$STAGE/pkg/$f/SKILL.md"
  if [ "$NAME" != "founder" ]; then   # every name, each command's pointer to the skill's folder, every `/command
    sed -e "s/^name: founder/name: $NAME/" -e "s|/\.\./founder/|/../$NAME/|g" -e "s|\`/founder|\`/$NAME|g" \
      "$skill" > "$skill.named"
    mv "$skill.named" "$skill"
  fi
  printf 'Founder %s, installed as /%s by install.sh. uninstall.sh removes only folders with this file.\n' \
    "$VERSION" "$f" > "$STAGE/pkg/$f/$MARKER"
done

# 4. What is already there, for every folder, before anything is touched.
mkdir -p "$SKILLS"
OURS="" THEIRS=""
for f in $FOLDERS; do
  if [ -f "$SKILLS/$f/$MARKER" ]; then OURS="$OURS /$f"; elif [ -e "$SKILLS/$f" ]; then THEIRS="$THEIRS $f"; fi
done
if [ -n "$OURS" ] && [ "$UPDATE" != 1 ] && ! ask "Founder is already installed as /$NAME. Replace it with $VERSION?"; then
  fail "an earlier Founder is installed as /$NAME and was kept. Run again with --update to replace it."
fi
if [ -n "$THEIRS" ]; then
  list="$(printf '/%s ' $THEIRS)"
  if [ "$REPLACE" = 1 ] || ask "Other skills already use ${list% }. Move them aside (each is kept as a backup) and install Founder?"; then
    mkdir -p "$BACKUP_DIR"
    for f in $THEIRS; do BACKUPS="$BACKUPS $f"; mv "$SKILLS/$f" "$BACKUP_DIR/$f"; done
  else
    fail "other skills already use ${list% }, and they were not touched. Install Founder as /$FALLBACK instead with: --name $FALLBACK"
  fi
fi

# 5. Into place: a failure never leaves half an installation, and whatever was there comes back.
mkdir -p "$RUN/new" "$RUN/old"
for f in $FOLDERS; do cp -R "$STAGE/pkg/$f" "$RUN/new/$f"; done
[ "${FOUNDER_FAIL_AT:-}" = "copy" ] && { say "test: stopping after the copy"; exit 1; }
for f in $FOLDERS; do
  if [ -e "$SKILLS/$f" ]; then mv "$SKILLS/$f" "$RUN/old/$f"; fi
  [ "${FOUNDER_FAIL_AT:-}" = "swap" ] && [ -n "$PLACED" ] && { say "test: stopping mid-swap"; exit 1; }
  PLACED="$PLACED $f"; mv "$RUN/new/$f" "$SKILLS/$f"
done
DONE=1
for f in $BACKUPS; do say "Your earlier /$f skill was kept at $BACKUP_DIR/$f."; done

# 6. Anything that could still answer to the same name.
[ -f "$HOME/.claude/commands/$NAME.md" ] && say "Note: you also have $HOME/.claude/commands/$NAME.md. The skill you just installed takes precedence; that file was left alone."
[ -d "$PWD/.claude/skills/$NAME" ] && say "Note: this project has its own /$NAME skill. Your personal Founder takes precedence over it."
command -v python3 >/dev/null 2>&1 || say "Note: Python 3 was not found. Founder works without it; a few of its tools need it."

say ""
say "Founder $VERSION is installed. Open Claude Code and type /$NAME"
[ -n "$COMMANDS" ] && say "Each of its commands also works on its own:$(for s in $COMMANDS; do printf ' /%s-%s' "$NAME" "$s"; done)"
say "If /$NAME opens something else, your organization may have its own: run /skills in Claude Code to check,"
say "or install Founder as /$FALLBACK with: --name $FALLBACK"
