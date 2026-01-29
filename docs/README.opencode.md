# ABAP Skills for OpenCode

Complete guide for using ABAP Skills with [OpenCode.ai](https://opencode.ai).

## Quick Install

Tell OpenCode:

```
Clone https://github.com/likweitan/abap-skills to ~/.config/opencode/abap-skills, then create directory ~/.config/opencode/skills, then symlink ~/.config/opencode/abap-skills/skills to ~/.config/opencode/skills/abap-skills, then restart opencode.
```

## Manual Installation

### Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- Git installed

### macOS / Linux

```bash
# 1. Install ABAP Skills (or update existing)
if [ -d ~/.config/opencode/abap-skills ]; then
  cd ~/.config/opencode/abap-skills && git pull
else
  git clone https://github.com/likweitan/abap-skills.git ~/.config/opencode/abap-skills
fi

# 2. Create skills directory
mkdir -p ~/.config/opencode/skills

# 3. Remove old symlink if it exists
rm -rf ~/.config/opencode/skills/abap-skills

# 4. Create symlink
ln -s ~/.config/opencode/abap-skills/skills ~/.config/opencode/skills/abap-skills

# 5. Restart OpenCode
```

#### Verify Installation

```bash
ls -l ~/.config/opencode/skills/abap-skills
```

Should show a symlink pointing to the abap-skills/skills directory.

### Windows

**Prerequisites:**
- Git installed
- Either **Developer Mode** enabled OR **Administrator privileges**
  - Windows 10: Settings → Update & Security → For developers
  - Windows 11: Settings → System → For developers

Pick your shell below: [Command Prompt](#command-prompt) | [PowerShell](#powershell) | [Git Bash](#git-bash)

#### Command Prompt

Run as Administrator, or with Developer Mode enabled:

```cmd
:: 1. Install ABAP Skills
git clone https://github.com/likweitan/abap-skills.git "%USERPROFILE%\.config\opencode\abap-skills"

:: 2. Create skills directory
mkdir "%USERPROFILE%\.config\opencode\skills" 2>nul

:: 3. Remove existing link (safe for reinstalls)
rmdir "%USERPROFILE%\.config\opencode\skills\abap-skills" 2>nul

:: 4. Create skills junction (works without special privileges)
mklink /J "%USERPROFILE%\.config\opencode\skills\abap-skills" "%USERPROFILE%\.config\opencode\abap-skills\skills"

:: 5. Restart OpenCode
```

#### PowerShell

Run as Administrator, or with Developer Mode enabled:

```powershell
# 1. Install ABAP Skills
git clone https://github.com/likweitan/abap-skills.git "$env:USERPROFILE\.config\opencode\abap-skills"

# 2. Create skills directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\skills"

# 3. Remove existing link (safe for reinstalls)
Remove-Item "$env:USERPROFILE\.config\opencode\skills\abap-skills" -Force -ErrorAction SilentlyContinue

# 4. Create skills junction (works without special privileges)
New-Item -ItemType Junction -Path "$env:USERPROFILE\.config\opencode\skills\abap-skills" -Target "$env:USERPROFILE\.config\opencode\abap-skills\skills"

# 5. Restart OpenCode
```

#### Git Bash

Note: Git Bash's native `ln` command copies files instead of creating symlinks. Use `cmd //c mklink` instead (the `//c` is Git Bash syntax for `/c`).

```bash
# 1. Install ABAP Skills
git clone https://github.com/likweitan/abap-skills.git ~/.config/opencode/abap-skills

# 2. Create skills directory
mkdir -p ~/.config/opencode/skills

# 3. Remove existing link (safe for reinstalls)
rm -rf ~/.config/opencode/skills/abap-skills 2>/dev/null

# 4. Create skills junction (works without special privileges)
cmd //c "mklink /J \"$(cygpath -w ~/.config/opencode/skills/abap-skills)\" \"$(cygpath -w ~/.config/opencode/abap-skills/skills)\""

# 5. Restart OpenCode
```

#### WSL Users

If running OpenCode inside WSL, use the [macOS / Linux](#macos--linux) instructions instead.

#### Verify Installation

**Command Prompt:**
```cmd
dir /AL "%USERPROFILE%\.config\opencode\skills"
```

**PowerShell:**
```powershell
Get-ChildItem "$env:USERPROFILE\.config\opencode\skills" | Where-Object { $_.LinkType }
```

Look for `<JUNCTION>` in the output.

#### Troubleshooting Windows

**"You do not have sufficient privilege" error:**
- Enable Developer Mode in Windows Settings, OR
- Right-click your terminal → "Run as Administrator"

**"Cannot create a file when that file already exists":**
- Run the removal commands (step 3) first, then retry

**Symlinks not working after git clone:**
- Run `git config --global core.symlinks true` and re-clone

## Usage

### Finding Skills

Use OpenCode's native `skill` tool to list all available skills:

```
use skill tool to list skills
```

### Loading a Skill

Use OpenCode's native `skill` tool to load a specific skill:

```
use skill tool to load abap-skills/released-abap-classes
use skill tool to load abap-skills/clean-abap
use skill tool to load abap-skills/sap-fiori-apps-reference
```

### Available Skills

#### Released ABAP Classes
Quick reference for released ABAP classes in ABAP Cloud Development:
```
What is the released class for sending email?
Give me the class for UUID generation
Show me classes for JSON processing
```

#### Clean ABAP
Check ABAP code for compliance with Clean ABAP principles:
```
Check this ABAP code for clean code compliance
Review my ABAP method for best practices
```

#### SAP Fiori Apps Reference
Generate SAP Fiori Launchpad URLs:
```
Generate URL for Create Maintenance Request app
Find apps related to 'Workflow'
```

### Personal Skills

Create your own skills in `~/.config/opencode/skills/`:

```bash
mkdir -p ~/.config/opencode/skills/my-skill
```

Create `~/.config/opencode/skills/my-skill/SKILL.md`:

```markdown
---
name: my-skill
description: Use when [condition] - [what it does]
---

# My Skill

[Your skill content here]
```

### Project Skills

Create project-specific skills in your OpenCode project:

```bash
# In your OpenCode project
mkdir -p .opencode/skills/my-project-skill
```

Create `.opencode/skills/my-project-skill/SKILL.md`:

```markdown
---
name: my-project-skill
description: Use when [condition] - [what it does]
---

# My Project Skill

[Your skill content here]
```

## Skill Locations

OpenCode discovers skills from these locations:

1. **Project skills** (`.opencode/skills/`) - Highest priority
2. **Personal skills** (`~/.config/opencode/skills/`)
3. **ABAP Skills** (`~/.config/opencode/skills/abap-skills/`) - via symlink

## Features

### Native Skills Integration

ABAP Skills uses OpenCode's native `skill` tool for skill discovery and loading. Skills are symlinked into `~/.config/opencode/skills/abap-skills/` so they appear alongside your personal and project skills.

### Available Skills

- **released-abap-classes**: Reference for 50+ released ABAP classes in ABAP Cloud Development
- **clean-abap**: Code analysis for Clean ABAP principles compliance
- **sap-fiori-apps-reference**: SAP Fiori Launchpad URL generation and app lookup

## Updating

```bash
cd ~/.config/opencode/abap-skills
git pull
```

Restart OpenCode to load the updates.

## Troubleshooting

### Skills not found

1. Verify skills symlink: `ls -l ~/.config/opencode/skills/abap-skills` (should point to abap-skills/skills/)
2. Use OpenCode's `skill` tool to list available skills
3. Check skill structure: each skill needs a `SKILL.md` file with valid frontmatter

### Windows: Module not found error

If you see `Cannot find module` errors on Windows:
- **Cause:** Git Bash `ln -sf` copies files instead of creating symlinks
- **Fix:** Use `mklink /J` directory junctions instead (see Windows installation steps)

## Getting Help

- Report issues: https://github.com/likweitan/abap-skills/issues
- Main documentation: https://github.com/likweitan/abap-skills
- OpenCode docs: https://opencode.ai/docs/

## Testing

Verify your installation:

```bash
# Check skills are discoverable
opencode run "use skill tool to list all skills" 2>&1 | grep -i abap-skills

# Test released ABAP classes skill
opencode run "What is the released class for sending email?"

# Test Clean ABAP skill
opencode run "Check this ABAP code: DATA lv_x TYPE i."

# Test Fiori apps skill
opencode run "Find Fiori apps related to maintenance"
```

The agent should be able to access and use the ABAP skills.