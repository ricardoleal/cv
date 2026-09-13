#!/usr/bin/env python3
"""Generate index.html from Ricardo_CV.yaml matching the PDF styling."""

import re
import sys
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def md_inline(text: str) -> str:
    """Convert basic Markdown inline: **bold** -> <strong>, *italic* -> <em>."""
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def render_highlights(items):
    if not items:
        return ""
    lis = "\n".join(f"          <li>{md_inline(h)}</li>" for h in items)
    return f"        <ul class=\"highlights\">\n{lis}\n        </ul>"


def render_experience(entries):
    blocks = []
    for e in entries:
        company = escape(e.get("company", ""))
        position = escape(e.get("position", ""))
        location = escape(e.get("location", ""))
        sd = e.get("start_date", "")
        ed = e.get("end_date", "")
        # Format dates as year-only
        def fmt_date(d):
            if not d:
                return ""
            s = str(d)
            if s.lower() == "present":
                return "present"
            if len(s) == 4:
                return s
            if len(s) == 7:
                return s[:4]
            return s

        date_str = f"{fmt_date(sd)} – {fmt_date(ed)}" if sd else ""
        highlights = render_highlights(e.get("highlights"))

        blocks.append(f"""      <div class="entry">
        <div class="entry-main">
          <div class="entry-title"><span class="label">{company}</span>, <span class="detail">{position}</span></div>
{highlights}
        </div>
        <div class="entry-meta">
          <span class="location">{location}</span>
          <span class="date">{date_str}</span>
        </div>
      </div>""")
    return "\n\n".join(blocks)


def render_education(entries):
    blocks = []
    for e in entries:
        inst = escape(e.get("institution", ""))
        area = escape(e.get("area", ""))
        degree = escape(e.get("degree", ""))
        location = escape(e.get("location", ""))
        sd = e.get("start_date", "")
        ed = e.get("end_date", "")

        def fmt_date(d):
            if not d:
                return ""
            s = str(d)
            if s.lower() == "present":
                return "present"
            if len(s) == 4:
                return s
            if len(s) == 7:
                return s[:4]
            return s

        date_str = f"{fmt_date(sd)} – {fmt_date(ed)}" if sd else ""
        highlights = render_highlights(e.get("highlights"))

        blocks.append(f"""      <div class="entry">
        <div class="entry-main">
          <div class="entry-title"><span class="label">{inst}</span>, <span class="detail">{area}</span></div>
          <div class="entry-degree">{degree}</div>
{highlights}
        </div>
        <div class="entry-meta">
          <span class="location">{location}</span>
          <span class="date">{date_str}</span>
        </div>
      </div>""")
    return "\n\n".join(blocks)


def render_skills(entries):
    rows = []
    for s in entries:
        label = escape(s.get("label", ""))
        details = escape(s.get("details", ""))
        rows.append(f'    <p class="skill-row"><strong>{label}:</strong> {details}</p>')
    return "\n".join(rows)


def render_interests(entries):
    items = []
    for e in entries:
        bullet = escape(e.get("bullet", ""))
        if bullet:
            items.append(f"      <li>{bullet}</li>")
    return "\n".join(items)


