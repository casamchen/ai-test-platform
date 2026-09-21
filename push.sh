#!/usr/bin/env bash
# =====================================================
# push.sh — One-shot push script for the AI Test Platform
# Usage:
#   GITHUB_PAT=ghp_xxx ./push.sh                 # uses default branch + repo
#   GITHUB_PAT=ghp_xxx REPO=jiasheng-chen/ai-test-platform ./push.sh
#
# What this script does:
#   1. Dry-run checks: .env absence, .gitignore health, no node_modules/
#   2. Initializes git if needed, sets remote with embedded PAT
#   3. Stages, commits, pushes
#
# IMPORTANT:
#   - GitHub no longer accepts passwords for git push. Use a PAT.
#   - Your PAT is passed via env var, NOT stored in this script.
#   - The remote URL embeds the PAT, but it is not echoed to logs.
# =====================================================

set -euo pipefail

# ---------- Inputs ----------
GITHUB_PAT="${GITHUB_PAT:-}"
GITHUB_USER="${GITHUB_USER:-jiasheng-chen}"
REPO="${REPO:-ai-test-platform}"
BRANCH="${BRANCH:-main}"
COMMIT_MSG="${COMMIT_MSG:-feat: initial public release of AI Test Management Platform}"

# ---------- Paths ----------
cd "$(dirname "$0")"
PROJECT_ROOT="$(pwd)"

# ---------- Colour helpers ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { printf "${CYAN}[info]${NC}    %s\n" "$*"; }
ok()      { printf "${GREEN}[ok]${NC}      %s\n" "$*"; }
warn()    { printf "${YELLOW}[warn]${NC}    %s\n" "$*"; }
error()   { printf "${RED}[error]${NC}   %s\n" "$*" >&2; exit 1; }

# =====================================================
# Step 0 — Validate inputs
# =====================================================
if [[ -z "$GITHUB_PAT" ]]; then
    error "GITHUB_PAT env var is empty.
    Generate one at:
      GitHub → Settings → Developer settings → Personal access tokens
      → Generate new token (classic) → check 'repo' scope
    Then re-run as:
      GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxx ./push.sh"
fi

# Quick PAT shape check (GitHub classic PATs start with ghp_, fine-grained with github_pat_)
if [[ ! "$GITHUB_PAT" =~ ^ghp_ ]] && [[ ! "$GITHUB_PAT" =~ ^github_pat_ ]]; then
    warn "PAT does not start with ghp_ / github_pat_ — double-check you pasted a token, not a password."
fi

# =====================================================
# Step 1 — Safety checks
# =====================================================
echo ""
info "Step 1 — Safety checks"

# 1.1 .env must NOT be staged
if [[ -f ".env" ]]; then
    # Confirm .gitignore excludes .env
    if grep -qE '^\.env(\s|$)' .gitignore 2>/dev/null || grep -qE '^\.env\*' .gitignore 2>/dev/null; then
        ok ".env present but excluded by .gitignore ✓"
    else
        error ".env exists but is NOT in .gitignore.
    Add a line '.env' to .gitignore, then re-run. Refusing to push."
    fi
fi

# 1.2 node_modules must NOT be staged (304MB)
if [[ -d "aitestpage/node_modules" ]] && ! grep -q "node_modules" .gitignore; then
    error "aitestpage/node_modules exists but is NOT in .gitignore.
    Refusing to push — that's 300+ MB of garbage.
    Add 'node_modules/' to .gitignore and re-run."
fi

# 1.3 vectorsFrame / dumps / screenshots must NOT be staged
for forbidden in vectorsFrame dump.rdb aitestapp/screenshot aitestapp/record aitestapp/interface_file; do
    if grep -qF "$forbidden" .gitignore; then
        ok "$forbidden excluded ✓"
    else
        warn "$forbidden NOT in .gitignore — recommend adding before pushing."
    fi
done

