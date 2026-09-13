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
    yaml_path = Path(__file__).parent / "src" / "Ricardo_CV.yaml"
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
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --blue: #004f90;
      --blue-hover: #003d70;
      --grey: #808080;
      --text: #1a1a1a;
      --text-secondary: #555;
      --text-detail: #444;
      --bg: #f5f5f5;
      --page-bg: #ffffff;
      --border: #cccccc;
      --shadow: rgba(0,0,0,0.1);
      --font: 'Source Sans 3', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    }}

    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --blue: #5ba3d9;
        --blue-hover: #7dbde8;
        --text: #e0e0e0;
        --text-secondary: #aaaaaa;
        --text-detail: #bbbbbb;
        --bg: #121212;
        --page-bg: #1e1e1e;
        --border: #333333;
        --shadow: rgba(0,0,0,0.4);
      }}
    }}

    [data-theme="dark"] {{
      --blue: #5ba3d9;
      --blue-hover: #7dbde8;
      --text: #e0e0e0;
      --text-secondary: #aaaaaa;
      --text-detail: #bbbbbb;
      --bg: #121212;
      --page-bg: #1e1e1e;
      --border: #333333;
      --shadow: rgba(0,0,0,0.4);
    }}

    body {{
      font-family: var(--font);
      color: var(--text);
      font-size: 10.5pt;
      line-height: 1.5;
      background: var(--bg);
      transition: background 0.3s, color 0.3s;
    }}

    .page {{
      max-width: 800px;
      margin: 0 auto;
      background: var(--page-bg);
      padding: 40px 50px;
      box-shadow: 0 1px 4px var(--shadow);
      transition: background 0.3s, box-shadow 0.3s;
    }}

    @media print {{
      body {{ background: #fff; color: #1a1a1a; }}
      .page {{ box-shadow: none; padding: 0; max-width: none; background: #fff; }}
      .download-bar {{ display: none !important; }}
      .theme-toggle {{ display: none !important; }}
    }}

    /* Theme toggle */
    .theme-toggle {{
      position: fixed;
      top: 16px;
      right: 16px;
      z-index: 100;
      background: var(--page-bg);
      border: 1px solid var(--border);
      border-radius: 50%;
      width: 40px;
      height: 40px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px var(--shadow);
      transition: background 0.3s, border-color 0.3s;
    }}
    .theme-toggle:hover {{ opacity: 0.8; }}
    .theme-toggle svg {{ width: 20px; height: 20px; fill: var(--text); transition: fill 0.3s; }}
    .theme-toggle .icon-moon {{ display: none; }}
    [data-theme="dark"] .theme-toggle .icon-sun {{ display: none; }}
    [data-theme="dark"] .theme-toggle .icon-moon {{ display: block; }}

    @media (max-width: 768px) {{
      .page {{ padding: 24px 20px; }}
      .download-bar {{ padding: 12px 20px; }}
      .theme-toggle {{ top: 10px; right: 10px; width: 36px; height: 36px; }}
      .theme-toggle svg {{ width: 18px; height: 18px; }}
    }}

    .header {{
      text-align: center;
      margin-bottom: 16px;
    }}
    .header h1 {{
      font-size: 28pt;
      font-weight: 700;
      color: var(--blue);
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .header .headline {{
      font-size: 11pt;
      color: var(--blue);
      margin-top: 2px;
    }}
    .connections {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 14px;
      margin-top: 14px;
      font-size: 9.5pt;
      color: var(--blue);
    }}
    .connections a {{
      color: var(--blue);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .connections a:hover {{ text-decoration: underline; }}
    .connections svg {{ width: 13px; height: 13px; fill: var(--blue); flex-shrink: 0; }}

    .section {{ margin-top: 18px; }}
    .section-title {{
      font-size: 13pt;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--blue);
      border-bottom: 0.5pt solid var(--border);
      padding-bottom: 3px;
      margin-bottom: 10px;
    }}

    .entry {{
      display: grid;
      grid-template-columns: 1fr 140px;
      gap: 0 12px;
      margin-bottom: 14px;
    }}
    .entry-main {{ min-width: 0; }}
    .entry-meta {{
      text-align: right;
      font-size: 9.5pt;
      color: var(--text-secondary);
      white-space: nowrap;
    }}
    .entry-meta .location {{ display: block; }}
    .entry-meta .date {{ display: block; font-weight: 600; color: var(--text); }}

    .entry-title {{
      font-size: 11pt;
      font-weight: 700;
    }}
    .entry-title .label {{ color: var(--text); }}
    .entry-title .detail {{ font-weight: 400; color: var(--text-detail); }}

    .entry-degree {{
      font-size: 10pt;
      font-weight: 600;
      margin-top: 1px;
    }}

    .highlights {{
      margin-top: 4px;
      padding-left: 16px;
    }}
    .highlights li {{
      margin-bottom: 3px;
      font-size: 10pt;
      line-height: 1.45;
    }}

    .summary {{
      font-size: 10.5pt;
      line-height: 1.5;
      margin-bottom: 4px;
    }}

    .skill-row {{
      font-size: 10pt;
      margin-bottom: 3px;
      line-height: 1.45;
    }}
    .skill-row strong {{ font-weight: 700; }}

    .interests-list {{
      list-style: disc;
      padding-left: 18px;
      font-size: 10pt;
    }}
    .interests-list li {{ margin-bottom: 2px; }}

    .download-bar {{
      text-align: right;
      padding: 12px 50px;
      max-width: 800px;
      margin: 0 auto;
    }}
    .download-btn {{
      display: inline-block;
      background: var(--blue);
      color: #fff;
      padding: 8px 16px;
      text-decoration: none;
      border-radius: 4px;
      font-size: 10pt;
      font-family: var(--font);
    }}
    .download-btn:hover {{ background: var(--blue-hover); }}

    /* Mobile responsive */
    @media (max-width: 600px) {{
      .header h1 {{ font-size: 22pt; }}
      .header .headline {{ font-size: 10pt; }}
      .connections {{ gap: 10px; font-size: 9pt; }}
      .connections svg {{ width: 11px; height: 11px; }}
      .entry {{
        grid-template-columns: 1fr;
        gap: 2px 0;
      }}
      .entry-meta {{
        text-align: left;
        margin-top: 2px;
        white-space: normal;
      }}
      .section-title {{ font-size: 12pt; }}
    }}
  </style>
</head>
<body>

<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
  <svg class="icon-sun" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
  <svg class="icon-moon" viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>
</button>

<div class="download-bar">
  <a class="download-btn" href="Ricardo_Leal_CV.pdf" download>Download PDF</a>
</div>

<div class="page">
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
