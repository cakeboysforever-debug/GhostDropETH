# GhostDropETH - Affiliate-Ready VPN Guide

This repository contains a polished affiliate landing page and companion guide for promoting vetted VPN offers. Use it as a plug-and-play template: drop in your affiliate IDs, regenerate the PDF, and deploy to GitHub Pages.

## What’s Inside

- `guide.md` – The Markdown source for the full VPN guide, including deal tables, setup steps, and FAQs. Update the `YOUR_*_AFFILIATE_ID` placeholders with the IDs from your affiliate dashboards.
- `guide.pdf` – A generated PDF version of the guide. Regenerate this file after updating `guide.md` so the downloadable version stays in sync.
- `index.html` – A modern landing page highlighting the featured deals with disclosure copy that matches the guide.
- `disclose.md` – Reusable disclosure text you can embed in additional assets (emails, blog posts, etc.).
- `.github/workflows/gh-pages.yml` – GitHub Actions workflow that deploys the site to GitHub Pages whenever you push to `main`.
- `.gitignore` – Keeps build artifacts and secrets out of version control.

## Customize the Affiliate Links

1. Sign up for the NordVPN, Surfshark, and ExpressVPN affiliate programs (Impact/PartnerStack/etc.).
2. Replace each `YOUR_*_AFFILIATE_ID` placeholder in `guide.md` and `index.html` with your assigned affiliate ID or tracking token.
3. Optionally add `aff_sub` or `utm_*` parameters for campaign tracking.

> 💡 Tip: Store your IDs in a `.env` file and use a templating step if you maintain multiple variants (e.g., TikTok vs. newsletter campaigns).

## Regenerate the PDF

Pandoc is the simplest way to regenerate `guide.pdf`:

```bash
pandoc guide.md -o guide.pdf --from markdown --pdf-engine=wkhtmltopdf
```

If Pandoc or `wkhtmltopdf` is not installed locally, install them via Homebrew (`brew install pandoc wkhtmltopdf`) or your package manager of choice.

## Deploy to GitHub Pages

1. Fork or clone this repository.
2. Commit your affiliate ID updates.
3. Push to `main`. The included workflow will build and publish the landing page to the `gh-pages` branch.
4. In GitHub, enable Pages and set the source to the deployed branch (GitHub Actions).

Your live site will be available at:

```
https://<your-username>.github.io/GhostDropETH/
```

Share that URL anywhere you promote the guide.

## Licensing & Attribution

The content in this repository is provided “as is.” You’re free to adapt it for your affiliate marketing campaigns. Please retain the disclosure language to stay compliant with FTC guidelines.
