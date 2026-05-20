#!/usr/bin/env python3
import os
import sys
import json
import argparse
from pathlib import Path
import re

# Ensure console output supports UTF-8 on Windows and other environments
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Ignore lists for directory traversal
IGNORED_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', 'env', '.env', 'dist', 'build', 
    'target', 'bin', 'obj', '.gradle', '.idea', '.vscode', '.gemini', 
    '__pycache__', 'out', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'
}

IGNORED_FILES = {
    '.DS_Store', 'thumbs.db', 'desktop.ini'
}

EXTENSION_MAP = {
    '.js': 'JavaScript',
    '.jsx': 'React JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'React TypeScript',
    '.py': 'Python',
    '.rs': 'Rust',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C',
    '.h': 'C/C++ Header',
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.swift': 'Swift',
    '.php': 'PHP',
    '.html': 'HTML',
    '.css': 'CSS',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.sh': 'Shell Script',
    '.ps1': 'PowerShell Script',
    '.bat': 'Batch Script',
    '.sql': 'SQL',
    '.gradle': 'Gradle Build',
    '.xml': 'XML'
}

def scan_project(root_path):
    """Scans the directory structure and gathers codebase statistics."""
    root = Path(root_path).resolve()
    stats = {
        'files_by_ext': {},
        'file_counts': 0,
        'total_size_bytes': 0,
        'dirs': [],
        'config_files': [],
        'languages': set(),
        'frameworks': set()
    }
    
    # Get immediate subdirectories in root
    try:
        for p in root.iterdir():
            if p.is_dir() and p.name not in IGNORED_DIRS:
                stats['dirs'].append(p.name)
    except Exception as e:
        print(f"⚠️ Error reading root directory: {e}")
        return stats

    # Traverse all files
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out ignored directories in-place
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        
        rel_dir = os.path.relpath(dirpath, root)
        
        for fname in filenames:
            if fname in IGNORED_FILES:
                continue
                
            fpath = Path(dirpath) / fname
            
            # Check for config files
            if fname in ['package.json', 'requirements.txt', 'pyproject.toml', 'Cargo.toml', 
                         'go.mod', 'Gemfile', 'pom.xml', 'build.gradle', 'composer.json']:
                stats['config_files'].append(os.path.join(rel_dir, fname) if rel_dir != '.' else fname)
            
            try:
                fsize = fpath.stat().st_size
                ext = fpath.suffix.lower()
                
                stats['file_counts'] += 1
                stats['total_size_bytes'] += fsize
                
                if ext in EXTENSION_MAP:
                    lang = EXTENSION_MAP[ext]
                    stats['files_by_ext'][lang] = stats['files_by_ext'].get(lang, 0) + 1
                    stats['languages'].add(lang)
            except Exception:
                pass
                
    return stats