def main():
    yaml_path = Path(__file__).parent / "src" / "render_cv.yaml"
    out_path = Path(__file__).parent / "index.html"

    data = yaml.load(yaml_path)
    cv = data["cv"]

    name = escape(cv.get("name", ""))
    headline = escape(cv.get("headline", ""))
    email = escape(cv.get("email", ""))
    location = escape(cv.get("location", ""))

    social = cv.get("social_networks", [])
    connections_html = []
    for s in social:
        network = s.get("network", "")
        username = s.get("username", "")
        if network == "LinkedIn":
            icon = '<svg viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>'
            url = f"https://linkedin.com/in/{escape(username)}"
        elif network == "GitHub":
            icon = '<svg viewBox="0 0 24 24"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>'
            url = f"https://github.com/{escape(username)}"
        else:
            icon = ""
            url = ""
        connections_html.append(f'      <a href="{url}" target="_blank">\n        {icon}\n        {escape(username)}\n      </a>')

    sections = cv.get("sections", {})
    # Find sections by key
    experience = sections.get("experience", [])
    education = sections.get("education", [])
    skills = sections.get("skills", [])
    interests = sections.get("Interests", sections.get("interests", []))

    # Career profile is the first text-only section
    career_profile = ""
    for key, val in sections.items():
        if key.lower() in ("career profile", "career_profile"):
            if isinstance(val, list):
                career_profile = " ".join(str(v) for v in val)
            else:
                career_profile = str(val)
            break

    # Find any remaining sections (non-standard)
    known = {"experience", "education", "skills", "interests", "career profile", "career_profile"}
    extra_sections = []
    for key, val in sections.items():
        if key.lower() not in known:
            if isinstance(val, list) and val and isinstance(val[0], dict):
                # entry-based section
                extra_sections.append((key, val))

    exp_html = render_experience(experience)
    edu_html = render_education(education)
    skills_html = render_skills(skills)
    interests_html = render_interests(interests)

    extra_html = ""
    for title, entries in extra_sections:
        extra_html += f"""
  <div class="section">
    <div class="section-title">{escape(title)}</div>
{render_experience(entries)}
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} - CV</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --accent: #004f90;
      --accent-hover: #003d70;
      --accent-light: #e8f0f8;
      --text: #1c1c1c;
      --text-secondary: #5a5a5a;
      --text-muted: #777;
      --bg: #f0eeeb;
      --page-bg: #ffffff;
      --border: #d8d4cf;
      --border-light: #eae7e3;
      --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
      --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      --font-heading: 'Source Sans 3', 'Inter', -apple-system, sans-serif;
    }}

    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --accent: #6aabde;
        --accent-hover: #8ec2ed;
        --accent-light: #1a2a3a;
        --text: #dcdcdc;
        --text-secondary: #a0a0a0;
        --text-muted: #777;
        --bg: #0e0e0e;
        --page-bg: #181818;
        --border: #2e2e2e;
        --border-light: #242424;
        --shadow: 0 1px 3px rgba(0,0,0,0.2), 0 4px 12px rgba(0,0,0,0.15);
      }}
    }}

    [data-theme="dark"] {{
      --accent: #6aabde;
      --accent-hover: #8ec2ed;
      --accent-light: #1a2a3a;
      --text: #dcdcdc;
      --text-secondary: #a0a0a0;
      --text-muted: #777;
      --bg: #0e0e0e;
      --page-bg: #181818;
      --border: #2e2e2e;
      --border-light: #242424;
      --shadow: 0 1px 3px rgba(0,0,0,0.2), 0 4px 12px rgba(0,0,0,0.15);
    }}

    body {{
      font-family: var(--font-body);
      color: var(--text);
      font-size: 10.5pt;
      line-height: 1.55;
      background: var(--bg);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }}

    .page {{
      max-width: 800px;
      margin: 0 auto;
      background: var(--page-bg);
      padding: 48px 56px;
      box-shadow: var(--shadow);
    }}

    @media print {{
      body {{ background: #fff; color: #1a1a1a; }}
      .page {{ box-shadow: none; padding: 0; max-width: none; background: #fff; }}
      .download-bar {{ display: none !important; }}
      .theme-toggle {{ display: none !important; }}
    }}

    /* Theme toggle - pill with icon swap */
    .theme-toggle {{
      position: relative;
      background: var(--border);
      border: 1px solid var(--border);
      border-radius: 24px;
      width: 56px;
      height: 30px;
      cursor: pointer;
      display: flex;
      align-items: center;
      padding: 3px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
      transition: background 0.2s, border-color 0.2s;
      flex-shrink: 0;
      overflow: hidden;
    }}
    .theme-toggle:hover {{
      border-color: var(--accent);
    }}
    .theme-toggle svg {{
      width: 14px;
      height: 14px;
      fill: var(--text-muted);
      transition: fill 0.2s;
      flex-shrink: 0;
      z-index: 1;
    }}
    .theme-toggle:hover svg {{ fill: var(--accent); }}
    .toggle-track {{
      position: absolute;
      left: 3px;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: var(--accent);
      transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    [data-theme="dark"] .toggle-track {{ transform: translateX(26px); }}
    .icon-moon {{ display: none; }}
    [data-theme="dark"] .icon-sun {{ display: none; }}
    [data-theme="dark"] .icon-moon {{ display: block; }}

    /* Header */
    .header {{
      text-align: center;
      margin-bottom: 28px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-light);
    }}
    .header h1 {{
      font-family: var(--font-heading);
      font-size: 30pt;
      font-weight: 700;
      color: var(--accent);
      margin: 0;
      letter-spacing: -0.5px;
      line-height: 1.1;
    }}
    .header .headline {{
      font-family: var(--font-body);
      font-size: 11pt;
      font-weight: 400;
      color: var(--text-secondary);
      margin-top: 6px;
      letter-spacing: 0.3px;
    }}
    .connections {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 6px 18px;
      margin-top: 16px;
      font-size: 9pt;
      color: var(--text-secondary);
    }}
    .connections a {{
      color: var(--text-secondary);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: color 0.15s;
    }}
    .connections a:hover {{ color: var(--accent); }}
    .connections svg {{ width: 12px; height: 12px; fill: currentColor; flex-shrink: 0; opacity: 0.7; }}

    /* Sections */
    .section {{ margin-top: 22px; }}
    .section-title {{
      font-family: var(--font-heading);
      font-size: 12pt;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 10px;
      padding-bottom: 6px;
      border-bottom: 2px solid var(--accent);
      letter-spacing: 0.2px;
    }}

    /* Entries */
    .entry {{
      display: grid;
      grid-template-columns: 1fr 140px;
      gap: 0 14px;
      margin-bottom: 16px;
    }}
    .entry:last-child {{ margin-bottom: 0; }}
    .entry-main {{ min-width: 0; }}
    .entry-meta {{
      text-align: right;
      font-size: 9pt;
      color: var(--text-muted);
      white-space: nowrap;
      padding-top: 2px;
    }}
    .entry-meta .location {{ display: block; }}
    .entry-meta .date {{ display: block; font-weight: 600; color: var(--text-secondary); font-size: 9.5pt; }}

    .entry-title {{
      font-family: var(--font-heading);
      font-size: 11pt;
      font-weight: 700;
      line-height: 1.3;
    }}
    .entry-title .label {{ color: var(--text); }}
    .entry-title .detail {{ font-weight: 400; color: var(--text-secondary); }}

    .entry-degree {{
      font-family: var(--font-body);
      font-size: 9.5pt;
      font-weight: 500;
      color: var(--text-secondary);
      margin-top: 1px;
    }}

    .highlights {{
      margin-top: 5px;
      padding-left: 16px;
    }}
    .highlights li {{
      margin-bottom: 3px;
      font-size: 10pt;
      line-height: 1.5;
      color: var(--text);
    }}
    .highlights li::marker {{ color: var(--accent); }}

    .summary {{
      font-size: 10.5pt;
      line-height: 1.6;
      color: var(--text);
    }}

    .skill-row {{
      font-size: 10pt;
      margin-bottom: 4px;
      line-height: 1.5;
      color: var(--text);
    }}
    .skill-row strong {{
      font-weight: 600;
      color: var(--text);
    }}

    .interests-list {{
      list-style: none;
      padding-left: 0;
      font-size: 10pt;
      display: flex;
      flex-wrap: wrap;
      gap: 4px 16px;
    }}
    .interests-list li {{
      position: relative;
      padding-left: 14px;
    }}
    .interests-list li::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 8px;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--accent);
    }}

    /* Download bar */
    .download-bar {{
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 8px;
      padding: 0 0 8px 0;
    }}
    .download-btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: transparent;
      color: var(--accent);
      padding: 7px 16px;
      text-decoration: none;
      border-radius: 6px;
      font-size: 9pt;
      font-family: var(--font-body);
      font-weight: 500;
      letter-spacing: 0.3px;
      border: 1.5px solid var(--border);
      transition: border-color 0.15s, color 0.15s, background 0.15s;
    }}
    .download-btn:hover {{
      border-color: var(--accent);
      background: var(--accent-light);
    }}
    .download-btn svg {{ width: 12px; height: 12px; fill: currentColor; }}

    /* Responsive */
    @media (max-width: 768px) {{
      .page {{ padding: 32px 24px; }}
      .theme-toggle {{ width: 50px; height: 26px; }}
      .toggle-track {{ width: 20px; height: 20px; }}
      [data-theme="dark"] .toggle-track {{ transform: translateX(24px); }}
    }}

    @media (max-width: 600px) {{
      .header h1 {{ font-size: 24pt; }}
      .header .headline {{ font-size: 10pt; }}
      .connections {{ gap: 4px 14px; font-size: 8.5pt; }}
      .connections svg {{ width: 11px; height: 11px; }}
      .entry {{
        grid-template-columns: 1fr;
        gap: 2px 0;
      }}
      .entry-meta {{
        text-align: left;
        margin-top: 3px;
        white-space: normal;
      }}
      .section-title {{ font-size: 11pt; }}
      .interests-list {{ flex-direction: column; gap: 4px; }}
    }}

    /* Focus visible for accessibility */
    :focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{ transition: none !important; }}
    }}
  </style>
</head>
<body>

<div class="page">
  <div class="download-bar">
    <a class="download-btn" href="cv.pdf" download>
      <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
      Download PDF
    </a>
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
      <span class="toggle-track"></span>
      <svg class="icon-sun" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
      <svg class="icon-moon" viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>
    </button>
  </div>

  <div class="header">
    <h1>{name}</h1>
    <div class="headline">{headline}</div>
    <div class="connections">
      <a href="mailto:{email}">
        <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        {email}
      </a>
{chr(10).join(connections_html)}
    </div>
  </div>

  <div class="section">
    <div class="section-title">Career Profile</div>
    <p class="summary">{escape(career_profile)}</p>
  </div>

  <div class="section">
    <div class="section-title">Education</div>
{edu_html}
  </div>

  <div class="section">
    <div class="section-title">Experience</div>
{exp_html}
  </div>

  <div class="section">
    <div class="section-title">Skills</div>
{skills_html}
  </div>

  <div class="section">
    <div class="section-title">Interests</div>
    <ul class="interests-list">
{interests_html}
    </ul>
  </div>
{extra_html}
</div>

<script>
(function() {{
  const root = document.documentElement;
  const saved = localStorage.getItem('theme');
  if (saved) {{
    root.setAttribute('data-theme', saved);
  }} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
    root.setAttribute('data-theme', 'dark');
  }}
}})();

function toggleTheme() {{
  const root = document.documentElement;
  const current = root.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}}
</script>

</body>
</html>"""

    out_path.write_text(html)
    print(f"Generated {out_path}")


if __name__ == "__main__":
    main()
