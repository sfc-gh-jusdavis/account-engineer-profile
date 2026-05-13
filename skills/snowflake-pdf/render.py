#!/usr/bin/env python3
"""
Snowflake-branded PDF renderer.

Usage:
    render.py --check
    render.py INPUT.md OUTPUT.pdf --references REFS.json [--meta key=value ...]
    render.py INPUT.md OUTPUT.pdf --no-validate          [--meta key=value ...]

Validation gate:
    The renderer refuses to run unless --references or --no-validate is supplied.
    The agent should drive the validation workflow described in SKILL.md.

Front-matter (YAML) in the markdown is honored. Supported keys:
    title, subtitle, customer, author, date, classification

Pipeline: markdown (+front-matter) -> Jinja2 HTML (brand template + CSS)
          -> PDF via WeasyPrint if available, otherwise Chrome headless.
"""
from __future__ import annotations
import argparse, base64, datetime, json, os, re, shutil, subprocess, sys, tempfile, pathlib
import jinja2, markdown
try:
    import yaml
except ImportError:
    yaml = None

SKILL_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE = SKILL_DIR / "template.html.j2"
CSS_FILE = SKILL_DIR / "brand.css"
LOGO_FILE = SKILL_DIR / "assets" / "snowflake-logo.png"


def logo_data_url() -> str:
    if not LOGO_FILE.exists():
        return ""
    b = base64.b64encode(LOGO_FILE.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b}"

AUDIENCES = {
    "customer-facing": {
        "label": "EXTERNAL USE",
        "color": "#29B5E8",
        "classification": "Customer Confidential",
    },
    "internal": {
        "label": "INTERNAL USE",
        "color": "#FF9F36",
        "classification": "Snowflake Confidential",
    },
    "partner": {
        "label": "EXTERNAL USE",
        "color": "#7B5DB8",
        "classification": "Snowflake & Partner Confidential",
    },
    "field-only": {
        "label": "INTERNAL USE",
        "color": "#5C6B72",
        "classification": "Snowflake Internal — Field",
    },
}

DEFAULTS = {
    "title": "Untitled Document",
    "subtitle": "",
    "customer": "",
    "author": "",
    "date": datetime.date.today().strftime("%B %d, %Y"),
    "classification": "Snowflake Confidential",
    "audience": "",
}

CATEGORY_ORDER = ["System Function", "SQL Command", "Usage View", "CLI / Tool", "Feature"]


def parse_front_matter(text: str):
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
        if m:
            front = m.group(1)
            body = text[m.end():]
            if yaml:
                meta = yaml.safe_load(front) or {}
            else:
                meta = {}
                for line in front.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip().strip('"').strip("'")
            return meta, body
    return {}, text


def md_to_html(body: str) -> str:
    return markdown.markdown(
        body,
        extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists"],
        output_format="html5",
    )


