# Mobile.Direct — Phase-wise build prompt

Use this prompt (phase by phase) to build, rebuild or extend the Mobile.Direct website. It is written so any capable developer or AI coding agent can execute it end to end.

---

## The idea (why this one wins)

**Mobile.Direct = the independent decision engine for phones, plans, travel eSIMs and trade-ins.** "Mobile direct" reads as *the direct route to the right mobile setup*. The site answers four money questions every phone owner asks every 1–3 years:

1. Which phone should I buy? (phone database, compare, personal match score)
2. Which plan should I be on? (plan finder quiz, carrier directory, savings estimate)
3. What do I use when I travel? (eSIM checker, destination planner, roaming-vs-eSIM calculator)
4. What is my old phone worth? (trade-in estimator, refurb-vs-new calculator)

### Why it beats the alternatives

| Option | Capital needed | Margin | Verdict |
|---|---|---|---|
| Online phone store | Inventory, warranty, payments | 3–8% hardware margin | Rejected: capital-heavy, price war with Amazon/carriers |
| Own MVNO / SIM reseller | Wholesale contracts, KYC, support | Good but slow | Rejected for v1: licensing + capex |
| Phone-repair directory | Local SEO per city | Low | Rejected: thin, local, slow |
| **Comparison + tools + lead gen hub** | **Zero inventory** | **Ads + leads + affiliate + sponsors** | **Chosen** |

Evidence from the 38-site study (see `RESEARCH.md`): the category leaders (WhistleOut, Uswitch, PlanHub, BankMyCell, SellCell, eSIMDB) all run this exact model; WhistleOut alone reports ~400,000 Canadian users a month, eSIMDB indexes 400k+ eSIM plans from 150+ providers, and buyback aggregators compare 20–40+ buyers. Telecom, device finance and travel are high-CPC advertiser categories, which lifts AdSense RPM above general-interest content.

### Revenue stack (in order of expected contribution)

1. **Lead generation** — consumer "Get matched" plan leads, B2B business-mobility quotes (highest value), trade-in quote requests, price-drop alerts.
2. **Google AdSense** — auto ads on every page (`ca-pub-6620975821265271`).
3. **Affiliate** — eSIM providers, refurbished retailers, MVNOs (add IDs in `data/config.json`).
4. **Sponsorships & advertising** — sponsored tools, newsletter, category sponsorships, white-label plan finder for publishers.
5. **Donations / supporter tiers** — PayPal donate + supporter pledges.
6. **Domain / partnership inquiries** — top-bar link on every page.

---

## Phase 0 — Positioning, brand and compliance

- Brand name always written **Mobile.Direct** (with the dot). Tagline: *Phones, plans and eSIMs — compared directly.*
- Independence policy: no carrier owns or controls rankings; affiliate links never change scores.
- Trademark/copyright disclosure page: not affiliated with any carrier, manufacturer, retailer or any business using a similar name; all marks belong to their owners; specs are manufacturer-published; prices are estimates.
- Top of **every** page: "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" linking to the owner's contact page (URL hidden under the link text).
- One private inbox receives every form. It is **never** printed anywhere; it is assembled at runtime from obfuscated pieces in `assets/js/site.js`.

## Phase 1 — Architecture and design system

- Static site, no build step required to host: plain HTML + CSS + vanilla JS, deployable on GitHub Pages free plan from `main` / root.
- A Python generator (`scripts/build.py`) renders every page from shared templates so header, footer, top bar, AdSense tag, schema and SEO tags stay identical.
- All internal links are relative so the site works on both `https://<user>.github.io/mobile-direct/` and the custom domain.
- Design tokens: ink `#14202B`, mineral paper `#F2F4F1`, SIM-chip gold `#D4A72C`, deep gold `#7E6110`, signal green `#1E7F5C`, weak-signal red `#B4432F`. Typeface: Archivo variable (expanded width for headlines, normal width for text).
- Signature shapes from the subject: SIM-card cut corner on interactive panels; 4-bar signal glyph used as a real data encoding (scores, signal quality).
- Light/dark theme toggle, keyboard focus states, reduced-motion support, responsive to 320 px.

## Phase 2 — Core data and content

- `data/phones.json` — 30+ current phones with launch price, screen, refresh rate, chipset, RAM/storage, battery, charging, cameras, IP rating, eSIM support.
- `data/carriers.json` — carriers for US, Canada, UK, India, Australia with type (network owner / sub-brand / MVNO), host network and official link.
- `data/bands.json` — 4G/5G bands per country for the "Will my phone work abroad?" tool.
- `data/esim-providers.json` — travel eSIM providers with plan types, hotspot and fair-use notes.
- 12+ original long-form guides (plan choice, MVNOs, eSIM, travel data, unlocking, trade-in, refurbished, used-phone safety, 5G, bill-cutting, business mobile, number porting) each with key takeaways, FAQ and links to tools.
- About page with scoring methodology and update policy (E-E-A-T).

