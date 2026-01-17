---
# Level 1: Core Metadata (Always Loaded)
name: "hundong2-sync-origin-forked"
description: "Git workflow for syncing forked repositories with upstream (original) repository"
version: "1.0.0"
category: "workflow"
modularized: true
user-invocable: true

# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~5000

# Trigger Conditions for Level 2 Loading
triggers:
  keywords: ["fork", "upstream", "sync", "pull", "merge", "remote", "original repository"]
  phases: []  # Utility skill, no specific phase
  agents: ["manager-git"]
  languages: []  # Language-agnostic

# Dependencies
requires: []
optional_requires: ["moai-foundation-core"]

# Allowed Tools
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion

# Skill Metadata
tags: ["git", "fork", "upstream", "sync", "workflow"]
updated: 2026-01-17
status: "active"
---

# Level 2: Skill Body (Conditional Load)

## Quick Reference

**What is Fork Sync Workflow?**

A structured workflow to synchronize a forked repository with its upstream (original) repository, ensuring your fork stays up-to-date with the latest changes.

**Key Benefits:**
- Automated upstream discovery using GitHub CLI
- Safe merge/rebase options with user confirmation
- Prevents conflicts with working directory checks
- Supports both merge and rebase strategies

**When to Use:**
- After forking a repository to pull latest changes
- Regular maintenance to keep fork synchronized
- Before creating pull requests to ensure compatibility
- When upstream has new features or bug fixes

**Quick Links:**
- Implementation: #implementation-guide
- Examples: #usage-examples

---

## Implementation Guide

### Core Concepts

**Repository Types:**
- **Upstream**: The original repository you forked from
- **Origin**: Your forked repository on GitHub
- **Local**: Your local git repository on your machine

**Workflow Overview:**
1. Verify current remote configuration
2. Discover upstream repository using GitHub CLI
3. Add upstream remote if not exists
4. Fetch changes from upstream
5. Choose merge strategy (merge/rebase/fetch-only)
6. Merge or rebase upstream changes
7. Push updated changes to origin

### Usage Pattern

**Step 1: Check Current Remote Configuration**

```bash
git remote -v
git branch -a
```

Expected output shows `origin` (your fork) but no `upstream`.

**Step 2: Discover Upstream Repository**

```bash
gh repo view --json parent,url
```

Returns parent repository information (upstream).

**Step 3: Add Upstream Remote**

```bash
git remote add upstream <upstream-url>
git remote -v
```

Verify both `origin` and `upstream` are configured.

**Step 4: Fetch Upstream Changes**

```bash
git fetch upstream
```

Downloads all branches and tags from upstream.

**Step 5: Choose Merge Strategy**

Present user with options:
- **Merge** (Recommended): Safe, preserves history with merge commit
- **Rebase**: Clean history, rewrites local commits on top of upstream
- **Fetch Only**: Download changes without merging

**Step 6: Merge or Rebase**

For merge strategy:
```bash
git merge upstream/main
```

For rebase strategy:
```bash
git rebase upstream/main
```

**Step 7: Push to Origin**

```bash
git push origin main
```

Updates your fork on GitHub.

### Integration Points

**With manager-git:**
- This workflow integrates with Git management operations
- Can be invoked when user requests fork synchronization
- Uses Git safety checks (working directory, branch status)

**With AskUserQuestion:**
- User confirmation for upstream URL
- Choice of merge strategy (merge/rebase/fetch-only)
- Confirmation before pushing to origin

---

## Advanced Topics

### Performance Considerations

**Large Repositories:**
- Use `git fetch upstream --depth=1` for shallow fetch
- Consider `git fetch upstream <branch-name>` for specific branches
- Use `git fetch --tags` separately if needed

**Network Optimization:**
- Fetch during off-peak hours for large repos
- Use SSH instead of HTTPS for better performance
- Consider `git config fetch.parallel <n>` for parallel fetching

### Edge Cases

**Conflict Resolution:**

If merge conflicts occur:
```bash
git status  # Check conflicting files
git diff    # Review conflicts
# Manually resolve conflicts
git add <resolved-files>
git commit
```

**Diverged Histories:**

If local has commits not in upstream:
- Use merge: Creates merge commit (preserves history)
- Use rebase: Replays local commits (clean history)

**Detached HEAD:**

If you're in detached HEAD state:
```bash
git checkout main  # Return to main branch first
```

**Already Up-to-Date:**

If `git merge upstream/main` shows "Already up-to-date":
- No action needed, fork is current
- Safe to continue working

### Best Practices

**Before Syncing:**
- Always commit or stash local changes
- Check `git status` to ensure clean working directory
- Review `git log` to understand local commits

