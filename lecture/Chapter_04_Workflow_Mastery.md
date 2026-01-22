# Chapter 04: Workflow Mastery

## 🔄 The Golden Cycle: Plan, Run, Sync

Mastering MoAI-ADK means mastering the **Spec-First Domain-Driven Design (DDD)** cycle.

### 1. The PLAN Phase (`/moai:plan`)
**"Don't write code until you know what to build."**

- **Command**: `/moai:1-plan "Add a user profile page"`
- **Agent**: `manager-spec`
- **Output**: A `SPEC-00X.md` file using EARS syntax.
- **Why**: It aligns the "Brain" on the requirements before a single line of code is written.

### 2. The RUN Phase (`/moai:run`)
**"Implement the plan, preserving the domain."**

- **Command**: `/moai:2-run SPEC-001`
- **Agent**: `expert-maker` (or specialized experts)
- **Output**: Code changes, tests.
- **Philosophy**:
    - **Analyze**: Check existing code.
    - **Preserve**: Don't break existing features.
    - **Improve**: Add the new feature.

### 3. The SYNC Phase (`/moai:sync`)
**"If it's not documented, it doesn't exist."**

- **Command**: `/moai:3-sync SPEC-001`
- **Agent**: `manager-docs`
- **Output**: Updated `README.md`, API docs, diagrams, and a Git Commit.

---

## 🎩 Meet Alfred: The Autonomous Agent

Sometimes you don't want to hold the AI's hand. Enter **Alfred**.

- **Command**: `/moai:alfred "Fix the login bug"`
- **What it does**:
    1.  **Explores** the codebase to find the issue.
    2.  Creates a **Plan** (internally).
    3.  **Fixes** the code.
    4.  **Verifies** with tests.
    5.  **Repeats** until done.

**When to use**: For bug fixes, small refactors, or well-defined isolated tasks.

---

## ♾️ The Loop: Self-Healing Code

The `/moai:loop` command is your safety net.

- **Command**: `/moai:loop`
- **What it does**:
    - Runs **Lints** (Ruff, ESLint).
    - Runs **Tests** (Pytest, Jest).
    - Runs **Type Checks**.
    - If anything fails, it **Fixes it** and runs again.
- **Use case**: Run this after you (or the AI) make messy edits. It polishes the code until it shines.

---

## ⏭️ Next Step

You are now a master of the workflow. The final step is making this system *yours*.
Proceed to **[Chapter 05: Personalization & "My Brain"](./Chapter_05_Personalization.md)**.
