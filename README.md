# GhostDropETH - First Guide

This repository contains a simple, working affiliate guide and landing page. It’s designed as a starting point for learning about affiliate marketing with free tools.

## What’s Inside

- `guide.md` – The source for the guide, written in Markdown. You can edit this file to update the content or replace the links with your own affiliate URLs.
- `guide.pdf` – A generated PDF version of the guide. If you change `guide.md` you can regenerate this file locally with Pandoc (see below).
- `index.html` – A minimal landing page that links to the PDF and includes an affiliate disclosure.
- `disclose.md` – The text of the affiliate disclosure used in the guide and site.
- `.github/workflows/gh‑pages.yml` – A GitHub Actions workflow that automatically deploys the site to GitHub Pages whenever you push to the `main` branch.
- `.gitignore` – Configuration to avoid committing unnecessary files, such as compiled Python files and your local `.env` file.

## Getting Started

1. Fork or clone this repository to your own GitHub account.
2. Edit `guide.md` and replace the example affiliate URLs with your own. Feel free to expand the guide with additional sections or recommendations.
3. (Optional) Regenerate `guide.pdf` from `guide.md` using Pandoc:

   ```bash
   pandoc guide.md -o guide.pdf --from markdown --pdf-engine=wkhtmltopdf
   ```

4. Commit your changes and push them to your GitHub repository.
5. In the GitHub repository settings, enable GitHub Pages and set the source to “GitHub Actions.” The included workflow will build and publish your site automatically.

Your site will be available at:

```
https://yourusername.github.io/GhostDropETH/
```

Replace `yourusername` with your GitHub username. You can share the link with anyone who wants the guide.