**Merge vs Rebase:**
- Use **merge** for:
  - Shared branches
  - Public history
  - Safe, predictable outcomes
- Use **rebase** for:
  - Personal feature branches
  - Clean linear history
  - When you understand the implications

**After Syncing:**
- Verify changes with `git log`
- Test your local application
- Review CHANGELOG for breaking changes

**Regular Maintenance:**
- Sync fork weekly or before starting new work
- Keep upstream remote configured
- Use `git fetch upstream` regularly to check for updates

---

## Works Well With

**Related Skills:**
- moai-foundation-core: SPEC-First workflow integration
- manager-git: Git operations and branch management

**Agents:**
- manager-git: Primary agent for Git workflow orchestration
- expert-devops: CI/CD integration with fork sync

**Commands:**
- Custom command for automated fork sync
- Integration with /moai:fix for quick updates

---

# Usage Examples

## Example 1: First-Time Fork Sync

```
User: "Fork를 해온 main branch의 내용을 pull 하고싶어"

Alfred:
1. Check current remotes: git remote -v
2. Discover upstream: gh repo view --json parent,url
3. Ask user about merge strategy
4. Add upstream: git remote add upstream <url>
5. Fetch upstream: git fetch upstream
6. Merge: git merge upstream/main
7. Push to origin: git push origin main

Result:
- Upstream remote added (modu-ai/moai-adk)
- 366 files changed (7,400 insertions, 14,434 deletions)
- Fast-forward merge successful
- Origin fork updated
```

## Example 2: Regular Sync (Upstream Already Configured)

```
User: "Update my fork with latest upstream changes"

Alfred:
1. Verify upstream exists: git remote -v
2. Check working directory: git status
3. Fetch upstream: git fetch upstream
4. Ask merge strategy preference
5. Merge: git merge upstream/main
6. Push to origin: git push origin main

Result:
- Fork synchronized with upstream
- No conflicts encountered
- Origin updated successfully
```

## Example 3: Sync with Rebase Strategy

```
User: "Sync fork using rebase for clean history"

Alfred:
1. Check remotes and status
2. Fetch upstream: git fetch upstream
3. User selects "Rebase" option
4. Rebase: git rebase upstream/main
5. Push with force (if needed): git push origin main --force-with-lease

Result:
- Clean linear history
- Local commits replayed on top of upstream
- Fork updated with rebase strategy
```

## Example 4: Conflict Resolution

```
User: "Sync fork but I have local changes"

Alfred:
1. Detect uncommitted changes: git status
2. Ask user to commit or stash changes
   - User commits: git add . && git commit -m "WIP"
   - Or stash: git stash
3. Proceed with sync workflow
4. If conflicts during merge:
   - Guide user through conflict resolution
   - Show conflicting files: git status
   - After resolution: git add . && git commit

Result:
- Conflicts resolved manually
- Merge completed successfully
- Fork synchronized with upstream
```

---

# Progressive Disclosure Levels Summary

| Level | What | When | Token Cost |
|-------|------|------|------------|
| 1 | YAML Metadata only | Agent initialization | ~100 tokens |
| 2 | SKILL.md Body | Keywords: fork, upstream, sync | ~5K tokens |
| 3+ | Bundled files (if any) | Claude decides | Unlimited |

---

# Implementation Checklist

When implementing this workflow:

- [ ] Check git remote -v for current configuration
- [ ] Use gh repo view to discover upstream automatically
- [ ] Verify working directory is clean (git status)
- [ ] Ask user for merge strategy preference
- [ ] Add upstream remote if missing
- [ ] Fetch upstream changes before merging
- [ ] Handle merge conflicts gracefully
- [ ] Verify merge success with git log
- [ ] Push to origin only after successful merge
- [ ] Inform user of changes and commit range

---

# Troubleshooting

## Issue: "fatal: remote upstream already exists"

**Solution:**
```bash
git remote remove upstream
git remote add upstream <new-url>
```

## Issue: "refusing to merge unrelated histories"

**Solution:**
```bash
git merge upstream/main --allow-unrelated-histories
```

## Issue: "Your branch and 'origin/main' have diverged"

**Solution:**
Choose one:
- Merge: `git merge origin/main`
- Rebase: `git rebase origin/main`
- Force push (careful): `git push origin main --force-with-lease`

## Issue: "gh: command not found"

**Solution:**
- Install GitHub CLI: `brew install gh` (macOS)
- Or use manual upstream URL input fallback

---

# Backward Compatibility Note

For agents that don't support Progressive Disclosure yet, the entire SKILL.md (Levels 1 + 2) will be loaded at initialization. This ensures compatibility while enabling optimization for Progressive Disclosure-aware agents.