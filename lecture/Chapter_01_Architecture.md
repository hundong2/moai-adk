# Chapter 01: Architecture & Philosophy

## 🏛️ What is "Agentic" Development?

Welcome to the new era of coding. If traditional AI coding assistants were "Copilots" (sitting next to you, suggesting lines), **MoAI-ADK** is designed to build "Agents" (sitting in their own office, doing the work you assigned).

**Key Differences:**
- **Copilot**: "Here is a function to calculate Fibonacci." (Function level)
- **Agent**: "I have implemented the payment module, added unit tests, and updated the documentation. Please review." (Feature/Task level)

MoAI-ADK (Agent Development Kit) provides the **framework** to build, control, and scale these agents.

---

## 🏗️ The Anatomy of MoAI-ADK

Open your project root. let's look at the key directories that make this engine run.

### 1. `src/moai_adk` (The Engine)
This is the core Python package that powers the CLI and the agents.
- **`cli/`**: Handles the `/` commands like `/moai:plan` or `/moai:loop`. It parses your intent and dispatches it to the right agent.
- **`core/`**: The brain of the operation. It includes the `LLM` interface, `Tool` definitions, and `Context` management.
- **`agentskills/`**: This is where the **Skills** live. Think of this as the "knowledge base" or "manuals" that agents read.

### 2. `.claude/skills` (The Knowledge)
This is the most critical folder for you. It contains the **Skill Definitions**.
- **`SKILL.md`**: The instruction manual for a specific topic (e.g., `git-expert`, `react-master`).
- **Progressive Disclosure**: Notice how skills are split? We'll cover this in Chapter 2, but essentially, it's about optimizing what the AI reads to save "brain space" (tokens).

### 3. `.moai/` (The Memory)
This hidden folder acts as the **Long-term Memory** for your project.
- **`specs/`**: Stores the Requirements (SPEC-001, SPEC-002...).
- **`reports/`**: Logs of what agents have done.
- **`config/`**: Project-specific settings.

---

## 🧠 Brain vs. Body

MoAI-ADK follows a distinct separation of concerns:

### The Brain (Claude / LLM)
- **Role**: Reasoning, Planning, Decision Making.
- **Inputs**: Context, Prompts, Skill Content.
- **Outputs**: Tool Calls, Plans, Code.

### The Body (MoAI Framework)
- **Role**: Execution, Sensing, interacting with the OS.
- **Components**:
    - **Tools**: `read_file`, `run_command`, `git_commit`.
    - **Sensors**: File watchers, Lints, Test runners.
    - **Safety**: Permission checks (stopping the AI from `rm -rf /`).

---

## 🧪 Quick Lab: Exploring the Core

Let's use Claude to verify our understanding. Run the following command in your terminal (or ask Claude to do it):

```bash
# List the available skills to see "The Knowledge"
ls -F agentskills/
```

You should see directories like `architect`, `coder`, `qa`. These represent the **Specialized Agents** that use the skills.

---

## ⏭️ Next Step

Now that we understand the "Body" (the framework), let's learn how to teach the "Brain" new tricks.
Proceed to **[Chapter 02: Skill Authoring & Progressive Disclosure](./Chapter_02_Skill_Authoring.md)**.
