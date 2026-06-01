# ABAP Skills for GitHub Copilot in VS Code

Complete guide for using ABAP Skills with [GitHub Copilot](https://github.com/features/copilot) in [Visual Studio Code](https://code.visualstudio.com/).

## Quick Install

Tell GitHub Copilot Chat in VS Code:

```text
Clone https://github.com/likweitan/abap-skills to a local folder, then use the relevant skill files under skills/ as context when answering ABAP, RAP, CDS, OData, ABAP Cloud, Clean ABAP, and SAP BTP questions.
```

For reusable prompts, follow the manual setup below.

## Manual Installation

### Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) installed
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) installed
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) installed, if your VS Code version does not include chat with Copilot
- Git installed
- An active GitHub Copilot subscription or organization entitlement

### 1. Install GitHub Copilot in VS Code

1. Open VS Code.
2. Open Extensions.
3. Search for `GitHub Copilot`.
4. Install `GitHub Copilot`.
5. Install `GitHub Copilot Chat` if it is listed separately.
6. Sign in with the GitHub account that has Copilot access.

Verify Copilot is working by opening Chat and asking:

```text
Are you available in this workspace?
```

### 2. Clone ABAP Skills

#### macOS / Linux

```bash
mkdir -p ~/.copilot
git clone https://github.com/likweitan/abap-skills.git ~/.copilot/abap-skills
```

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.copilot"
git clone https://github.com/likweitan/abap-skills.git "$env:USERPROFILE\.copilot\abap-skills"
```

If you prefer, you can clone the repository anywhere and adjust the paths in the examples below.

Copilot can use files that are available in your VS Code workspace or explicitly attached to chat. For best results, add the cloned `abap-skills` folder to your VS Code workspace:

1. Open the Command Palette.
2. Run `Workspaces: Add Folder to Workspace`.
3. Select the cloned `abap-skills` folder.

### 3. Create Reusable Prompt Files

GitHub Copilot in VS Code can use prompt files from your user prompts folder or from a workspace `.github/prompts` folder.

Use user prompt files when you want ABAP Skills available across projects. Use workspace prompt files when you want them only in a single repository.

#### User Prompt Location

| Platform | Folder                                            |
| -------- | ------------------------------------------------- |
| macOS    | `~/Library/Application Support/Code/User/prompts` |
| Linux    | `~/.config/Code/User/prompts`                     |
| Windows  | `%APPDATA%\Code\User\prompts`                     |

#### macOS

```bash
mkdir -p "$HOME/Library/Application Support/Code/User/prompts"
cat > "$HOME/Library/Application Support/Code/User/prompts/abap-skills.prompt.md" <<'EOF'
# ABAP Skills

Use the ABAP Skills repository as reference material for SAP ABAP development tasks.

Repository location: ~/.copilot/abap-skills

Before answering, inspect the most relevant skill file under ~/.copilot/abap-skills/skills/:

- abap/SKILL.md for general ABAP, abaplint, and Clean ABAP review
- clean-abap/SKILL.md for Clean ABAP guidance
- rap/SKILL.md for RAP development
- cds-view-entities/SKILL.md for CDS view entities
- odata/SKILL.md for OData services
- abap-cloud/SKILL.md for ABAP Cloud and Clean Core work
- abap-unit-testing/SKILL.md for ABAP Unit tests
- sap-fiori-apps-reference/SKILL.md for SAP Fiori app lookup and FLP URL generation

Prefer the repository's examples and references over generic ABAP guidance.
EOF
```

#### Linux

```bash
mkdir -p "$HOME/.config/Code/User/prompts"
cat > "$HOME/.config/Code/User/prompts/abap-skills.prompt.md" <<'EOF'
# ABAP Skills

Use the ABAP Skills repository as reference material for SAP ABAP development tasks.

Repository location: ~/.copilot/abap-skills

Before answering, inspect the most relevant skill file under ~/.copilot/abap-skills/skills/:

- abap/SKILL.md for general ABAP, abaplint, and Clean ABAP review
- clean-abap/SKILL.md for Clean ABAP guidance
- rap/SKILL.md for RAP development
- cds-view-entities/SKILL.md for CDS view entities
- odata/SKILL.md for OData services
- abap-cloud/SKILL.md for ABAP Cloud and Clean Core work
- abap-unit-testing/SKILL.md for ABAP Unit tests
- sap-fiori-apps-reference/SKILL.md for SAP Fiori app lookup and FLP URL generation

Prefer the repository's examples and references over generic ABAP guidance.
EOF
```

#### Windows PowerShell

```powershell
$PromptFolder = Join-Path $env:APPDATA "Code\User\prompts"
New-Item -ItemType Directory -Force -Path $PromptFolder

