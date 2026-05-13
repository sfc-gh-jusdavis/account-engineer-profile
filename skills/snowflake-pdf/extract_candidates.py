#!/usr/bin/env python3
"""
Extract Snowflake reference candidates from a markdown document.

Usage:
    extract_candidates.py INPUT.md
    # prints JSON to stdout

Categories:
    - system_functions      SYSTEM$XXX
    - ddl_dml_keywords      SHOW/ALTER/CREATE/DESC/DESCRIBE/GRANT/REVOKE <object>
    - usage_views           ACCOUNT_USAGE.* / INFORMATION_SCHEMA.*
    - cli_tools             SnowCD, snow <subcmd>
    - feature_names         curated phrases (Azure Private Link, network policy, ...)

Each entry: {"label": "<text>", "line": <1-based int>}
"""
from __future__ import annotations
import json, re, sys, pathlib

FRONT_MATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")

SYSTEM_FN_RE = re.compile(r"\bSYSTEM\$[A-Z_][A-Z0-9_]*\b")
DDL_RE = re.compile(
    r"\b(SHOW|ALTER|CREATE|DESC|DESCRIBE|GRANT|REVOKE)\s+"
    r"(?:OR\s+REPLACE\s+)?"
    r"([A-Z][A-Z_]*(?:\s+[A-Z][A-Z_]*){0,2})\b"
)
USAGE_VIEW_RE = re.compile(r"\b(ACCOUNT_USAGE|INFORMATION_SCHEMA|ORGANIZATION_USAGE)\.[A-Z_][A-Z0-9_]*\b")
SNOW_CLI_RE = re.compile(r"\bsnow\s+([a-z][a-z\-]*(?:\s+[a-z][a-z\-]*)?)\b")
SNOWCD_RE = re.compile(r"\bSnowCD\b")

FEATURE_PHRASES = [
    "Azure Private Link",
    "AWS PrivateLink",
    "Private Link",
    "network policy",
    "network policies",
    "Tri-Secret Secure",
    "Client Redirect",
    "OCSP",
    "SnowCD",
    "Business Critical",
    "ACCOUNTADMIN",
    "SECURITYADMIN",
    "Snowsight",
    "private endpoint",
]


def strip_for_scan(text: str) -> str:
    """Remove front-matter and fenced code blocks but preserve line numbering."""
    text = FRONT_MATTER_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text, count=1)

    def blank_lines(m: re.Match) -> str:
        return "\n" * m.group(0).count("\n")

    text = CODE_FENCE_RE.sub(blank_lines, text)
    return text


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def dedupe(items):
    seen = set()
    out = []
    for it in items:
        key = it["label"]
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def extract(text: str) -> dict:
    body = strip_for_scan(text)

    system_functions = [
        {"label": m.group(0), "line": line_of(body, m.start())}
        for m in SYSTEM_FN_RE.finditer(body)
    ]

    ddl = []
    for m in DDL_RE.finditer(body):
        verb = m.group(1)
        obj = m.group(2).strip()
        # Filter out matches inside ordinary prose like "SHOW the user"
        if obj.upper() != obj or len(obj) < 3:
            continue
        ddl.append({"label": f"{verb} {obj}", "line": line_of(body, m.start())})

    usage_views = [
        {"label": m.group(0), "line": line_of(body, m.start())}
        for m in USAGE_VIEW_RE.finditer(body)
    ]

    cli = []
    for m in SNOWCD_RE.finditer(body):
        cli.append({"label": "SnowCD", "line": line_of(body, m.start())})
    for m in SNOW_CLI_RE.finditer(body):
        cli.append({"label": f"snow {m.group(1)}", "line": line_of(body, m.start())})

    features = []
    lower = body.lower()
    for phrase in FEATURE_PHRASES:
        idx = 0
        p = phrase.lower()
        while True:
            pos = lower.find(p, idx)
            if pos < 0:
                break
            features.append({"label": phrase, "line": line_of(body, pos)})
            idx = pos + len(p)

    return {
        "system_functions": dedupe(system_functions),
        "ddl_dml_keywords": dedupe(ddl),
        "usage_views": dedupe(usage_views),
        "cli_tools": dedupe(cli),
        "feature_names": dedupe(features),
    }


def main():
    if len(sys.argv) != 2:
        print("usage: extract_candidates.py INPUT.md", file=sys.stderr)
        sys.exit(2)
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    print(json.dumps(extract(text), indent=2))


if __name__ == "__main__":
    main()
