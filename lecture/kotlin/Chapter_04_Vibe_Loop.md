# Chapter 04: The Vibe Loop

## ♾️ What is the Vibe Loop?

The "Vibe" in Vibe Coding comes from **Fast Feedback**.
You write code, and the machine tells you *instantly* if it's good.

In MoAI-ADK, the `/moai:loop` command is the engine that drives this.
For Kotlin, we want the loop to:

1.  **Format** the code (`ktlint --format`).
2.  **Lint** for bugs (`detekt`).
3.  **Test** the changes (`gradle test`).

If any of these fail, the Agent captures the output and **fixes the code automatically**.

## 📝 Lab: Creating the Kotlin Loop

To enable this, we need to create a **Project-Specific Loop Configuration**.

### Step 1: `moai-loop` Script
MoAI looks for a `scripts/loop.sh` (or similar) to run its quality checks.
Create `scripts/kotlin-loop.sh`:

```bash
#!/bin/bash
# scripts/kotlin-loop.sh

echo "🔍 Running Ktlint..."
ktlint --format || exit 1

echo "🔍 Running Detekt..."
detekt || exit 1

echo "🧪 Running Tests..."
./gradlew test || exit 1

echo "✅ All System Go!"
```

Don't forget to make it executable: `chmod +x scripts/kotlin-loop.sh`

### Step 2: Teaching Claude to Use it
Now, update your `lang-kotlin` skill (from Chapter 2) to include instructions about the loop.

Add this to `.claude/skills/lang-kotlin/SKILL.md`:

```markdown
## The Vibe Loop
When the user asks to "fix issues" or "run the loop", ALWAYS run:
`./scripts/kotlin-loop.sh`

If it fails:
1. Read the error output.
2. Fix the specific file.
3. Run it again.
```

## 🏃‍♀️ Try it out

1.  Intentionally break a rule (e.g., bad indentation in a `.kt` file).
2.  Run: `/moai:loop` (or ask Claude "Run the Kotlin loop and fix errors").
3.  Watch as Claude runs the script, sees the failure, modifies the file, and passes the test.

**That is the Vibe.**

---

## ⏭️ Next Step

The training is complete. It's time for the final exam.
Proceed to **[Chapter 05: Capstone - Building a Service](./Chapter_05_Capstone.md)**.
