# SKILL.md 작성 가이드

**Progressive Disclosure를 활용한 Claude Code 스킬 생성, 구조화 및 최적화를 위한 종합 가이드**

버전: 1.0.0
최종 업데이트: 2026-01-17
작성자: MoAI-ADK Team

---

## 목차

1. [소개](#소개)
2. [SKILL.md란 무엇인가?](#skillmd란-무엇인가)
3. [Progressive Disclosure 시스템](#progressive-disclosure-시스템)
4. [SKILL.md 구조](#skillmd-구조)
5. [첫 번째 SKILL.md 작성하기](#첫-번째-skillmd-작성하기)
6. [YAML Frontmatter 레퍼런스](#yaml-frontmatter-레퍼런스)
7. [트리거 설정](#트리거-설정)
8. [Claude Code에서 스킬이 로드되는 방법](#claude-code에서-스킬이-로드되는-방법)
9. [모듈화 패턴](#모듈화-패턴)
10. [토큰 최적화 전략](#토큰-최적화-전략)
11. [모범 사례](#모범-사례)
12. [예제 및 템플릿](#예제-및-템플릿)
13. [문제 해결](#문제-해결)
14. [고급 주제](#고급-주제)

---

## 소개

### 이 가이드의 목적

이 가이드는 **Progressive Disclosure** 시스템을 사용하여 Claude Code용 **스킬(Skills)**을 만드는 방법을 가르칩니다. 스킬은 Claude가 필요에 따라 로드할 수 있는 재사용 가능한 지식 모듈로, 전체 기능을 유지하면서 토큰 소비를 극적으로 줄입니다.

### 누가 이 가이드를 읽어야 하나요?

- Claude Code 커스텀 스킬을 만드는 개발자
- AI 에이전트를 위한 도메인별 지식을 구축하는 팀
- MoAI-ADK 또는 유사한 프레임워크의 기여자
- Claude의 컨텍스트 윈도우 사용을 최적화하려는 모든 사람

### 주요 이점

- **67% 이상의 토큰 절감** - 3단계 로딩을 통해
- **온디맨드 지식** - 필요한 것만 로드
- **모듈식 아키텍처** - 유지보수 및 확장이 용이
- **하위 호환성** - 기존 에이전트와 호환

---

## SKILL.md란 무엇인가?

### 정의

**SKILL.md** 파일은 특정 도메인, 기술 또는 워크플로우에 대한 전문 지식, 패턴 및 모범 사례를 포함하는 구조화된 마크다운 문서입니다. 토큰 사용을 최적화하기 위해 **Progressive Disclosure** 패턴을 따릅니다.

### 핵심 특성

1. **계층적 구조**: 3단계 로딩 (메타데이터 → 본문 → 번들 파일)
2. **트리거 기반 로딩**: 키워드, 단계, 에이전트 또는 언어에 따라 로드
3. **모듈식 디자인**: 확장 문서를 위한 외부 파일 참조 가능
4. **사용자 호출 가능**: 사용자가 직접 호출하거나 에이전트가 로드 가능

### 파일 위치

```
.claude/skills/
├── skill-name/
│   ├── SKILL.md           # 메인 스킬 파일 (Level 1 + 2)
│   ├── examples.md        # Level 3+ (온디맨드)
│   ├── reference.md       # Level 3+ (온디맨드)
│   └── modules/           # Level 3+ (온디맨드)
│       ├── pattern-1.md
│       ├── pattern-2.md
│       └── ...
```

### SKILL.md 구조

```markdown
---
# Level 1: 메타데이터 (항상 로드됨)
name: "skill-name"
description: "간단한 설명"
triggers:
  keywords: ["keyword1", "keyword2"]
---

# Level 2: 스킬 본문 (조건부 로드)
## Quick Reference
## Implementation Guide
## Advanced Topics

# Level 3: 번들 파일 (온디맨드)
## Module References
## Examples
## Reference
```

---

## Progressive Disclosure 시스템

### 개요

**Progressive Disclosure**는 관련성에 따라 콘텐츠를 단계별로 로드하는 토큰 최적화 패턴입니다. 모든 문서를 미리 로드하는 대신, Claude는 필요할 때만 점점 더 자세한 정보를 받습니다.

### 왜 Progressive Disclosure를 사용하나요?

**문제**: 기존 방식은 전체 문서 세트를 로드하여 막대한 토큰을 소비합니다:
- 48개 스킬 × ~5K 토큰 = **240K 토큰** (Claude의 200K 한계 초과)

**해결책**: Progressive Disclosure로 이를 줄입니다:
- 48개 스킬 × ~100 토큰 = **4.8K 토큰** (98% 감소)

전체 문서는 트리거가 사용자 의도와 일치할 때만 로드됩니다.

### 3단계 시스템

#### Level 1: 메타데이터만 (스킬당 ~100 토큰)

**로드되는 내용:**
- YAML frontmatter만
- 스킬 이름, 설명, 버전
- 트리거 조건
- 종속성
- 허용된 도구

**로드 시점:**
- 에이전트 초기화 중
- 에이전트의 `skills:` 필드에 나열된 스킬에 대해 항상 로드

**토큰 비용:**
- 스킬당 ~100 토큰
- 컨텍스트 윈도우에 최소한의 영향

**예제:**
```yaml
---
name: "moai-workflow-spec"
description: "SPEC 워크플로우 전문가"
version: "1.0.0"
triggers:
  keywords: ["SPEC", "requirement", "EARS"]
---
```

#### Level 2: 스킬 본문 (스킬당 ~5K 토큰)

**로드되는 내용:**
- YAML frontmatter 이후의 전체 마크다운 본문
- Quick Reference 섹션
- Implementation Guide
- Advanced Topics
- 사용 예제

**로드 시점:**
- 트리거 조건이 사용자 프롬프트와 일치할 때
- 에이전트가 명시적으로 스킬을 요청할 때
- 단계가 트리거 설정과 일치할 때

**토큰 비용:**
- 스킬당 ~5K 토큰
- 관련 스킬에 대해서만 로드

**예제:**
```markdown
## Quick Reference

**SPEC 워크플로우란 무엇인가?**

요구사항 문서화를 위한 구조화된 접근 방식...

## Implementation Guide

### Step 1: 요구사항 분석
...
```

#### Level 3+: 번들 파일 (무제한)

**로드되는 내용:**
- 스킬 디렉토리의 외부 마크다운 파일
- 모듈, 예제, 참조 문서
- 코드 샘플, 다이어그램, 상세 가이드

**로드 시점:**
- Claude가 필요할 때 온디맨드로
- Claude가 작업 요구사항에 따라 결정
- 사용자가 특정 모듈 요청 가능

**토큰 비용:**
- 무제한 (필요에 따라 로드)
- 초기 예산에 포함되지 않음

**예제:**
```
skill-name/
├── SKILL.md
├── examples.md       # Level 3
├── reference.md      # Level 3
└── modules/          # Level 3+
    ├── advanced-patterns.md
    └── troubleshooting.md
```

### 토큰 예산 비교

| 접근 방식 | 로드된 스킬 | 토큰 비용 | 남은 컨텍스트 |
|----------|---------------|------------|-------------------|
| **Progressive Disclosure 없음** | 48개 스킬 | ~240K 토큰 | ❌ 한계 초과 |
| **Progressive Disclosure (Level 1)** | 48개 스킬 | ~4.8K 토큰 | ✅ 195K 여유 |
| **Progressive Disclosure (L1+L2)** | 5개 트리거된 스킬 | ~25K 토큰 | ✅ 175K 여유 |

### 로딩 플로우 다이어그램

```
사용자 프롬프트: "인증을 위한 SPEC 문서 작성"
    ↓
┌───────────────────────────────────────────────┐
│ 1. 에이전트 초기화                            │
│    에이전트의 모든 스킬에 대해 Level 1 로드   │
│    토큰 비용: 48 × 100 = 4,800 토큰           │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ 2. 트리거 매칭                                │
│    키워드 확인: "SPEC", "인증"                │
│    일치: moai-workflow-spec                   │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ 3. 일치된 스킬에 대해 Level 2 로드            │
│    moai-workflow-spec의 전체 본문 로드        │
│    토큰 비용: +5,000 토큰                     │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ 4. Claude가 로드된 지식 사용                  │
│    로드된 컨텍스트를 사용하여 SPEC 문서 생성  │
│    필요시 Level 3 모듈 요청 가능              │
└───────────────────────────────────────────────┘
```

---

## SKILL.md 구조

### 완전한 템플릿

```markdown
---
# ═══════════════════════════════════════════════
# Level 1: 핵심 메타데이터 (항상 로드 ~100 토큰)
# ═══════════════════════════════════════════════
name: "skill-name"
description: "이 스킬이 하는 일에 대한 한 줄 설명"
version: "1.0.0"
category: "workflow"  # foundation, lang, platform, library, workflow, domain
modularized: true
user-invocable: true

# Progressive Disclosure 설정
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~5000

# Level 2 로딩을 위한 트리거 조건
triggers:
  keywords: ["keyword1", "keyword2", "keyword3"]
  phases: ["plan", "run", "sync"]
  agents: ["manager-spec", "expert-backend"]
  languages: ["python", "typescript"]

# 종속성
requires: []
optional_requires: ["related-skill"]

# 허용된 도구
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash

# 스킬 메타데이터
tags: ["tag1", "tag2"]
updated: 2026-01-17
status: "active"  # active, experimental, deprecated
---

# ═══════════════════════════════════════════════
# Level 2: 스킬 본문 (조건부 로드 ~5K 토큰)
# ═══════════════════════════════════════════════

## Quick Reference

**[skill-name]이란 무엇인가?**

핵심 목적을 설명하는 한 문장.

**주요 이점:**
- 이점 1
- 이점 2
- 이점 3

**사용 시점:**
- 사용 사례 1
- 사용 사례 2

**빠른 링크:**
- 구현: #implementation-guide
- 예제: examples.md
- 참조: reference.md

---

## Implementation Guide

### 핵심 개념

주요 개념에 대한 간단한 설명 (1-2 단락).

### 단계별 프로세스

**Step 1: [첫 번째 단계]**

설명 및 예제.

**Step 2: [두 번째 단계]**

설명 및 예제.

### 통합 지점

이 스킬이 다른 스킬 및 에이전트와 통합되는 방법.

---

## Advanced Topics

### 성능 고려사항

최적 성능을 위한 팁.

### 예외 케이스

특수한 경우 및 에러 시나리오 처리.

### 모범 사례

권장 패턴 및 안티패턴.

---

## 잘 작동하는 조합

**관련 스킬:**
- skill-one: 함께 사용할 때
- skill-two: 보완적 사용 사례

**에이전트:**
- agent-name: 이 에이전트가 이 스킬을 사용하는 방법

**명령어:**
- /command: 이 스킬을 호출하는 명령어

---

# ═══════════════════════════════════════════════
# Level 3: 번들 파일 (온디맨드 로드)
# ═══════════════════════════════════════════════

## 모듈 참조

모듈화된 파일의 확장 문서:

- **modules/patterns.md**: 상세 디자인 패턴
- **modules/examples.md**: 종합 예제
- **modules/reference.md**: API 참조
- **modules/troubleshooting.md**: 일반적인 문제

## Examples

**examples.md**의 작동하는 코드 샘플:
- Example 1: 기본 사용법
- Example 2: 고급 사용법
- Example 3: 통합 패턴

## Reference

**reference.md**의 외부 리소스:
- 공식 문서
- 커뮤니티 리소스
- 관련 도구

---

# Progressive Disclosure 레벨 요약

| 레벨 | 내용 | 시점 | 토큰 비용 |
|-------|------|------|------------|
| 1 | YAML 메타데이터만 | 에이전트 초기화 | ~100 토큰 |
| 2 | SKILL.md 본문 | 트리거 키워드 일치 | ~5K 토큰 |
| 3+ | 번들 파일 | Claude가 결정 | 무제한 |

---

# 하위 호환성 참고사항

Progressive Disclosure를 아직 지원하지 않는 에이전트의 경우, 전체 SKILL.md(레벨 1 + 2)가 초기화 시 로드됩니다. 이는 Progressive Disclosure 인식 에이전트의 최적화를 활성화하면서 호환성을 보장합니다.
```

### 섹션 분류

#### Quick Reference (Level 2)

**목적**: 즉각적이고 실행 가능한 정보 제공

**구성 요소**:
- **[skill-name]이란 무엇인가?**: 한 문장 설명
- **주요 이점**: 3-5개 항목
- **사용 시점**: 일반적인 사용 사례
- **빠른 링크**: 상세 섹션으로의 탐색

**가이드라인**:
- 스캔 가능하게 유지 (사용자가 10초 내에 관련성 판단 가능)
- "무엇"과 "왜"에 초점, "어떻게"는 아님
- 명확하고 비전문적인 언어 사용

#### Implementation Guide (Level 2)

**목적**: 사용자에게 스킬 적용 방법 가르치기

**구성 요소**:
- **핵심 개념**: 기초 지식
- **단계별 프로세스**: 실행 가능한 지침
- **통합 지점**: 다른 스킬과의 연결 방법

**가이드라인**:
- 순차적 프로세스에 번호 매긴 단계 사용
- 해당하는 경우 코드 예제 포함
- 전/후 상태 표시

#### Advanced Topics (Level 2)

**목적**: 예외 케이스 및 최적화 처리

**구성 요소**:
- **성능 고려사항**: 최적화 팁
- **예외 케이스**: 특수 시나리오
- **모범 사례**: 해야 할 것과 하지 말아야 할 것

**가이드라인**:
- 고급 사용자를 위한 선택적 읽기
- 일반적인 함정에 대한 경고 포함
- 심층 분석을 위해 Level 3 모듈 참조

#### 번들 파일 (Level 3+)

**목적**: 무제한 상세 문서 제공

**구성 요소**:
- **examples.md**: 완전한 작동 예제
- **reference.md**: 외부 링크, API 문서
- **modules/*.md**: 전문화된 하위 주제

**가이드라인**:
- 자체 완결적 (SKILL.md 없이 읽기 가능)
- 관련 모듈 상호 참조
- 종합적인 코드 샘플 포함

---

## 첫 번째 SKILL.md 작성하기

### 단계별 튜토리얼

#### Step 1: 스킬 디렉토리 생성

```bash
mkdir -p .claude/skills/my-first-skill
cd .claude/skills/my-first-skill
```

#### Step 2: SKILL.md 파일 생성

```bash
touch SKILL.md
```

#### Step 3: YAML Frontmatter 작성

```yaml
---
name: "my-first-skill"
description: "Progressive Disclosure를 시연하는 튜토리얼 스킬"
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

#### Step 4: Quick Reference 작성

```markdown
## Quick Reference

**my-first-skill이란 무엇인가?**

Progressive Disclosure 패턴을 시연하고 스킬 작성을 배우는 데 도움이 되는 간단한 튜토리얼 스킬입니다.

**주요 이점:**
- 예제로 배우기
- Progressive Disclosure 이해
- 자신의 스킬을 위한 템플릿

**사용 시점:**
- 스킬 작성 학습 시
- 새로운 스킬의 참조로
- 스킬 로딩 테스트용

**빠른 링크:**
- 구현: #implementation-guide
```

#### Step 5: Implementation Guide 작성

```markdown
## Implementation Guide

### 핵심 개념

이 스킬은 Progressive Disclosure의 작동 방식을 시연합니다:
1. 메타데이터가 먼저 로드됨 (~100 토큰)
2. 트리거되면 본문 로드 (~3K 토큰)
3. 추가 파일은 온디맨드로 로드

### 단계별 프로세스

**Step 1: 스킬 트리거**

프롬프트에 다음 키워드 중 하나를 사용하세요:
- "tutorial"
- "first skill"
- "learning"

**Step 2: 로딩 관찰**

Claude는:
1. 초기화 중에 Level 1 메타데이터 로드
2. 키워드가 일치할 때 Level 2 본문 로드
3. 세부 정보를 요청하면 Level 3 파일 액세스

**Step 3: 동작 확인**

Claude에게 물어보세요: "튜토리얼 스킬 세부 정보를 보여줘"
```

#### Step 6: 스킬 테스트

```
사용자: "튜토리얼 스킬을 보여줘"

예상: Claude가 Level 2를 로드하고 내용을 표시
```

#### Step 7: Level 3 파일 추가 (선택사항)

```bash
# 예제 파일 생성
touch examples.md

# 참조 파일 생성
touch reference.md

# 모듈 디렉토리 생성
mkdir modules
touch modules/advanced-patterns.md
```

---

## YAML Frontmatter 레퍼런스

### 완전한 필드 레퍼런스

```yaml
---
# ═══════════════════════════════════════════════
# 필수 필드
# ═══════════════════════════════════════════════

name: "skill-name"
# - 모든 스킬에서 고유해야 함
# - kebab-case 사용 (하이픈이 있는 소문자)
# - 디렉토리 이름과 일치
# 예: "moai-workflow-spec"

description: "간단한 한 줄 설명"
# - 명확하고 간결해야 함 (< 100자)
# - 스킬이 하는 일을 설명, 방법이 아님
# 예: "요구사항 문서화를 위한 SPEC 워크플로우 전문가"

version: "1.0.0"
# - 시맨틱 버저닝을 따라야 함 (major.minor.patch)
# - 변경 시 증가:
#   - major: 호환성을 깨는 변경
#   - minor: 새로운 기능 (하위 호환)
#   - patch: 버그 수정

# ═══════════════════════════════════════════════
# 분류
# ═══════════════════════════════════════════════

category: "workflow"
# - 다음 중 하나여야 함:
#   - foundation: 핵심 MoAI 개념
#   - lang: 프로그래밍 언어 스킬
#   - platform: 플랫폼별 (Vercel, Supabase 등)
#   - library: 라이브러리 스킬 (shadcn, Nextra 등)
#   - workflow: 프로세스 스킬 (SPEC, TDD 등)
#   - domain: 도메인 스킬 (backend, frontend 등)

modularized: true
# - true: 스킬이 Level 3 모듈을 가짐
# - false: 스킬이 SKILL.md에 자체 포함됨

user-invocable: true
# - true: 사용자가 이 스킬을 직접 호출 가능
# - false: 에이전트만 로드

# ═══════════════════════════════════════════════
# PROGRESSIVE DISCLOSURE
# ═══════════════════════════════════════════════

progressive_disclosure:
  enabled: true
  # - true: 3단계 로딩 사용
  # - false: 전체 SKILL.md를 한 번에 로드

  level1_tokens: ~100
  # - YAML frontmatter의 예상 토큰 수
  # - 대략적인 값에 ~ 접두사 사용

  level2_tokens: ~5000
  # - 전체 마크다운 본문의 예상 토큰 수
  # - 대략적인 값에 ~ 접두사 사용

# ═══════════════════════════════════════════════
# 트리거 조건
# ═══════════════════════════════════════════════

triggers:
  keywords: ["keyword1", "keyword2", "keyword3"]
  # - 트리거 키워드 목록 (대소문자 구분 안 함)
  # - 사용자 프롬프트에 키워드가 나타나면 Level 2 로드
  # - 예: ["SPEC", "requirement", "EARS", "planning"]

  phases: ["plan", "run", "sync"]
  # - 특정 워크플로우 단계에서 Level 2 로드
  # - 유효한 단계: plan, run, sync
  # - 빈 목록 [] = 단계 트리거 없음

  agents: ["manager-spec", "expert-backend"]
  # - 이러한 에이전트가 활성화될 때 Level 2 로드
  # - 에이전트 이름 사용 (.md 확장자 제외)
  # - 빈 목록 [] = 에이전트 트리거 없음

  languages: ["python", "typescript", "javascript"]
  # - 이러한 언어로 작업할 때 Level 2 로드
  # - 파일 확장자나 사용자 언급에서 감지
  # - 빈 목록 [] = 언어 트리거 없음

# ═══════════════════════════════════════════════
# 종속성
# ═══════════════════════════════════════════════

requires: []
# - 이 스킬보다 먼저 로드되어야 하는 스킬
# - 스킬 이름 사용 (.md 확장자 제외)
# - 예: ["moai-foundation-core"]

optional_requires: []
# - 이 스킬을 향상시킬 수 있는 스킬
# - 사용 가능하면 로드되지만 필수는 아님
# - 예: ["moai-foundation-philosopher"]

# ═══════════════════════════════════════════════
# 허용된 도구
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
# - 이 스킬이 사용할 수 있는 도구 목록
# - 안전을 위해 도구 액세스 제한
# - 공식 Claude Code 도구 이름 사용

# ═══════════════════════════════════════════════
# 메타데이터
# ═══════════════════════════════════════════════

tags: ["tag1", "tag2", "tag3"]
# - 스킬 검색을 위한 검색 가능한 태그
# - 소문자, 단일 단어 사용
# - 예: ["git", "workflow", "automation"]

updated: 2026-01-17
# - 마지막 업데이트 날짜 (YYYY-MM-DD 형식)
# - 중요한 변경 시 업데이트

status: "active"
# - 수명 주기 상태
# - 유효한 값:
#   - active: 완전히 지원됨, 권장
#   - experimental: 테스트 단계, 변경 가능
#   - deprecated: 더 이상 유지보수 안 함, 대안 사용
---
```

### 필드 유효성 검사 규칙

**name**:
- ✅ `moai-workflow-spec`
- ✅ `my-custom-skill`
- ❌ `MyCustomSkill` (PascalCase 금지)
- ❌ `my_custom_skill` (밑줄 금지)

**description**:
- ✅ `요구사항 문서화를 위한 SPEC 워크플로우 전문가`
- ✅ `Git fork 동기화 워크플로우`
- ❌ (빈 문자열)
- ❌ `이 스킬은 많은 것을 합니다...` (너무 모호함)

**version**:
- ✅ `1.0.0`
- ✅ `2.3.1`
- ❌ `1.0` (패치 버전 누락)
- ❌ `v1.0.0` ("v" 접두사 금지)

**category**:
- ✅ `workflow`
- ✅ `lang`
- ❌ `custom` (허용 목록에 없음)

**triggers.keywords**:
- ✅ `["SPEC", "requirement"]`
- ✅ `[]` (빈 목록)
- ❌ `"SPEC"` (목록이어야 함, 문자열 아님)

---

## 트리거 설정

### 트리거 이해하기

트리거는 Level 2 (스킬 본문)가 로드되어야 하는 시점을 결정합니다. 다음을 기반으로 런타임에 평가됩니다:
1. **사용자 프롬프트 내용** (keywords)
2. **현재 워크플로우 단계** (phases)
3. **활성 에이전트** (agents)
4. **프로그래밍 언어** (languages)

### 트리거 유형

#### 1. 키워드 트리거

**작동 방식**:
- 사용자 프롬프트에서 트리거 키워드 스캔
- 대소문자 구분 없는 매칭
- 부분 단어 매칭 (예: "specification"이 "SPEC"과 매칭)

**설정**:
```yaml
triggers:
  keywords: ["SPEC", "requirement", "EARS", "planning", "specification"]
```

**트리거 예제**:
- ✅ "SPEC 문서 작성" → "SPEC"과 매칭
- ✅ "인증을 위한 요구사항 작성" → "requirement"와 매칭
- ✅ "계획을 도와줘" → "planning"과 매칭
- ❌ "백엔드 API 구축" → 매칭 없음

**모범 사례**:
- 3-10개 키워드 포함
- 단수형과 복수형 모두 사용
- 일반적인 동의어 포함
- 지나치게 일반적인 단어 피하기 (예: "code", "help")

#### 2. 단계 트리거

**작동 방식**:
- MoAI-ADK에 사전 정의된 워크플로우 단계가 있음
- 단계가 트리거와 일치하면 스킬 로드

**설정**:
```yaml
triggers:
  phases: ["plan", "run", "sync"]
```

**사용 가능한 단계**:
- `plan`: 요구사항 수집, SPEC 생성
- `run`: 구현, 코딩, 테스팅
- `sync`: 문서화, 업데이트, 동기화 작업

**트리거 예제**:
- ✅ `/moai:1-plan "새로운 기능"` → 단계 = "plan"
- ✅ `/moai:2-run SPEC-001` → 단계 = "run"
- ✅ `/moai:3-sync SPEC-001` → 단계 = "sync"

**모범 사례**:
- 워크플로우별 스킬에 단계 사용
- `plan` 단계: SPEC, 전략, 디자인 스킬
- `run` 단계: TDD, 구현, 테스팅 스킬
- `sync` 단계: 문서화, 업데이트 스킬

#### 3. 에이전트 트리거

**작동 방식**:
- 특정 에이전트가 활성화될 때 스킬 로드
- 에이전트별 지식 주입 가능

**설정**:
```yaml
triggers:
  agents: ["manager-spec", "manager-strategy", "expert-backend"]
```

**트리거 예제**:
- ✅ 사용자가 `manager-spec` 호출 → SPEC 관련 스킬 로드
- ✅ 사용자가 `expert-backend` 호출 → 백엔드 스킬 로드
- ❌ 사용자가 `expert-frontend` 호출 → 매칭 없음

**모범 사례**:
- 이 스킬이 필요한 에이전트 나열
- 모든 에이전트를 나열하지 않기 (트리거의 목적을 무효화)
- 전문화된 도메인별 스킬에 사용

#### 4. 언어 트리거

**작동 방식**:
- 다음에서 프로그래밍 언어 감지:
  - 대화의 파일 확장자
  - 사용자가 언어 이름 언급
  - 언어 태그가 있는 코드 블록

**설정**:
```yaml
triggers:
  languages: ["python", "typescript", "javascript", "go"]
```

**트리거 예제**:
- ✅ "Python 코드를 작성해..." → "python"과 매칭
- ✅ "TypeScript 인터페이스를..." → "typescript"와 매칭
- ✅ 파일 열림: `app.py` → "python"과 매칭
- ❌ "웹 앱 구축" → 언어 언급 없음

**모범 사례**:
- 언어별 스킬에 사용
- 모든 변형이 아닌 주요 언어 나열
- 관련 언어 포함 고려 (예: JS + TS)

### 트리거 전략 결정 매트릭스

| 스킬 유형 | 권장 트리거 | 예제 |
|------------|---------------------|---------|
| **워크플로우** | 키워드 + 단계 | SPEC 워크플로우: keywords=["SPEC"], phases=["plan"] |
| **언어** | 키워드 + 언어 | Python 스킬: keywords=["python"], languages=["python"] |
| **플랫폼** | 키워드만 | Vercel 스킬: keywords=["vercel", "deployment"] |
| **도메인** | 키워드 + 에이전트 | 백엔드 스킬: keywords=["API"], agents=["expert-backend"] |
| **기초** | 비어 있음 (항상 L2 로드) | 핵심 개념: 모든 트리거=[] |

### 트리거 테스트

**테스트 1: 키워드 트리거**
```
사용자: "SPEC 문서를 작성하도록 도와줘"

예상:
1. 모든 스킬에 대해 Level 1 메타데이터 로드
2. 키워드 "SPEC" 매칭
3. moai-workflow-spec의 Level 2 로드
```

**테스트 2: 단계 트리거**
```
사용자: "/moai:1-plan 새로운 인증 시스템"

예상:
1. 단계 = "plan" 감지
2. phases=["plan"]인 모든 스킬의 Level 2 로드
```

**테스트 3: 다중 트리거**
```
사용자: "SPEC-001을 위한 Python 코드 작성"

예상:
1. 키워드 "Python" 매칭 → moai-lang-python의 Level 2 로드
2. 키워드 "SPEC" 매칭 → moai-workflow-spec의 Level 2 로드
```

---

## Claude Code에서 스킬이 로드되는 방법

### 로딩 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    사용자 프롬프트                        │
│  "Python에서 인증을 위한 SPEC 문서 작성"                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              1. 에이전트 초기화                           │
│  - 에이전트 frontmatter 로드 (manager-spec.md)          │
│  - skills: 필드 추출                                    │
│  - skills: moai-foundation-core, moai-workflow-spec     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         2. 에이전트 스킬에 대해 Level 1 로드              │
│  - YAML frontmatter만 파싱                              │
│  - 토큰 비용: 2 × 100 = 200 토큰                        │
│  - 트리거 조건 추출                                      │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              3. 사용자 프롬프트 분석                      │
│  - 키워드 추출: "SPEC", "인증", "Python"                 │
│  - 단계 감지: None (/moai 명령 아님)                     │
│  - 언어 감지: "Python"                                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              4. 트리거 매칭                               │
│  - moai-workflow-spec:                                  │
│    - keywords: ["SPEC"] ✅ 매칭                         │
│  - moai-lang-python:                                    │
│    - languages: ["python"] ✅ 매칭                      │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         5. 매칭된 스킬에 대해 Level 2 로드                │
│  - 전체 마크다운 본문 로드 (YAML frontmatter 이후)       │
│  - moai-workflow-spec: +5K 토큰                         │
│  - moai-lang-python: +5K 토큰                           │
│  - 총 Level 2 비용: 10K 토큰                            │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│         6. Claude가 요청 처리                             │
│  - 로드된 스킬을 사용하여 작업 이해                       │
│  - 필요시 Level 3 파일 요청 가능                         │
│  - 예: 코드 샘플을 위해 examples.md 읽기                 │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              7. 응답 생성                                 │
│  - 로드된 지식을 사용하여 SPEC 문서 생성                  │
│  - Python 모범 사례 적용                                 │
│  - moai-workflow-spec의 EARS 형식 사용                  │
└─────────────────────────────────────────────────────────┘
```

### 로딩 프로세스 세부사항

#### Phase 1: 에이전트 초기화

**발생하는 일**:
1. 사용자가 에이전트 호출 (명시적으로 또는 Alfred 라우팅을 통해)
2. 에이전트 frontmatter 파싱
3. `skills:` 필드 추출

**코드 예제** (내부):
```python
agent_metadata = parse_agent_frontmatter("manager-spec.md")
skill_names = agent_metadata.get("skills", "").split(",")
# skill_names = ["moai-foundation-core", "moai-workflow-spec"]
```

**토큰 비용**: 최소 (에이전트 frontmatter ~200 토큰)

#### Phase 2: Level 1 메타데이터 로드

**발생하는 일**:
1. `skills:` 목록의 각 스킬에 대해
2. SKILL.md의 YAML frontmatter 파싱
3. 트리거, 종속성, 메타데이터 추출
4. 마크다운 본문 전에 파싱 중지

**코드 예제** (내부):
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

**토큰 비용**: 스킬당 ~100 토큰

#### Phase 3: 사용자 프롬프트 분석

**발생하는 일**:
1. 사용자 프롬프트에서 키워드 추출
2. 워크플로우 단계 감지 (해당하는 경우)
3. 프로그래밍 언어 감지
4. 컨텍스트 딕셔너리 구축

**코드 예제** (내부):
```python
context = {
    "prompt": "Python에서 인증을 위한 SPEC 문서 작성",
    "keywords": ["SPEC", "인증", "Python"],
    "phase": None,
    "agent": "manager-spec",
    "language": "python"
}
```

**토큰 비용**: 없음 (메타데이터 처리)

#### Phase 4: 트리거 매칭

**발생하는 일**:
1. 레지스트리의 각 스킬에 대해
2. 트리거가 컨텍스트와 일치하는지 확인
3. Level 2에서 로드할 스킬 목록 구축

**코드 예제** (내부):
```python
def should_load_level2(skill_metadata, context):
    triggers = skill_metadata.get("triggers", {})

    # 키워드 트리거 확인
    keywords = triggers.get("keywords", [])
    if any(kw.lower() in context["prompt"].lower() for kw in keywords):
        return True

    # 단계 트리거 확인
    phases = triggers.get("phases", [])
    if context.get("phase") in phases:
        return True

    # 에이전트 트리거 확인
    agents = triggers.get("agents", [])
    if context.get("agent") in agents:
        return True

    # 언어 트리거 확인
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

**토큰 비용**: 없음 (메타데이터 처리)

#### Phase 5: Level 2 본문 로드

**발생하는 일**:
1. 매칭된 각 스킬에 대해
2. 전체 SKILL.md 파일 읽기
3. YAML frontmatter 이후의 마크다운 콘텐츠 추출
4. Claude의 컨텍스트에 추가

**코드 예제** (내부):
```python
from src.moai_adk.core.skill_loading_system import load_skill_body

level2_content = []
for skill_name in skills_to_load:
    body = load_skill_body(skill_name)
    level2_content.append(body)
    # body = "## Quick Reference\n\n**SPEC 워크플로우란?**\n\n..."

# Claude의 시스템 프롬프트에 주입
system_prompt += "\n\n".join(level2_content)
```

**토큰 비용**: 매칭된 스킬당 ~5K 토큰

#### Phase 6: Claude 처리

**발생하는 일**:
1. Claude가 전체 컨텍스트 수신 (시스템 + 사용자 프롬프트)
2. 로드된 스킬 지식을 사용하여 작업 이해
3. Read 도구를 통해 Level 3 파일 요청 가능

**예제**:
```
Claude: "SPEC 문서를 작성하겠습니다. 예제를 확인해 보겠습니다."
[Claude가 내부적으로 Read 도구 호출]
Read("moai-workflow-spec/examples.md")
```

**토큰 비용**: Level 3 토큰 (온디맨드)

#### Phase 7: 응답 생성

**발생하는 일**:
1. Claude가 로드된 지식을 사용하여 응답 생성
2. 스킬의 패턴 적용
3. 사용자에게 반환

**토큰 비용**: 출력 토큰 (입력과 별도)

### 토큰 예산 추적

**예제 세션**:
```
에이전트 초기화: 200 토큰
Level 1 (10개 스킬): 1,000 토큰
Level 2 (2개 매칭된 스킬): 10,000 토큰
사용자 프롬프트: 500 토큰
시스템 프롬프트: 10,000 토큰
──────────────────────────────────
총 입력 토큰: 21,700 토큰
사용 가능: 178,300 토큰 (89% 여유)
```

**Progressive Disclosure 없이**:
```
에이전트 초기화: 200 토큰
모든 스킬 (10 × 5K): 50,000 토큰
사용자 프롬프트: 500 토큰
시스템 프롬프트: 10,000 토큰
──────────────────────────────────
총 입력 토큰: 60,700 토큰
사용 가능: 139,300 토큰 (70% 여유)
```

**절감**: 39,000 토큰 (65% 감소)

---

## 모듈화 패턴

### 왜 모듈화하나요?

**문제**: 단일 SKILL.md 파일이 너무 커짐:
- 유지보수 어려움
- 탐색 어려움
- Level 2 토큰 예산 초과

**해결책**: 콘텐츠를 Level 3 모듈로 분할:
- SKILL.md는 간결하게 유지
- 모듈은 온디맨드로 로드
- 유지보수 및 확장 용이

### 모듈 구조

```
skill-name/
├── SKILL.md                  # Level 1 + 2 (~5K 토큰)
├── examples.md               # Level 3 (작동하는 코드 샘플)
├── reference.md              # Level 3 (외부 링크, API 문서)
└── modules/                  # Level 3+ (전문 주제)
    ├── README.md             # 모듈 인덱스
    ├── pattern-1.md          # 특정 패턴/주제
    ├── pattern-2.md
    └── advanced-topics.md
```

### 모듈 생성 시기

**모듈을 생성해야 하는 경우**:
- 주제가 자체 완결적 (독립적으로 읽기 가능)
- 콘텐츠가 1,000 토큰 초과
- 주제가 고급/선택사항
- 여러 관련 패턴이 존재

**SKILL.md에 유지해야 하는 경우**:
- 콘텐츠가 기초적
- 주제가 < 500 토큰
- 정보가 항상 필요함
- 콘텐츠가 개요 제공

### 모듈 명명 규칙

**좋은 모듈 이름**:
- ✅ `react19-patterns.md` (구체적, 서술적)
- ✅ `performance-optimization.md` (명확한 주제)
- ✅ `troubleshooting.md` (잘 알려진 범주)

**나쁜 모듈 이름**:
- ❌ `module1.md` (서술적이지 않음)
- ❌ `misc.md` (너무 모호함)
- ❌ `everything-else.md` (포괄적)

### 모듈 템플릿

```markdown
# [모듈 주제 이름]

**소속**: [skill-name]
**버전**: 1.0.0
**최종 업데이트**: 2026-01-17

---

## 개요

이 모듈이 다루는 내용에 대한 간단한 설명 (1-2 단락).

---

## 전제 조건

이 모듈을 읽기 전에 사용자가 알아야 할 것:
- 전제 조건 1
- 전제 조건 2

---

## 핵심 내용

### 하위 주제 1

예제가 포함된 상세 설명.

### 하위 주제 2

예제가 포함된 상세 설명.

---

## 예제

개념을 시연하는 작동하는 코드 샘플.

---

## 관련 모듈

- [pattern-1.md](./pattern-1.md): 설명
- [pattern-2.md](./pattern-2.md): 설명

---

## 외부 리소스

- [공식 문서](https://example.com)
- [커뮤니티 가이드](https://example.com)
```

### SKILL.md에서 모듈 참조하기

**Level 2 본문에서**:
```markdown
## Advanced Topics

상세 패턴은 다음을 참조하세요:
- **modules/react19-patterns.md**: React 19 특정 패턴
- **modules/performance-optimization.md**: 최적화 기법
- **modules/troubleshooting.md**: 일반적인 문제 및 해결책

Claude는 필요할 때 이러한 파일에 온디맨드로 액세스할 수 있습니다.
```

**Quick Reference에서**:
```markdown
**빠른 링크:**
- 구현: #implementation-guide
- 예제: examples.md (Level 3)
- 패턴: modules/react19-patterns.md
- 참조: reference.md (Level 3)
```

### 모듈 로딩 동작

**자동 로딩** (Level 3):
- Claude가 모듈을 언제 로드할지 결정
- 작업 요구사항에 기반
- 내부적으로 Read 도구 사용

**사용자 요청 로딩**:
```
사용자: "프론트엔드 스킬에서 React 19 패턴을 보여줘"

Claude: [내부적으로 Read 도구 호출]
Read("moai-domain-frontend/modules/react19-patterns.md")
```

**에이전트 트리거 로딩**:
```markdown
<!-- 에이전트 지침에서 -->
React 컴포넌트를 구현할 때 참조:
- moai-domain-frontend/modules/react19-patterns.md
```

---

## 토큰 최적화 전략

### 토큰 예산 관리

**200K 토큰 예산 분석**:
```
시스템 프롬프트: ~10K 토큰 (5%)
에이전트 정의: ~500 토큰 (0.25%)
Level 1 스킬: ~5K 토큰 (2.5%)
Level 2 스킬: ~25K 토큰 (12.5%)
사용자 프롬프트: ~500 토큰 (0.25%)
대화 기록: ~20K 토큰 (10%)
──────────────────────────────────
사용: ~61K 토큰 (30.5%)
여유: ~139K 토큰 (69.5%) ← 출력에 사용 가능
```

**Progressive Disclosure 없이**:
```
시스템 프롬프트: ~10K 토큰
에이전트 정의: ~500 토큰
모든 스킬 (48 × 5K): ~240K 토큰 ← 한계 초과!
```

### 최적화 기법

#### 1. Level 1 메타데이터 최소화

**전략**: YAML frontmatter를 간결하게 유지

**이전** (장황함):
```yaml
---
name: "moai-workflow-spec"
description: "이 스킬은 EARS 형식을 사용하여 SPEC 문서 작성, 요구사항 수집, 이해관계자 분석 및 검증 프로세스를 포함한 SPEC 문서 작성을 위한 포괄적인 문서 및 모범 사례를 제공합니다."
# ... (150+ 토큰)
```

**이후** (최적화):
```yaml
---
name: "moai-workflow-spec"
description: "요구사항 문서화를 위한 SPEC 워크플로우 전문가"
# ... (100 토큰)
```

**절감**: 스킬당 50 토큰 × 48개 스킬 = 2,400 토큰

#### 2. 정확한 트리거 사용

**전략**: 지나치게 광범위한 트리거 피하기

**이전** (광범위):
```yaml
triggers:
  keywords: ["code", "help", "create", "build", "make", "develop", "write"]
  # 거의 모든 프롬프트와 매칭!
```

**이후** (정확):
```yaml
triggers:
  keywords: ["SPEC", "requirement", "EARS", "specification"]
  # 관련 프롬프트만 매칭
```

**영향**: 불필요한 Level 2 로딩 감소

#### 3. 대형 스킬 모듈화

**전략**: >10K 토큰 스킬을 모듈로 분할

**이전** (단일체):
```markdown
<!-- SKILL.md: 15K 토큰 -->
## React 패턴 (3K 토큰)
## Next.js 패턴 (3K 토큰)
## 상태 관리 (3K 토큰)
## 성능 (3K 토큰)
## 테스팅 (3K 토큰)
```

**이후** (모듈화):
```markdown
<!-- SKILL.md: 5K 토큰 -->
## Quick Reference
## Implementation Guide

<!-- modules/react19-patterns.md: 3K 토큰 -->
<!-- modules/nextjs16-patterns.md: 3K 토큰 -->
<!-- modules/state-management.md: 3K 토큰 -->
(등)
```

**영향**: Level 2 로드 = 15K 대신 5K (10K 절감)

#### 4. 스킬 종속성 현명하게 사용

**전략**: 중복을 피하기 위해 종속성 선언

**이전** (중복된 콘텐츠):
```yaml
# skill-a/SKILL.md
---
name: "skill-a"
# ... 기초 개념 포함 (1K 토큰)
---

# skill-b/SKILL.md
---
name: "skill-b"
# ... 동일한 기초 개념 포함 (1K 토큰)
---
```

**이후** (공유 기초):
```yaml
# moai-foundation-core/SKILL.md
---
name: "moai-foundation-core"
# ... 기초 개념 (1K 토큰)
---

# skill-a/SKILL.md
---
name: "skill-a"
requires: ["moai-foundation-core"]
# ... 특정 콘텐츠만
---

# skill-b/SKILL.md
---
name: "skill-b"
requires: ["moai-foundation-core"]
# ... 특정 콘텐츠만
---
```

**영향**: 기초는 한 번만 로드되고 여러 스킬이 공유

#### 5. 예제를 지연 로드

**전략**: 예제를 Level 3으로 이동

**이전** (Level 2에):
```markdown
## 예제

### 예제 1: 기본 사용법
(500 토큰)

### 예제 2: 고급 사용법
(800 토큰)

### 예제 3: 통합
(600 토큰)

총: Level 2에 1,900 토큰
```

**이후** (Level 3):
```markdown
## 예제

작동하는 코드 샘플은 **examples.md**를 참조하세요:
- 예제 1: 기본 사용법
- 예제 2: 고급 사용법
- 예제 3: 통합

Claude는 온디맨드로 예제에 액세스할 수 있습니다.

총: Level 2에 100 토큰
```

**영향**: 예제가 있는 스킬당 1,800 토큰 절감

### 토큰 추정

**Level 1 토큰 추정**:
1. YAML frontmatter 복사
2. 토큰 카운터에 붙여넣기: https://platform.openai.com/tokenizer
3. `level1_tokens` 필드에 카운트 기록

**Level 2 토큰 추정**:
1. 전체 마크다운 본문 복사 (YAML 이후)
2. 토큰 카운터에 붙여넣기
3. `level2_tokens` 필드에 카운트 기록

**SKILL.md 업데이트**:
```yaml
progressive_disclosure:
  enabled: true
  level1_tokens: ~110  # 실제 측정된 카운트
  level2_tokens: ~4850 # 실제 측정된 카운트
```

---

## 모범 사례

### 콘텐츠 가이드라인

#### DO: 스캔 가능하게 작성하기

**좋음**:
```markdown
## Quick Reference

**SPEC 워크플로우란 무엇인가?**

요구사항 문서화를 위한 구조화된 접근 방식.

**주요 이점:**
- 명확한 요구사항
- 이해관계자 정렬
- 테스트 가능한 기준
```

**나쁨**:
```markdown
## 소개

SPEC 워크플로우는 현대 소프트웨어 개발 프로젝트에서 요구사항을 캡처, 문서화 및 검증하는 복잡한 과제에 대해 구조화되고 반복 가능하며 확장 가능한 접근 방식을 만들기 위해 여러 도메인에 걸쳐 다양한 이해관계자와 함께 수년 동안 작업하며 개발한 포괄적인 방법론입니다...

(텍스트 장벽 계속)
```

#### DO: 점진적 세부사항 사용

**좋음**:
```markdown
## Implementation Guide

### Step 1: 요구사항 분석

간단한 개요 (1 단락).

상세한 분석 기법은 modules/requirement-analysis.md를 참조하세요.

### Step 2: SPEC 작성

간단한 개요 (1 단락).

EARS 형식 세부사항은 modules/ears-format.md를 참조하세요.
```

**나쁨**:
```markdown
## Implementation Guide

### Step 1: 요구사항 분석

(Level 2에 5페이지의 상세 콘텐츠)
```

#### DO: 명확한 예제 제공

**좋음**:
```markdown
## 예제: 기본 SPEC 문서

```markdown
# SPEC-001: 사용자 인증

WHEN 사용자가 유효한 자격 증명을 입력할 때
THE 시스템은 사용자를 인증해야 함
AND 보호된 리소스에 대한 액세스 부여
```

완전한 예제는 examples.md를 참조하세요.
```

**나쁨**:
```markdown
## 예제

예제는 examples.md를 참조하세요.
```

#### DO: 관련 스킬 상호 참조

**좋음**:
```markdown
## 잘 작동하는 조합

**관련 스킬:**
- moai-foundation-core: TRUST 5 검증 프레임워크 제공
- moai-workflow-ddd: SPEC 생성 후 DDD 사이클 사용

**에이전트:**
- manager-spec: SPEC 생성을 위한 주요 에이전트
- manager-strategy: SPEC 후 시스템 설계에 사용
```

**나쁨**:
```markdown
## 관련

다른 스킬이 존재합니다.
```

### 유지보수 가이드라인

#### 버전 관리

**증가 시점**:
- **Major** (1.x.x → 2.x.x): 호환성을 깨는 변경, 호환되지 않는 API
- **Minor** (x.1.x → x.2.x): 새로운 기능, 하위 호환
- **Patch** (x.x.1 → x.x.2): 버그 수정, 오타, 명확화

**업데이트 프로세스**:
1. SKILL.md 변경
2. frontmatter에서 버전 증가
3. `updated` 날짜 업데이트
4. 스킬의 CHANGELOG에 변경사항 문서화 (있는 경우)
5. 트리거 동작 테스트

#### 문서 부패 방지

**일정**:
- **월별**: 토큰 추정 검토 (>10% 차이 시 재계산)
- **분기별**: 트리거 키워드 검토 (사용량에 따라 추가/제거)
- **반기별**: 모듈 검토 (필요에 따라 통합 또는 분할)

**체크리스트**:
- [ ] 예제가 현재 도구와 작동
- [ ] 외부 링크가 끊어지지 않음
- [ ] 트리거 키워드가 사용자 언어와 일치
- [ ] 토큰 카운트가 정확
- [ ] 종속성이 여전히 유효

#### 폐기 프로세스

**Step 1**: 폐기로 표시
```yaml
status: "deprecated"
```

**Step 2**: 폐기 공지 추가
```markdown
> **⚠️ DEPRECATED**: 이 스킬은 더 이상 유지보수되지 않습니다.
> 대신 [replacement-skill]을 사용하세요.
>
> **마이그레이션 가이드**: [migration.md](./migration.md)를 참조하세요
```

**Step 3**: 6개월 동안 유지 후 아카이브

### 테스트 가이드라인

#### 수동 테스트

**테스트 1: 트리거 매칭**
```
1. Claude Code 열기
2. 입력: "[트리거 키워드] 테스트"
3. Level 2 로드 확인
4. /context로 확인
```

**테스트 2: 토큰 예산**
```
1. Level 1에서 스킬 로드
2. /context를 사용하여 토큰 사용량 확인
3. level1_tokens 추정과 비교
4. 차이가 >10%이면 재계산 및 업데이트
```

**테스트 3: 모듈 액세스**
```
1. Claude에게 질문: "[skill-name]에서 [module-name]을 보여줘"
2. Claude가 Read 도구 사용 확인
3. 모듈 콘텐츠가 표시되는지 확인
```

#### 자동화된 테스트

**토큰 카운트 검증** (Python):
```python
import tiktoken

def count_tokens(text: str) -> int:
    """tiktoken을 사용한 토큰 카운트 (GPT-4 인코딩)"""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def validate_skill_tokens(skill_path: str):
    """SKILL.md frontmatter의 토큰 추정 검증"""
    with open(skill_path, "r") as f:
        content = f.read()

    # frontmatter와 본문 분할
    parts = content.split("---")
    frontmatter = parts[1]
    body = "---".join(parts[2:])

    # 토큰 카운트
    l1_actual = count_tokens(frontmatter)
    l2_actual = count_tokens(body)

    # frontmatter에서 추정값 추출
    # (level1_tokens 및 level2_tokens 파싱)

    # 비교
    if abs(l1_actual - l1_estimate) > l1_estimate * 0.1:
        print(f"⚠️ Level 1 차이: {l1_actual} vs {l1_estimate}")

    if abs(l2_actual - l2_estimate) > l2_estimate * 0.1:
        print(f"⚠️ Level 2 차이: {l2_actual} vs {l2_estimate}")

# 검증 실행
validate_skill_tokens(".claude/skills/moai-workflow-spec/SKILL.md")
```

### 일반적인 함정

#### 함정 1: 지나치게 광범위한 트리거

**문제**: 거의 모든 프롬프트에 대해 스킬이 로드됨

**예제**:
```yaml
triggers:
  keywords: ["code", "help", "create"]
```

**해결책**: 구체적인 도메인 관련 키워드 사용
```yaml
triggers:
  keywords: ["SPEC", "requirement", "EARS", "specification"]
```

#### 함정 2: 중복된 콘텐츠

**문제**: 동일한 콘텐츠가 여러 스킬에 존재

**예제**:
- `skill-a/SKILL.md`에 Git 기초 포함 (1K 토큰)
- `skill-b/SKILL.md`에 Git 기초 포함 (1K 토큰)
- 총 낭비: 1K 토큰

**해결책**: 기초 스킬로 추출
```yaml
# moai-foundation-git/SKILL.md
---
name: "moai-foundation-git"
# Git 기초 (1K 토큰)
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

#### 함정 3: 불충분한 Quick Reference

**문제**: 사용자가 빠르게 관련성을 평가할 수 없음

**예제**:
```markdown
## Quick Reference

이 스킬은 웹 개발과 관련된 다양한 주제를 다룹니다.
```

**해결책**: 구체적인 이점 및 사용 사례 제공
```markdown
## Quick Reference

**[skill-name]이란 무엇인가?**

React 19 및 Next.js 16 프론트엔드 개발 전문가.

**주요 이점:**
- Server Components 패턴
- App Router 최적화
- 최신 React 훅

**사용 시점:**
- React 19 앱 구축
- Next.js 성능 최적화
- SSR/SSG 구현
```

---

## 예제 및 템플릿

### 예제 1: 간단한 워크플로우 스킬

**파일**: `my-workflow-skill/SKILL.md`

```markdown
---
name: "my-workflow-skill"
description: "팀 코드 리뷰를 위한 커스텀 워크플로우"
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

**my-workflow-skill이란 무엇인가?**

자동화된 검사와 수동 검사 지점을 통해 철저한 코드 리뷰를 수행하기 위한 구조화된 워크플로우.

**주요 이점:**
- 일관된 리뷰 프로세스
- 자동화된 품질 게이트
- 실행 가능한 피드백 형식

**사용 시점:**
- 풀 리퀘스트 병합 전
- 코드 리뷰 세션 중
- 리뷰 표준 수립 시

---

## Implementation Guide

### Step 1: 자동화된 검사

린터 및 테스트 실행:
```bash
ruff check src/
pytest tests/
```

### Step 2: 수동 리뷰

리뷰 체크리스트:
- [ ] 코드가 팀 표준을 따름
- [ ] 테스트가 예외 케이스를 다룸
- [ ] 문서가 업데이트됨

### Step 3: 피드백 제공

건설적인 형식 사용:
- **관찰**: 보이는 것
- **영향**: 중요한 이유
- **제안**: 개선 방법

---

## 잘 작동하는 조합

**관련 스킬:**
- moai-foundation-quality: TRUST 5 검증

**에이전트:**
- manager-quality: 주요 품질 조정자

**명령어:**
- /moai:3-sync: 문서 동기화 워크플로우
```

### 예제 2: 모듈이 있는 언어 스킬

**디렉토리 구조**:
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

**파일**: `my-lang-skill/SKILL.md`

```markdown
---
name: "my-lang-skill"
description: "Rust 1.92+ 개발 전문가"
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

**my-lang-skill이란 무엇인가?**

소유권, 빌림, 비동기 패턴 및 성능 최적화를 다루는 Rust 1.92+ 개발 전문가.

**주요 이점:**
- GC 없는 메모리 안전성
- 제로 비용 추상화
- 두려움 없는 동시성

**사용 시점:**
- 시스템 소프트웨어 구축
- 고성능 애플리케이션
- 안전한 동시 프로그램

**빠른 링크:**
- 구현: #implementation-guide
- 패턴: modules/advanced-patterns.md
- 성능: modules/performance.md
- 예제: examples.md

---

## Implementation Guide

### 핵심 개념

**소유권 규칙**:
1. 각 값은 단일 소유자를 가짐
2. 소유자가 범위를 벗어나면 값이 드롭됨
3. 값은 빌릴 수 있음 (불변 또는 가변)

**예제**:
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1이 s2로 이동됨
    // println!("{}", s1); // 에러: s1이 더 이상 유효하지 않음
    println!("{}", s2); // OK
}
```

### 단계별 프로세스

**Step 1: 프로젝트 설정**
```bash
cargo new my_project
cd my_project
```

**Step 2: 모듈 정의**

모듈 조직 패턴은 modules/advanced-patterns.md를 참조하세요.

**Step 3: 기능 구현**

작동하는 코드 샘플은 examples.md를 참조하세요.

---

## Advanced Topics

### 성능 최적화

상세한 성능 기법은 다음을 참조하세요:
- **modules/performance.md**: 프로파일링, 벤치마킹, 최적화

### 비동기 패턴

async/await 패턴은 다음을 참조하세요:
- **modules/advanced-patterns.md**: Tokio, async-std, futures

---

## 잘 작동하는 조합

**관련 스킬:**
- moai-domain-backend: API 개발 패턴
- moai-foundation-core: TRUST 5 검증

**에이전트:**
- expert-backend: 백엔드 구현
- expert-performance: 성능 최적화
```

**파일**: `my-lang-skill/modules/advanced-patterns.md`

```markdown
# Rust 고급 패턴

**소속**: my-lang-skill
**버전**: 1.0.0
**최종 업데이트**: 2026-01-17

---

## 개요

이 모듈은 다음을 포함한 고급 Rust 패턴을 다룹니다:
- 스마트 포인터 (Box, Rc, Arc, RefCell)
- 트레이트 객체 및 동적 디스패치
- Tokio를 사용한 Async/await 패턴
- 매크로 및 메타프로그래밍

---

## 스마트 포인터

### Box<T>

알 수 없는 크기의 타입에 대한 힙 할당:

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {}", b);
}
```

### Rc<T> 및 Arc<T>

공유 소유권을 위한 참조 카운팅:

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(5);
    let b = Rc::clone(&a);
    println!("count = {}", Rc::strong_count(&a)); // 2
}
```

---

## 비동기 패턴

### Tokio 런타임

```rust
#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("Result: {}", result);
}

async fn fetch_data() -> String {
    // 비동기 작업
    "data".to_string()
}
```

---

## 관련 모듈

- [performance.md](./performance.md): 성능 최적화 기법
- [README.md](./README.md): 모듈 인덱스

---

## 외부 리소스

- [Rust Book](https://doc.rust-lang.org/book/)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
```

### 예제 3: 플랫폼 스킬

**파일**: `my-platform-skill/SKILL.md`

```markdown
---
name: "my-platform-skill"
description: "AWS Lambda 서버리스 전문가"
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

**my-platform-skill이란 무엇인가?**

함수 개발, 이벤트 기반 아키텍처 및 배포 자동화를 다루는 AWS Lambda 서버리스 전문가.

**주요 이점:**
- 제로 서버 관리
- 자동 확장
- 사용량 기반 요금

**사용 시점:**
- 이벤트 기반 시스템 구축
- 서버리스 API
- 백그라운드 처리

**빠른 링크:**
- 구현: #implementation-guide
- 예제: examples.md
- 참조: reference.md

---

## Implementation Guide

### Step 1: Lambda 함수 생성

**Python 예제**:
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
```

**TypeScript 예제**:
```typescript
export const handler = async (event: any) => {
    return {
        statusCode: 200,
        body: 'Hello from Lambda!'
    };
};
```

### Step 2: 함수 배포

AWS SAM 사용:
```bash
sam build
sam deploy --guided
```

### Step 3: 함수 테스트

```bash
aws lambda invoke \
  --function-name my-function \
  --payload '{}' \
  response.json
```

---

## Advanced Topics

### 콜드 스타트 최적화

콜드 스타트 시간을 줄이는 기법:
- 패키지 크기 최소화
- 프로비저닝된 동시성 사용
- 초기화 코드 최적화

상세한 전략은 modules/performance.md를 참조하세요.

### 이벤트 소스

Lambda는 여러 이벤트 소스를 지원합니다:
- API Gateway (REST/HTTP)
- S3 이벤트
- DynamoDB Streams
- SQS/SNS 메시지

통합 패턴은 modules/event-sources.md를 참조하세요.

---

## 잘 작동하는 조합

**관련 스킬:**
- moai-lang-python: Python Lambda 함수
- moai-lang-typescript: TypeScript Lambda 함수

**에이전트:**
- expert-backend: API 구현
- expert-devops: 배포 자동화
```

---

## 문제 해결

### 문제 1: Level 2가 로드되지 않음

**증상**: 프롬프트에 키워드가 있음에도 스킬 본문이 로드되지 않음

**진단**:
1. YAML frontmatter의 트리거 설정 확인
2. 키워드 철자 및 대소문자 확인
3. 에이전트의 `skills:` 필드에 스킬이 나열되어 있는지 확인

**해결책**:
```yaml
# 이전
triggers:
  keywords: ["SPEc"]  # 오타!

# 이후
triggers:
  keywords: ["SPEC", "spec"]  # 양쪽 케이스
```

### 문제 2: 토큰 카운트 불일치

**증상**: 예상 토큰이 실제 사용량과 일치하지 않음

**진단**:
1. 토큰 카운터 사용: https://platform.openai.com/tokenizer
2. YAML frontmatter (Level 1) 또는 전체 본문 (Level 2) 붙여넣기
3. frontmatter의 추정값과 비교

**해결책**:
```yaml
# 추정값 업데이트
progressive_disclosure:
  enabled: true
  level1_tokens: ~110  # 실제 값으로 업데이트
  level2_tokens: ~4850 # 실제 값으로 업데이트
```

### 문제 3: 모듈을 찾을 수 없음

**증상**: Claude가 Level 3 모듈에 액세스할 수 없음

**진단**:
1. 파일이 존재하는지 확인: `ls .claude/skills/skill-name/modules/`
2. SKILL.md의 파일 경로 확인
3. Claude가 Read 도구 액세스 권한이 있는지 확인

**해결책**:
```markdown
<!-- 이전 -->
자세한 내용은 modules/patterns.md를 참조하세요

<!-- 이후 -->
자세한 내용은 다음을 참조하세요:
- **modules/patterns.md**: 디자인 패턴 (Claude가 Read 도구를 통해 액세스 가능)
```

### 문제 4: 스킬이 나타나지 않음

**증상**: 스킬이 전혀 로드되지 않음 (Level 1 또는 2)

**진단**:
1. 스킬 디렉토리 이름이 `name:` 필드와 일치하는지 확인
2. 디렉토리에 SKILL.md가 존재하는지 확인
3. 에이전트가 `skills:` 필드에 스킬을 나열했는지 확인

**해결책**:
```yaml
# 에이전트 frontmatter
---
name: manager-spec
skills: moai-foundation-core, moai-workflow-spec, my-custom-skill
---
```

### 문제 5: 순환 종속성

**증상**: 무한 루프 또는 스택 오버플로우

**진단**:
1. 모든 스킬의 `requires:` 필드 확인
2. 순환 찾기: A가 B를 요구, B가 A를 요구

**해결책**:
```yaml
# 이전 (순환)
# skill-a/SKILL.md
requires: ["skill-b"]

# skill-b/SKILL.md
requires: ["skill-a"]

# 이후 (순환 제거)
# skill-a/SKILL.md
requires: []

# skill-b/SKILL.md
requires: ["skill-a"]
```

---

## 고급 주제

### 커스텀 스킬 카테고리

**새 카테고리 생성**:

1. 프로젝트의 스킬 시스템에 카테고리 정의
2. 스킬 전체에서 일관된 명명 사용
3. 카테고리 목적 문서화

**예제**:
```yaml
category: "custom-domain"  # 커스텀 카테고리
```

**표준 카테고리**:
- `foundation`: 핵심 개념 (TRUST 5, SPEC 등)
- `lang`: 프로그래밍 언어
- `platform`: 클라우드 플랫폼 (AWS, Vercel 등)
- `library`: 라이브러리 (shadcn, Nextra 등)
- `workflow`: 개발 워크플로우
- `domain`: 도메인 스킬 (backend, frontend 등)

### 동적 트리거 조정

**사용 사례**: 사용 패턴에 따라 트리거 조정

**구현**:
1. 어떤 키워드가 스킬 로딩을 트리거하는지 모니터링
2. 트리거해야 하는데 안 하는 사용자 프롬프트 분석
3. `keywords:` 목록을 적절히 업데이트

**예제**:
```yaml
# 초기 트리거
triggers:
  keywords: ["SPEC", "requirement"]

# 분석 후 사용자가 다음과 같이도 말함:
# - "specification"
# - "requirements doc"
# - "req doc"

# 업데이트된 트리거
triggers:
  keywords: ["SPEC", "requirement", "specification", "requirements doc", "req doc"]
```

### 다중 언어 스킬

**사용 사례**: 여러 언어에 적용되는 스킬

**구현**:
```yaml
triggers:
  languages: ["python", "typescript", "javascript", "go"]
```

**조직**:
```
skill-name/
├── SKILL.md               # 언어 무관 콘텐츠
├── modules/
│   ├── python-specific.md
│   ├── typescript-specific.md
│   └── go-specific.md
```

**SKILL.md에서**:
```markdown
## 언어별 패턴

- **Python**: modules/python-specific.md 참조
- **TypeScript**: modules/typescript-specific.md 참조
- **Go**: modules/go-specific.md 참조

Claude는 감지된 언어에 따라 적절한 모듈을 로드합니다.
```

### 스킬 조합

**사용 사례**: 복잡한 작업을 위해 여러 스킬 결합

**패턴 1: 기초 + 전문화**:
```yaml
# specialized-skill/SKILL.md
---
name: "specialized-skill"
requires: ["moai-foundation-core"]  # 기초
optional_requires: ["moai-lang-python"]  # 언어별
---
```

**패턴 2: 워크플로우 + 도메인**:
```yaml
# workflow-skill/SKILL.md
---
name: "workflow-skill"
requires: ["moai-foundation-core"]
optional_requires: [
  "moai-domain-backend",  # 도메인 전문성
  "moai-domain-frontend"
]
---
```

**패턴 3: 플랫폼 + 언어**:
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

### 조건부 모듈 로딩

**사용 사례**: 컨텍스트에 따라 모듈 로드

**SKILL.md에서**:
```markdown
## Advanced Topics

Claude는 필요에 따라 적절한 모듈을 로드합니다:

**성능 최적화**:
- 프로파일링: modules/profiling.md
- 벤치마킹: modules/benchmarking.md
- 캐싱: modules/caching.md

**보안**:
- 인증: modules/auth.md
- 인가: modules/authz.md
- 암호화: modules/crypto.md

필요에 따라 Claude에게 특정 모듈에 액세스하도록 요청하세요.
```

### 스킬 테스트 프레임워크

**테스트 스위트** (Python):
```python
import pytest
from pathlib import Path
import yaml

def load_skill_metadata(skill_path: Path) -> dict:
    """SKILL.md에서 YAML frontmatter 로드"""
    content = skill_path.read_text()
    parts = content.split("---")
    frontmatter = parts[1]
    return yaml.safe_load(frontmatter)

def test_skill_has_required_fields():
    """모든 스킬이 필수 YAML 필드를 가지고 있는지 확인"""
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
                f"{skill_dir.name}/SKILL.md에 필수 필드 누락: {field}"

def test_skill_triggers_are_valid():
    """트리거 설정이 유효한지 확인"""
    skills_dir = Path(".claude/skills")

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        metadata = load_skill_metadata(skill_file)
        triggers = metadata.get("triggers", {})

        # 트리거 타입 확인
        assert isinstance(triggers.get("keywords", []), list)
        assert isinstance(triggers.get("phases", []), list)
        assert isinstance(triggers.get("agents", []), list)
        assert isinstance(triggers.get("languages", []), list)

        # 단계가 유효한지 확인
        valid_phases = ["plan", "run", "sync"]
        for phase in triggers.get("phases", []):
            assert phase in valid_phases, \
                f"{skill_dir.name}에 유효하지 않은 단계: {phase}"

def test_skill_modules_exist():
    """참조된 모듈이 존재하는지 확인"""
    skills_dir = Path(".claude/skills")

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        metadata = load_skill_metadata(skill_file)

        # modularized=true이면 modules 디렉토리가 존재하는지 확인
        if metadata.get("modularized", False):
            modules_dir = skill_dir / "modules"
            assert modules_dir.exists(), \
                f"{skill_dir.name}이 modularized로 표시되었지만 modules/가 없음"

# 테스트 실행
pytest.main([__file__, "-v"])
```

---

## 부록

### A. SKILL.md 체크리스트

스킬 게시 전:

**메타데이터**:
- [ ] `name`이 디렉토리 이름과 일치
- [ ] `description`이 명확하고 간결 (<100자)
- [ ] `version`이 시맨틱 버저닝을 따름
- [ ] `category`가 표준 카테고리 중 하나
- [ ] `modularized`가 구조를 정확히 반영
- [ ] `user-invocable`이 올바르게 설정됨

**Progressive Disclosure**:
- [ ] 토큰 최적화를 위해 `enabled: true`
- [ ] `level1_tokens`이 실제 카운트와 일치 (토크나이저 사용)
- [ ] `level2_tokens`이 실제 카운트와 일치 (토크나이저 사용)

**트리거**:
- [ ] `keywords`가 구체적이고 관련성 있음
- [ ] `phases`가 MoAI 워크플로우 단계와 일치 (해당하는 경우)
- [ ] `agents`가 이 스킬이 필요한 에이전트를 나열
- [ ] `languages`가 관련 프로그래밍 언어를 나열

**종속성**:
- [ ] `requires`가 하드 종속성을 나열
- [ ] `optional_requires`가 선택적 향상을 나열
- [ ] 순환 종속성 없음

**도구**:
- [ ] `allowed-tools`가 스킬이 사용할 수 있는 모든 도구를 나열
- [ ] 도구가 스킬 도메인에 적합

**콘텐츠**:
- [ ] Quick Reference가 즉각적인 가치 제공
- [ ] Implementation Guide에 명확한 단계가 있음
- [ ] Advanced Topics가 Level 3 모듈 참조
- [ ] Works Well With 섹션이 관련 스킬/에이전트를 나열

**모듈** (`modularized: true`인 경우):
- [ ] 작동하는 코드 샘플이 있는 `examples.md` 존재
- [ ] 외부 링크가 있는 `reference.md` 존재
- [ ] `modules/` 디렉토리 존재
- [ ] 모듈 인덱스를 제공하는 `modules/README.md` 존재
- [ ] 참조된 모든 모듈 존재

**테스트**:
- [ ] 에이전트 초기화 시 Level 1에서 스킬 로드
- [ ] 트리거될 때 Level 2에서 스킬 로드
- [ ] 토큰 사용량이 추정값과 일치 (±10%)
- [ ] Read 도구를 통해 모듈 액세스 가능

### B. 토큰 카운터 도구

**온라인 도구**:
- OpenAI Tokenizer: https://platform.openai.com/tokenizer
- Anthropic Console: https://console.anthropic.com/

**Python 라이브러리**:
```bash
pip install tiktoken
```

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Level 1 토큰 카운트
with open(".claude/skills/my-skill/SKILL.md") as f:
    content = f.read()
    parts = content.split("---")
    frontmatter = parts[1]
    print(f"Level 1 토큰: {count_tokens(frontmatter)}")

    body = "---".join(parts[2:])
    print(f"Level 2 토큰: {count_tokens(body)}")
```

**CLI 도구**:
```bash
# 설치
pip install tiktoken-cli

# 토큰 카운트
tiktoken count .claude/skills/my-skill/SKILL.md
```

### C. YAML 문법 참조

**스칼라**:
```yaml
string: "value"
number: 42
boolean: true
null_value: null
```

**리스트**:
```yaml
# 플로우 스타일
keywords: ["keyword1", "keyword2", "keyword3"]

# 블록 스타일
keywords:
  - keyword1
  - keyword2
  - keyword3
```

**주석**:
```yaml
# 이것은 주석입니다
name: "skill-name"  # 인라인 주석
```

**여러 줄 문자열**:
```yaml
# 리터럴 블록 (줄바꿈 유지)
description: |
  여러 줄
  설명으로
  줄바꿈이 유지됩니다.

# 접힌 블록 (줄바꿈을 공백으로 변환)
description: >
  여러 줄
  설명이
  한 줄로 접힙니다.
```

**앵커 및 별칭**:
```yaml
# 앵커 정의
common_tools: &tools
  - Read
  - Write
  - Edit

# 앵커 참조
allowed-tools: *tools
```

### D. 관련 문서

**MoAI-ADK**:
- CLAUDE.md: Alfred 실행 지침
- CLAUDE.local.md: 로컬 개발 가이드
- SKILL_TEMPLATE.md: 빈 스킬 템플릿

**Claude Code**:
- 공식 문서: https://docs.anthropic.com/claude-code
- 스킬 가이드: moai-foundation-claude/SKILL.md
- Sub-Agents 가이드: moai-foundation-claude/reference/sub-agents/

**Progressive Disclosure**:
- CLAUDE.md § 12: Progressive Disclosure 시스템
- moai-foundation-core/modules/progressive-disclosure.md

### E. 용어집

**Agent**: 특정 전문성을 가진 Claude Code 하위 에이전트

**Level 1**: 초기화 중 로드되는 YAML frontmatter (메타데이터) (~100 토큰)

**Level 2**: 트리거가 일치할 때 로드되는 마크다운 본문 (~5K 토큰)

**Level 3**: 온디맨드로 로드되는 번들 파일 (예제, 모듈, 참조) (무제한)

**Module**: `modules/` 디렉토리의 자체 완결적 마크다운 파일

**Progressive Disclosure**: 콘텐츠를 단계별로 로드하는 토큰 최적화 패턴

**Skill**: 전문 지식을 포함하는 구조화된 마크다운 문서 (SKILL.md)

**Trigger**: Level 2가 로드되도록 하는 조건 (keywords, phases, agents, languages)

**User-Invocable**: 사용자가 직접 호출할 수 있는 스킬 (에이전트만이 아님)

---

## 결론

이제 다음에 대한 포괄적인 이해를 갖추셨습니다:
- ✅ SKILL.md 구조 및 목적
- ✅ Progressive Disclosure 3단계 시스템
- ✅ YAML frontmatter 설정
- ✅ 트리거 기반 로딩 메커니즘
- ✅ 모듈화 패턴
- ✅ 토큰 최적화 전략
- ✅ 모범 사례 및 테스트

### 다음 단계

1. **첫 번째 스킬 만들기**:
   ```bash
   mkdir -p .claude/skills/my-first-skill
   cp .claude/skills/SKILL_TEMPLATE.md .claude/skills/my-first-skill/SKILL.md
   # 콘텐츠로 SKILL.md 편집
   ```

2. **스킬 테스트**:
   - Claude Code 열기
   - 트리거 키워드 입력
   - Level 2 로드 확인
   - 토큰 사용량은 /context로 확인

3. **반복 및 개선**:
   - 어떤 키워드가 로딩을 트리거하는지 모니터링
   - 사용량에 따라 트리거 조정
   - 대형 스킬을 모듈로 분할
   - 토큰 추정값 업데이트

4. **스킬 공유**:
   - 팀 저장소에 게시
   - 프로젝트 README에 문서화
   - MoAI-ADK에 제출 (해당하는 경우)

### 지원

- **이슈**: https://github.com/modu-ai/moai-adk/issues
- **토론**: https://github.com/modu-ai/moai-adk/discussions
- **문서**: moai-foundation-claude/SKILL.md

---

**즐거운 스킬 작성 되세요! 🚀**
