# init-harness-experimental Skill

An agent skill that scaffolds and configures the Harness v0 operating environment in any target project directory using [hoangnb24/harness-experimental](https://github.com/hoangnb24/harness-experimental).

## Purpose

Harness v0 is an operating harness for agent-driven software development. It helps coding agents perform work safely and structured by introducing:
- **`AGENTS.md`** - Defining the agent operating rules, source of truth, and done criteria.
- **`docs/`** - Holding features classification, backlog, decisions, architectures, and testing metrics.
- **`scripts/`** - Standard scripts to maintain, merge, and install the harness.

This skill allows the agent to immediately bootstrap this complete operating framework in any project, ensuring that subsequent agent sessions are well-guided, predictable, and compliant with best engineering practices.

## Installation

This skill is pre-installed in the `.agents/skills/init-harness-experimental` directory. 

To activate and use this skill locally, ensure your agent has access to run bash commands, or symlink the skill files globally.

## Usage

You can trigger this skill by asking the agent to install or configure the harness.

### Command Line Examples

#### 1. Dry Run / Preview Changes
Verify what files will be created without modifying the disk:
```bash
bash .agents/skills/init-harness-experimental/scripts/install-harness.sh --directory ./target-project --dry-run
```

#### 2. Clean Installation (Safe Merge)
Install missing harness files without overwriting existing customized code or documents:
```bash
bash .agents/skills/init-harness-experimental/scripts/install-harness.sh --directory ./target-project --yes --merge
```

#### 3. Override Existing Harness
Back up existing files and replace them with fresh default harness templates:
```bash
bash .agents/skills/init-harness-experimental/scripts/install-harness.sh --directory ./target-project --yes --override
```

## Structure

```text
init-harness-experimental/
├── SKILL.md            # Skill specification and triggering rules
├── README.md           # This user-facing guide
├── AGENTS.md           # Agent operating instructions template
├── docs/               # Harness architecture, safety, and backlog templates
└── scripts/
    └── install-harness.sh   # The scaffolding installer script
```

## Safety and Backups

The installer script is fully non-destructive by default. If a conflict occurs with protected files (`AGENTS.md`, `docs/`, or `scripts/`):
1. **Interactive mode**: Prompts you to merge, override, or stop.
2. **Non-interactive mode (`--yes`)**: Fails unless `--merge` or `--override` is explicitly passed.
3. **Backups**: If `--override` or `--force` is used, existing files are safely backed up to `./target-project/.harness-backup/` with a precise timestamp.
