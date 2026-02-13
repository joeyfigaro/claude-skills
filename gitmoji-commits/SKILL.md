---
name: gitmoji-commits
description: Use when creating git commits - automatically selects and includes gitmoji based on change type
---

# Gitmoji Commits

## Overview

Automatically enhance commit messages with gitmoji that visually represents the type of change. Analyze the diff to select the most appropriate gitmoji.

## When to Use

**Always** - Apply to every git commit you create.

## Commit Message Format

```
<gitmoji> <type>: <description>

[optional body]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Gitmoji Selection Guide

Schema for all gitmoji can be found in the schema.json in this directory. 
Analyze the git diff and select an appropriate emoji using the description from the emoji's object in schema.json.


## Selection Process

1. **Read git diff** - Understand what changed
2. **Identify primary change type** - What's the main purpose?
3. **Select ONE gitmoji** - Choose the most representative
4. **Format message** - `<gitmoji> <type>: <description>`

## Examples

```bash
# New feature added
✨ feat: add user authentication system

# Bug fix
🐛 fix: resolve race condition in async handler

# Documentation
📝 docs: update API endpoint documentation

# Refactoring
♻️ refactor: extract validation logic into separate module

# Performance improvement
⚡️ perf: optimize database query with indexes

# Test addition
✅ test: add integration tests for payment flow

# Dependency update
⬆️ upgrade: bump react from 18.0.0 to 18.2.0

# Multiple file types - pick primary purpose
✨ feat: add dark mode toggle
# Even if it includes CSS, tests, docs - primary is new feature
```

## Decision Rules

**Multiple change types?** Pick the primary purpose:
- New feature + tests → ✨ feat (feature is primary)
- Bug fix + tests → 🐛 fix (fix is primary)
- Refactor + perf → Choose which is more significant

**File patterns:**
- Only .md, docs/ changes → 📝 docs
- Only package.json/lock → 📦 package
- Only .css, .scss, design files → 💄 style
- Only test files → ✅ test
- Only config (.yml, .json, .config.*) → 🔧 chore

**Unclear?** Ask yourself: "What problem does this solve?" Pick the gitmoji that matches that answer.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Multiple gitmojis | Use ONE - the primary purpose |
| Wrong type | Read diff carefully - what's the main change? |
| Generic "update" | Be specific - is it feat, fix, refactor? |
| Forgetting gitmoji | Every commit needs one |
| WIP on main branch | Use ✨/🐛/♻️ instead - commits on main should be complete |
| Using :text: codes | Use actual emoji character (✨ not :sparkles:) |

## Integration with Existing Workflow

**This skill modifies Step 2 of the standard commit workflow:**

Standard Step 2: "Draft a concise commit message..."

**Now becomes:** "Analyze diff, select gitmoji, draft message with format: `<gitmoji> <type>: <description>`"

All other steps remain the same (git status, git diff, git add, creating commit, git status after).
