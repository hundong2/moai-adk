# Fork Sync Workflow - Examples

This document provides detailed examples for fork synchronization workflows.

---

## Complete Workflow Example

### Scenario: First-Time Fork Sync

**Initial State:**
```bash
# User forked modu-ai/moai-adk to hundong2/moai-adk
# Local repository only has 'origin' remote
```

**Step-by-Step Execution:**

```bash
# 1. Check current remote configuration
$ git remote -v
origin  https://github.com/hundong2/moai-adk.git (fetch)
origin  https://github.com/hundong2/moai-adk.git (push)

# 2. Check current branch
$ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

# 3. Discover upstream repository using GitHub CLI
$ gh repo view --json parent,url
{
  "parent": {
    "name": "moai-adk",
    "owner": {
      "login": "modu-ai"
    }
  },
  "url": "https://github.com/hundong2/moai-adk"
}

# 4. Add upstream remote
$ git remote add upstream https://github.com/modu-ai/moai-adk.git

# 5. Verify upstream was added
$ git remote -v
origin    https://github.com/hundong2/moai-adk.git (fetch)
origin    https://github.com/hundong2/moai-adk.git (push)
upstream  https://github.com/modu-ai/moai-adk.git (fetch)
upstream  https://github.com/modu-ai/moai-adk.git (push)

# 6. Fetch upstream changes
$ git fetch upstream
From https://github.com/modu-ai/moai-adk
 * [new branch]      main -> upstream/main
 * [new tag]         v1.3.7 -> v1.3.7
 * [new tag]         v1.3.6 -> v1.3.6
 ... (more tags)

# 7. Check current status before merge
$ git status
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean

# 8. Merge upstream changes
$ git merge upstream/main
Updating 42730a41..874edefe
Fast-forward
 366 files changed, 7400 insertions(+), 14434 deletions(-)
 create mode 100644 .claude/agents/moai/manager-ddd.md
 delete mode 100644 .claude/agents/moai/manager-tdd.md
 ... (more changes)

# 9. Push to origin fork
$ git push origin main
To https://github.com/hundong2/moai-adk.git
   42730a41..874edefe  main -> main

# 10. Verify synchronization
$ git log --oneline -5
874edefe (HEAD -> main, upstream/main, origin/main) chore: Bump version to 1.3.7
53a25288 test: Update git tests with DDD terminology
409caca5 refactor(git): Rename TDD to DDD terminology
99fdaf7f docs(release): Add config version files to release checklist
8e8d3c0d fix: Update config version to 1.3.6
```

**Result:**
- ✅ Upstream remote configured
- ✅ 366 files synchronized
- ✅ Fast-forward merge (no conflicts)
- ✅ Origin fork updated
- ✅ Local, upstream, and origin all aligned

---

## Example: Handling Merge Conflicts

### Scenario: Local Changes Conflict with Upstream

**Initial State:**
```bash
# User has local commits
# Upstream has conflicting changes
```

**Execution:**

```bash
# 1. Fetch upstream
$ git fetch upstream

# 2. Attempt merge
$ git merge upstream/main
Auto-merging src/moai_adk/cli/commands/init.py
CONFLICT (content): Merge conflict in src/moai_adk/cli/commands/init.py
Automatic merge failed; fix conflicts and then commit the result.

# 3. Check conflicting files
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   src/moai_adk/cli/commands/init.py

# 4. View conflict
$ git diff src/moai_adk/cli/commands/init.py
<<<<<<< HEAD
def init_command(project_name: str):
    # Local implementation
    print(f"Initializing {project_name}")
=======
def init_command(project_name: str, template: str):
    # Upstream implementation
    print(f"Initializing {project_name} with {template}")
>>>>>>> upstream/main

# 5. Resolve conflict manually
# Edit src/moai_adk/cli/commands/init.py to merge both changes

# 6. Mark as resolved
$ git add src/moai_adk/cli/commands/init.py

# 7. Complete merge
$ git commit -m "Merge upstream/main with conflict resolution"

# 8. Push to origin
$ git push origin main
```

**Result:**
- ✅ Conflicts identified and resolved
- ✅ Merge commit created with resolution
- ✅ Fork synchronized successfully

---

## Example: Rebase Strategy

### Scenario: Clean Linear History

**Execution:**

```bash
# 1. Fetch upstream
$ git fetch upstream

# 2. Rebase instead of merge
$ git rebase upstream/main
Successfully rebased and updated refs/heads/main.

# 3. Force push to origin (rebase rewrites history)
$ git push origin main --force-with-lease
To https://github.com/hundong2/moai-adk.git
 + 42730a41...874edefe main -> main (forced update)

# 4. Verify clean history
$ git log --oneline --graph -10
* 874edefe (HEAD -> main, upstream/main, origin/main) chore: Bump version
* 53a25288 test: Update git tests
* 409caca5 refactor: Rename TDD to DDD
* 99fdaf7f docs: Add config version
* 8e8d3c0d fix: Update config version
```

