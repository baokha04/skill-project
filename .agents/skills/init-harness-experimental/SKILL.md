---
name: init-harness-experimental
description: "Scaffold the Harness v0 operating environment in a project to enable structured agent-driven collaboration. Use when starting a new project, onboarding an agent to a clean repository, or initializing the hoangnb24/harness-experimental repository framework in a target folder."
license: MIT
metadata:
  category: development
  risk: safe
  source: https://github.com/hoangnb24/harness-experimental.git
  date_added: "2026-05-20"
  author: hoangnb24
  tags: [scaffolding, agent-harness, project-init, configuration]
  tools: [claude, cursor, windsurf]
  compatibility: claude-code
---

# Init Harness Experimental

## Overview

This skill enables coding agents to scaffold and configure the Harness v0 operating environment in any target project directory. It integrates the human-agent operating model from `hoangnb24/harness-experimental`, helping agents understand safety lanes, product truth, done definitions, and stories before writing application code.

## When to Use This Skill

- Use when the user asks to "install harness", "initialize harness", "init harness-experimental", or "setup agent operating model".
- Use when starting a new software project to establish clean agent operating procedures.
- Use when onboarding to a new codebase where you want to introduce a robust agent-human operating guide.
- Do **NOT** use if the repository already has an active, custom, established project operating harness that differs from `harness-experimental`.

## Core Concepts of Harness v0

A repository has a harness when it helps agents answer practical questions without relying only on transient chat history:
- **`AGENTS.md`**: The entrypoint, agent task loop, done definitions, and source of truth hierarchy.
- **`docs/HARNESS.md`**: The human-agent operating and collaboration model.
- **`docs/FEATURE_INTAKE.md`**: Classification criteria for tiny, normal, and high-risk work.
- **`docs/ARCHITECTURE.md`**: Architecture rules, boundary definitions, and discovery guides.
- **`docs/TEST_MATRIX.md`**: Behavior-to-proof control panel for status and proof links.
- **`docs/stories/`**: Story templates and active backlog.
- **`docs/decisions/`**: Durable design decisions and trade-offs.

## Installation Workflow

This skill packages the official `install-harness.sh` script to perform safe local setup.

### Step 1: Detect Target Directory and Strategy

Determine the target directory for the harness. By default, it is the workspace root or current directory.
Identify if conflict paths (`AGENTS.md`, `docs/`, `scripts/`) already exist in the target.

### Step 2: Choose Conflict Mode

- **Merge (`--merge`)**: Keep existing files in protected paths intact and install only missing Harness files. This is recommended if you have customized your harness.
- **Override (`--override`)**: Move existing `AGENTS.md`, `docs/`, and `scripts/` paths into a dated folder inside `.harness-backup/` and replace them with fresh harness templates.
- **Stop (`--stop`)**: Refuse to install if any conflict path is found.

### Step 3: Run the Scaffolding Script

You can execute the offline installer script packaged inside this skill:

```powershell
# In PowerShell (Windows)
bash ".agents/skills/init-harness-experimental/scripts/install-harness.sh" --directory "C:\Path\To\Target\Project" --yes --merge
```

```bash
# In Bash (Linux/macOS)
bash ".agents/skills/init-harness-experimental/scripts/install-harness.sh" --directory "/path/to/target/project" --yes --merge
```

Alternatively, you can pull and execute the installer remotely via GitHub:

```bash
curl -fsSL "https://raw.githubusercontent.com/hoangnb24/harness-experimental/main/scripts/install-harness.sh" | bash -s -- --directory "/path/to/target/project" --yes --merge
```

### Options Reference

- `-d, --directory <path>`: Target directory (defaults to current directory).
- `-y, --yes`: Accept defaults and skip prompts (ideal for non-interactive execution).
- `--merge`: Keep existing files on protected-path conflict, only adding missing files.
- `--override`: On protected-path conflict, back up and replace files with default templates.
- `--force`: Overwrite existing files after backing them up.
- `--dry-run`: Preview all changes without writing anything to disk.

## Safety and Best Practices

- Always run in `--dry-run` mode first if the target directory contains active code or custom configuration files.
- Prefer `--merge` over `--override` unless you explicitly want to reset the harness to its default template state.
- After installation, confirm that the files are properly integrated and git-tracked:
  ```bash
  git status
  ```