## Phase 3 — Interactive tools (the traffic engine)

Phone finder + compare (up to 3) + personal match score with user weights · Plan finder quiz · Data usage calculator · Total cost of ownership calculator (A vs B, price rises included) · Refurb vs new savings · Trade-in value estimator · eSIM compatibility checker (EID test) · Will my phone work abroad (band match) · IMEI validator (Luhn + official blocklist links) · Roaming vs travel eSIM cost · Family plan bill splitter · Signal strength interpreter (RSRP/RSRQ/SINR to bars).

## Phase 4 — Lead-generation engine (dedicated, high-converting)

- `get-matched.html`: 6-step questionnaire (country, lines, data, priority, phone plan, current bill) → instant personalised recommendation + estimated yearly savings → capture form (name, email, phone optional, postal code, consent) → "Email my plan report".
- Hero on the home page starts the quiz (step 1 inline) so the first click is a commitment.
- `business.html`: B2B fleet quote (company, lines, devices, MDM, international, IoT, timeline, spend).
- Secondary capture: price-drop alerts on phones, trade-in quote requests, newsletter, eSIM trip plan by email.
- Conversion devices: progress bar, savings number before the form, trust line (free, no spam, unsubscribe anytime), consent checkbox, one-time gentle slide-in after engagement.

## Phase 5 — Monetisation pages

- AdSense: `<script async src=".../adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous">` in every `<head>`, `ads.txt` at root, optional manual slots in `data/config.json`.
- `support.html`: donations (one-time amounts + custom via PayPal, supporter tiers via pledge form); what money funds (operations, promotions, marketing, hiring, contests, prizes).
- `contests.html`: monthly contest with entry form, official rules (no purchase necessary), prize sponsorship CTA.
- `careers.html`: open roles (writers, video creators, data contributors, ambassadors, growth) + application form.
- `advertise.html`: sponsorship packages, white-label tools, newsletter sponsorship, domain/partnership inquiry.

## Phase 6 — Automation (self-updating)

- GitHub Actions workflow `auto-refresh.yml` runs every 6 hours, on push, and on demand:
  1. `scripts/refresh.py` pulls mobile news RSS feeds and YouTube channel feeds, de-duplicates, tags (iPhone, Android, Samsung, Pixel, 5G, eSIM, Carriers, Deals), writes `data/news.json`, `data/videos.json`, `data/meta.json`.
  2. `scripts/build.py` re-renders pages so headlines and videos are static HTML (crawlable), refreshes `sitemap.xml` dates.
  3. Commits only if something changed, then asks GitHub Pages to rebuild.
- Client-side: tip of the day rotates daily; "last updated" stamp reads `data/meta.json`.

## Phase 7 — SEO and AdSense approval checklist

Unique titles/descriptions, canonical URLs, Open Graph, JSON-LD (Organization, WebSite+SearchAction, Article, FAQPage, BreadcrumbList), `sitemap.xml`, `robots.txt`, `ads.txt`, privacy policy (AdSense cookies, opt-out links), terms, disclaimer, cookie policy, about, contact, no broken links, no thin pages, no copyrighted copy, ads never placed next to form buttons, original guides of 600+ words, fast load (no frameworks), mobile-friendly.

## Phase 8 — Deploy

1. Push to `main` of the GitHub repo.
2. Settings → Pages → Deploy from a branch → `main` / `(root)`.
3. Custom domain: add `mobile.direct` in Pages settings; at the registrar create `A` records to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 and a `CNAME` for `www` → `<user>.github.io`; tick "Enforce HTTPS".
4. Submit the domain to AdSense, verify ads.txt, enable Google's consent message (Privacy & messaging) for EEA/UK.
5. Send one test form; confirm the one-time activation email from the form relay.

## Phase 9 — 90-day growth plan

- Weeks 1–2: Search Console + sitemap, 10 more guides on long-tail queries ("best plan for seniors in Ontario", "will iPhone 17 work in Japan").
- Weeks 3–6: programmatic country pages (`esim-<country>.html`, `bands-<country>.html`) from existing JSON.
- Weeks 6–10: affiliate IDs for eSIM + refurb partners; sell B2B leads to 2–3 business-mobility resellers.
- Weeks 10–13: newsletter sponsorships, first sponsored contest, white-label plan finder pitch to publishers.
