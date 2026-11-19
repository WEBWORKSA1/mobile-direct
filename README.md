# Mobile.Direct

Independent tools and guides for choosing phones, plans and travel eSIMs. Static site, hosted free on GitHub Pages from `main` (root), monetised with Google AdSense, lead generation, sponsorships, contests and reader contributions.

- **Concept, revenue model and phase-wise build prompt:** [`docs/PROMPT.md`](docs/PROMPT.md)
- **38-site niche research:** [`docs/RESEARCH.md`](docs/RESEARCH.md)

## What is in the site

| Area | Pages |
|---|---|
| Decision tools | Phone finder + compare + personal match score, plan match quiz, travel eSIM planner, trade-in estimator, 9 calculators on `tools.html` |
| Lead generation | `get-matched.html` (consumer plan leads), `business.html` (B2B fleet quotes), trade-in quote requests, price-drop alerts, eSIM trip plans, deal alerts, newsletter |
| Content | 12 original guides in `guides/`, carrier directory for US/CA/UK/IN/AU, eSIM provider comparison, deal calendar |
| Auto-updated | `news.html` and `videos.html` (plus home page blocks), refreshed every 6 hours by GitHub Actions |
| Monetisation | AdSense auto ads on every page + `ads.txt`, `support.html` (PayPal contributions + pledges), `contests.html`, `careers.html`, `advertise.html` |
| Trust and compliance | `about.html` (methodology), `privacy.html`, `terms.html`, `disclaimer.html` (trademark/copyright/affiliate disclosure), `cookies.html`, `contact.html` |

Every page carries the owner contact strip at the top. All forms post to the owner's private inbox through FormSubmit; the address is assembled at runtime in `assets/js/site.js` and never appears in the HTML.

## Editing

All pages are generated. Edit the source, then rebuild:

```bash
python3 scripts/build.py
```

| To change | Edit |
|---|---|
| Phones | `data/phones.json` |
| Carriers and price ranges | `data/carriers.json` |
| Country bands | `data/bands.json` |
| eSIM providers | `data/esim-providers.json` |
| Contest | `data/contests.json` |
| Manual AdSense slots, affiliate IDs | `data/config.json` |
| Guides | `scripts/guides_content.py` |
| Page copy and layout | `scripts/pages_content.py`, `scripts/build.py` |
| Styles | `assets/css/site.css` |
| News feeds and video channels | `scripts/refresh.py`, `data/videos.json` |

## Automation

`.github/workflows/auto-refresh.yml` runs every six hours, on every push to `main` and on demand (Actions → Auto-refresh content → Run workflow). It pulls headlines and YouTube uploads, rebuilds pages and the sitemap, commits only when something changed and asks Pages to rebuild.

## Go-live checklist

1. **Pages:** Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save.
2. **Custom domain:** in the same screen enter `mobile.direct`, then at the registrar add `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` and a `CNAME` for `www` → `webworksa1.github.io`. Tick **Enforce HTTPS** once the certificate is issued.
3. **Forms:** submit any form once on the live site. FormSubmit sends a one-time activation email to the owner inbox; click *Activate*. Until then submissions are held.
4. **AdSense:** add the site in AdSense, confirm `ads.txt` is detected, and turn on the Google consent message (Privacy & messaging) for EEA/UK/Switzerland traffic.
5. **Search Console:** verify the domain and submit `https://mobile.direct/sitemap.xml`.

## Licence

© Mobile.Direct. All rights reserved. Brand and product names belong to their owners; see `disclaimer.html`.