def load_references(path: pathlib.Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    grouped = {}
    for item in data:
        cat = item.get("category", "Reference")
        grouped.setdefault(cat, []).append(item)
    ordered = []
    for cat in CATEGORY_ORDER:
        if cat in grouped:
            ordered.append((cat, grouped.pop(cat)))
    for cat, items in grouped.items():
        ordered.append((cat, items))
    return ordered


def render_html(md_path: pathlib.Path, overrides: dict, references) -> tuple[str, dict]:
    raw = md_path.read_text(encoding="utf-8")
    meta, body_md = parse_front_matter(raw)
    ctx = {**DEFAULTS, **meta, **overrides}

    audience = (ctx.get("audience") or "").strip().lower()
    if audience not in AUDIENCES:
        raise SystemExit(
            "ERROR: front-matter `audience` is required and must be one of: "
            + ", ".join(AUDIENCES.keys())
            + f"\n  got: {audience!r}\n"
            "  The agent should run the Audience Workflow in SKILL.md before rendering."
        )
    ctx["audience"] = audience
    aud = AUDIENCES[audience]
    ctx["audience_label"] = aud["label"]
    ctx["audience_color"] = aud["color"]
    # Auto-classify if user didn't override
    if not meta.get("classification") and not overrides.get("classification"):
        ctx["classification"] = aud["classification"]

    if not ctx.get("subtitle"):
        ctx["subtitle"] = ctx.get("customer", "")
    body_html = md_to_html(body_md)

    css = CSS_FILE.read_text(encoding="utf-8")
    css = css.replace("{{ classification }}", ctx["classification"]).replace(
        "{{ customer }}", ctx["customer"]
    ).replace("{{ audience_color }}", ctx["audience_color"])

    tpl = jinja2.Template(TEMPLATE.read_text(encoding="utf-8"))
    html = tpl.render(css=css, body=body_html, references=references, logo_data_url=logo_data_url(), **ctx)
    return html, ctx


def html_to_pdf(html: str, out_pdf: pathlib.Path) -> str:
    try:
        from weasyprint import HTML  # type: ignore
        HTML(string=html, base_url=str(SKILL_DIR)).write_pdf(str(out_pdf))
        return "weasyprint"
    except Exception:
        pass

    chrome = chrome_path()
    if not chrome:
        raise RuntimeError("No PDF renderer available (WeasyPrint failed and Chrome not found).")

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp_html = f.name
    try:
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={out_pdf}",
                f"file://{tmp_html}",
            ],
            check=True,
            capture_output=True,
        )
        return "chrome-headless"
    finally:
        os.unlink(tmp_html)


def chrome_path():
    if sys.platform == "darwin":
        p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        return p if os.path.exists(p) else None
    return shutil.which("google-chrome") or shutil.which("chromium")


def cmd_check():
    print(f"python  : {sys.executable} ({sys.version.split()[0]})")
    try:
        import weasyprint  # noqa: F401
        print("weasyprint: ok")
    except Exception as e:
        print(f"weasyprint: missing ({type(e).__name__})")
    cp = chrome_path()
    print(f"chrome  : {cp or 'not found'}")
    for mod in ("jinja2", "markdown", "yaml"):
        try:
            __import__(mod)
            print(f"{mod:8s}: ok")
        except Exception:
            print(f"{mod:8s}: missing")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md", nargs="?")
    ap.add_argument("output_pdf", nargs="?")
    ap.add_argument(
        "--meta",
        action="append",
        default=[],
        help="Override front-matter, e.g. --meta customer='<example-customer>'",
    )
    ap.add_argument("--references", help="Path to validated references JSON")
    ap.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation gate (no References section). Use only for non-Snowflake docs.",
    )
    ap.add_argument("--debug-html", help="Write generated HTML to this path")
    ap.add_argument("--check", action="store_true", help="Print backend availability and exit")
    args = ap.parse_args()

    if args.check:
        cmd_check()
        return

    if not args.input_md or not args.output_pdf:
        ap.error("input_md and output_pdf are required (or pass --check)")

    if not args.references and not args.no_validate:
        sys.stderr.write(
            "ERROR: refusing to render without validation.\n"
            "  Provide --references PATH after running the SKILL.md validation workflow,\n"
            "  or pass --no-validate for non-Snowflake docs.\n"
        )
        sys.exit(2)

    overrides = {}
    for kv in args.meta:
        if "=" in kv:
            k, v = kv.split("=", 1)
            overrides[k.strip()] = v.strip()

    references = None
    if args.references:
        references = load_references(pathlib.Path(args.references))

    html, ctx = render_html(pathlib.Path(args.input_md), overrides, references)
    if args.debug_html:
        pathlib.Path(args.debug_html).write_text(html, encoding="utf-8")

    out = pathlib.Path(args.output_pdf)
    out.parent.mkdir(parents=True, exist_ok=True)
    backend = html_to_pdf(html, out)
    refs_count = sum(len(items) for _, items in references) if references else 0
    print(f"OK  backend={backend}  pdf={out}  ({out.stat().st_size:,} bytes)  refs={refs_count}")
    print(f"    title='{ctx['title']}'  customer='{ctx['customer']}'  audience={ctx['audience']}  date={ctx['date']}")


if __name__ == "__main__":
    main()
