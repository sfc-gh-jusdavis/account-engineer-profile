# INSTALL — snowflake-pdf

This file is followed by the CoCo agent to install or upgrade the skill on the user's machine. Each numbered step is a single command. The agent must ask the user to approve each command before running it.

## 1. Clone or update the skill folder

```bash
git clone <REPO_URL> ~/.snowflake/cortex/skills/snowflake-pdf
# or, to upgrade an existing install:
git -C ~/.snowflake/cortex/skills/snowflake-pdf pull --ff-only
```

## 2. Install Python dependencies

The skill defaults to `/opt/anaconda3/bin/python3` if present, falling back to `python3`:

```bash
/opt/anaconda3/bin/python3 -m pip install --user jinja2 markdown pyyaml weasyprint
```

`weasyprint` is preferred (best CSS Paged Media support — running headers, page numbers, classification footer). The skill works without it via the Chrome-headless fallback.

## 3. Optional — system libraries for full WeasyPrint support (macOS only)

Skip this step on a fresh laptop if the user prefers minimum install. The skill will work via Chrome.

```bash
brew list pango >/dev/null 2>&1 || brew install pango cairo gdk-pixbuf libffi
```

If `brew install` fails or the user declines, that's fine — the skill falls back to Chrome and prints a note.

## 4. Verify the install

```bash
/opt/anaconda3/bin/python3 ~/.snowflake/cortex/skills/snowflake-pdf/render.py --check
```

Expected output (Chrome fallback is acceptable):

```
python  : /opt/anaconda3/bin/python3 (3.x.x)
weasyprint: ok          (or: missing - Chrome fallback will be used)
chrome  : /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
jinja2  : ok
markdown: ok
yaml    : ok
```

## 5. Self-test against the bundled sample

```bash
/opt/anaconda3/bin/python3 ~/.snowflake/cortex/skills/snowflake-pdf/render.py \
  ~/.snowflake/cortex/skills/snowflake-pdf/samples/example.md \
  /tmp/snowflake-pdf-selftest.pdf \
  --references ~/.snowflake/cortex/skills/snowflake-pdf/samples/example.references.json
```

Expected: `OK  backend=...  pdf=/tmp/snowflake-pdf-selftest.pdf  (...bytes)  refs=...`

Open `/tmp/snowflake-pdf-selftest.pdf` to confirm cover page and References section render correctly.

## 6. Restart CoCo

The skill is loaded at CoCo startup. Tell the user:

> **Restart CoCo. After it reloads, the `snowflake-pdf` skill will be available.**

## Troubleshooting

| Symptom | Fix |
|---|---|
| `weasyprint: missing (OSError)` on macOS | Run step 3 (`brew install pango cairo gdk-pixbuf libffi`). Or accept the Chrome fallback. |
| `chrome: not found` | Install Google Chrome from https://www.google.com/chrome/ |
| `ERROR: refusing to render without validation` | The agent must run the validation workflow in `SKILL.md` first, or pass `--no-validate` for non-Snowflake docs. |
| Skill doesn't appear in CoCo | Confirm `~/.snowflake/cortex/skills/snowflake-pdf/SKILL.md` exists, then restart CoCo. |