# 1.4 Quick scan for accidentally embedded secrets in tracked files
echo ""
info "Scanning for accidentally embedded secrets..."
if grep -rEn "ZHIPUAI_API_KEY\s*=\s*['\"][^'\"]+['\"]" --include="*.py" --include="*.js" --include="*.vue" --exclude-dir=node_modules --exclude-dir=vectorsFrame --exclude-dir=.git . 2>/dev/null | grep -v "os.getenv\|process.env\|example" | head -5; then
    error "Possible hard-coded API key found. Fix before pushing."
fi
ok "No obvious hard-coded secrets detected ✓"

# =====================================================
# Step 2 — Estimate what will be pushed
# =====================================================
echo ""
info "Step 2 — Estimating push size"

# Use git's dry-run to estimate (works only if git is initialized)
if [[ -d ".git" ]]; then
    echo ""
    info "Files git would push right now:"
    git status --short | head -40
    file_count=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
    info "Total tracked + untracked files: $file_count"
fi

# =====================================================
# Step 3 — Confirm with user
# =====================================================
echo ""
printf "${YELLOW}About to push to:${NC}  https://github.com/${GITHUB_USER}/${REPO}.git\n"
printf "${YELLOW}Branch:${NC}           ${BRANCH}\n"
printf "${YELLOW}Commit message:${NC}   ${COMMIT_MSG}\n"
echo ""
printf "Continue? [y/N] "
read -r answer
if [[ ! "$answer" =~ ^[Yy]$ ]]; then
    warn "Aborted by user."
    exit 0
fi

# =====================================================
# Step 4 — Initialize or update git
# =====================================================
echo ""
info "Step 4 — Initializing git"

if [[ ! -d ".git" ]]; then
    git init -b "$BRANCH"
    ok "git initialized on branch '$BRANCH'"
else
    ok "git already initialized"
    # Ensure we're on the right branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    if [[ "$current_branch" != "$BRANCH" ]]; then
        warn "Current branch is '$current_branch', target is '$BRANCH'."
        if git show-ref --quiet "refs/heads/$BRANCH"; then
            git checkout "$BRANCH"
        else
            git checkout -b "$BRANCH"
        fi
    fi
fi

# Configure user (only if not set globally)
if ! git config user.email >/dev/null; then
    git config user.email "szchenjiasheng@163.com"
fi
if ! git config user.name >/dev/null; then
    git config user.name "Jiasheng Chen"
fi

# =====================================================
# Step 5 — Set remote with embedded PAT
# =====================================================
REMOTE_URL="https://${GITHUB_USER}:${GITHUB_PAT}@github.com/${GITHUB_USER}/${REPO}.git"

if git remote get-url origin >/dev/null 2>&1; then
    info "Updating existing remote 'origin'"
    git remote set-url origin "$REMOTE_URL"
else
    info "Adding remote 'origin'"
    git remote add origin "$REMOTE_URL"
fi
ok "remote configured"

# =====================================================
# Step 6 — Stage, commit, push
# =====================================================
echo ""
info "Step 6 — Stage, commit, push"

git add -A
info "Staged files:"
git status --short | head -30

# Confirm one last time with what's about to be committed
if [[ -n "$(git status --short)" ]]; then
    echo ""
    printf "${YELLOW}Files staged above are about to be committed and pushed.${NC}\n"
    printf "Continue? [y/N] "
    read -r answer2
    if [[ ! "$answer2" =~ ^[Yy]$ ]]; then
        warn "Aborted by user."
        exit 0
    fi
fi

git commit -m "$COMMIT_MSG" || warn "Nothing to commit (working tree clean)"

# Push (set upstream if first push)
if git ls-remote --heads origin "$BRANCH" >/dev/null 2>&1; then
    info "Pushing to existing branch '$BRANCH' on remote..."
    git push -u origin "$BRANCH"
else
    info "First push — creating branch '$BRANCH' on remote..."
    git push -u origin "$BRANCH"
fi

ok "Push complete!"
echo ""
echo "Repo:   https://github.com/${GITHUB_USER}/${REPO}"
echo "Branch: ${BRANCH}"
echo ""
echo "Next steps:"
echo "  1. Visit https://github.com/${GITHUB_USER}/${REPO}"
echo "  2. Add a description + topics in 'About' section"
echo "  3. Pin this repo to your GitHub profile"
echo "  4. Add the URL to your resume / cover letter"