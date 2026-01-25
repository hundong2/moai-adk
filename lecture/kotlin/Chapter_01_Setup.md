# Chapter 01: Environment & Tooling

## 🛠️ Preparing the Forge

Before we can teach the AI, we need to make sure *our* environment is ready.
MoAI-ADK relies on the local environment to run tests and linters.

### 1. The Essentials

You need the following tools installed:

```bash
# MacOS (using brew)
brew install openjdk kotlin gradle
```

- **OpenJDK**: The runtime.
- **Kotlin**: The compiler (`kotlinc`).
- **Gradle**: The build tool (we'll use Kotlin DSL).

### 2. The "Vibe" Tools

"Vibe Coding" relies on fast feedback loops. For Kotlin, we use:

- **Ktlint**: For enforcing style (no more bike-shedding on PRs).
- **Detekt**: For static analysis (finding bugs before they happen).

```bash
brew install ktlint detekt
```

### 3. Configuring Claude

We need to tell Claude that "Kotlin exists" in this project.
Open your `.claude/settings.json` (or create it if it doesn't exist) and ensure:

```json
{
  "commands": {
    "auto_approve": ["gradle", "./gradlew", "ktlint", "kotlinc"]
  }
}
```

**Why?**
When MoAI runs `/moai:loop`, it will try to run `./gradlew test`. If it stops to ask for permission every time, the "Vibe" is killed.
Whitelisting these commands allows for **Autonomous Vibe Coding**.

---

## 🧪 Lab: Verify Setup

Run this command to check if your environment is ready:

```bash
java -version && kotlin -version && gradle -version
```

If you see versions for all three, you are ready to proceed.

---

## ⏭️ Next Step

Now that the forge is hot, let's teach the brain how to hammer.
Proceed to **[Chapter 02: Teaching the Brain (`lang-kotlin`)](./Chapter_02_Language_Skill.md)**.