@'
# ABAP Skills

Use the ABAP Skills repository as reference material for SAP ABAP development tasks.

Repository location: %USERPROFILE%\.copilot\abap-skills

Before answering, inspect the most relevant skill file under %USERPROFILE%\.copilot\abap-skills\skills\:

- abap/SKILL.md for general ABAP, abaplint, and Clean ABAP review
- clean-abap/SKILL.md for Clean ABAP guidance
- rap/SKILL.md for RAP development
- cds-view-entities/SKILL.md for CDS view entities
- odata/SKILL.md for OData services
- abap-cloud/SKILL.md for ABAP Cloud and Clean Core work
- abap-unit-testing/SKILL.md for ABAP Unit tests
- sap-fiori-apps-reference/SKILL.md for SAP Fiori app lookup and FLP URL generation

Prefer the repository's examples and references over generic ABAP guidance.
'@ | Set-Content -Path (Join-Path $PromptFolder "abap-skills.prompt.md") -Encoding UTF8
```

### 4. Optional Workspace Prompt

For a project-specific setup, create `.github/prompts/abap-skills.prompt.md` in your workspace instead of using the user prompts folder.

Example:

```bash
mkdir -p .github/prompts
cp ~/.copilot/abap-skills/docs/examples/abap-skills.prompt.md .github/prompts/abap-skills.prompt.md
```

If you cloned ABAP Skills to a different location, edit the copied prompt file and update the repository path.

### 5. Restart or Reload VS Code

Reload VS Code after creating prompt files:

1. Open the Command Palette.
2. Run `Developer: Reload Window`.

## Usage

### Use the Prompt File

In Copilot Chat, type `/` and select the `abap-skills` prompt file if it appears in your VS Code version.

Then ask a task-specific question, for example:

```text
/abap-skills Review this ABAP class for Clean ABAP issues.
```

```text
/abap-skills Create a RAP behavior definition with validation and determination examples.
```

```text
/abap-skills Generate a Fiori Launchpad URL for the Create Maintenance Request app.
```

### Add Skill Files as Context

You can also attach the relevant `SKILL.md` file directly in Copilot Chat by using `#file` or the chat context picker.

Useful files include:

- `skills/abap/SKILL.md`
- `skills/clean-abap/SKILL.md`
- `skills/rap/SKILL.md`
- `skills/cds-view-entities/SKILL.md`
- `skills/abap-cloud/SKILL.md`
- `skills/abap-unit-testing/SKILL.md`
- `skills/sap-fiori-apps-reference/SKILL.md`

### Example Prompts

```text
Using the ABAP Skills context, review this method for Clean ABAP naming, table handling, error handling, and testability.
```

```text
Using the RAP skill, create a managed RAP BO example with draft handling, validations, determinations, and EML usage.
```

```text
Using the ABAP Cloud skill, check whether this code follows released API and Clean Core expectations.
```

## Updating

Update your local copy of ABAP Skills regularly:

#### macOS / Linux

```bash
cd ~/.copilot/abap-skills
git pull
```

#### Windows PowerShell

```powershell
cd "$env:USERPROFILE\.copilot\abap-skills"
git pull
```

## Verify Installation

Ask Copilot Chat:

```text
Using the abap-skills prompt, list the available ABAP skill areas you can use.
```

Expected result: Copilot should mention areas such as ABAP, Clean ABAP, RAP, CDS view entities, OData, ABAP Cloud, ABAP Unit Testing, abapGit, authorization, and SAP BTP.

## Troubleshooting

### Copilot Chat does not show the prompt file

1. Confirm the file ends with `.prompt.md`.
2. Confirm it is in the user prompts folder or `.github/prompts` in the workspace.
3. Run `Developer: Reload Window` in VS Code.
4. Check that prompt files are enabled in your VS Code and Copilot settings.

### Copilot cannot find the skill files

1. Confirm the repository exists at the path referenced in the prompt file.
2. Add the cloned `abap-skills` folder to your VS Code workspace.
3. If you cloned to a different location, update the path in `abap-skills.prompt.md`.
4. Attach the relevant `SKILL.md` file directly with `#file` as a fallback.

### Copilot gives generic ABAP answers

1. Start the chat with the `abap-skills` prompt file.
2. Attach the relevant `SKILL.md` file as context.
3. Ask Copilot to cite which ABAP Skills file it used before giving the final answer.

## Getting Help

- Report issues: https://github.com/likweitan/abap-skills/issues
- GitHub Copilot docs: https://docs.github.com/en/copilot
- VS Code Copilot docs: https://code.visualstudio.com/docs/copilot/overview
