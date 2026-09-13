# CV

A personal resume website built with [RenderCV](https://github.com/rendercv/rendercv) and deployed via GitHub Pages.

**Live site:** [cv.ricardoleal.me](https://cv.ricardoleal.me)

## Features

- PDF generation from YAML using RenderCV
- Styled HTML page with dark mode toggle
- Print interception (Ctrl+P / Cmd+P opens PDF)
- Mobile responsive design
- Auto-deploy on push via GitHub Actions

## Fork & Customize

1. **Fork this repo** to your GitHub account

2. **Enable GitHub Pages:**
   - Go to Settings → Pages → Source → **GitHub Actions**

3. **Edit `src/render_cv.yaml`** with your own data (see template below)

4. **Push your changes** — the site deploys automatically

## YAML Template

Copy and edit `src/render_cv.yaml`:

```yaml
cv:
  name: Your Name
  headline: Your Job Title
  location: City, Country
  email: you@example.com
  phone: "+1234567890"
  social_networks:
    - network: LinkedIn
      username: your-linkedin
    - network: GitHub
      username: your-github
  sections:
    Career Profile:
      - A brief summary of your career...
    education:
      - institution: University Name
        area: Field of Study
        degree: Degree Type
        location: City, Country
        start_date: 2015
        end_date: 2019
        highlights:
          - Key achievement or note
    experience:
      - company: Company Name
        position: Job Title
        location: City
        start_date: 2021-01
        end_date: present
        highlights:
          - What you accomplished
          - "**Stack:** Tech1, Tech2, Tech3"
    Key Skills:
      - Category:
        - Skill 1
        - Skill 2
    Interests:
      - Interest 1
      - Interest 2
```

### Date formats

- Year only: `2019`
- Year-month: `2023-08`
- Current role: `end_date: present`

### Markdown in highlights

Bold text with `**text**` is supported in highlight entries.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Render PDF
rendercv render src/render_cv.yaml

# Generate HTML
python build_html.py

# Open in browser
open index.html
```

## Project Structure

```
.
├── .github/workflows/
│   └── rendercv.yaml    # Build & deploy workflow
├── src/
│   └── render_cv.yaml   # Your CV data (edit this)
├── build_html.py        # Generates index.html from YAML
├── requirements.txt     # rendercv[full]
└── index.html           # Generated (do not edit)
```

## License

MIT
