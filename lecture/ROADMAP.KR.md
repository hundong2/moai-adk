# 🎓 Claude Code & MoAI-ADK 마스터 클래스

**MoAI-ADK 마스터 클래스**에 오신 것을 환영합니다. 이 강의 시리즈는 Claude Code에 대한 기초적인 이해부터 **에이전틱 워크플로우 아키텍트(Agentic Workflow Architect)**가 되기까지의 과정을 안내합니다.

이 과정에서 여러분은 MoAI-ADK 프레임워크를 사용하여 AI 에이전트를 구축하고, 지휘하고, 확장하는 방법을 배우게 됩니다.

## 🗺️ 커리큘럼 로드맵

### **챕터 1: 기초 (The Foundation)**
> **주제**: MoAI-ADK의 "이유(Why)"와 "방법(How)" 이해하기.
- [ ] **[챕터 01: 아키텍처 및 철학](./Chapter_01_Architecture.md)**
    - "에이전틱(Agentic)" 개발이란 무엇인가?
    - `src`와 `agentskills` 구조 심층 분석.
    - "두뇌(Brain)"와 "신체(Body)"의 분리 이해.

### **챕터 2: 스킬 제작자 (The Skill Smith)**
> **주제**: 토큰 예산을 폭파시키지 않고 AI에게 새로운 기술 가르치기.
- [ ] **[챕터 02: 스킬 저작 & 점진적 공개](./Chapter_02_Skill_Authoring.md)**
    - `SKILL.md`의 해부학.
    - **점진적 공개(Progressive Disclosure)**가 토큰의 90%를 절약하는 방법.
    - **실습**: 3단계 로딩을 적용한 `my-first-skill` 만들기.

### **챕터 3: 오케스트레이터 (The Orchestrator)**
> **주제**: 전문 에이전트 군단 지휘하기.
- [ ] **[챕터 03: 커스텀 에이전트 & 페르소나](./Chapter_03_Custom_Agents.md)**
    - `agentskills`에서 에이전트 페르소나 정의하기.
    - 라우팅 로직: MoAI가 누가 무엇을 할지 결정하는 방법.
    - **실습**: 전문화된 "리뷰어 에이전트" 구축하기.

### **챕터 4: 사령관 (The Commander)**
> **주제**: CLI 및 워크플로우 루프 마스터하기.
- [ ] **[챕터 04: 워크플로우 마스터리](./Chapter_04_Workflow_Mastery.md)**
    - `plan` -> `run` -> `sync` 사이클.
    - 자율 실행을 위한 `/moai:alfred` 사용법.
    - 자가 치유(Self-healing) `/moai:loop`.

### **챕터 5: 아키텍트 (The Architect)**
> **주제**: 개인화 및 고급 지식 주입.
- [ ] **[챕터 05: 개인화 & "나만의 두뇌"](./Chapter_05_Personalization.md)**
    - `.claude/settings.json` 커스터마이징.
    - 품질 강제를 위한 Git 훅(Hooks).
    - 시스템에 나만의 엔지니어링 DNA 주입하기.

---

## 🎯 시작하기

**[챕터 01: 아키텍처 및 철학](./Chapter_01_Architecture.md)**을 열어 시작하세요.
각 챕터는 이전 개념을 바탕으로 진행되므로 순서대로 수강하는 것을 권장합니다.

> **팁**: Claude를 활용해 보세요! 다음과 같이 말해보세요:
> *"Claude, 챕터 1을 읽고 핵심 내용을 요약해줘."*
