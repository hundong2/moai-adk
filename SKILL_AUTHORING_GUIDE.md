# SKILL.md Authoring Guide

**Comprehensive guide for creating, structuring, and optimizing Claude Code skills with Progressive Disclosure**

Version: 1.0.0
Last Updated: 2026-01-17
Author: Hundong2
[KOR🇰🇷](./SKILL_AUTHORING_GUIDE.kr.md)

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is a SKILL.md?](#what-is-a-skillmd)
3. [Progressive Disclosure System](#progressive-disclosure-system)
4. [SKILL.md Structure](#skillmd-structure)
5. [Writing Your First SKILL.md](#writing-your-first-skillmd)
6. [YAML Frontmatter Reference](#yaml-frontmatter-reference)
7. [Trigger Configuration](#trigger-configuration)
8. [How Skills are Loaded in Claude Code](#how-skills-are-loaded-in-claude-code)
9. [Modularization Patterns](#modularization-patterns)
10. [Token Optimization Strategies](#token-optimization-strategies)
11. [Best Practices](#best-practices)
12. [Examples and Templates](#examples-and-templates)
13. [Troubleshooting](#troubleshooting)
14. [Advanced Topics](#advanced-topics)

---

## Introduction

### Purpose of This Guide

This guide teaches you how to create **Skills** for Claude Code using the **Progressive Disclosure** system. Skills are reusable knowledge modules that Claude can load on-demand, dramatically reducing token consumption while maintaining full functionality.

### Who Should Read This?

- Developers creating custom Claude Code skills
- Teams building domain-specific knowledge for AI agents
- Contributors to MoAI-ADK or similar frameworks
- Anyone wanting to optimize Claude's context window usage

### Key Benefits

- **67%+ token reduction** through 3-level loading
- **On-demand knowledge**: Load only what's needed
- **Modular architecture**: Easy to maintain and extend
- **Backward compatible**: Works with existing agents

---

## What is a SKILL.md?

### Definition

A **SKILL.md** file is a structured markdown document that contains specialized knowledge, patterns, and best practices for a specific domain, technology, or workflow. It follows the **Progressive Disclosure** pattern to optimize token usage.

### Core Characteristics

1. **Hierarchical Structure**: 3-level loading (Metadata → Body → Bundled Files)
2. **Trigger-Based Loading**: Loads based on keywords, phases, agents, or languages
3. **Modular Design**: Can reference external files for extended documentation
4. **User-Invocable**: Can be called directly by users or loaded by agents

### File Location

```
.claude/skills/
├── skill-name/
│   ├── SKILL.md           # Main skill file (Level 1 + 2)
│   ├── examples.md        # Level 3+ (On-demand)
│   ├── reference.md       # Level 3+ (On-demand)
│   └── modules/           # Level 3+ (On-demand)
│       ├── pattern-1.md
│       ├── pattern-2.md
│       └── ...
```

### SKILL.md Anatomy

```markdown
---
# Level 1: Metadata (Always Loaded)
name: "skill-name"
description: "Brief description"
triggers:
  keywords: ["keyword1", "keyword2"]
---

# Level 2: Skill Body (Conditional Load)
## Quick Reference
## Implementation Guide
## Advanced Topics

# Level 3: Bundled Files (On-Demand)
## Module References
## Examples
## Reference
```

---

## Progressive Disclosure System

### Overview

**Progressive Disclosure** is a token optimization pattern that loads content in stages based on relevance. Instead of loading all documentation upfront, Claude receives increasingly detailed information only when needed.

### Why Progressive Disclosure?

**Problem**: Traditional approaches load entire documentation sets, consuming massive tokens:
- 48 skills × ~5K tokens = **240K tokens** (exceeds Claude's 200K limit)

**Solution**: Progressive Disclosure reduces this to:
- 48 skills × ~100 tokens = **4.8K tokens** (98% reduction)

Full documentation loads only when triggers match user intent.

### The Three Levels

#### Level 1: Metadata Only (~100 tokens per skill)

**What's Loaded:**
- YAML frontmatter only
- Skill name, description, version
- Trigger conditions
- Dependencies
- Allowed tools

**When Loaded:**
- During agent initialization
- Always loaded for skills listed in agent's `skills:` field

**Token Cost:**
- ~100 tokens per skill
- Minimal impact on context window

**Example:**
```yaml
---
name: "moai-workflow-spec"
description: "SPEC workflow specialist"
version: "1.0.0"
triggers:
  keywords: ["SPEC", "requirement", "EARS"]
---
```

#### Level 2: Skill Body (~5K tokens per skill)

**What's Loaded:**
- Full markdown body after YAML frontmatter
- Quick Reference section
- Implementation Guide
- Advanced Topics
- Usage Examples

**When Loaded:**
- When trigger conditions match user prompt
- When agent explicitly requests the skill
- When phase matches trigger configuration

**Token Cost:**
- ~5K tokens per skill
- Only loaded for relevant skills

**Example:**
```markdown
## Quick Reference

**What is SPEC workflow?**

A structured approach to requirements documentation...

## Implementation Guide

### Step 1: Analyze Requirements
...
```

#### Level 3+: Bundled Files (Unlimited)

**What's Loaded:**
- External markdown files in skill directory
- Modules, examples, reference documentation
- Code samples, diagrams, detailed guides

**When Loaded:**
- On-demand by Claude when needed
- Claude decides based on task requirements
- User can request specific modules

**Token Cost:**
- Unlimited (loaded as needed)
- Not counted in initial budget

**Example:**
```
skill-name/
├── SKILL.md
├── examples.md       # Level 3
├── reference.md      # Level 3
└── modules/          # Level 3+
    ├── advanced-patterns.md
    └── troubleshooting.md
```

### Token Budget Comparison

| Approach | Skills Loaded | Token Cost | Context Remaining |
|----------|---------------|------------|-------------------|
| **No Progressive Disclosure** | 48 skills | ~240K tokens | ❌ Exceeds limit |
| **Progressive Disclosure (Level 1)** | 48 skills | ~4.8K tokens | ✅ 195K free |
| **Progressive Disclosure (L1+L2)** | 5 triggered skills | ~25K tokens | ✅ 175K free |

### Loading Flow Diagram

```
User Prompt: "Create a SPEC document for authentication"
    ↓
┌───────────────────────────────────────────────┐
│ 1. Agent Initialization                       │
│    Load Level 1 for all skills in agent       │
│    Token Cost: 48 × 100 = 4,800 tokens        │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ 2. Trigger Matching                           │
│    Check keywords: "SPEC", "authentication"   │
│    Matches: moai-workflow-spec                │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ 3. Load Level 2 for Matched Skills            │
│    Load full body of moai-workflow-spec       │
│    Token Cost: +5,000 tokens                  │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ 4. Claude Uses Loaded Knowledge               │
│    Creates SPEC document using loaded context │
│    Can request Level 3 modules if needed      │
└───────────────────────────────────────────────┘
```

---

## SKILL.md Structure

### Complete Template

```markdown
---
# ═══════════════════════════════════════════════
# Level 1: Core Metadata (Always Loaded ~100 tokens)
# ═══════════════════════════════════════════════
name: "skill-name"
description: "One-line description of what this skill does"
version: "1.0.0"
category: "workflow"  # foundation, lang, platform, library, workflow, domain
modularized: true
user-invocable: true

# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~5000

# Trigger Conditions for Level 2 Loading
triggers:
  keywords: ["keyword1", "keyword2", "keyword3"]
  phases: ["plan", "run", "sync"]
  agents: ["manager-spec", "expert-backend"]
  languages: ["python", "typescript"]

# Dependencies
requires: []
optional_requires: ["related-skill"]

# Allowed Tools
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash

# Skill Metadata
tags: ["tag1", "tag2"]
updated: 2026-01-17
status: "active"  # active, experimental, deprecated
---

# ═══════════════════════════════════════════════
# Level 2: Skill Body (Conditional Load ~5K tokens)
# ═══════════════════════════════════════════════

## Quick Reference

**What is [skill-name]?**

One-sentence answer explaining the core purpose.

**Key Benefits:**
- Benefit 1
- Benefit 2
- Benefit 3

**When to Use:**
- Use case 1
- Use case 2

**Quick Links:**
- Implementation: #implementation-guide
- Examples: examples.md
- Reference: reference.md

---

## Implementation Guide

### Core Concepts

Brief explanation of the main concepts (1-2 paragraphs).

### Step-by-Step Process

**Step 1: [First Step]**

Description and example.

**Step 2: [Second Step]**

Description and example.

### Integration Points

How this skill integrates with other skills and agents.

---

## Advanced Topics

### Performance Considerations

Tips for optimal performance.

### Edge Cases

Handling special cases and error scenarios.

### Best Practices

Recommended patterns and anti-patterns.

---

## Works Well With

**Related Skills:**
- skill-one: When to use together
- skill-two: Complementary use cases

**Agents:**
- agent-name: How this agent uses this skill

**Commands:**
- /command: Command that invokes this skill

---

# ═══════════════════════════════════════════════
# Level 3: Bundled Files (On-Demand Load)
# ═══════════════════════════════════════════════

## Module References

Extended documentation in modular files:

- **modules/patterns.md**: Detailed design patterns
- **modules/examples.md**: Comprehensive examples
- **modules/reference.md**: API reference
- **modules/troubleshooting.md**: Common issues

## Examples

Working code samples in **examples.md**:
- Example 1: Basic usage
- Example 2: Advanced usage
- Example 3: Integration pattern

## Reference

External resources in **reference.md**:
- Official documentation
- Community resources
- Related tools

---

# Progressive Disclosure Levels Summary

| Level | What | When | Token Cost |
|-------|------|------|------------|
| 1 | YAML Metadata only | Agent initialization | ~100 tokens |
| 2 | SKILL.md Body | Trigger keywords match | ~5K tokens |
| 3+ | Bundled files | Claude decides | Unlimited |

---

# Backward Compatibility Note

For agents that don't support Progressive Disclosure yet, the entire SKILL.md (Levels 1 + 2) will be loaded at initialization. This ensures compatibility while enabling optimization for Progressive Disclosure-aware agents.
```

### Section Breakdown

#### Quick Reference (Level 2)

**Purpose**: Provide immediate, actionable information

**Components**:
- **What is [skill-name]?**: One-sentence explanation
- **Key Benefits**: 3-5 bullet points
- **When to Use**: Common use cases
- **Quick Links**: Navigation to detailed sections

**Guidelines**:
- Keep it scannable (user can decide relevance in 10 seconds)
- Focus on "what" and "why", not "how"
- Use clear, non-technical language

#### Implementation Guide (Level 2)

**Purpose**: Teach users how to apply the skill

**Components**:
- **Core Concepts**: Foundational knowledge
- **Step-by-Step Process**: Actionable instructions
- **Integration Points**: How it connects to other skills

**Guidelines**:
- Use numbered steps for sequential processes
- Include code examples where applicable
- Show before/after states

#### Advanced Topics (Level 2)

**Purpose**: Handle edge cases and optimizations

**Components**:
- **Performance Considerations**: Optimization tips
- **Edge Cases**: Special scenarios
- **Best Practices**: Dos and don'ts

**Guidelines**:
- Optional reading for advanced users
- Include warnings for common pitfalls
- Reference Level 3 modules for deep dives

#### Bundled Files (Level 3+)

**Purpose**: Provide unlimited detailed documentation

**Components**:
- **examples.md**: Complete working examples
- **reference.md**: External links, API docs
- **modules/*.md**: Specialized subtopics

**Guidelines**:
- Self-contained (readable without SKILL.md)
- Cross-reference related modules
- Include comprehensive code samples

---

## Writing Your First SKILL.md

### Step-by-Step Tutorial

#### Step 1: Create Skill Directory

```bash
mkdir -p .claude/skills/my-first-skill
cd .claude/skills/my-first-skill
```

#### Step 2: Create SKILL.md File

```bash
touch SKILL.md
```

#### Step 3: Write YAML Frontmatter

```yaml
---
name: "my-first-skill"
description: "A tutorial skill demonstrating Progressive Disclosure"
version: "1.0.0"
category: "workflow"
modularized: false
user-invocable: true

progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~3000

triggers:
  keywords: ["tutorial", "first skill", "learning"]
  phases: []
  agents: []
  languages: []

requires: []
optional_requires: []

allowed-tools:
  - Read

tags: ["tutorial", "beginner"]
updated: 2026-01-17
status: "active"
---
```

#### Step 4: Write Quick Reference

```markdown
## Quick Reference

**What is my-first-skill?**

A simple tutorial skill that demonstrates the Progressive Disclosure pattern and helps you learn skill authoring.

**Key Benefits:**
- Learn by example
- Understand Progressive Disclosure
- Template for your own skills

**When to Use:**
- When learning skill authoring
- As a reference for new skills
- For testing skill loading

**Quick Links:**
- Implementation: #implementation-guide
```

#### Step 5: Write Implementation Guide

```markdown
## Implementation Guide

### Core Concepts

This skill demonstrates how Progressive Disclosure works:
1. Metadata loads first (~100 tokens)
2. Body loads when triggered (~3K tokens)
3. Additional files load on-demand

### Step-by-Step Process

**Step 1: Trigger the Skill**

Use any of these keywords in your prompt:
- "tutorial"
- "first skill"
- "learning"

**Step 2: Observe Loading**

Claude will:
1. Load Level 1 metadata during initialization
2. Load Level 2 body when keywords match
3. Access Level 3 files if you ask for details

**Step 3: Verify Behavior**

Ask Claude: "Show me the tutorial skill details"
```

#### Step 6: Test Your Skill

```
User: "Show me the tutorial skill"

Expected: Claude loads Level 2 and shows content
```

#### Step 7: Add Level 3 Files (Optional)

```bash
# Create examples file
touch examples.md

# Create reference file
touch reference.md

# Create modules directory
mkdir modules
touch modules/advanced-patterns.md
```

---

## YAML Frontmatter Reference

### Complete Field Reference

```yaml
---
# ═══════════════════════════════════════════════
# REQUIRED FIELDS
# ═══════════════════════════════════════════════

name: "skill-name"
# - MUST be unique across all skills
# - Use kebab-case (lowercase with hyphens)
# - Match directory name
# Example: "moai-workflow-spec"

description: "Brief one-line description"
# - MUST be clear and concise (< 100 chars)
# - Explain what the skill does, not how
# Example: "SPEC workflow specialist for requirements documentation"

version: "1.0.0"
# - MUST follow semantic versioning (major.minor.patch)
# - Increment on changes:
#   - major: Breaking changes
#   - minor: New features (backward compatible)
#   - patch: Bug fixes

# ═══════════════════════════════════════════════
# CATEGORIZATION
# ═══════════════════════════════════════════════

category: "workflow"
# - MUST be one of:
#   - foundation: Core MoAI concepts
#   - lang: Programming language skills
#   - platform: Platform-specific (Vercel, Supabase, etc.)
#   - library: Library skills (shadcn, Nextra, etc.)
#   - workflow: Process skills (SPEC, TDD, etc.)
#   - domain: Domain skills (backend, frontend, etc.)

modularized: true
# - true: Skill has Level 3 modules
# - false: Skill is self-contained in SKILL.md

user-invocable: true
# - true: Users can call this skill directly
# - false: Only loaded by agents

# ═══════════════════════════════════════════════
# PROGRESSIVE DISCLOSURE
# ═══════════════════════════════════════════════

progressive_disclosure:
  enabled: true
  # - true: Use 3-level loading
  # - false: Load entire SKILL.md at once

  level1_tokens: ~100
  # - Estimated token count for YAML frontmatter
  # - Use ~ prefix for approximate values

  level2_tokens: ~5000
  # - Estimated token count for full markdown body
  # - Use ~ prefix for approximate values

# ═══════════════════════════════════════════════
# TRIGGER CONDITIONS
# ═══════════════════════════════════════════════

triggers:
  keywords: ["keyword1", "keyword2", "keyword3"]
  # - List of trigger keywords (case-insensitive)
  # - When ANY keyword appears in user prompt, load Level 2
  # - Examples: ["SPEC", "requirement", "EARS", "planning"]

  phases: ["plan", "run", "sync"]
  # - Load Level 2 during specific workflow phases
  # - Valid phases: plan, run, sync
  # - Empty list [] = no phase triggers

  agents: ["manager-spec", "expert-backend"]
  # - Load Level 2 when these agents are active
  # - Use agent names (without .md extension)
  # - Empty list [] = no agent triggers

  languages: ["python", "typescript", "javascript"]
  # - Load Level 2 when working with these languages
  # - Detected from file extensions or user mention
  # - Empty list [] = no language triggers

# ═══════════════════════════════════════════════
# DEPENDENCIES
# ═══════════════════════════════════════════════

requires: []
# - Skills that MUST be loaded before this one
# - Use skill names (without .md extension)
# - Example: ["moai-foundation-core"]

optional_requires: []
# - Skills that CAN enhance this skill
# - Loaded if available, but not required
# - Example: ["moai-foundation-philosopher"]

# ═══════════════════════════════════════════════
# ALLOWED TOOLS
# ═══════════════════════════════════════════════

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - TodoWrite
# - List of tools this skill can use
# - Restricts tool access for safety
# - Use official Claude Code tool names

# ═══════════════════════════════════════════════
# METADATA
# ═══════════════════════════════════════════════

tags: ["tag1", "tag2", "tag3"]
# - Searchable tags for skill discovery
# - Use lowercase, single words
# - Example: ["git", "workflow", "automation"]

updated: 2026-01-17
# - Last update date (YYYY-MM-DD format)
# - Update when making significant changes

status: "active"
# - Lifecycle status
# - Valid values:
#   - active: Fully supported, recommended
#   - experimental: Testing phase, may change
#   - deprecated: No longer maintained, use alternative
---
```

### Field Validation Rules

**name**:
- ✅ `moai-workflow-spec`
- ✅ `my-custom-skill`
- ❌ `MyCustomSkill` (no PascalCase)
- ❌ `my_custom_skill` (no underscores)

**description**:
- ✅ `SPEC workflow specialist for requirements documentation`
- ✅ `Git fork synchronization workflow`
- ❌ (empty string)
- ❌ `This skill does many things...` (too vague)

**version**:
- ✅ `1.0.0`
- ✅ `2.3.1`
- ❌ `1.0` (missing patch version)
- ❌ `v1.0.0` (no "v" prefix)

**category**:
- ✅ `workflow`
- ✅ `lang`
- ❌ `custom` (not in allowed list)

**triggers.keywords**:
- ✅ `["SPEC", "requirement"]`
- ✅ `[]` (empty list)
- ❌ `"SPEC"` (must be list, not string)

---

## Trigger Configuration

### Understanding Triggers

Triggers determine WHEN Level 2 (skill body) should be loaded. They are evaluated at runtime based on:
1. **User prompt content** (keywords)
2. **Current workflow phase** (phases)
3. **Active agent** (agents)
4. **Programming language** (languages)

### Trigger Types

#### 1. Keyword Triggers

**How It Works**:
- User prompt is scanned for trigger keywords
- Case-insensitive matching
- Partial word matching (e.g., "specification" matches "SPEC")

**Configuration**:
```yaml
triggers:
  keywords: ["SPEC", "requirement", "EARS", "planning", "specification"]
```

**Trigger Examples**:
- ✅ "Create a SPEC document" → Matches "SPEC"
- ✅ "Write requirements for authentication" → Matches "requirement"
- ✅ "Help me with planning" → Matches "planning"
- ❌ "Build a backend API" → No match

**Best Practices**:
- Include 3-10 keywords
- Use both singular and plural forms
- Include common synonyms
- Avoid overly generic words (e.g., "code", "help")

#### 2. Phase Triggers

**How It Works**:
- MoAI-ADK has predefined workflow phases
- Skills load when phase matches trigger

**Configuration**:
```yaml
triggers:
  phases: ["plan", "run", "sync"]
```

**Available Phases**:
- `plan`: Requirements gathering, SPEC creation
- `run`: Implementation, coding, testing
- `sync`: Documentation, updates, sync operations

**Trigger Examples**:
- ✅ `/moai:1-plan "New feature"` → Phase = "plan"
- ✅ `/moai:2-run SPEC-001` → Phase = "run"
- ✅ `/moai:3-sync SPEC-001` → Phase = "sync"

**Best Practices**:
- Use phases for workflow-specific skills
- `plan` phase: SPEC, strategy, design skills
- `run` phase: TDD, implementation, testing skills
- `sync` phase: Documentation, update skills

#### 3. Agent Triggers

**How It Works**:
- Skills load when specific agents are active
- Enables agent-specific knowledge injection

**Configuration**:
```yaml
triggers:
  agents: ["manager-spec", "manager-strategy", "expert-backend"]
```

**Trigger Examples**:
- ✅ User invokes `manager-spec` → Load SPEC-related skills
- ✅ User invokes `expert-backend` → Load backend skills
- ❌ User invokes `expert-frontend` → No match

**Best Practices**:
- List agents that NEED this skill
- Don't list all agents (defeats purpose of triggers)
- Use for specialized, domain-specific skills

#### 4. Language Triggers

**How It Works**:
- Detects programming language from:
  - File extensions in conversation
  - User mentioning language name
  - Code blocks with language tags

**Configuration**:
```yaml
triggers:
  languages: ["python", "typescript", "javascript", "go"]
```

**Trigger Examples**:
- ✅ "Write Python code for..." → Matches "python"
- ✅ "TypeScript interface for..." → Matches "typescript"
- ✅ File opened: `app.py` → Matches "python"
- ❌ "Build a web app" → No language mentioned

**Best Practices**:
- Use for language-specific skills
- List primary languages, not all variants
- Consider including related languages (e.g., JS + TS)

### Trigger Strategy Decision Matrix

| Skill Type | Recommended Triggers | Example |
|------------|---------------------|---------|
| **Workflow** | Keywords + Phases | SPEC workflow: keywords=["SPEC"], phases=["plan"] |
| **Language** | Keywords + Languages | Python skill: keywords=["python"], languages=["python"] |
| **Platform** | Keywords only | Vercel skill: keywords=["vercel", "deployment"] |
| **Domain** | Keywords + Agents | Backend skill: keywords=["API"], agents=["expert-backend"] |
| **Foundation** | Empty (always load L2) | Core concepts: all triggers=[] |

### Trigger Testing

**Test 1: Keyword Trigger**
```
User: "Help me create a SPEC document"

Expected:
1. Load Level 1 metadata for all skills
2. Match keyword "SPEC"
3. Load Level 2 of moai-workflow-spec
```

**Test 2: Phase Trigger**
```
User: "/moai:1-plan New authentication system"

Expected:
1. Detect phase = "plan"
2. Load Level 2 of all skills with phases=["plan"]
```

**Test 3: Multiple Triggers**
```
User: "Write Python code for SPEC-001"

Expected:
1. Match keyword "Python" → Load Level 2 of moai-lang-python
2. Match keyword "SPEC" → Load Level 2 of moai-workflow-spec
```

---

## How Skills are Loaded in Claude Code

### Loading Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Prompt                          │
│  "Create a SPEC document for authentication in Python"  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              1. Agent Initialization                     │
│  - Load agent frontmatter (manager-spec.md)             │
│  - Extract skills: field                                │
│  - skills: moai-foundation-core, moai-workflow-spec     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         2. Load Level 1 for Agent Skills                │
│  - Parse YAML frontmatter only                          │
│  - Token cost: 2 × 100 = 200 tokens                     │
│  - Extract trigger conditions                           │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              3. Analyze User Prompt                      │
│  - Extract keywords: "SPEC", "authentication", "Python"  │
│  - Detect phase: None (not a /moai command)            │
│  - Detect language: "Python"                            │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              4. Match Triggers                          │
│  - moai-workflow-spec:                                  │
│    - keywords: ["SPEC"] ✅ MATCH                        │
│  - moai-lang-python:                                    │
│    - languages: ["python"] ✅ MATCH                     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         5. Load Level 2 for Matched Skills              │
│  - Load full markdown body (after YAML frontmatter)     │
│  - moai-workflow-spec: +5K tokens                       │
│  - moai-lang-python: +5K tokens                         │
│  - Total Level 2 cost: 10K tokens                       │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         6. Claude Processes Request                      │
│  - Uses loaded skills to understand task                │
│  - Can request Level 3 files if needed                  │
│  - Example: Read examples.md for code samples          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              7. Generate Response                        │
│  - Creates SPEC document using loaded knowledge         │
│  - Applies Python best practices                        │
│  - Uses EARS format from moai-workflow-spec             │
└─────────────────────────────────────────────────────────┘
```

### Loading Process Details

#### Phase 1: Agent Initialization

**What Happens**:
1. User invokes agent (explicitly or via Alfred routing)
2. Agent frontmatter is parsed
3. `skills:` field is extracted

**Code Example** (internal):
```python
agent_metadata = parse_agent_frontmatter("manager-spec.md")
skill_names = agent_metadata.get("skills", "").split(",")
# skill_names = ["moai-foundation-core", "moai-workflow-spec"]
```

**Token Cost**: Minimal (agent frontmatter ~200 tokens)

#### Phase 2: Load Level 1 Metadata

**What Happens**:
1. For each skill in `skills:` list
2. Parse YAML frontmatter of SKILL.md
3. Extract triggers, dependencies, metadata
4. Stop parsing before markdown body

**Code Example** (internal):
```python
from src.moai_adk.core.skill_loading_system import load_skill_metadata

for skill_name in skill_names:
    metadata = load_skill_metadata(skill_name)
    # metadata = {
    #     "name": "moai-workflow-spec",
    #     "triggers": {"keywords": ["SPEC", "requirement"]},
    #     "level1_tokens": 100,
    #     "level2_tokens": 5000
    # }
    skill_registry[skill_name] = metadata
```

**Token Cost**: ~100 tokens per skill

#### Phase 3: Analyze User Prompt

**What Happens**:
1. Extract keywords from user prompt
2. Detect workflow phase (if applicable)
3. Detect programming language
4. Build context dictionary

**Code Example** (internal):
```python
context = {
    "prompt": "Create a SPEC document for authentication in Python",
    "keywords": ["SPEC", "authentication", "Python"],
    "phase": None,
    "agent": "manager-spec",
    "language": "python"
}
```

**Token Cost**: None (metadata processing)

#### Phase 4: Match Triggers

**What Happens**:
1. For each skill in registry
2. Check if triggers match context
3. Build list of skills to load at Level 2

**Code Example** (internal):
```python
def should_load_level2(skill_metadata, context):
    triggers = skill_metadata.get("triggers", {})

    # Check keyword triggers
    keywords = triggers.get("keywords", [])
    if any(kw.lower() in context["prompt"].lower() for kw in keywords):
        return True

    # Check phase triggers
    phases = triggers.get("phases", [])
    if context.get("phase") in phases:
        return True

    # Check agent triggers
    agents = triggers.get("agents", [])
    if context.get("agent") in agents:
        return True

    # Check language triggers
    languages = triggers.get("languages", [])
    if context.get("language") in languages:
        return True

    return False

skills_to_load = [
    name for name, metadata in skill_registry.items()
    if should_load_level2(metadata, context)
]
# skills_to_load = ["moai-workflow-spec", "moai-lang-python"]
```

**Token Cost**: None (metadata processing)

#### Phase 5: Load Level 2 Body

**What Happens**:
1. For each matched skill
2. Read full SKILL.md file
3. Extract markdown content after YAML frontmatter
4. Add to Claude's context

**Code Example** (internal):
```python
from src.moai_adk.core.skill_loading_system import load_skill_body

level2_content = []
for skill_name in skills_to_load:
    body = load_skill_body(skill_name)
    level2_content.append(body)
    # body = "## Quick Reference\n\n**What is SPEC workflow?**\n\n..."

# Inject into Claude's system prompt
system_prompt += "\n\n".join(level2_content)
```

**Token Cost**: ~5K tokens per matched skill

#### Phase 6: Claude Processing

**What Happens**:
1. Claude receives full context (system + user prompt)
2. Uses loaded skill knowledge to understand task
3. Can request Level 3 files via Read tool

**Example**:
```
Claude: "I'll create a SPEC document. Let me check the examples."
[Claude internally calls Read tool]
Read("moai-workflow-spec/examples.md")
```

**Token Cost**: Level 3 tokens (on-demand)

#### Phase 7: Response Generation

**What Happens**:
1. Claude generates response using loaded knowledge
2. Applies patterns from skills
3. Returns to user

**Token Cost**: Output tokens (separate from input)

### Token Budget Tracking

**Example Session**:
```
Agent Initialization: 200 tokens
Level 1 (10 skills): 1,000 tokens
Level 2 (2 matched skills): 10,000 tokens
User Prompt: 500 tokens
System Prompt: 10,000 tokens
──────────────────────────────────
Total Input Tokens: 21,700 tokens
Available: 178,300 tokens (89% free)
```

**Without Progressive Disclosure**:
```
Agent Initialization: 200 tokens
All Skills (10 × 5K): 50,000 tokens
User Prompt: 500 tokens
System Prompt: 10,000 tokens
──────────────────────────────────
Total Input Tokens: 60,700 tokens
Available: 139,300 tokens (70% free)
```

**Savings**: 39,000 tokens (65% reduction)

---

## Modularization Patterns

### Why Modularize?

**Problem**: Single SKILL.md files become too large:
- Hard to maintain
- Difficult to navigate
- Exceeds Level 2 token budget

**Solution**: Split content into Level 3 modules:
- SKILL.md remains concise
- Modules load on-demand
- Easier to maintain and extend

### Module Structure

```
skill-name/
├── SKILL.md                  # Level 1 + 2 (~5K tokens)
├── examples.md               # Level 3 (working code samples)
├── reference.md              # Level 3 (external links, API docs)
└── modules/                  # Level 3+ (specialized topics)
    ├── README.md             # Module index
    ├── pattern-1.md          # Specific pattern/topic
    ├── pattern-2.md
    └── advanced-topics.md
```

### When to Create Modules

**Create a Module When**:
- Topic is self-contained (readable independently)
- Content exceeds 1,000 tokens
- Topic is advanced/optional
- Multiple related patterns exist

**Keep in SKILL.md When**:
- Content is foundational
- Topic is < 500 tokens
- Information is always needed
- Content provides overview

### Module Naming Conventions

**Good Module Names**:
- ✅ `react19-patterns.md` (specific, descriptive)
- ✅ `performance-optimization.md` (clear topic)
- ✅ `troubleshooting.md` (well-known category)

**Bad Module Names**:
- ❌ `module1.md` (not descriptive)
- ❌ `misc.md` (too vague)
- ❌ `everything-else.md` (catch-all)

### Module Template

```markdown
# [Module Topic Name]

**Part of**: [skill-name]
**Version**: 1.0.0
**Last Updated**: 2026-01-17

---

## Overview

Brief description of what this module covers (1-2 paragraphs).

---

## Prerequisites

What users should know before reading this module:
- Prerequisite 1
- Prerequisite 2

---

## Core Content

### Subtopic 1

Detailed explanation with examples.

### Subtopic 2

Detailed explanation with examples.

---

## Examples

Working code samples demonstrating concepts.

---

## Related Modules

- [pattern-1.md](./pattern-1.md): Description
- [pattern-2.md](./pattern-2.md): Description

---

## External Resources

- [Official Documentation](https://example.com)
- [Community Guide](https://example.com)
```

### Referencing Modules in SKILL.md

**In Level 2 Body**:
```markdown
## Advanced Topics

For detailed patterns, see:
- **modules/react19-patterns.md**: React 19 specific patterns
- **modules/performance-optimization.md**: Optimization techniques
- **modules/troubleshooting.md**: Common issues and solutions

Claude can access these files on-demand when needed.
```

**In Quick Reference**:
```markdown
**Quick Links:**
- Implementation: #implementation-guide
- Examples: examples.md (Level 3)
- Patterns: modules/react19-patterns.md
- Reference: reference.md (Level 3)
```

### Module Loading Behavior

**Automatic Loading** (Level 3):
- Claude decides when to load modules
- Based on task requirements
- Uses Read tool internally

**User-Requested Loading**:
```
User: "Show me React 19 patterns from the frontend skill"

Claude: [Internally calls Read tool]
Read("moai-domain-frontend/modules/react19-patterns.md")
```

**Agent-Triggered Loading**:
```markdown
<!-- In agent instructions -->
When implementing React components, reference:
- moai-domain-frontend/modules/react19-patterns.md
```

---

## Token Optimization Strategies

### Token Budget Management

**200K Token Budget Breakdown**:
```
System Prompt: ~10K tokens (5%)
Agent Definition: ~500 tokens (0.25%)
Level 1 Skills: ~5K tokens (2.5%)
Level 2 Skills: ~25K tokens (12.5%)
User Prompt: ~500 tokens (0.25%)
Conversation History: ~20K tokens (10%)
──────────────────────────────────
Used: ~61K tokens (30.5%)
Free: ~139K tokens (69.5%) ← Available for output
```

**Without Progressive Disclosure**:
```
System Prompt: ~10K tokens
Agent Definition: ~500 tokens
All Skills (48 × 5K): ~240K tokens ← Exceeds limit!
```

### Optimization Techniques

#### 1. Minimize Level 1 Metadata

**Strategy**: Keep YAML frontmatter concise

**Before** (verbose):
```yaml
---
name: "moai-workflow-spec"
description: "This skill provides comprehensive documentation and best practices for creating SPEC documents using the EARS format, including requirements gathering, stakeholder analysis, and validation processes."
# ... (150+ tokens)
```

**After** (optimized):
```yaml
---
name: "moai-workflow-spec"
description: "SPEC workflow specialist for requirements documentation"
# ... (100 tokens)
```

**Savings**: 50 tokens per skill × 48 skills = 2,400 tokens

#### 2. Use Precise Triggers

**Strategy**: Avoid overly broad triggers

**Before** (broad):
```yaml
triggers:
  keywords: ["code", "help", "create", "build", "make", "develop", "write"]
  # Matches almost every prompt!
```

**After** (precise):
```yaml
triggers:
  keywords: ["SPEC", "requirement", "EARS", "specification"]
  # Matches only relevant prompts
```

**Impact**: Reduces unnecessary Level 2 loading

#### 3. Modularize Large Skills

**Strategy**: Split >10K token skills into modules

**Before** (monolithic):
```markdown
<!-- SKILL.md: 15K tokens -->
## React Patterns (3K tokens)
## Next.js Patterns (3K tokens)
## State Management (3K tokens)
## Performance (3K tokens)
## Testing (3K tokens)
```

**After** (modularized):
```markdown
<!-- SKILL.md: 5K tokens -->
## Quick Reference
## Implementation Guide

<!-- modules/react19-patterns.md: 3K tokens -->
<!-- modules/nextjs16-patterns.md: 3K tokens -->
<!-- modules/state-management.md: 3K tokens -->
(etc.)
```

**Impact**: Level 2 load = 5K instead of 15K (10K savings)

#### 4. Use Skill Dependencies Wisely

**Strategy**: Declare dependencies to avoid duplication

**Before** (duplicated content):
```yaml
# skill-a/SKILL.md
---
name: "skill-a"
# ... includes foundational concepts (1K tokens)
---

# skill-b/SKILL.md
---
name: "skill-b"
# ... includes same foundational concepts (1K tokens)
---
```

**After** (shared foundation):
```yaml
# moai-foundation-core/SKILL.md
---
name: "moai-foundation-core"
# ... foundational concepts (1K tokens)
---

# skill-a/SKILL.md
---
name: "skill-a"
requires: ["moai-foundation-core"]
# ... specific content only
---

# skill-b/SKILL.md
---
name: "skill-b"
requires: ["moai-foundation-core"]
# ... specific content only
---
```

**Impact**: Foundation loaded once, shared by multiple skills

#### 5. Lazy Load Examples

**Strategy**: Move examples to Level 3

**Before** (in Level 2):
```markdown
## Examples

### Example 1: Basic Usage
(500 tokens)

### Example 2: Advanced Usage
(800 tokens)

### Example 3: Integration
(600 tokens)

Total: 1,900 tokens in Level 2
```

**After** (Level 3):
```markdown
## Examples

See **examples.md** for working code samples:
- Example 1: Basic usage
- Example 2: Advanced usage
- Example 3: Integration

Claude can access examples on-demand.

Total: 100 tokens in Level 2
```

**Impact**: 1,800 token savings per skill with examples

### Token Estimation

**Estimate Level 1 Tokens**:
1. Copy YAML frontmatter
2. Paste into token counter: https://platform.openai.com/tokenizer
3. Record count in `level1_tokens` field

**Estimate Level 2 Tokens**:
1. Copy full markdown body (after YAML)
2. Paste into token counter
3. Record count in `level2_tokens` field

**Update SKILL.md**:
```yaml
progressive_disclosure:
  enabled: true
  level1_tokens: ~110  # Actual measured count
  level2_tokens: ~4850 # Actual measured count
```

---

## Best Practices

### Content Guidelines

#### DO: Write for Skimmability

**Good**:
```markdown
## Quick Reference

**What is SPEC workflow?**

A structured approach to requirements documentation.

**Key Benefits:**
- Clear requirements
- Stakeholder alignment
- Testable criteria
```

**Bad**:
```markdown
## Introduction

The SPEC workflow is a comprehensive methodology that we have developed over many years of working with various stakeholders across multiple domains to create a structured, repeatable, and scalable approach to the complex challenge of capturing, documenting, and validating requirements in modern software development projects...

(wall of text continues)
```

#### DO: Use Progressive Detail

**Good**:
```markdown
## Implementation Guide

### Step 1: Analyze Requirements

Brief overview (1 paragraph).

For detailed analysis techniques, see modules/requirement-analysis.md

### Step 2: Write SPEC

Brief overview (1 paragraph).

For EARS format details, see modules/ears-format.md
```

**Bad**:
```markdown
## Implementation Guide

### Step 1: Analyze Requirements

(5 pages of detailed content in Level 2)
```

#### DO: Provide Clear Examples

**Good**:
```markdown
## Example: Basic SPEC Document

```markdown
# SPEC-001: User Authentication

WHEN a user enters valid credentials
THE system SHALL authenticate the user
AND grant access to protected resources
```

For complete examples, see examples.md
```

**Bad**:
```markdown
## Examples

See examples.md for examples.
```

#### DO: Cross-Reference Related Skills

**Good**:
```markdown
## Works Well With

**Related Skills:**
- moai-foundation-core: Provides TRUST 5 validation framework
- moai-workflow-ddd: Use DDD cycle after SPEC creation

**Agents:**
- manager-spec: Primary agent for SPEC creation
- manager-strategy: Use for system design after SPEC
```

**Bad**:
```markdown
## Related

Other skills exist.
```

### Maintenance Guidelines

#### Version Management

**When to Increment**:
- **Major** (1.x.x → 2.x.x): Breaking changes, incompatible API
- **Minor** (x.1.x → x.2.x): New features, backward compatible
- **Patch** (x.x.1 → x.x.2): Bug fixes, typos, clarifications

**Update Process**:
1. Make changes to SKILL.md
2. Increment version in frontmatter
3. Update `updated` date
4. Document changes in skill's CHANGELOG (if exists)
5. Test trigger behavior

#### Documentation Decay Prevention

**Schedule**:
- **Monthly**: Review token estimates (recount if >10% drift)
- **Quarterly**: Review trigger keywords (add/remove based on usage)
- **Semi-annually**: Review modules (consolidate or split as needed)

**Checklist**:
- [ ] Examples still work with current tools
- [ ] External links are not broken
- [ ] Trigger keywords match user language
- [ ] Token counts are accurate
- [ ] Dependencies are still valid

#### Deprecation Process

**Step 1**: Mark as deprecated
```yaml
status: "deprecated"
```

**Step 2**: Add deprecation notice
```markdown
> **⚠️ DEPRECATED**: This skill is no longer maintained.
> Use [replacement-skill] instead.
>
> **Migration Guide**: See [migration.md](./migration.md)
```

**Step 3**: Keep for 6 months, then archive

### Testing Guidelines

#### Manual Testing

**Test 1: Trigger Matching**
```
1. Open Claude Code
2. Type: "[trigger keyword] test"
3. Verify Level 2 loads
4. Check /context to confirm
```

**Test 2: Token Budget**
```
1. Load skill at Level 1
2. Use /context to check token usage
3. Compare with level1_tokens estimate
4. If drift >10%, recount and update
```

**Test 3: Module Access**
```
1. Ask Claude: "Show me [module-name] from [skill-name]"
2. Verify Claude uses Read tool
3. Confirm module content is shown
```

#### Automated Testing

**Token Count Validation** (Python):
```python
import tiktoken

def count_tokens(text: str) -> int:
    """Count tokens using tiktoken (GPT-4 encoding)"""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def validate_skill_tokens(skill_path: str):
    """Validate token estimates in SKILL.md frontmatter"""
    with open(skill_path, "r") as f:
        content = f.read()

    # Split frontmatter and body
    parts = content.split("---")
    frontmatter = parts[1]
    body = "---".join(parts[2:])

    # Count tokens
    l1_actual = count_tokens(frontmatter)
    l2_actual = count_tokens(body)

    # Extract estimates from frontmatter
    # (parse level1_tokens and level2_tokens)

    # Compare
    if abs(l1_actual - l1_estimate) > l1_estimate * 0.1:
        print(f"⚠️ Level 1 drift: {l1_actual} vs {l1_estimate}")

    if abs(l2_actual - l2_estimate) > l2_estimate * 0.1:
        print(f"⚠️ Level 2 drift: {l2_actual} vs {l2_estimate}")

# Run validation
validate_skill_tokens(".claude/skills/moai-workflow-spec/SKILL.md")
```

### Common Pitfalls

#### Pitfall 1: Overly Broad Triggers

**Problem**: Skill loads for almost every prompt

**Example**:
```yaml
triggers:
  keywords: ["code", "help", "create"]
```

**Solution**: Use specific, domain-related keywords
```yaml
triggers:
  keywords: ["SPEC", "requirement", "EARS", "specification"]
```

#### Pitfall 2: Duplicate Content

**Problem**: Same content exists in multiple skills

**Example**:
- `skill-a/SKILL.md` includes Git basics (1K tokens)
- `skill-b/SKILL.md` includes Git basics (1K tokens)
- Total waste: 1K tokens

**Solution**: Extract to foundation skill
```yaml
# moai-foundation-git/SKILL.md
---
name: "moai-foundation-git"
# Git basics (1K tokens)
---

# skill-a/SKILL.md
---
name: "skill-a"
requires: ["moai-foundation-git"]
---

# skill-b/SKILL.md
---
name: "skill-b"
requires: ["moai-foundation-git"]
---
```

#### Pitfall 3: Insufficient Quick Reference

**Problem**: Users can't quickly assess relevance

**Example**:
```markdown
## Quick Reference

This skill covers various topics related to web development.
```

**Solution**: Provide concrete benefits and use cases
```markdown
## Quick Reference

**What is [skill-name]?**

A specialist for React 19 and Next.js 16 frontend development.

**Key Benefits:**
- Server Components patterns
- App Router optimization
- Modern React hooks

**When to Use:**
- Building React 19 apps
- Optimizing Next.js performance
- Implementing SSR/SSG
```

---

## Examples and Templates

### Example 1: Simple Workflow Skill

**File**: `my-workflow-skill/SKILL.md`

```markdown
---
name: "my-workflow-skill"
description: "Custom workflow for team code reviews"
version: "1.0.0"
category: "workflow"
modularized: false
user-invocable: true

progressive_disclosure:
  enabled: true
  level1_tokens: ~110
  level2_tokens: ~3500

triggers:
  keywords: ["code review", "review workflow", "PR review"]
  phases: ["sync"]
  agents: ["manager-quality"]
  languages: []

requires: []
optional_requires: ["moai-foundation-quality"]

allowed-tools:
  - Read
  - Bash
  - AskUserQuestion

tags: ["workflow", "quality", "review"]
updated: 2026-01-17
status: "active"
---

## Quick Reference

**What is my-workflow-skill?**

A structured workflow for conducting thorough code reviews with automated checks and manual inspection points.

**Key Benefits:**
- Consistent review process
- Automated quality gates
- Actionable feedback format

**When to Use:**
- Before merging pull requests
- During code review sessions
- When establishing review standards

---

## Implementation Guide

### Step 1: Automated Checks

Run linters and tests:
```bash
ruff check src/
pytest tests/
```

### Step 2: Manual Review

Review checklist:
- [ ] Code follows team standards
- [ ] Tests cover edge cases
- [ ] Documentation is updated

### Step 3: Provide Feedback

Use constructive format:
- **Observation**: What you see
- **Impact**: Why it matters
- **Suggestion**: How to improve

---

## Works Well With

**Related Skills:**
- moai-foundation-quality: TRUST 5 validation

**Agents:**
- manager-quality: Primary quality orchestrator

**Commands:**
- /moai:3-sync: Documentation sync workflow
```

### Example 2: Language Skill with Modules

**Directory Structure**:
```
my-lang-skill/
├── SKILL.md
├── examples.md
├── reference.md
└── modules/
    ├── README.md
    ├── advanced-patterns.md
    └── performance.md
```

**File**: `my-lang-skill/SKILL.md`

```markdown
---
name: "my-lang-skill"
description: "Rust 1.92+ development specialist"
version: "1.0.0"
category: "lang"
modularized: true
user-invocable: true

progressive_disclosure:
  enabled: true
  level1_tokens: ~120
  level2_tokens: ~4500

triggers:
  keywords: ["rust", "cargo", "ownership", "borrowing"]
  phases: ["run"]
  agents: ["expert-backend", "expert-performance"]
  languages: ["rust"]

requires: []
optional_requires: ["moai-foundation-core"]

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash

tags: ["rust", "systems", "performance"]
updated: 2026-01-17
status: "active"
---

## Quick Reference

**What is my-lang-skill?**

Rust 1.92+ development specialist covering ownership, borrowing, async patterns, and performance optimization.

**Key Benefits:**
- Memory safety without GC
- Zero-cost abstractions
- Fearless concurrency

**When to Use:**
- Building systems software
- High-performance applications
- Safe concurrent programs

**Quick Links:**
- Implementation: #implementation-guide
- Patterns: modules/advanced-patterns.md
- Performance: modules/performance.md
- Examples: examples.md

---

## Implementation Guide

### Core Concepts

**Ownership Rules**:
1. Each value has a single owner
2. When owner goes out of scope, value is dropped
3. Values can be borrowed (immutably or mutably)

**Example**:
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 is moved to s2
    // println!("{}", s1); // Error: s1 is no longer valid
    println!("{}", s2); // OK
}
```

### Step-by-Step Process

**Step 1: Project Setup**
```bash
cargo new my_project
cd my_project
```

**Step 2: Define Modules**

See modules/advanced-patterns.md for module organization patterns.

**Step 3: Implement Features**

See examples.md for working code samples.

---

## Advanced Topics

### Performance Optimization

For detailed performance techniques, see:
- **modules/performance.md**: Profiling, benchmarking, optimization

### Async Patterns

For async/await patterns, see:
- **modules/advanced-patterns.md**: Tokio, async-std, futures

---

## Works Well With

**Related Skills:**
- moai-domain-backend: API development patterns
- moai-foundation-core: TRUST 5 validation

**Agents:**
- expert-backend: Backend implementation
- expert-performance: Performance optimization
```

**File**: `my-lang-skill/modules/advanced-patterns.md`

```markdown
# Rust Advanced Patterns

**Part of**: my-lang-skill
**Version**: 1.0.0
**Last Updated**: 2026-01-17

---

## Overview

This module covers advanced Rust patterns including:
- Smart pointers (Box, Rc, Arc, RefCell)
- Trait objects and dynamic dispatch
- Async/await patterns with Tokio
- Macros and metaprogramming

---

## Smart Pointers

### Box<T>

Heap allocation for types with unknown size:

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {}", b);
}
```

### Rc<T> and Arc<T>

Reference counting for shared ownership:

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(5);
    let b = Rc::clone(&a);
    println!("count = {}", Rc::strong_count(&a)); // 2
}
```

---

## Async Patterns

### Tokio Runtime

```rust
#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("Result: {}", result);
}

async fn fetch_data() -> String {
    // Async operation
    "data".to_string()
}
```

---

## Related Modules

- [performance.md](./performance.md): Performance optimization techniques
- [README.md](./README.md): Module index

---

## External Resources

- [Rust Book](https://doc.rust-lang.org/book/)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
```

### Example 3: Platform Skill

**File**: `my-platform-skill/SKILL.md`

```markdown
---
name: "my-platform-skill"
description: "AWS Lambda serverless specialist"
version: "1.0.0"
category: "platform"
modularized: true
user-invocable: true

progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~4200

triggers:
  keywords: ["lambda", "serverless", "AWS", "function"]
  phases: ["run"]
  agents: ["expert-backend", "expert-devops"]
  languages: ["python", "typescript", "javascript"]

requires: []
optional_requires: ["moai-lang-python", "moai-lang-typescript"]

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash

tags: ["aws", "lambda", "serverless"]
updated: 2026-01-17
status: "active"
---

## Quick Reference

**What is my-platform-skill?**

AWS Lambda serverless specialist covering function development, event-driven architecture, and deployment automation.

**Key Benefits:**
- Zero server management
- Automatic scaling
- Pay-per-use pricing

**When to Use:**
- Building event-driven systems
- Serverless APIs
- Background processing

**Quick Links:**
- Implementation: #implementation-guide
- Examples: examples.md
- Reference: reference.md

---

## Implementation Guide

### Step 1: Create Lambda Function

**Python Example**:
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
```

**TypeScript Example**:
```typescript
export const handler = async (event: any) => {
    return {
        statusCode: 200,
        body: 'Hello from Lambda!'
    };
};
```

### Step 2: Deploy Function

Using AWS SAM:
```bash
sam build
sam deploy --guided
```

### Step 3: Test Function

```bash
aws lambda invoke \
  --function-name my-function \
  --payload '{}' \
  response.json
```

---

## Advanced Topics

### Cold Start Optimization

Techniques to reduce cold start time:
- Minimize package size
- Use provisioned concurrency
- Optimize initialization code

For detailed strategies, see modules/performance.md

### Event Sources

Lambda supports multiple event sources:
- API Gateway (REST/HTTP)
- S3 events
- DynamoDB Streams
- SQS/SNS messages

For integration patterns, see modules/event-sources.md

---

## Works Well With

**Related Skills:**
- moai-lang-python: Python Lambda functions
- moai-lang-typescript: TypeScript Lambda functions

**Agents:**
- expert-backend: API implementation
- expert-devops: Deployment automation
```

---

## Troubleshooting

### Issue 1: Level 2 Not Loading

**Symptom**: Skill body doesn't load despite keyword in prompt

**Diagnosis**:
1. Check trigger configuration in YAML frontmatter
2. Verify keyword spelling and case
3. Confirm skill is listed in agent's `skills:` field

**Solution**:
```yaml
# Before
triggers:
  keywords: ["SPEc"]  # Typo!

# After
triggers:
  keywords: ["SPEC", "spec"]  # Both cases
```

### Issue 2: Token Count Mismatch

**Symptom**: Estimated tokens don't match actual usage

**Diagnosis**:
1. Use token counter: https://platform.openai.com/tokenizer
2. Paste YAML frontmatter (Level 1) or full body (Level 2)
3. Compare with estimates in frontmatter

**Solution**:
```yaml
# Update estimates
progressive_disclosure:
  enabled: true
  level1_tokens: ~110  # Update to actual
  level2_tokens: ~4850 # Update to actual
```

### Issue 3: Module Not Found

**Symptom**: Claude can't access Level 3 module

**Diagnosis**:
1. Verify file exists: `ls .claude/skills/skill-name/modules/`
2. Check file path in SKILL.md
3. Confirm Claude has Read tool access

**Solution**:
```markdown
<!-- Before -->
For details, see modules/patterns.md

<!-- After -->
For details, see:
- **modules/patterns.md**: Design patterns (Claude can access via Read tool)
```

### Issue 4: Skill Not Appearing

**Symptom**: Skill doesn't load at all (Level 1 or 2)

**Diagnosis**:
1. Check skill directory name matches `name:` field
2. Verify SKILL.md exists in directory
3. Confirm agent lists skill in `skills:` field

**Solution**:
```yaml
# Agent frontmatter
---
name: manager-spec
skills: moai-foundation-core, moai-workflow-spec, my-custom-skill
---
```

### Issue 5: Circular Dependencies

**Symptom**: Infinite loop or stack overflow

**Diagnosis**:
1. Check `requires:` fields in all skills
2. Look for cycles: A requires B, B requires A

**Solution**:
```yaml
# Before (circular)
# skill-a/SKILL.md
requires: ["skill-b"]

# skill-b/SKILL.md
requires: ["skill-a"]

# After (remove cycle)
# skill-a/SKILL.md
requires: []

# skill-b/SKILL.md
requires: ["skill-a"]
```

---

## Advanced Topics

### Custom Skill Categories

**Creating New Category**:

1. Define category in your project's skill system
2. Use consistent naming across skills
3. Document category purpose

**Example**:
```yaml
category: "custom-domain"  # Your custom category
```

**Standard Categories**:
- `foundation`: Core concepts (TRUST 5, SPEC, etc.)
- `lang`: Programming languages
- `platform`: Cloud platforms (AWS, Vercel, etc.)
- `library`: Libraries (shadcn, Nextra, etc.)
- `workflow`: Development workflows
- `domain`: Domain skills (backend, frontend, etc.)

### Dynamic Trigger Adjustment

**Use Case**: Adjust triggers based on usage patterns

**Implementation**:
1. Monitor which keywords trigger skill loading
2. Analyze user prompts that should trigger but don't
3. Update `keywords:` list accordingly

**Example**:
```yaml
# Initial triggers
triggers:
  keywords: ["SPEC", "requirement"]

# After analysis, users also say:
# - "specification"
# - "requirements doc"
# - "req doc"

# Updated triggers
triggers:
  keywords: ["SPEC", "requirement", "specification", "requirements doc", "req doc"]
```

### Multi-Language Skills

**Use Case**: Skill applies to multiple languages

**Implementation**:
```yaml
triggers:
  languages: ["python", "typescript", "javascript", "go"]
```

**Organization**:
```
skill-name/
├── SKILL.md               # Language-agnostic content
├── modules/
│   ├── python-specific.md
│   ├── typescript-specific.md
│   └── go-specific.md
```

**In SKILL.md**:
```markdown
## Language-Specific Patterns

- **Python**: See modules/python-specific.md
- **TypeScript**: See modules/typescript-specific.md
- **Go**: See modules/go-specific.md

Claude will load the appropriate module based on detected language.
```

### Skill Composition

**Use Case**: Combine multiple skills for complex tasks

**Pattern 1: Foundation + Specialized**:
```yaml
# specialized-skill/SKILL.md
---
name: "specialized-skill"
requires: ["moai-foundation-core"]  # Foundation
optional_requires: ["moai-lang-python"]  # Language-specific
---
```

**Pattern 2: Workflow + Domain**:
```yaml
# workflow-skill/SKILL.md
---
name: "workflow-skill"
requires: ["moai-foundation-core"]
optional_requires: [
  "moai-domain-backend",  # Domain expertise
  "moai-domain-frontend"
]
---
```

**Pattern 3: Platform + Language**:
```yaml
# platform-skill/SKILL.md
---
name: "aws-lambda-skill"
requires: []
optional_requires: [
  "moai-lang-python",     # Python Lambda
  "moai-lang-typescript", # TypeScript Lambda
  "moai-lang-go"          # Go Lambda
]
---
```

### Conditional Module Loading

**Use Case**: Load modules based on context

**In SKILL.md**:
```markdown
## Advanced Topics

Claude will load appropriate modules based on your needs:

**Performance Optimization**:
- For profiling: modules/profiling.md
- For benchmarking: modules/benchmarking.md
- For caching: modules/caching.md

**Security**:
- For authentication: modules/auth.md
- For authorization: modules/authz.md
- For encryption: modules/crypto.md

Ask Claude to access specific modules as needed.
```

### Skill Testing Framework

**Test Suite** (Python):
```python
import pytest
from pathlib import Path
import yaml

def load_skill_metadata(skill_path: Path) -> dict:
    """Load YAML frontmatter from SKILL.md"""
    content = skill_path.read_text()
    parts = content.split("---")
    frontmatter = parts[1]
    return yaml.safe_load(frontmatter)

def test_skill_has_required_fields():
    """Verify all skills have required YAML fields"""
    skills_dir = Path(".claude/skills")
    required_fields = ["name", "description", "version", "category"]

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        metadata = load_skill_metadata(skill_file)

        for field in required_fields:
            assert field in metadata, \
                f"{skill_dir.name}/SKILL.md missing required field: {field}"

def test_skill_triggers_are_valid():
    """Verify trigger configuration is valid"""
    skills_dir = Path(".claude/skills")

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        metadata = load_skill_metadata(skill_file)
        triggers = metadata.get("triggers", {})

        # Check trigger types
        assert isinstance(triggers.get("keywords", []), list)
        assert isinstance(triggers.get("phases", []), list)
        assert isinstance(triggers.get("agents", []), list)
        assert isinstance(triggers.get("languages", []), list)

        # Check phases are valid
        valid_phases = ["plan", "run", "sync"]
        for phase in triggers.get("phases", []):
            assert phase in valid_phases, \
                f"{skill_dir.name} has invalid phase: {phase}"

def test_skill_modules_exist():
    """Verify referenced modules exist"""
    skills_dir = Path(".claude/skills")

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        metadata = load_skill_metadata(skill_file)

        # If modularized=true, check modules directory exists
        if metadata.get("modularized", False):
            modules_dir = skill_dir / "modules"
            assert modules_dir.exists(), \
                f"{skill_dir.name} marked as modularized but modules/ missing"

# Run tests
pytest.main([__file__, "-v"])
```

---

## Appendix

### A. SKILL.md Checklist

Before publishing a skill:

**Metadata**:
- [ ] `name` matches directory name
- [ ] `description` is clear and concise (<100 chars)
- [ ] `version` follows semantic versioning
- [ ] `category` is one of standard categories
- [ ] `modularized` accurately reflects structure
- [ ] `user-invocable` is set correctly

**Progressive Disclosure**:
- [ ] `enabled: true` for token optimization
- [ ] `level1_tokens` matches actual count (use tokenizer)
- [ ] `level2_tokens` matches actual count (use tokenizer)

**Triggers**:
- [ ] `keywords` are specific and relevant
- [ ] `phases` match MoAI workflow phases (if applicable)
- [ ] `agents` list agents that need this skill
- [ ] `languages` list relevant programming languages

**Dependencies**:
- [ ] `requires` lists hard dependencies
- [ ] `optional_requires` lists optional enhancements
- [ ] No circular dependencies

**Tools**:
- [ ] `allowed-tools` lists all tools skill may use
- [ ] Tools are appropriate for skill domain

**Content**:
- [ ] Quick Reference provides immediate value
- [ ] Implementation Guide has clear steps
- [ ] Advanced Topics reference Level 3 modules
- [ ] Works Well With section lists related skills/agents

**Modules** (if `modularized: true`):
- [ ] `examples.md` exists with working code samples
- [ ] `reference.md` exists with external links
- [ ] `modules/` directory exists
- [ ] `modules/README.md` provides module index
- [ ] All referenced modules exist

**Testing**:
- [ ] Skill loads at Level 1 during agent init
- [ ] Skill loads at Level 2 when triggered
- [ ] Token usage matches estimates (±10%)
- [ ] Modules are accessible via Read tool

### B. Token Counter Tools

**Online Tools**:
- OpenAI Tokenizer: https://platform.openai.com/tokenizer
- Anthropic Console: https://console.anthropic.com/

**Python Libraries**:
```bash
pip install tiktoken
```

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Count Level 1 tokens
with open(".claude/skills/my-skill/SKILL.md") as f:
    content = f.read()
    parts = content.split("---")
    frontmatter = parts[1]
    print(f"Level 1 tokens: {count_tokens(frontmatter)}")

    body = "---".join(parts[2:])
    print(f"Level 2 tokens: {count_tokens(body)}")
```

**CLI Tools**:
```bash
# Install
pip install tiktoken-cli

# Count tokens
tiktoken count .claude/skills/my-skill/SKILL.md
```

### C. YAML Syntax Reference

**Scalars**:
```yaml
string: "value"
number: 42
boolean: true
null_value: null
```

**Lists**:
```yaml
# Flow style
keywords: ["keyword1", "keyword2", "keyword3"]

# Block style
keywords:
  - keyword1
  - keyword2
  - keyword3
```

**Comments**:
```yaml
# This is a comment
name: "skill-name"  # Inline comment
```

**Multiline Strings**:
```yaml
# Literal block (preserves newlines)
description: |
  This is a multi-line
  description that preserves
  line breaks.

# Folded block (folds newlines to spaces)
description: >
  This is a multi-line
  description that folds
  into a single line.
```

**Anchors and Aliases**:
```yaml
# Define anchor
common_tools: &tools
  - Read
  - Write
  - Edit

# Reference anchor
allowed-tools: *tools
```

### D. Related Documentation

**MoAI-ADK**:
- CLAUDE.md: Alfred execution directives
- CLAUDE.local.md: Local development guide
- SKILL_TEMPLATE.md: Blank skill template

**Claude Code**:
- Official Docs: https://docs.anthropic.com/claude-code
- Skills Guide: moai-foundation-claude/SKILL.md
- Sub-Agents Guide: moai-foundation-claude/reference/sub-agents/

**Progressive Disclosure**:
- CLAUDE.md § 12: Progressive Disclosure System
- moai-foundation-core/modules/progressive-disclosure.md

### E. Glossary

**Agent**: A specialized Claude Code sub-agent with specific expertise

**Level 1**: YAML frontmatter (metadata) loaded during initialization (~100 tokens)

**Level 2**: Markdown body loaded when triggers match (~5K tokens)

**Level 3**: Bundled files (examples, modules, reference) loaded on-demand (unlimited)

**Module**: A self-contained markdown file in the `modules/` directory

**Progressive Disclosure**: Token optimization pattern that loads content in stages

**Skill**: A structured markdown document (SKILL.md) containing specialized knowledge

**Trigger**: Condition that causes Level 2 to load (keywords, phases, agents, languages)

**User-Invocable**: Skill that users can call directly (not just agents)

---

## Conclusion

You now have a comprehensive understanding of:
- ✅ SKILL.md structure and purpose
- ✅ Progressive Disclosure 3-level system
- ✅ YAML frontmatter configuration
- ✅ Trigger-based loading mechanics
- ✅ Modularization patterns
- ✅ Token optimization strategies
- ✅ Best practices and testing

### Next Steps

1. **Create Your First Skill**:
   ```bash
   mkdir -p .claude/skills/my-first-skill
   cp .claude/skills/SKILL_TEMPLATE.md .claude/skills/my-first-skill/SKILL.md
   # Edit SKILL.md with your content
   ```

2. **Test Your Skill**:
   - Open Claude Code
   - Type a trigger keyword
   - Verify Level 2 loads
   - Check /context for token usage

3. **Iterate and Improve**:
   - Monitor which keywords trigger loading
   - Adjust triggers based on usage
   - Split large skills into modules
   - Update token estimates

4. **Share Your Skill**:
   - Publish to team repository
   - Document in project README
   - Submit to MoAI-ADK (if applicable)

### Support

- **Issues**: https://github.com/modu-ai/moai-adk/issues
- **Discussions**: https://github.com/modu-ai/moai-adk/discussions
- **Documentation**: moai-foundation-claude/SKILL.md

---

**Happy Skill Authoring! 🚀**
