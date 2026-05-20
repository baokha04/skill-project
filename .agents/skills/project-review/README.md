# Project Review Agent Skill

A powerful, automated agent skill designed to scan codebase architectures, detect technologies and frameworks, and instantly scaffold a premium, standard-compliant **Harness v0** collaboration environment.

---

## 🌟 Features

- **Codebase Crawling**: Crawls project folders while automatically skipping build, package, and version control directories.
- **Stack & Tool Auto-Detection**: Inspects package manifests (`package.json`, `requirements.txt`, `Cargo.toml`, etc.) to map programming languages, testing frameworks, and tooling.
- **Dynamic Scaffolding**: Automatically populates folder structure, statistics, and tool lists in generated harness markdown documents.
- **Safety Safeguards**: Supports `--dry-run` and interactive approvals to prevent accidental overwrites of existing custom documentation.

---

## 📂 Skill Folder Structure

```
project-review/
├── SKILL.md                 # Main agent instructions, triggers, and workflow decision trees
├── README.md                # This user-facing guide
├── scripts/
│   └── analyze_project.py   # Codebase analyzer and Harness generation engine
└── references/
    └── harness_guidelines.md# Reference documentation outlining Harness v0 principles
```

---

## 🚀 How to Use

### 1. Trigger the Skill
You can ask your agent to trigger this skill using any of the following prompts:
- *"Perform a project review"*
- *"Scan this project architecture"*
- *"Set up our repository operating harness"*
- *"Build the harness docs"*

### 2. Run the Analyzer Manually

You can also execute the included Python engine directly from your terminal:

```bash
# Preview the generated files without writing to disk (Dry Run)
python .agents/skills/project-review/scripts/analyze_project.py --dry-run

# Scan and write the harness files directly, skipping confirmation
python .agents/skills/project-review/scripts/analyze_project.py --yes

# Specify a target directory to scan
python .agents/skills/project-review/scripts/analyze_project.py --directory "/path/to/target/project"
```

---

## 📄 Harness v0 Documents Generated

Upon successful completion, this skill creates:

1. **`AGENTS.md`**: The primary operational dashboard and entrypoint for collaborating AI agents.
2. **`docs/HARNESS.md`**: Defines safety lanes (Tiny, Normal, High-risk work) and workspace guidelines.
3. **`docs/ARCHITECTURE.md`**: Maps out the detected folder boundaries, codebase ratios, and design principles.
4. **`docs/FEATURE_INTAKE.md`**: A decision matrix helping humans and agents classify work scope and risks.
5. **`docs/TEST_MATRIX.md`**: A control panel mapping behaviors to proofs and validation status.

## /grill-me and /goal mode hepler 
```bash
# /grill-me mode: "we are going to implement [feature name or task name], grill me."
# You have to approve by replaying "grill me" again.
# After finish, approve: "use it as our next goal and set_goals" to save it into our harness docs.
# /goal mode
```