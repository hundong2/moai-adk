# Chapter 02: Teaching the Brain (`lang-kotlin`)

## 🧠 What Makes a "Language Skill"?

A language skill isn't a text book. It's a **Cheat Sheet** for the AI.
Claude already knows Kotlin syntax (mostly). What it *doesn't* know is:

1.  **Your Version**: Are you using Kotlin 1.9 or 2.0?
2.  **Your Libraries**: Ktor or Spring? Arrow or standard lib?
3.  **Your Idioms**: Do you prefer `runCatching` or `try-catch`?

We need to create a `lang-kotlin` skill to align Claude with your preferences.

## 📝 Lab: Create `agentskills/lang-kotlin`

### Step 1: The Structure
Run:
```bash
mkdir -p .claude/skills/lang-kotlin
```

### Step 2: The `SKILL.md`
Create `.claude/skills/lang-kotlin/SKILL.md`:

```yaml
---
name: "lang-kotlin"
description: "Expert knowledge of Kotlin 2.0 and Coroutines"
triggers:
  keywords: ["kotlin", ".kt", "gradle.kts"]
  languages: ["kotlin"]
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
---

# Kotlin Expert Guidelines

## Quick Reference
- **Version**: Kotlin 2.0
- **Build**: Gradle Kotlin DSL
- **Style**: Ktlint standard

## Idioms to Follow

### 1. Expressions over Statements
**YES**:
```kotlin
val status = if (isValid) "OK" else "FAIL"
```
**NO**:
```kotlin
var status = ""
if (isValid) { status = "OK" } else { status = "FAIL" }
```

### 2. Coroutines
Always expose `suspend` functions for I/O.
Use `Flow` for streams, not RxJava.

### 3. Null Safety
Never use `!!`. Use `?.` or `?:` or `requireNotNull()`.

```kotlin
val name = user?.name ?: "Guest"
```

### 4. Testing
Use Kotest style assertions if available, or JUnit 5.
```kotlin
assertThat(result).isEqualTo(expected)
```
```

## 🎓 Why This Matters

When you save this file, every time you open a `.kt` file, MoAI will inject these rules into Claude's brain.
You will never have to say "Don't use `!!` please" again.

---

## ⏭️ Next Step

We taught the brain *how* to write Kotlin. Now let's define *who* writes it.
Proceed to **[Chapter 03: The Kotlin Expert Persona](./Chapter_03_Kotlin_Agent.md)**.
