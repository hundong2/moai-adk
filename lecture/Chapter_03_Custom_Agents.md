# Chapter 03: Custom Agents & Personas

## 🎭 Who is "Claude"?

In MoAI-ADK, "Claude" isn't just one entity. It's a **hive mind** of specialized agents.
When you run a command, the **Router** decides which "Persona" should handle the request.

- **`manager-spec`**: The Planner. High-level, obsessed with requirements.
- **`expert-backend`**: The Coder. Writes Python/Go/Java, ignores UI.
- **`expert-frontend`**: The Designer. Cares about CSS, React, and UX.
- **`quality-assurance`**: The Tester. Cynical, breaks things, writes tests.

## 🎛️ How Routing Works

The system uses **Triggers** (just like Skills) to wake up the right agent.

1.  **User says**: *"Create a new React component for the login button."*
2.  **Router hears**: "React", "Unknown", "Component".
3.  **Action**: Activates `expert-frontend` agent.
4.  **Result**: The agent loads only the skills relevant to Frontend (CSS, React patterns) and ignores Backend skills (SQL, Docker).

## 🛠️ Lab: Creating a Custom "Reviewer" Persona

Let's define a new persona that is strict about code style.

### Step 1: Define the Persona
In your `agentskills` or a custom skill folder, you can define a `persona-reviewer` skill.

Create `.claude/skills/persona-reviewer/SKILL.md`:

```yaml
---
name: "persona-reviewer"
description: "A strict code reviewer persona"
triggers:
  agents: ["reviewer"]  # <-- Activates when acting as 'reviewer'
  keywords: ["review", "critique", "audit"]
progressive_disclosure:
  enabled: true
---

# 🕵️ Persona: The Code Auditor

You are **The Auditor**. You do not write code. You construct critiques.
Your goal is to find:
1. Security vulnerabilities.
2. Inefficient algorithms.
3. Bad variable names.

**Style**: Be direct, strict, and professional. Use "I recommend" instead of "Maybe".
```

### Step 2: Invoke the Persona

Now, you can explicitly ask Claude to adopt this persona (if the Router logic allows) or simply trigger it with keywords.

**Try this with Claude**:
*"Act as The Auditor and review the `src/main.py` file."*

Because you used the keywords ("Auditor", "review"), the `persona-reviewer` Body (Level 2) loads.
Claude reads "You are The Auditor..." and shifts its tone immediately.

## 🧩 The Power of "Agent + Skill"

This is the formula for MoAI-ADK:
> **Agent Persona** (Who I am) + **Skill Knowledge** (What I know) = **Agentic Workflow**

By mixing and matching Personas and Skills, you can build a team of virtual employees.

---

## ⏭️ Next Step

You have the Brain (Architecture), the Knowledge (skills), and the Personality (Agents).
Now, let's put them to work with **Workflows**.
Proceed to **[Chapter 04: Workflow Mastery](./Chapter_04_Workflow_Mastery.md)**.
