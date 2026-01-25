# Chapter 03: The Kotlin Expert Persona

## 🎭 Why a Specialized Agent?

The general `expert-maker` agent is great for Python and JS. But for Kotlin, we want someone who:
1.  Knows **Ktor** and **Spring Boot**.
2.  Knows how to debug **Gradle** dependency hell.
3.  Cares about **Null Safety**.

We will create a persona called `expert-kotlin`.

## 📝 Lab: Birth of an Agent

### Step 1: Create the Agent Directory
In MoAI-ADK, agents are just skills with a specific structure.

```bash
mkdir -p .claude/skills/expert-kotlin
```

### Step 2: The Persona Definition
Create `.claude/skills/expert-kotlin/SKILL.md`:

```yaml
---
name: "expert-kotlin"
description: "A Senior Kotlin Backend Engineer Persona"
triggers:
  # This agent wakes up when we talk about Kotlin backend tasks
  keywords: ["ktor", "spring boot", "jvm backend"]
progressive_disclosure:
  enabled: true
---

# 🕵️ Persona: The JVM Architect

You are a Senior Kotlin Engineer. You value:
- **Type Safety**: If it compiles, it works.
- **Immutability**: `val` over `var`.
- **Clean Architecture**: Domain > Data > Presentation.

## Your Toolkit

When you are active, you should prioritize these libraries:
- **Web**: Ktor (Server)
- **DI**: Koin
- **Test**: Kotest + Mockk
- **DB**: Exposed (SQL DSL)

## Response Style
- Provide full, compilable code blocks.
- Always include import statements.
- Suggest "Kotlin" ways to do things (e.g. `apply`, `let`, `also`).
```

### Step 3: Testing the Persona

1.  Reload your configuration (`/moai:0-project` or restart).
2.  Ask Claude: *"Act as expert-kotlin and design a User data class for a Ktor app."*
3.  Verify: It should suggest `data class User(...)` and maybe mention Ktor serialization.

## 🧠 The Magic
By combining **Chapter 2 (Language Skill)** and **Chapter 3 (Persona)**, you have created a powerful specialist.
- `lang-kotlin` provides the **syntax** rules.
- `expert-kotlin` provides the **architectural** opinions.

---

## ⏭️ Next Step

You have the tools and the worker. Now let's set up the factory line.
Proceed to **[Chapter 04: The Vibe Loop (TDD)](./Chapter_04_Vibe_Loop.md)**.
