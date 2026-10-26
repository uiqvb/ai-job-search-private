#!/usr/bin/env bash
# Commit and push the whole workspace to the PRIVATE repo (remote "origin").
# .gitignore stays the public template's version, so personal files are
# force-added here. Left out on purpose: resumes, video media, node_modules,
# automation/config.json (ntfy topic) and .env files.
# Usage: bash tools/push_private.sh ["commit message"]
set -euo pipefail
cd "$(dirname "$0")/.."

url=$(git remote get-url origin 2>/dev/null || true)
case "$url" in
  *uiqvb/ai-job-search.git|*MadsLorentzen*|"")
    echo "origin is not the private repo ($url). Stopping." >&2; exit 1 ;;
esac

# Mirror Claude's memory into the repo (it lives outside it, in ~/.claude).
mem="$HOME/.claude/projects/C--Users-Manit-Khera-Documents-ai-job-search/memory"
if [ -d "$mem" ]; then
  rm -rf documents/notes/claude-memory
  mkdir -p documents/notes/claude-memory
  cp "$mem"/*.md documents/notes/claude-memory/
fi

git add -A

git add -f -- \
  documents job_search_tracker.csv planned_applications.csv gmail_sync \
  reports company_research cover_letters job_scraper automation/logs upskill \
  ':(exclude,glob)**/node_modules/**' \
  ':(exclude,glob)**/__pycache__/**' \
  ':(exclude,glob)**/*.pyc' \
  ':(exclude,glob,icase)**/*.mp4' ':(exclude,glob,icase)**/*.mov' \
  ':(exclude,glob,icase)**/*.m4a' ':(exclude,glob,icase)**/*.wav' \
  ':(exclude,glob,icase)**/*.mp3' ':(exclude,glob,icase)**/*.mkv' \
  ':(exclude,glob,icase)**/*.webm' ':(exclude,glob,icase)**/*.aac' \
  ':(exclude,glob)documents/cv/**' \
  ':(exclude,glob,icase)**/*resume*' \
  ':(exclude,glob,icase)**/*cv_draft*' \
  ':(exclude,glob,icase)**/* CV *' \
  ':(exclude,glob,icase)**/*.ats.txt'

# Blank Deakin resume templates are samples, not Manit's resume.
git add -f -- 'documents/notes/templates/Resume-Template-'*.docx 2>/dev/null || true

# Safety net: nothing resume-like, no secrets, nothing over 95 MB.
bad=$(git diff --cached --name-only | grep -iE '(^|/)documents/cv/|resume|cv_draft| CV |\.ats\.txt$|automation/config\.json|(^|/)\.env' \
      | grep -v 'documents/notes/templates/Resume-Template-' || true)
if [ -n "$bad" ]; then echo "Refusing: these should not be committed:"; echo "$bad"; exit 1; fi
big=$(git diff --cached --name-only -z | xargs -0 -I{} sh -c '[ -f "{}" ] && [ $(wc -c < "{}") -gt 95000000 ] && echo "{}"' || true)
if [ -n "$big" ]; then echo "Refusing: files over 95 MB:"; echo "$big"; exit 1; fi

if git diff --cached --quiet; then echo "Nothing to commit."; else
  git commit -q -m "${1:-Workspace sync $(date '+%Y-%m-%d %H:%M')}"
fi
git push -u origin HEAD
