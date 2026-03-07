#!/usr/bin/env python3
"""Rebuild all LLC pages with editorial design (de-AI)."""

import os, re, glob, random

FEATURED_IMAGES = [
    ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1400&q=80", "City business district"),
    ("https://images.unsplash.com/photo-1497366216548-37526070297c?w=1400&q=80", "Modern office space"),
    ("https://images.unsplash.com/photo-1560472355-536de3962603?w=1400&q=80", "Coworking area"),
    ("https://images.unsplash.com/photo-1556761175-b413da4baf72?w=1400&q=80", "Team working together"),
    ("https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1400&q=80", "Business meeting"),
    ("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1400&q=80", "Reviewing paperwork"),
    ("https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=1400&q=80", "Office collaboration"),
    ("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1400&q=80", "Startup office"),
    ("https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1400&q=80", "Desk workspace"),
    ("https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1400&q=80", "Business planning"),
    ("https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1400&q=80", "Working on laptop"),
    ("https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1400&q=80", "Presentation"),
]

random.seed(42)  # Reproducible

def slug_to_name(slug):
    """Convert 'new-york' to 'New York'."""
    parts = slug.replace("-", " ").split()
    exceptions = {"of": "of", "the": "the"}
    return " ".join(exceptions.get(p, p.capitalize()) for p in parts)

def extract_meta(html):
    """Extract title, description, keywords from <head>."""
    title = ""
    desc = ""
    keywords = ""
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if m:
        title = m.group(1).strip()
    m = re.search(r'name="description"\s+content="(.*?)"', html, re.DOTALL)
    if m:
        desc = m.group(1).strip()
    m = re.search(r'name="keywords"\s+content="(.*?)"', html, re.DOTALL)
    if m:
        keywords = m.group(1).strip()
    return title, desc, keywords

def extract_canonical(html):
    m = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', html)
    return m.group(1) if m else ""

def extract_h1(html):
    m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_quick_facts(html):
    """Extract quick-facts values into list of (label, value) tuples."""
    facts = []
    pattern = re.compile(
        r'<div class="fact-label">(.*?)</div>\s*<div class="fact-value[^"]*">(.*?)</div>',
        re.DOTALL
    )
    for m in pattern.finditer(html):
        facts.append((m.group(1).strip(), m.group(2).strip()))
    return facts

def extract_body_content(html):
    """Extract everything between first <div class="content"> and the footer."""
    # Find the start of body content (after quick-facts)
    # The content lives inside <div class="container"> ... </div> ... <footer>
    m = re.search(
        r'<div class="container">\s*<div class="content">(.*?)</div>\s*</div>\s*<footer>',
        html,
        re.DOTALL
    )
    if m:
        return m.group(1)
    # Fallback: try to get everything between container and footer
    m = re.search(r'<div class="container">(.*?)<footer>', html, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def extract_one_faq_schema(html):
    """Extract just ONE FAQPage schema block (deduplicate)."""
    m = re.search(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"FAQPage".*?\}\s*</script>',
        html,
        re.DOTALL
    )
    return m.group(0) if m else ""

def extract_breadcrumb_schema(html):
    m = re.search(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"BreadcrumbList".*?\}\s*</script>',
        html,
        re.DOTALL
    )
    return m.group(0) if m else ""

def extract_howto_schema(html):
    m = re.search(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"HowTo".*?\}\s*</script>',
        html,
        re.DOTALL
    )
    return m.group(0) if m else ""

def clean_body(body):
    """Clean up stray wrapper divs and inline styles in body content."""
    # Remove remaining inline styles
    body = re.sub(r'\s*style="[^"]*"', '', body)
    # Remove the old ad-slot divs
    body = re.sub(r'<div class="ad-slot">.*?</div>', '', body, flags=re.DOTALL)
    # Remove stray </div> from old nested .content wrappers
    # These appear as standalone </div> lines between content sections
    # Strategy: balance div opens/closes and remove excess closes
    lines = body.split('\n')
    result = []
    depth = 0
    for line in lines:
        opens = len(re.findall(r'<div\b', line))
        closes = len(re.findall(r'</div>', line))
        new_depth = depth + opens - closes
        # If this line is just whitespace + </div> and it would make depth negative, skip it
        if new_depth < 0 and re.match(r'^\s*</div>\s*$', line):
            new_depth += 1  # Skip this close
            continue
        depth = new_depth
        result.append(line)
    return '\n'.join(result).strip()

