# Fork Sync Workflow - Reference

External resources, documentation, and best practices for fork synchronization.

---

## Official Documentation

### Git Documentation

**Git Remote Management:**
- [git-remote](https://git-scm.com/docs/git-remote) - Manage remote repositories
- [git-fetch](https://git-scm.com/docs/git-fetch) - Download objects from remote
- [git-merge](https://git-scm.com/docs/git-merge) - Join development histories
- [git-rebase](https://git-scm.com/docs/git-rebase) - Reapply commits on top of another base

**Git Workflow Guides:**
- [About remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories)
- [Managing remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)

### GitHub Documentation

**Fork Management:**
- [Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [Syncing a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)
- [Configuring a remote for a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork)

**GitHub CLI:**
- [gh repo view](https://cli.github.com/manual/gh_repo_view) - View repository details
- [gh repo sync](https://cli.github.com/manual/gh_repo_sync) - Sync fork with upstream

---

## Command Reference

### Essential Git Commands

**Remote Management:**
```bash
# List remotes
git remote -v

# Add remote
git remote add <name> <url>

# Remove remote
git remote remove <name>

# Rename remote
git remote rename <old> <new>

# Change remote URL
git remote set-url <name> <new-url>

# Show remote info
git remote show <name>
```

**Fetching:**
```bash
# Fetch all remotes
git fetch --all

# Fetch specific remote
git fetch <remote>

# Fetch specific branch
git fetch <remote> <branch>

# Fetch with tags
git fetch --tags

# Fetch and prune deleted branches
git fetch --prune
```

**Merging:**
```bash
# Merge remote branch
git merge <remote>/<branch>

# Merge with custom message
git merge <remote>/<branch> -m "Merge message"

# Merge unrelated histories
git merge <remote>/<branch> --allow-unrelated-histories

# Abort merge
git merge --abort
```

**Rebasing:**
```bash
# Rebase on remote branch
git rebase <remote>/<branch>

# Interactive rebase
git rebase -i <remote>/<branch>

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip

# Abort rebase
git rebase --abort
```

**Pushing:**
```bash
# Push to remote
git push <remote> <branch>

# Force push with lease (safer)
git push <remote> <branch> --force-with-lease

# Force push (dangerous)
git push <remote> <branch> --force

# Push all branches
git push --all

# Push tags
git push --tags
```

### GitHub CLI Commands

**Repository Operations:**
```bash
# View repository info
gh repo view

# View repository with JSON output
gh repo view --json parent,url

# View specific repository
gh repo view <owner>/<repo>

# Sync fork with upstream
gh repo sync

# Clone fork
gh repo fork <owner>/<repo> --clone
```

---

## Workflow Diagrams

### Fork Sync Flow (Merge Strategy)

```
┌─────────────┐
│   Upstream  │ (modu-ai/moai-adk)
└──────┬──────┘
       │ fork
       ↓
┌─────────────┐
│   Origin    │ (hundong2/moai-adk)
└──────┬──────┘
       │ clone
       ↓
┌─────────────┐
│    Local    │ (your machine)
└─────────────┘

Sync Process:
1. git fetch upstream      → Download upstream changes
2. git merge upstream/main → Merge into local
3. git push origin main    → Upload to origin

Result:
Local = Upstream = Origin (all aligned)
```

### Fork Sync Flow (Rebase Strategy)

```
Before:
Upstream:  A---B---C---D
Local:     A---B---E---F

After Rebase:
Upstream:  A---B---C---D
Local:     A---B---C---D---E'---F'

E' and F' are rebased commits (new commit hashes)
```

---

## Best Practices

### When to Sync

**Regular Schedule:**
- Weekly for active projects
- Before starting new feature work
- Before creating pull requests
- After major upstream releases

**Event-Driven:**
- When upstream has critical bug fixes
- When upstream has features you need
- Before submitting contributions
- When resolving merge conflicts in PRs

### Merge vs Rebase Decision Matrix

| Scenario | Recommended Strategy | Reason |
|----------|---------------------|--------|
| Shared branch (main, develop) | Merge | Preserves history, safer |
| Personal feature branch | Rebase | Clean linear history |
| Before pull request | Rebase | Clean PR history |
| After conflicts | Merge | Explicit resolution record |
| Public commits | Merge | Don't rewrite public history |
| Local-only commits | Rebase | Clean up before pushing |

### Safety Checklist

Before syncing:
- [ ] Working directory is clean (no uncommitted changes)
- [ ] All important changes are committed
- [ ] You know which branch you're on
- [ ] You've backed up important work (if unsure)

During sync:
- [ ] Review what's being merged (git log, git diff)
- [ ] Resolve conflicts carefully
- [ ] Test after merging
- [ ] Verify commit history looks correct

After sync:
- [ ] Run tests (if available)
- [ ] Review CHANGELOG for breaking changes
- [ ] Update dependencies if needed
- [ ] Push to origin to share changes

---

## Troubleshooting Guide

### Common Issues

**Issue 1: Diverged Histories**

**Symptom:**
```
Your branch and 'upstream/main' have diverged,
and have 5 and 10 different commits each, respectively.
```

**Solutions:**
```bash
# Option A: Merge (preserves history)
git merge upstream/main

# Option B: Rebase (clean history)
git rebase upstream/main

# Option C: Reset (discard local commits)
git reset --hard upstream/main  # CAREFUL: loses local commits
```

**Issue 2: Merge Conflicts**

**Symptom:**
```
CONFLICT (content): Merge conflict in <file>
Automatic merge failed; fix conflicts and then commit the result.
```

**Solutions:**
```bash
# 1. View conflicting files
git status

# 2. View conflict details
git diff

# 3. Open files and resolve conflicts manually
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# 4. Mark as resolved
git add <resolved-files>

# 5. Complete merge
git commit

# Alternative: Use merge tool
git mergetool
```

**Issue 3: Accidentally Pushed Wrong Changes**

**Symptom:**
```
Pushed to origin but realized it was wrong
```

**Solutions:**
```bash
# Option A: Revert commit (safe, creates new commit)
git revert <commit-hash>
git push origin main

# Option B: Force push (dangerous, rewrites history)
git reset --hard <good-commit>
git push origin main --force-with-lease

# Option C: Create fix commit
git revert --no-commit <bad-commit>
# Make corrections
git commit -m "Fix incorrect changes"
git push origin main
```

**Issue 4: Lost Commits After Rebase**

**Symptom:**
```
Can't find commits after rebase
```

**Solutions:**
```bash
# Find lost commits using reflog
git reflog

# Recover lost commit
git cherry-pick <commit-hash>

# Or reset to before rebase
git reset --hard HEAD@{n}  # n from reflog
```

---

## Advanced Techniques

### Selective Cherry-Pick from Upstream

```bash
# Fetch upstream
git fetch upstream

# List upstream commits
git log upstream/main --oneline

# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Cherry-pick range
git cherry-pick <start-hash>^..<end-hash>

# Push to origin
git push origin main
```

### Squash Merge from Upstream

```bash
# Fetch upstream
git fetch upstream

# Squash merge (all commits become one)
git merge --squash upstream/main

# Review changes
git diff --cached

# Commit with custom message
git commit -m "Sync with upstream: <describe changes>"

# Push to origin
git push origin main
```

### Partial Sync (Specific Files)

```bash
# Fetch upstream
git fetch upstream

# Checkout specific files from upstream
git checkout upstream/main -- path/to/file

# Stage changes
git add path/to/file

# Commit
git commit -m "Sync specific file from upstream"

# Push to origin
git push origin main
```

---

## Integration with CI/CD

### GitHub Actions Workflow

```yaml
name: Sync Fork with Upstream

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Add upstream remote
        run: |
          git remote add upstream https://github.com/modu-ai/moai-adk.git
          git fetch upstream

      - name: Merge upstream
        run: |
          git merge upstream/main

      - name: Push to origin
        run: |
          git push origin main
```

### Pre-Sync Hook

```bash
#!/bin/bash
# .git/hooks/pre-merge-commit

echo "🔍 Running pre-sync checks..."

# Check if tests pass
if ! pytest tests/; then
    echo "❌ Tests failed, aborting sync"
    exit 1
fi

# Check linting
if ! ruff check src/; then
    echo "❌ Linting failed, aborting sync"
    exit 1
fi

echo "✅ Pre-sync checks passed"
exit 0
```

---

## Related Tools

### GUI Clients

**GitKraken:**
- Visual fork management
- One-click upstream sync
- Interactive conflict resolution

**GitHub Desktop:**
- Fork sync support
- Visual diff viewer
- Simple merge interface

**SourceTree:**
- Fork management
- Visual history graph
- Advanced merge tools

### CLI Tools

**lazygit:**
- Terminal UI for git
- Visual merge conflict resolution
- Interactive rebase

**tig:**
- Text-mode interface for git
- History browsing
- Commit inspection

**hub (deprecated, use gh):**
- GitHub-specific git wrapper
- Fork management
- PR creation

---

## Further Reading

### Books

- **Pro Git** by Scott Chacon and Ben Straub
  - Chapter 3: Git Branching
  - Chapter 5: Distributed Git

### Articles

- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
- [Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows)

### Videos

- [Git and GitHub for Beginners - Crash Course](https://www.youtube.com/watch?v=RGOj5yH7evk)
- [Advanced Git Tutorial](https://www.youtube.com/watch?v=Uszj_k0DGsg)

---

## Community Resources

**Forums:**
- [Stack Overflow - Git](https://stackoverflow.com/questions/tagged/git)
- [Reddit - r/git](https://reddit.com/r/git)
- [GitHub Community](https://github.community/)

**Cheat Sheets:**
- [Git Cheat Sheet (GitHub)](https://education.github.com/git-cheat-sheet-education.pdf)
- [Git Cheat Sheet (Atlassian)](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)

**Interactive Learning:**
- [Learn Git Branching](https://learngitbranching.js.org/)
- [Git Immersion](https://gitimmersion.com/)
- [GitHub Learning Lab](https://lab.github.com/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive fork sync workflow |

---

## Contributing

If you find issues or have suggestions for this skill:

1. Check existing issues/PRs
2. Open a new issue with detailed description
3. Submit PR with improvements
4. Follow MoAI-ADK contribution guidelines

---

## License

This skill documentation follows the MoAI-ADK project license.
