#!/usr/bin/env python3
"""Generate per-page OGP images for veryl-lang.org.

Reads frontmatter from content/*.md and content/blog/*.md, fills the SVG
template at scripts/ogp/template.svg with the page-specific title and
subtitle, and pipes the result through rsvg-convert to produce a 1200x630
PNG under static/ogp/.

Slug derivation matches Zola's default behavior: lowercase + hyphenate
non-alphanumerics. Date prefixes (YYYY-MM-DD-) on blog filenames are
stripped, since Zola promotes them into page.date.
"""
from __future__ import annotations

import base64
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
TEMPLATE = ROOT / "scripts" / "ogp" / "template.svg"
LOGO = ROOT / "static" / "logo.png"
OUT_DIR = ROOT / "static" / "ogp"

DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


@dataclass
class Page:
    slug: str
    title: str
    subtitle: str


def slugify(name: str) -> str:
    """Approximate Zola's default slugify: lowercase, non-alnum -> hyphen."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_frontmatter(md_path: Path) -> dict[str, str]:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("+++"):
        return {}
    end = text.find("+++", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, _, value = line.partition("=")
        fm[key.strip()] = value.strip().strip('"')
    return fm


def collect_pages() -> list[Page]:
    pages: list[Page] = []

    # Homepage
    fm = parse_frontmatter(CONTENT / "_index.md")
    pages.append(
        Page(
            slug="index",
            title=fm.get("title", "Veryl"),
            subtitle="Optimized syntax · SystemVerilog interop · Modern tooling",
        )
    )

    # Top-level standalone pages.  The frontmatter description on these
    # pages is just a short label and would duplicate the title in the OGP,
    # so we hand-pick a more useful subtitle here.
    standalone_subtitles = {
        "install": "Install Veryl with the verylup toolchain installer",
        "docs": "Reference, tutorials, and the playground",
        "statistics": "GitHub activity, releases, and adoption",
    }
    for md in sorted(CONTENT.glob("*.md")):
        if md.name == "_index.md":
            continue
        fm = parse_frontmatter(md)
        slug = md.stem.lower()
        pages.append(
            Page(
                slug=slug,
                title=fm.get("title", md.stem),
                subtitle=standalone_subtitles.get(slug, fm.get("description", "")),
            )
        )

    # Blog index
    fm = parse_frontmatter(CONTENT / "blog" / "_index.md")
    pages.append(
        Page(
            slug="blog",
            title=fm.get("title", "Blog"),
            subtitle="Release notes, articles, and announcements",
        )
    )

    # Individual blog posts
    for md in sorted((CONTENT / "blog").glob("*.md")):
        if md.name == "_index.md":
            continue
        fm = parse_frontmatter(md)
        stem = md.stem
        m = DATE_PREFIX.match(stem)
        if m:
            date, rest = m.group(1), m.group(2)
        else:
            date, rest = "", stem
        slug = slugify(rest)
        title = fm.get("title", rest)
        subtitle_parts = []
        if date:
            subtitle_parts.append(date)
        subtitle_parts.append(category_for(title))
        pages.append(Page(slug=slug, title=title, subtitle=" · ".join(subtitle_parts)))

    return pages


def category_for(title: str) -> str:
    t = title.lower()
    if "announcing veryl" in t or "annoucing veryl" in t:
        return "Release notes"
    if "verylup" in t:
        return "Toolchain"
    return "Article"


# Approximate text-width fitting for the SVG title.  We don't have real font
# metrics in pure Python, so we estimate em-width and pick a font size + line
# wrap that keeps the title inside the 1040px content box.
CONTENT_WIDTH = 1040
EM_RATIO = 0.55  # rough average glyph width / font-size for Inter-like fonts


def wrap_title(title: str) -> tuple[list[str], int]:
    """Return (lines, font_size).  Picks the largest size that fits in <=2 lines."""
    for size in (76, 68, 60, 54, 48):
        max_chars = max(8, int(CONTENT_WIDTH / (size * EM_RATIO)))
        lines = wrap_to_width(title, max_chars)
        if len(lines) <= 2:
            return lines, size
    # Fall back to 3 lines at the smallest size
    return wrap_to_width(title, max(8, int(CONTENT_WIDTH / (48 * EM_RATIO)))), 48


def wrap_to_width(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= max_chars:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render(page: Page, template: str) -> str:
    lines, font_size = wrap_title(page.title)
    line_height = int(font_size * 1.15)
    # Anchor the title block so a single line sits around y=380, two lines
    # straddle that point evenly.  Subtitle follows beneath the last line.
    n = len(lines)
    block_height = line_height * (n - 1)
    title_y = 380 - block_height // 2
    subtitle_y = title_y + block_height + int(font_size * 0.95) + 30

    tspans = []
    for i, line in enumerate(lines):
        dy = "0" if i == 0 else str(line_height)
        tspans.append(f'<tspan x="80" dy="{dy}">{xml_escape(line)}</tspan>')
    title_lines = "".join(tspans)

    return (
        template.replace("__TITLE_LINES__", title_lines)
        .replace("__TITLE_Y__", str(title_y))
        .replace("__TITLE_SIZE__", str(font_size))
        .replace("__SUBTITLE_Y__", str(subtitle_y))
        .replace("__SUBTITLE__", xml_escape(page.subtitle))
    )


def main() -> int:
    if not shutil.which("rsvg-convert"):
        print("error: rsvg-convert not found on PATH", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    logo_b64 = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    template = TEMPLATE.read_text(encoding="utf-8").replace("__LOGO_B64__", logo_b64)

    pages = collect_pages()
    seen: set[str] = set()
    for page in pages:
        if page.slug in seen:
            print(f"warning: duplicate slug {page.slug!r}, skipping", file=sys.stderr)
            continue
        seen.add(page.slug)

        svg = render(page, template)
        out_path = OUT_DIR / f"{page.slug}.png"
        proc = subprocess.run(
            ["rsvg-convert", "-w", "1200", "-h", "630", "-o", str(out_path)],
            input=svg.encode("utf-8"),
            capture_output=True,
        )
        if proc.returncode != 0:
            print(f"error generating {out_path}: {proc.stderr.decode()}", file=sys.stderr)
            return 1
        print(f"wrote {out_path.relative_to(ROOT)}")

    print(f"\ngenerated {len(seen)} OGP image(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
