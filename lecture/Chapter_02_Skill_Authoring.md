# Chapter 02: Skill Authoring & Progressive Disclosure

## 📉 The Token Problem

Imagine you have 50 specialized skills (Git expert, React pro, Python guru...).
If you load all of them into Claude's context at once:
- **50 skills × 5,000 tokens** = **250,000 tokens**.
- **Claude's Limit**: ~200,000 tokens.

**Result**: Claude crashes or forgets everything.

## 💡 The Solution: Progressive Disclosure

MoAI-ADK uses a "Progressive Disclosure" pattern to solve this. It works like a polite conversation:

1.  **Level 1 (The Handshake)**: "Hi, I'm the Git expert." (~100 tokens)
    - Always loaded.
    - Contains only metadata (name, description, triggers).
2.  **Level 2 (The Conversation)**: "Here is my core knowledge." (~5,000 tokens)
    - Loaded **ONLY** when you mention a trigger keyword (e.g., "git pull").
3.  **Level 3 (The Encyclopedia)**: "Here are the deep details." (Unlimited)
    - External files loaded **ONLY** on demand.

**Result**: Total context usage drops from **250k** to **~5k**.

---

## 🧬 Anatomy of a SKILL.md

A `SKILL.md` file is divided into two parts by the YAML Frontmatter.

### Level 1: The Metadata (The "Header")
This part is **always visible** to the agent.

```yaml
---
name: "my-first-skill"
description: "A tutorial skill to learn authoring."
triggers:
  keywords: ["tutorial", "learn"]  # <-- The magic switch
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~1000
---
```

### Level 2: The Body (The "Content")
Everything *below* the second `---` is hidden until triggered.

```markdown
# My First Skill Guide

## Quick Reference
Do this, not that.

## Implementation
1. Step one...
2. Step two...
```

---

## 🧪 Lab: Create Your First Skill

Let's practice by creating a real skill in your environment.

### Step 1: Create the Directory
Run this command in your terminal:
```bash
mkdir -p .claude/skills/my-first-skill
```

### Step 2: Create the SKILL.md
Create a file named `.claude/skills/my-first-skill/SKILL.md` with:

```yaml
---
name: "my-first-skill"
description: "A demonstration of Progressive Disclosure"
triggers:
  keywords: ["demo", "flash"]
progressive_disclosure:
  enabled: true
---

# Welcome to Level 2!

If you are reading this, the skill has been **triggered**!
You mentioned "demo" or "flash", so MoAI-ADK loaded this content.

## What to do next?
Try asking Claude: "What can you do with the flash demo?"
```

### Step 3: Test It

1.  **Reload configuration**: Run `/moai:0-project` (or just restart Claude).
2.  **Trigger it**: Say to Claude: *"Show me the flash demo info."*
3.  **Verify**: use `grep_search` or just check if Claude responds with the "Welcome to Level 2!" text.

---

## ⏭️ Next Step

Now that you can teach Claude new skills, let's see how to give it a personality.
Proceed to **[Chapter 03: Custom Agents & Personas](./Chapter_03_Custom_Agents.md)**.
