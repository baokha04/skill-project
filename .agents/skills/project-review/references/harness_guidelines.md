# Harness v0 Operating Model Guidelines

A software repository has an **Operating Harness** when it equips human-agent pairs with clear boundaries, status, and definitions of done without relying on ephemeral, easily lost chat history. This document defines the components of **Harness v0** and best practices for managing them.

## Core Harness v0 Documents

### 1. `AGENTS.md`
- **Location**: Repository root.
- **Purpose**: The primary operational entrypoint and context hub for AI agents.
- **Target Content**:
  - **Source of Truth Hierarchy**: Explicit order of precedence for documentation files.
  - **Technical Profile**: High-level summary of the codebase stack and folder structure.
  - **Task Loop**: Step-by-step instructions of how the agent discovers tasks, writes plans, executes code, runs tests, and documents walkthroughs.
  - **Definition of Done (DoD)**: List of requirements before a task can be considered complete.

### 2. `docs/HARNESS.md`
- **Location**: `docs/HARNESS.md`.
- **Purpose**: Establishes the human-agent collaboration and safety lanes.
- **Target Content**:
  - **Operating Lanes**: Rules for safe execution based on risk.
  - **Safety Categorizations**:
    - **Tiny/Low-Risk**: Self-approving, direct edits.
    - **Normal-Risk**: Upfront design + planning artifact (`implementation_plan.md`) + approval + TDD.
    - **High-Risk**: High architectural review + ADR + test scenarios + rigorous human sign-off.
  - **Workspace Hygiene**: Rules regarding TODOs, git commit conventions, and minimal diffs.

### 3. `docs/ARCHITECTURE.md`
- **Location**: `docs/ARCHITECTURE.md`.
- **Purpose**: High-level architectural map and rules of the road.
- **Target Content**:
  - **Directory Map**: Details on what each primary folder does and what boundaries should be respected.
  - **Tech Stack & Libraries**: Detailed lists of technologies, frameworks, and packages.
  - **Architecture Principles**: Module separation, data layers, style guides, and language specifications.

### 4. `docs/FEATURE_INTAKE.md`
- **Location**: `docs/FEATURE_INTAKE.md`.
- **Purpose**: The decision matrix used to classify upcoming work by risk.
- **Target Content**:
  - **Risk Classification Matrix**: A table mapping impact radius, data touches, breaking potential, and dependencies to safety levels.
  - **Protocol Details**: Detailed checklist of what an agent must do for each level of risk.

### 5. `docs/TEST_MATRIX.md`
- **Location**: `docs/TEST_MATRIX.md`.
- **Purpose**: The behavior-to-proof control panel verifying that the system acts exactly as specified.
- **Target Content**:
  - **Test Matrix Table**: Tracks story IDs, descriptions, environment, verification method (Unit, Integration, E2E, Manual), status, and proof links (pointing to walkthroughs or CI runs).
  - **Manual Verification Guide**: Clear procedures for recording manual proofs when automated testing is not feasible.

---

## Best Practices for Agent-Human Collaboration

1. **Keep Harness Documents Up to Date**: As components are refactored or new dependencies added, the agent should update `docs/ARCHITECTURE.md` and `AGENTS.md`.
2. **Strict Planning**: Never execute normal/high-risk tasks without preparing the `implementation_plan.md` artifact and waiting for explicit user approval.
3. **No Slop**: Avoid inserting placeholders, incomplete templates, or "TODO" comments. Code and documentation must be fully complete and functional.
4. **Behavior-to-Proof Tracking**: Every non-trivial change must be accompanied by explicit test runs or logs posted as proof in `docs/TEST_MATRIX.md`.