**Result:**
- ✅ Clean linear history (no merge commits)
- ✅ Local commits replayed on top of upstream
- ✅ Force push successful with --force-with-lease

---

## Example: Fetch-Only Strategy

### Scenario: Review Changes Before Merging

**Execution:**

```bash
# 1. Fetch upstream
$ git fetch upstream

# 2. Review changes without merging
$ git log upstream/main --oneline -10
874edefe chore: Bump version to 1.3.7
53a25288 test: Update git tests with DDD terminology
409caca5 refactor(git): Rename TDD to DDD terminology

# 3. Check diff between local and upstream
$ git diff main upstream/main --stat
 366 files changed, 7400 insertions(+), 14434 deletions(-)

# 4. Review specific file changes
$ git diff main upstream/main -- CLAUDE.md

# 5. Decide to merge after review
$ git merge upstream/main
Updating 42730a41..874edefe
Fast-forward
 366 files changed, 7400 insertions(+), 14434 deletions(-)

# 6. Push to origin
$ git push origin main
```

**Result:**
- ✅ Changes reviewed before merging
- ✅ Informed decision made
- ✅ Safe merge executed

---

## Example: Automated Script

### Scenario: Scripted Fork Sync

**Bash Script: `sync-fork.sh`**

```bash
#!/bin/bash
set -e

echo "🔄 Fork Sync Workflow"
echo "===================="

# 1. Check if upstream exists
if ! git remote | grep -q upstream; then
    echo "📡 Discovering upstream repository..."
    PARENT_REPO=$(gh repo view --json parent --jq '.parent.owner.login + "/" + .parent.name')
    UPSTREAM_URL="https://github.com/${PARENT_REPO}.git"

    echo "✅ Found upstream: ${UPSTREAM_URL}"
    git remote add upstream "${UPSTREAM_URL}"
fi

# 2. Verify working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Working directory has uncommitted changes"
    echo "Please commit or stash changes before syncing"
    exit 1
fi

# 3. Fetch upstream
echo "📥 Fetching upstream changes..."
git fetch upstream

# 4. Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# 5. Merge upstream
echo "🔀 Merging upstream/${CURRENT_BRANCH}..."
git merge "upstream/${CURRENT_BRANCH}"

# 6. Push to origin
echo "📤 Pushing to origin..."
git push origin "${CURRENT_BRANCH}"

echo "✅ Fork sync complete!"
```

**Usage:**
```bash
chmod +x sync-fork.sh
./sync-fork.sh
```

**Result:**
- ✅ Automated fork synchronization
- ✅ Error handling for dirty working directory
- ✅ Upstream auto-discovery with gh CLI

---

## Example: Multiple Branch Sync

### Scenario: Sync Multiple Branches

**Execution:**

```bash
# 1. Fetch all upstream branches
$ git fetch upstream

# 2. List upstream branches
$ git branch -r | grep upstream
  upstream/main
  upstream/develop
  upstream/feature/new-ui

# 3. Sync main branch
$ git checkout main
$ git merge upstream/main
$ git push origin main

# 4. Sync develop branch
$ git checkout develop
$ git merge upstream/develop
$ git push origin develop

# 5. Sync feature branch
$ git checkout -b feature/new-ui upstream/feature/new-ui
$ git push origin feature/new-ui
```

**Result:**
- ✅ Multiple branches synchronized
- ✅ All branches up-to-date with upstream
- ✅ New upstream branches tracked locally

---

## Best Practices Summary

1. **Always fetch before merge**: See what's coming
2. **Check working directory**: Avoid conflicts with uncommitted changes
3. **Choose strategy wisely**: Merge for safety, rebase for clean history
4. **Use --force-with-lease**: Safer than --force when pushing after rebase
5. **Review changes**: Use git log and git diff before merging
6. **Test after sync**: Verify application still works
7. **Sync regularly**: Weekly or before starting new work

---

## Common Patterns

### Pattern 1: Safe Sync

```bash
git fetch upstream
git status  # Ensure clean
git merge upstream/main
git push origin main
```

### Pattern 2: Clean History Sync

```bash
git fetch upstream
git rebase upstream/main
git push origin main --force-with-lease
```

### Pattern 3: Review First Sync

```bash
git fetch upstream
git log upstream/main --oneline
git diff main upstream/main
git merge upstream/main  # After review
git push origin main
```

### Pattern 4: Conflict-Aware Sync

```bash
git fetch upstream
git merge upstream/main
# If conflicts:
git status
# Resolve conflicts
git add .
git commit
git push origin main
```