def build_page(filename, title, desc, keywords, canonical, h1, facts, body, faq_schema, breadcrumb_schema, howto_schema, state_name, state_slug, featured_img, featured_alt):
    facts_html = ""
    for label, value in facts:
        facts_html += f'            <div class="fact"><div class="fact-label">{label}</div><div class="fact-value">{value}</div></div>\n'

    schemas = ""
    if faq_schema:
        schemas += f"    {faq_schema}\n"
    if breadcrumb_schema:
        schemas += f"    {breadcrumb_schema}\n"
    if howto_schema:
        schemas += f"    {howto_schema}\n"

    canonical_tag = f'    <link rel="canonical" href="{canonical}">\n' if canonical else ""
    keywords_tag = f'    <meta name="keywords" content="{keywords}">\n' if keywords else ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-5MF05LMQTC"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}};gtag('js',new Date());gtag('config','G-5MF05LMQTC');</script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4019204583657083" crossorigin="anonymous"></script>
{schemas}    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
{keywords_tag}{canonical_tag}    <title>{title}</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <nav class="site-nav">
        <a href="/" class="logo">StatesLLCGuide</a>
        <div class="nav-links">
            <a href="/about">About</a>
            <a href="/privacy-policy">Privacy Policy</a>
        </div>
    </nav>

    <div class="breadcrumbs">
        <a href="/">Home</a><span class="sep">&rsaquo;</span>
        {state_name} LLC
    </div>

    <div class="featured-img">
        <img src="{featured_img}" alt="{featured_alt}">
        <div class="caption">Starting a business in {state_name}</div>
    </div>

    <div class="article-header">
        <h1>{h1}</h1>
        <p class="byline">By <strong>StatesLLCGuide Staff</strong> &middot; Updated March 2026</p>
    </div>

    <div class="quick-facts">
        <div class="quick-facts-inner">
{facts_html}        </div>
    </div>

    <div class="article-body">
{body}
    </div>

    <footer>
        <div class="footer-links">
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/privacy-policy">Privacy Policy</a>
        </div>
        <p>&copy; 2026 StatesLLCGuide.com &middot; Free LLC guides for all 50 states.</p>
        <p>This guide is for informational purposes only. Consult a licensed attorney or CPA for advice specific to your situation.</p>
    </footer>
</body>
</html>'''


def process_file(filepath):
    filename = os.path.basename(filepath)
    # Get state slug (e.g. "california" from "california-llc.html")
    state_slug = filename.replace("-llc.html", "")
    state_name = slug_to_name(state_slug)

    with open(filepath, "r") as f:
        html = f.read()

    title, desc, keywords = extract_meta(html)
    canonical = extract_canonical(html)
    h1_text = extract_h1(html)
    facts = extract_quick_facts(html)
    body = extract_body_content(html)
    body = clean_body(body)
    faq_schema = extract_one_faq_schema(html)
    breadcrumb_schema = extract_breadcrumb_schema(html)
    howto_schema = extract_howto_schema(html)

    # Pick a featured image (deterministic per state)
    img_idx = hash(state_slug) % len(FEATURED_IMAGES)
    featured_img, featured_alt = FEATURED_IMAGES[img_idx]

    new_html = build_page(
        filename, title, desc, keywords, canonical, h1_text,
        facts, body, faq_schema, breadcrumb_schema, howto_schema,
        state_name, state_slug, featured_img, featured_alt
    )

    with open(filepath, "w") as f:
        f.write(new_html)

    print(f"  Rebuilt: {filename} ({state_name})")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    files = sorted([f for f in glob.glob("*-llc.html") if not f.startswith("blog-")])
    print(f"Found {len(files)} state pages to rebuild.\n")
    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print(f"  ERROR on {f}: {e}")
    print(f"\nDone. Rebuilt {len(files)} pages.")