def detect_tech_stack(root_path, stats):
    """Detects languages, frameworks, and packages from configuration files."""
    root = Path(root_path).resolve()
    frameworks = set()
    
    # Process package.json
    package_json_path = root / 'package.json'
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                
                # Check for UI frameworks
                if 'react' in deps: frameworks.add('React')
                if 'vue' in deps: frameworks.add('Vue')
                if 'angular' in deps: frameworks.add('Angular')
                if 'next' in deps: frameworks.add('Next.js')
                if 'nuxt' in deps: frameworks.add('Nuxt.js')
                if 'svelte' in deps: frameworks.add('Svelte')
                
                # Check for backend frameworks
                if 'express' in deps: frameworks.add('Express')
                if '@nestjs/core' in deps: frameworks.add('NestJS')
                if 'fastify' in deps: frameworks.add('Fastify')
                if 'koa' in deps: frameworks.add('Koa')
                
                # Tools
                if 'typescript' in deps: frameworks.add('TypeScript')
                if 'eslint' in deps: frameworks.add('ESLint')
                if 'prettier' in deps: frameworks.add('Prettier')
                if 'jest' in deps: frameworks.add('Jest')
                if 'mocha' in deps: frameworks.add('Mocha')
                if 'tailwindcss' in deps: frameworks.add('TailwindCSS')
        except Exception:
            pass

    # Process requirements.txt
    req_txt_path = root / 'requirements.txt'
    if req_txt_path.exists():
        try:
            with open(req_txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'flask' in content.lower(): frameworks.add('Flask')
                if 'django' in content.lower(): frameworks.add('Django')
                if 'fastapi' in content.lower(): frameworks.add('FastAPI')
                if 'sqlalchemy' in content.lower(): frameworks.add('SQLAlchemy')
                if 'pytest' in content.lower(): frameworks.add('pytest')
        except Exception:
            pass

    # Process pyproject.toml
    pyproject_toml_path = root / 'pyproject.toml'
    if pyproject_toml_path.exists():
        try:
            with open(pyproject_toml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'poetry' in content.lower(): frameworks.add('Poetry')
                if 'django' in content.lower(): frameworks.add('Django')
                if 'fastapi' in content.lower(): frameworks.add('FastAPI')
                if 'black' in content.lower(): frameworks.add('Black')
        except Exception:
            pass

    # Process Cargo.toml
    cargo_toml_path = root / 'Cargo.toml'
    if cargo_toml_path.exists():
        try:
            with open(cargo_toml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'tokio' in content.lower(): frameworks.add('Tokio')
                if 'actix' in content.lower(): frameworks.add('Actix Web')
                if 'axum' in content.lower(): frameworks.add('Axum')
                if 'serde' in content.lower(): frameworks.add('Serde')
        except Exception:
            pass

    # Process go.mod
    go_mod_path = root / 'go.mod'
    if go_mod_path.exists():
        try:
            with open(go_mod_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'gin-gonic' in content.lower(): frameworks.add('Gin')
                if 'fiber' in content.lower(): frameworks.add('Fiber')
                if 'beego' in content.lower(): frameworks.add('Beego')
        except Exception:
            pass

    # Process Gemfile
    gemfile_path = root / 'Gemfile'
    if gemfile_path.exists():
        try:
            with open(gemfile_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'rails' in content.lower(): frameworks.add('Ruby on Rails')
                if 'sinatra' in content.lower(): frameworks.add('Sinatra')
        except Exception:
            pass

    stats['frameworks'] = frameworks
    return stats

def generate_agents_md(stats, project_name):
    """Generates the contents for AGENTS.md."""
    frameworks_str = ", ".join(sorted(stats['frameworks'])) if stats['frameworks'] else "None detected"
    dirs_str = "\n".join([f"- **`{d}/`**: Core component folder." for d in sorted(stats['dirs'])])
    
    return f"""# AGENTS.md - Agent Operations Entrypoint

Welcome to **{project_name}**! This document serves as the primary operational entrypoint and context hub for AI coding agents collaborating on this codebase.

## Source of Truth Hierarchy

When resolving conflicts or understanding project status, trust files in the following order:
1. **`AGENTS.md`** (This file - high-level status, agent task loop, done definitions)
2. **`docs/ARCHITECTURE.md`** (Architecture boundaries, directory layout, language conventions)
3. **`docs/HARNESS.md`** (Operating lanes and communication rules)
4. **`docs/TEST_MATRIX.md`** (Testing and verification controls)
5. **Codebase Files** (Active source code, test suites, configuration files)

---

## Technical Profile

- **Detected Languages**: {", ".join(sorted(stats['languages'])) if stats['languages'] else "None detected"}
- **Detected Frameworks**: {frameworks_str}
- **Primary Directories**:
{dirs_str if dirs_str else "- No primary subdirectories detected."}

---

## Agent Task Loop

To maintain maximum safety, transparency, and high quality, follow this task loop:
1. **Discover & Align**: Read `AGENTS.md` and check active tickets/backlog in `docs/stories/`.
2. **Plan & Draft**:
   - Create or update the `implementation_plan.md` artifact.
   - For any normal or high-risk task, obtain human approval before starting code edits.
3. **Execute & Test**:
   - Create `task.md` to track progress.
   - Follow Test-Driven Development (TDD) principles. Implement tests first, verify, then write code.
   - Update `docs/TEST_MATRIX.md` with behavioral coverage and proof links.
4. **Verify & Review**:
   - Generate `walkthrough.md` to show diffs and test logs.
   - Run linter/type checks and ensure zero regression.

---

## Definition of Done (DoD)

A task is considered fully **DONE** when and only when:
- [ ] **Implementation**: Code meets the requirements perfectly.
- [ ] **Quality**: Zero linting, formatting, or compiler errors.
- [ ] **Testing**: Unit, integration, or manual verification is fully implemented. Tests pass.
- [ ] **Documentation**: Harness documentation is updated.
- [ ] **Walkthrough**: A comprehensive `walkthrough.md` is provided.
- [ ] **Tracking**: The story is marked completed.
"""

def generate_harness_md(project_name):
    """Generates the contents for docs/HARNESS.md."""
    return f"""# HARNESS.md - Human-Agent Operating Model

This document outlines the collaboration guidelines, safety levels, and operations for human-agent pairing in the **{project_name}** repository.

## Collaboration Guidelines

1. **Clear Boundaries**: The agent operates within the guidelines set out by the harness docs.
2. **Feedback Loop**: For complex changes, the agent requests feedback and waits for approval.
3. **Code Safety**: The agent must avoid breaking existing production code and run tests locally.
4. **Continuous Improvement (Kaizen)**: Always improve documentation, comments, and structure.

## Safety Lanes & Work Classification

We classify all engineering work into three safety categories:

### 1. Tiny/Low-Risk Work
- **Definition**: Cosmetic changes, spelling fixes, simple comment updates, minor formatting, or additions of simple utility functions with zero side-effects.
- **Protocol**: Direct execution allowed. No formal planning or upfront approval is needed.

### 2. Normal-Risk Work
- **Definition**: Minor feature implementations, bug fixes, refactoring a single file, adding unit tests, or upgrading non-breaking packages.
- **Protocol**: Requires a clear draft of changes. The agent must create an `implementation_plan.md` and obtain approval before editing files.

### 3. High-Risk Work
- **Definition**: Major architectural shifts, database schema migrations, package upgrades with breaking changes, changes to core modules or security layers.
- **Protocol**: Requires extensive architecture review, comprehensive testing strategy, explicit sign-off on the `implementation_plan.md`, and strict verification.

---

## Workspace Hygiene

- **No Placeholders**: Never write TODOs or placeholders in production files; write complete, functional implementations.
- **Git Commit Etiquette**: Generate clean conventional commit messages.
- **Clean Diffs**: Avoid modifying unrelated lines of code to maintain clean git histories.
"""

def generate_architecture_md(stats, project_name):
    """Generates the contents for docs/ARCHITECTURE.md."""
    # List files by extension
    ext_ranking = sorted(stats['files_by_ext'].items(), key=lambda x: x[1], reverse=True)
    ext_ranking_str = "\n".join([f"- **{lang}**: {count} file(s)" for lang, count in ext_ranking])
    
    config_files_str = "\n".join([f"- `{cfg}`" for cfg in sorted(stats['config_files'])])
    
    return f"""# ARCHITECTURE.md - Codebase Architecture Guide

This document describes the architectural layout, technology stack, and engineering conventions of the **{project_name}** project.

## Directory Layout & Key Components

Below is the directory map of this workspace, detailing the purpose and boundaries of each folder:

- **`AGENTS.md`**: Operations entrypoint and task loops.
- **`docs/`**: Central repository for all design, decision, story, and harness documentation.
  - **`docs/decisions/`**: Durable Architecture Decision Records (ADRs).
  - **`docs/stories/`**: Story definitions and requirements backlog.
- **`.agents/`**: Repository configuration, skills, and templates.

### Project Folders
{chr(10).join([f"- **`{d}/`**: Subfolder containing parts of the codebase." for d in sorted(stats['dirs'])]) if stats['dirs'] else "- No primary subfolders detected."}

---

## Technology Stack Profile

### Codebase Composition
{ext_ranking_str if ext_ranking_str else "- No files found."}

### Detected Config & Tool Files
{config_files_str if config_files_str else "- No configuration files detected."}

---

## Architecture Principles & Boundaries

1. **Separation of Concerns**: Keep business logic separated from presentation layers and framework delivery mechanisms.
2. **Modularity**: Design components to be cohesive, loosely-coupled, and highly testable.
3. **Safety Lanes**: Do not introduce circular dependencies. Respect directory boundaries.
4. **Style Guides**: Match the surrounding formatting conventions. If the project contains ESLint, Prettier, or PEP8 configs, format exactly according to those rules.
"""

def generate_feature_intake_md():
    """Generates the contents for docs/FEATURE_INTAKE.md."""
    return """# FEATURE_INTAKE.md - Work Classification Matrix

This document helps agents and human reviewers classify any new task or feature request, directing the agent to the appropriate safety protocol.

## Intake Decision Matrix

Use the matrix below to classify a task:

| Criteria | Tiny / Low-Risk | Normal-Risk | High-Risk |
|---|---|---|---|
| **Impact Radius** | Single line, comment, or local utility | Single module, service, or interface | Multi-system, database, or shared core |
| **Data Touch** | Read-only / no data operations | Modifies non-critical database fields | Modifies critical tables or schemas |
| **Breaking Potential** | Zero chance | Low, isolated behind flags or scopes | High potential for regression |
| **Dependencies** | No new imports or libraries | Adds standard, well-verified utility | Introduces new complex middleware |

---

## Action Plan by Risk Level

### Tiny/Low-Risk
- **Steps**:
  1. Make the change directly.
  2. Test locally.
  3. Commit and request human review.

### Normal-Risk
- **Steps**:
  1. Write down an `implementation_plan.md` in your artifact folder.
  2. Ask the user for explicit approval on the plan.
  3. Scaffold unit/integration tests representing the behavioral expectations.
  4. Write implementation code.
  5. Run test suites and verify.

### High-Risk
- **Steps**:
  1. Draft a comprehensive design document in `docs/decisions/` or in the `implementation_plan.md` outlining architectural alternatives.
  2. Conduct a detailed review of data safety, failure modes, and recovery paths.
  3. Request design sign-off.
  4. Write failing tests covering critical edge-cases.
  5. Implement changes in atomic, easily-reviewable commits.
  6. Perform exhaustive integration testing.
"""

def generate_test_matrix_md():
    """Generates the contents for docs/TEST_MATRIX.md."""
    return """# TEST_MATRIX.md - Behavior Verification Control Panel

This document tracks behavior specifications, verification methods, and evidence to prove the correctness of implemented work.

## Testing Strategy & Standards

- **TDD (Test-Driven Development)**: Whenever possible, implement failing tests before writing production code.
- **Coverage**: Aim for high test coverage on core business logic.
- **Evidence**: Provide clear, copy-pastable test execution logs or screenshots in your `walkthrough.md`.

## Verification Status

| Feature ID / Story | Description | Target Environment | Verification Method | Status | Proof / Evidence Link |
|---|---|---|---|---|---|
| *Sample-01* | Example feature validation | Local | Unit + Integration tests | `Passed` | [Walkthrough Link](walkthrough.md) |

---

## Manual Verification Guidelines

When automated tests are not fully viable (e.g. certain UI/UX interactions or external integrations):
1. **Prepare Scenarios**: Document the exact, step-by-step user actions to take.
2. **Execute & Record**: Capture logs, outputs, or screenshots.
3. **Save Artifacts**: Store evidence files under `docs/` or within the conversation walkthrough.
"""

def main():
    parser = argparse.ArgumentParser(description="Scan codebase and generate Harness v0 docs.")
    parser.add_argument("--directory", "-d", default=".", help="Target project directory (defaults to current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Scan codebase and preview files without writing them to disk")
    parser.add_argument("--yes", "-y", action="store_true", help="Automatically write files without interactive confirmation")
    args = parser.parse_args()
    
    target_dir = Path(args.directory).resolve()
    print(f"🔍 Scanning project in: {target_dir}")
    
    if not target_dir.exists():
        print(f"❌ Error: Target directory '{target_dir}' does not exist.")
        sys.exit(1)
        
    stats = scan_project(target_dir)
    stats = detect_tech_stack(target_dir, stats)
    
    project_name = target_dir.name
    # Clean project name if it is empty or dot
    if project_name in ['.', '']:
        project_name = "Target Project"
    
    print("\n📊 Project Scan Summary:")
    print(f"   Name: {project_name}")
    print(f"   Files counted: {stats['file_counts']}")
    print(f"   Total size: {stats['total_size_bytes'] / (1024*1024):.2f} MB")
    print(f"   Languages found: {', '.join(sorted(stats['languages'])) if stats['languages'] else 'None detected'}")
    print(f"   Frameworks/Tools: {', '.join(sorted(stats['frameworks'])) if stats['frameworks'] else 'None detected'}")
    print(f"   Primary folders: {', '.join(sorted(stats['dirs'])) if stats['dirs'] else 'None detected'}")
    print(f"   Config files found: {', '.join(sorted(stats['config_files'])) if stats['config_files'] else 'None'}")
    
    # Pre-render files
    files_to_write = {
        target_dir / 'AGENTS.md': generate_agents_md(stats, project_name),
        target_dir / 'docs' / 'HARNESS.md': generate_harness_md(project_name),
        target_dir / 'docs' / 'ARCHITECTURE.md': generate_architecture_md(stats, project_name),
        target_dir / 'docs' / 'FEATURE_INTAKE.md': generate_feature_intake_md(),
        target_dir / 'docs' / 'TEST_MATRIX.md': generate_test_matrix_md()
    }
    
    if args.dry_run:
        print("\n✨ DRY RUN ACTIVE - Previewing generated Harness docs:")
        for path, content in files_to_write.items():
            rel_path = path.relative_to(target_dir)
            print(f"\n==================================================")
            print(f"📄 PREVIEW: {rel_path}")
            print(f"==================================================")
            # Show first 15 lines of content
            lines = content.split('\n')
            preview = "\n".join(lines[:15])
            print(preview)
            if len(lines) > 15:
                print(f"... ({len(lines) - 15} more lines)")
        print("\n✅ Dry run completed. No files were created or modified.")
        sys.exit(0)
        
    print("\n🛠️ Preparing to write Harness v0 files:")
    for path in files_to_write.keys():
        status = "Will overwrite" if path.exists() else "Will create"
        print(f"   - {path.relative_to(target_dir)} ({status})")
        
    if not args.yes:
        confirm = input("\nWrite these files? [y/N]: ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Operation cancelled.")
            sys.exit(0)
            
    # Ensure docs directory exists
    docs_dir = target_dir / 'docs'
    try:
        docs_dir.mkdir(exist_ok=True)
        # Ensure decisions and stories subfolders exist too
        (docs_dir / 'decisions').mkdir(exist_ok=True)
        (docs_dir / 'stories').mkdir(exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating docs directories: {e}")
        sys.exit(1)
        
    # Write files
    for path, content in files_to_write.items():
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Wrote: {path.relative_to(target_dir)}")
        except Exception as e:
            print(f"❌ Error writing to {path}: {e}")
            
    print("\n🎉 Harness v0 docs successfully built!")
    print("🚀 You can now commit these docs to git and begin using Harness operating lanes!")

if __name__ == "__main__":
    main()
