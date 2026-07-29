# Installing ABAP Skills for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- Git installed

## Installation Steps

### 1. Clone ABAP Skills

```bash
git clone https://github.com/likweitan/abap-skills.git ~/.config/opencode/abap-skills
```

### 2. Link Skills

Link each skill into OpenCode's global skills directory. Existing skills with the same name are left unchanged:

```bash
mkdir -p ~/.config/opencode/skills
for source in ~/.config/opencode/abap-skills/skills/*; do
	name=$(basename "$source")
	target="$HOME/.config/opencode/skills/$name"
	if [ -e "$target" ] || [ -L "$target" ]; then
		echo "Skipping existing skill: $name"
		continue
	fi
	ln -s "$source" "$target"
done
```

### 3. Restart OpenCode

Restart OpenCode so it discovers all 18 skills.

Verify by asking: "Use the skill tool to list the available ABAP skills."

## Usage

### Finding Skills

Use OpenCode's native `skill` tool to list available skills:

```
use skill tool to list skills
```

### Loading a Skill

Use OpenCode's native `skill` tool to load a specific skill:

```
use skill tool to load sap-fiori-url-generator
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

Create project-specific skills in `.opencode/skills/` within your project.

Project skills can override global skills with the same name.

## Updating

```bash
cd ~/.config/opencode/abap-skills
git pull
```

The symlinks continue to point to the updated skill directories.

## Troubleshooting

### Skills not found

1. Check a skill symlink: `ls -l ~/.config/opencode/skills/sap-fiori-url-generator`
2. Verify it points to: `~/.config/opencode/abap-skills/skills/sap-fiori-url-generator`
3. Confirm `SKILL.md` exists inside the linked directory
4. Restart OpenCode and use the `skill` tool to list discovered skills

## Getting Help

- Report issues: https://github.com/likweitan/abap-skills/issues
- Full documentation: https://github.com/likweitan/abap-skills/blob/main/docs/README.opencode.md
