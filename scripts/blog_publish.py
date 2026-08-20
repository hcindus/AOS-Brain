#!/usr/bin/env python3
"""
Blog Publisher — deterministic publishing for psdepot.com weekly blog.

This handles the MECHANICS only (render from template, write to both mirror
versions, update index + sitemap, mark the calendar topic published). The
CONTENT is written by the agent (weekly cron) and passed in as a JSON file.

Usage:
  python3 blog_publish.py /path/to/post.json
  python3 blog_publish.py --next        # auto-pick next unpublished topic (needs content.json already written)

The post JSON shape (matching editorial_calendar.json + template markers):
{
  "slug": "pos-paper-cafes-guide",
  "title": "POS Paper & Receipts for Cafés",
  "category": "Hospitality Solutions",
  "description": "meta + card summary (~150-160 chars)",
  "emoji": "☕",
  "read_time": "5 min read",
  "date": "2026-08-24",
  "body": "<p>intro</p><h2>Section 1</h2><p>...</p><h2>Conclusion</h2><p>...</p>",
  "cta": {"headline": "...", "line": "...", "button": "..."}
}
"""
import json
import os
import re
import sys
from datetime import date, datetime

BLOG = "/var/www/psdepot.com/blog"
VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]  # live + working
TEMPLATE = os.path.join(BLOG, "_template.html")
CALENDAR = "/root/.openclaw/workspace/blog/editorial_calendar.json"


def load_template() -> str:
    with open(TEMPLATE) as f:
        return f.read()


def render_post(post: dict) -> str:
    tpl = load_template()
    slug = post["slug"]
    title = post["title"]
    desc = post.get("description", title)
    category = post.get("category", "Hospitality Solutions")
    emoji = post.get("emoji", "🏪")
    read_time = post.get("read_time", "5 min read")
    date_str = post.get("date", date.today().isoformat())
    body = post.get("body", "")
    cta = post.get("cta", {
        "headline": "Need help choosing the right supplies?",
        "line": "Not sure which paper, printer, or drawer fits your business? Ask us.",
        "button": "Talk to a Supply Expert",
    })

    url = f"https://psdepot.com/blog/{slug}.html"

    # Replace template INSERT markers
    html = tpl
    html = html.replace("INSERT: SEO Blog Post Title", title)
    html = html.replace(
        "INSERT: 1-2 sentence meta description with keyword + benefit (~150-160 chars).",
        desc,
    )
    html = html.replace("INSERT-filename.html", f"{slug}.html")
    html = html.replace("INSERT: Final blog post headline", title)
    html = html.replace("INSERT: Blog meta description", desc)
    html = html.replace('"datePublished": "2026-08-20"', f'"datePublished": "{date_str}"')
    html = html.replace('"dateModified": "2026-08-20"', f'"dateModified": "{date_str}"')
    html = html.replace("INSERT: Category (e.g. Buying Guide, Maintenance)", category)
    html = html.replace("INSERT: Blog post headline — keyword-rich and benefit-led", title)
    html = html.replace("INSERT: Publication date", date_str)
    html = html.replace("INSERT: CTA headline", cta["headline"])
    html = html.replace("INSERT: CTA supporting line. e.g. \"Not sure which supply fits your printer? Ask us.\"",
                        cta["line"])
    html = html.replace("INSERT: CTA Button Label", cta["button"])

    # Replace the whole post-body placeholder with real body
    # The template body sits between <div class="post-body"> ... </div> (first one)
    # Simpler: inject body into the first .post-body div's inner content.
    pattern = re.compile(r'(<div class="post-body">)(.*?)(</div>\s*<div class="post-cta">)', re.S)
    html = pattern.sub(lambda m: m.group(1) + "\n" + body + "\n        " + m.group(3), html, count=1)

    return html


def update_index(post: dict) -> None:
    """Insert a new blog card at the top of the grid in each version's index."""
    slug = post["slug"]
    title = post["title"]
    category = post.get("category", "Hospitality Solutions")
    emoji = post.get("emoji", "🏪")
    desc = post.get("description", title)
    read_time = post.get("read_time", "5 min read")

    card = f'''            <a href="/blog/{slug}.html" class="blog-card">
                <div class="blog-card-image">{emoji}</div>
                <div class="blog-card-content">
                    <div class="blog-category">{category}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <div class="blog-meta">
                        <span>{read_time}</span>
                        <span class="read-more">Read More →</span>
                    </div>
                </div>
            </a>
'''

    for ver in VERSIONS:
        idx = os.path.join(ver, "blog", "index.html")
        if not os.path.exists(idx):
            continue
        with open(idx) as f:
            content = f.read()
        # Insert right after the grid opening div
        anchor = '<div class="blog-grid">'
        if anchor not in content:
            continue
        content = content.replace(anchor, anchor + "\n" + card, 1)
        with open(idx, "w") as f:
            f.write(content)
        print(f"  index updated: {idx}")


def update_sitemap(slug: str, date_str: str) -> None:
    """Add the new post URL to each version's sitemap."""
    entry = f'''  <url>
    <loc>https://psdepot.com/blog/{slug}.html</loc>
    <lastmod>{date_str}</lastmod>
    <priority>0.6</priority>
  </url>
'''
    for ver in VERSIONS:
        sm = os.path.join(ver, "sitemap.xml")
        if not os.path.exists(sm):
            continue
        with open(sm) as f:
            content = f.read()
        if f"/blog/{slug}.html" in content:
            continue
        content = content.replace("</urlset>", entry + "</urlset>", 1)
        with open(sm, "w") as f:
            f.write(content)
        print(f"  sitemap updated: {sm}")


def mark_published(slug: str) -> None:
    with open(CALENDAR) as f:
        cal = json.load(f)
    for t in cal["topics"]:
        if t["slug"] == slug:
            t["published"] = True
            t["published_at"] = datetime.now().isoformat()
            break
    with open(CALENDAR, "w") as f:
        json.dump(cal, f, indent=2)


def publish(post: dict) -> int:
    slug = post["slug"]
    html = render_post(post)
    date_str = post.get("date", date.today().isoformat())

    # Write the rendered post to BOTH versions (live + working)
    for ver in VERSIONS:
        out = os.path.join(ver, "blog", f"{slug}.html")
        with open(out, "w") as f:
            f.write(html)
        print(f"  wrote: {out}")

    update_index(post)
    update_sitemap(slug, date_str)
    mark_published(slug)
    print(f"PUBLISHED: {slug} ({date_str})")
    return 0


def next_topic() -> dict | None:
    with open(CALENDAR) as f:
        cal = json.load(f)
    for t in cal["topics"]:
        if not t.get("published"):
            return t
    return None


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--next":
        t = next_topic()
        print(json.dumps(t, indent=2) if t else "No unpublished topics remain.")
        sys.exit(0 if t else 1)

    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        post = json.load(f)
    sys.exit(publish(post))
