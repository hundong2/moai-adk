# Chapter 05: Personalization & "My Brain"

## 🧠 Making MoAI Your Own

MoAI-ADK is powerful out of the box, but it shines when you inject your own DNA into it.
This final chapter teaches you how to customize the "Brain" and the "Body".

### 1. Customizing `.claude/settings.json`

This file controls the global behavior of your agent.

```json
{
  "commands": {
    "auto_approve": ["ls", "grep"]  // Commands safe to run without asking
  },
  "nlu": {
    "locale": "ko-KR" // Force Korean responses
  }
}
```

**Tip**: Use this to whitelist trusted commands or change the default language.

### 2. The Power of Git Hooks

MoAI-ADK comes with strict quality gates.
Check `scripts/check-hooks.sh`. These hooks ensure that **YOU** (and the AI) don't commit bad code.

- **pre-commit**: Runs linting and simple checks.
- **pre-push**: Runs the full `pytest` suite.

To enable them:
```bash
./scripts/install-hooks.sh
```

### 3. Injecting "My Brain" (Knowledge Graph)

You can add your own engineering principles to the system.

1.  Create a folder `.claude/skills/my-principles`.
2.  Add a `SKILL.md` with:
    ```yaml
    triggers:
      keywords: ["design", "architecture"]
    ```
3.  Add your rules:
    - "Always use functional components."
    - "Never use `any` type in TypeScript."

Now, whenever you discuss design, Claude will respect **YOUR** rules.

---

## 🎓 Graduation

Congratulations! You have completed the **MoAI-ADK Master Class**.

### Checklist
- [ ] You understand the **Agentic Architecture**.
- [ ] You can author **Skills with Progressive Disclosure**.
- [ ] You can create **Custom Personas**.
- [ ] You have mastered the **Plan-Run-Sync** loop.
- [ ] You have personalized the system.

**What's Next?**
Start building! The best way to learn is to code.
Use `/moai:alfred` to build something crazy.

**Good luck, Architect.**
