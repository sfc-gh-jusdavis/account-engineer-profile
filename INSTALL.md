# Install the Account Engineer profile

This profile is installed via Cortex Code Desktop's profile creation form.

## Prerequisites

- Cortex Code Desktop installed and authenticated
- A Snowflake connection configured locally (used by skills that query Snowflake)
- Optionally: `gh` CLI authenticated, if you plan to contribute back

## Install (Form mode)

1. Open Cortex Code Desktop
2. Open the profile picker -> **Create New Profile**
3. Select the **Form** tab and fill in:
   - **Profile Name:** `Account Engineer`
   - **Description:** `Cortex Code profile for Snowflake Account Engineers. Bundles asset-creation discipline, account-workflow skills, and an ACE-tuned system prompt.`
   - **Owner Team:** `Account Engineering`
   - **Version:** `0.1.0`
   - **Skill Repositories** (Git): `https://github.com/sfc-gh-jusdavis/account-engineer-profile/tree/main/skills`
   - **MCP Servers:** leave empty
   - **System Prompt** (Git): `https://github.com/sfc-gh-jusdavis/account-engineer-profile/blob/main/system-prompt.md`
4. Click **Save**
5. Switch to the new profile via the profile picker

## Install (JSON mode)

1. Open Cortex Code Desktop
2. Open the profile picker -> **Create New Profile**
3. Select the **JSON** tab and paste:

```json
{
  "name": "Account Engineer",
  "description": "Cortex Code profile for Snowflake Account Engineers. Bundles asset-creation discipline, account-workflow skills, and an ACE-tuned system prompt.",
  "ownerTeam": "Account Engineering",
  "version": "0.1.0",
  "skillRepos": [
    "https://github.com/sfc-gh-jusdavis/account-engineer-profile/tree/main/skills"
  ],
  "mcpServers": {},
  "commandRepos": [
    "https://github.com/sfc-gh-jusdavis/account-engineer-profile/tree/main/commands"
  ],
  "hooks": {},
  "envVars": {
    "ACE_DEFAULT_CONN": "<your-snowflake-connection-name>",
    "ACE_USER_HANDLE": "<your-snowflake-username>"
  },
  "settingsOverrides": {},
  "localModified": false
}
```

4. Set the env var values to match your environment
5. Click **Save**

## Configure environment variables

The profile reads two env vars:

| Variable | Purpose | Example |
|---|---|---|
| `ACE_DEFAULT_CONN` | Default Snowflake connection name passed to SQL tools | `MY_AWS_CONN` |
| `ACE_USER_HANDLE` | Your Snowflake username; used to scope writes to `TEMP.<USER>` | `JANE_DOE` |

These can be set on the profile (recommended) or in your shell (`~/.zshrc`).

## Verify install

After saving the profile and switching to it:

1. Open a fresh chat
2. Type: `draft a notebook for analyzing account churn`
3. Expect the agent to first surface clarifying questions (audience, scope, dataset, success criteria) before writing any cells. That's the asset-creation-discipline skill activating.

If the agent jumps straight to writing cells without surfacing assumptions, the skill is not active. Check that the profile is the active profile in the picker, and that the skill repo URL in the form is correct.

## Update

To pick up profile updates:

1. Open the profile picker -> **Edit** the Account Engineer profile
2. Click **Save** without changing anything (forces CCD to re-fetch the Git repos)
3. Restart your CCD session

Or simply re-create the profile by repeating the install steps.

## Uninstall

1. Open the profile picker -> **Delete** the Account Engineer profile
2. Switch to your prior profile (or default)

## Forking This Profile

If you fork this repo for team-specific or personal customization, update the URLs in your `profile.json` to point at your fork:

```json
"skillRepos": [
  "https://github.com/<your-handle-or-org>/account-engineer-profile/tree/main/skills"
],
"commandRepos": [
  "https://github.com/<your-handle-or-org>/account-engineer-profile/tree/main/commands"
]
```

The same applies to the System Prompt URL in the Form view.

The canonical repo at `github.com/sfc-gh-jusdavis/account-engineer-profile` will continue to exist; your fork is yours to evolve. If you make improvements that generalize, consider opening a PR upstream.
