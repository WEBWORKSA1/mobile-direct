#!/usr/bin/env python3
"""Render every Mobile.Direct page from shared templates.

Run from anywhere:  python3 scripts/build.py
Pages are written to the repository root (and guides/). Data comes from data/*.json.
The auto-refresh workflow runs this after refresh.py so headlines and videos are static, crawlable HTML.
"""
import hashlib
import html
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guides_content import GUIDES  # noqa: E402
from pages_content import PAGES_CONTENT  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://mobile.direct"
CONTENT_DATE = "2026-11-19"
ADSENSE = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
           '?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>')
OWNER_LINK = "https://web.works/contact"
TOPLINE = "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership"
THEME_INIT = ("<script>try{var t=localStorage.getItem('md-theme');"
              "if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>")
e = html.escape

NAV = [
    ("phones.html", "Phones"), ("plans.html", "Plans"), ("esim.html", "eSIM"),
    ("trade-in.html", "Trade-in"), ("tools.html", "Tools"), ("guides.html", "Guides"),
    ("news.html", "News"), ("videos.html", "Videos"),
]
SITEMAP = []  # (path, lastmod, priority)


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def ver(rel):
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


# ---------- shared bits ----------

def bars(n, weak=False, lg=False):
    n = max(0, min(4, round(n)))
    cls = "bars b%d%s%s" % (n, " weak" if weak else "", " lg" if lg else "")
    return '<span class="%s" aria-hidden="true"><i></i><i></i><i></i><i></i></span>' % cls


CHIP = {
    "A19 Pro": 10, "Snapdragon 8 Elite Gen 5": 10, "Snapdragon 8 Elite Gen 5 for Galaxy": 10,
    "A19": 9.5, "Snapdragon 8 Elite": 9.4, "Snapdragon 8 Elite for Galaxy": 9.5,
    "A18": 8.8, "Snapdragon 8 Gen 3": 8.5, "Snapdragon 8s Gen 4": 8.3, "Tensor G5": 8.2, "Exynos 2500": 8.2,
    "Exynos 2400": 8.0, "Tensor G4": 7.5, "Exynos 1580": 6.4, "Dimensity 7400X": 6.3,
    "Snapdragon 7s Gen 3": 6.2, "Dimensity 6300": 4.8,
}


def clamp(v, a=0, b=10):
    return max(a, min(b, v))


def pscore(p):
    """Same formula as assets/js/phones.js (keep in sync)."""
    perf = CHIP.get(p["chipset"], 6)
    cams = p["cameras"]
    camera = 5 + min(2, len(cams) - 1) * 1.1 + (1.4 if p.get("tele") else 0) + \
        (0.7 if cams[0] >= 200 else 0.5 if cams[0] >= 48 else 0) + (0.4 if perf >= 9 else 0)
    battery = 4 + ((p.get("battery") or 4000) - 3000) / 700 + (1.2 if p["os"] == "iOS" else 0) + \
        (0.5 if (p.get("charging") or 25) >= 60 else 0)
    display = 5 + (2 if p["refresh"] >= 120 else 1 if p["refresh"] >= 90 else 0) + \
        (0.5 if p["refresh"] > 120 else 0) + clamp((p["display"] - 6.0) * 1.6, 0, 2.2)
    avg = (perf + clamp(camera) + clamp(battery) + clamp(display)) / 4
    value = 2 + 8 * (avg / 10) * math.sqrt(700 / max(150, p["price"]))
    s = dict(perf=clamp(perf), camera=clamp(camera), battery=clamp(battery), display=clamp(display), value=clamp(value))
    s["match"] = sum(s.values()) / 5
    return s


def pname(p):
    return p["model"] if p["model"].lower().startswith(p["brand"].lower()) else p["brand"] + " " + p["model"]


def spec_line(p):
    batt = ("~" if p.get("batteryApprox") else "") + "%d mAh" % p["battery"] if p.get("battery") else "battery n/a"
    cams = " + ".join(("%g" % c) for c in p["cameras"])
    return '%s" %sHz, %s, %s GB RAM, %s, %s MP' % (p["display"], p["refresh"], p["chipset"], p["ram"], batt, cams)


def money(n):
    return "${:,.0f}".format(n)


def jsonld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (u, n) in enumerate(items)]}


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def faq_html(faq):
    return '<div class="faq">' + "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in faq) + "</div>"


# ---------- page shell ----------

def head(path, title, desc, r, ld, og_type, robots, base_script=""):
    canon = SITE + "/" + ("" if path == "index.html" else path)
    full_title = title if path == "index.html" else "%s | Mobile.Direct" % title
    lds = "".join(jsonld(x) for x in (ld or []))
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{r}">
<head>
<meta charset="utf-8">
{base_script}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:site_name" content="Mobile.Direct">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14202B">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/img/icon-192.png">
<link rel="manifest" href="{r}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&amp;display=swap">
<link rel="stylesheet" href="{r}assets/css/site.css?v={ver('assets/css/site.css')}">
{THEME_INIT}
{ADSENSE}
{lds}
</head>"""


def header(r, active):
    items = "".join(
        '<li><a href="%s%s"%s>%s</a></li>' % (r, u, ' aria-current="page"' if u == active else "", n) for u, n in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><a href="{OWNER_LINK}" target="_blank" rel="noopener">{TOPLINE}</a></div></div>
<header class="site-header"><div class="wrap">
<a class="logo" href="{r}index.html" aria-label="Mobile.Direct home"><span class="logo-bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span>Mobile<span class="dot">.</span>Direct</span></a>
<nav class="nav" id="site-nav" aria-label="Main"><ul>{items}</ul></nav>
<div class="header-actions">
<button class="icon-btn" id="theme-toggle" type="button" aria-label="Switch colour theme"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg></button>
<button class="icon-btn menu-btn" id="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2"/></svg></button>
<a class="btn btn-sm btn-gold" href="{r}get-matched.html">Get matched</a>
</div></div></header>"""


def footer(r):
    col = lambda title, links: "<div><h2>%s</h2><ul>%s</ul></div>" % (
        title, "".join('<li><a href="%s%s">%s</a></li>' % (r, u, n) for u, n in links))
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div>
<a class="logo" href="{r}index.html"><span class="logo-bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span>Mobile<span class="dot">.</span>Direct</span></a>
<p class="small" style="margin-top:12px">Independent tools and guides for choosing phones, plans and eSIMs.</p>
<form class="newsletter-form" data-md-form="Newsletter signup" data-success="Subscribed. The next deals and plan-change briefing lands in your inbox on Thursday.">
<label for="nl-email">Weekly plan and phone deals briefing</label>
<div class="newsletter"><input id="nl-email" type="email" name="email" required autocomplete="email" placeholder="you@example.com"><button class="btn btn-sm" type="submit">Subscribe</button></div>
<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<p class="form-status small" role="status"></p>
</form>
<p class="small">Data last refreshed <time data-last-updated>recently</time>.</p>
</div>
{col("Compare", [("phones.html", "Phone finder"), ("plans.html", "Plans and carriers"), ("esim.html", "Travel eSIM"), ("trade-in.html", "Trade-in value"), ("deals.html", "Deal calendar")])}
{col("Learn", [("tools.html", "All tools"), ("guides.html", "Guides"), ("news.html", "News"), ("videos.html", "Videos"), ("get-matched.html", "Plan match")])}
{col("Get involved", [("support.html", "Support Mobile.Direct"), ("contests.html", "Contests and prizes"), ("careers.html", "Careers"), ("advertise.html", "Advertise and partner"), ("business.html", "Business quotes")])}
{col("About", [("about.html", "About and methodology"), ("contact.html", "Contact"), ("privacy.html", "Privacy policy"), ("terms.html", "Terms of use"), ("disclaimer.html", "Disclaimer and trademarks"), ("cookies.html", "Cookie policy")])}
</div>
<p class="legal-line">&copy; <span data-year>2026</span> Mobile.Direct. An independent website, not affiliated with any carrier, manufacturer, retailer or business with a similar name. Product and carrier names are trademarks of their owners. Prices and specs are estimates; confirm with the provider. Some links may earn us a commission, which never changes a ranking. <a href="{r}disclaimer.html">Full disclosure</a>.</p>
</div></footer>
<div class="cookie" id="cookie" hidden role="region" aria-label="Cookie notice"><p>We use cookies to show ads (Google AdSense), play embedded videos and remember your settings. Read the <a href="{r}cookies.html">cookie policy</a>.</p><button class="btn btn-sm" type="button" data-cookie-ok="ok">OK</button></div>
<aside class="slidein" id="slidein" aria-label="Plan match"><div class="sim"><div class="sim-body"><button class="close" type="button" aria-label="Close">&times;</button><p class="quiz-q">Paying too much for your plan?</p><p class="small">Six questions, about a minute. See your best-fit plan and an estimated yearly saving.</p><a class="btn" href="{r}get-matched.html">Find my plan</a></div></div></aside>"""


def render(path, title, desc, body, *, scripts=(), ld=None, active=None, og_type="website",
           robots="index,follow", priority="0.6", lastmod=CONTENT_DATE, body_attr="", sitemap=True, base_script=""):
    depth = path.count("/")
    r = "../" * depth if not base_script else ""
    js = ['<script src="%sassets/js/site.js?v=%s" defer></script>' % (r, ver("assets/js/site.js"))]
    for s in scripts:
        js.append('<script src="%sassets/js/%s?v=%s" defer></script>' % (r, s, ver("assets/js/" + s)))
    doc = "%s\n<body%s>\n%s\n<main id=\"main\">\n%s\n</main>\n%s\n%s\n</body>\n</html>\n" % (
        head(path, title, desc, r, ld, og_type, robots, base_script), body_attr, header(r, active),
        body.replace("{r}", r), footer(r), "\n".join(js))
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    if sitemap:
        SITEMAP.append((path, lastmod, priority))


def page_head(title, lede, crumbs=None):
    c = ""
    if crumbs:
        c = '<p class="crumbs"><a href="{r}index.html">Home</a> / ' + " / ".join(
            '<a href="{r}%s">%s</a>' % (u, e(n)) for u, n in crumbs[:-1]) + (" / " if len(crumbs) > 1 else "") + e(crumbs[-1][1]) + "</p>"
    return '<section class="page-head"><div class="wrap">%s<h1>%s</h1><p class="lede">%s</p></div></section>' % (c, e(title), lede)


# ---------- tools (reused on several pages) ----------

def range_field(id_, label, rate=None, mn=0, mx=8, step=0.25, val=0, unit=" h"):
    rate_attr = ' data-rate="%s"' % rate if rate is not None else ""
    return ('<div class="field"><label for="%s">%s</label><div class="range-row"><input type="range" id="%s"%s min="%s" max="%s" step="%s" value="%s">'
            '<output for="%s" data-unit="%s"></output></div></div>') % (id_, label, id_, rate_attr, mn, mx, step, val, id_, unit)


def consent(text="I agree that Mobile.Direct may contact me about this request and share it with up to three matched providers so they can contact me. I can opt out at any time."):
    return '<div class="field"><label class="check"><input type="checkbox" name="consent" value="yes" required> <span>%s See the <a href="{r}privacy.html">privacy policy</a>.</span></label></div>' % text


HONEY = '<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'


def tool_data():
    rows = [("d-sd", "Video streaming, standard definition", 1.0, 0.25), ("d-hd", "Video streaming, HD", 3.0, 0),
            ("d-social", "Social media with video", 0.7, 0.5), ("d-calls", "Video calls", 1.0, 0),
            ("d-music", "Music or podcasts", 0.15, 0.5), ("d-web", "Web, email and messaging", 0.1, 1.5),
            ("d-maps", "Maps and navigation", 0.05, 0.25), ("d-games", "Online gaming", 0.06, 0)]
    fields = "".join(range_field(i, l, r, val=v) for i, l, r, v in rows)
    return f"""<div class="tool" id="tool-data">
<div class="tool-in"><h2>Data usage calculator</h2><p class="small">Set the hours a day you spend on each activity away from Wi-Fi.</p>
<div class="grid-2">{fields}</div>
{range_field("data-wifi", "Share of that time on Wi-Fi anyway", None, 0, 90, 5, 50, "%")}
</div>
<div class="tool-out" aria-live="polite"><p class="small">Estimated mobile data a month</p><div id="data-bars"></div><p class="big-out" id="data-out">0 GB</p><p id="data-rec"></p>
<p class="small">Rates used: SD video about 1 GB an hour, HD about 3 GB, high-quality music about 0.15 GB.</p>
<a class="btn" href="{{r}}get-matched.html">Match me to a plan this size</a></div>
</div>"""


def tool_tco():
    def col(p, name, dev, trade, plan, extras, months, rise):
        f = lambda n, l, v, step="1": '<div class="field"><label for="%s%s">%s</label><input id="%s%s" name="%s%s" type="number" min="0" step="%s" value="%s"></div>' % (p, n, l, p, n, p, n, step, v)
        return "<div><h3>%s</h3>%s%s%s%s%s%s</div>" % (name, f("device", "Phone price (total)", dev), f("trade", "Trade-in or credit", trade),
                                                      f("plan", "Plan per month", plan), f("extras", "Extras per month (insurance, add-ons)", extras),
                                                      f("months", "Months you will keep it", months), f("rise", "Yearly price rise (%)", rise, "0.1"))
    return f"""<div class="tool" id="tool-tco">
<div class="tool-in"><h2>Total cost of ownership</h2><p class="small">Compare a carrier deal with buying unlocked plus a cheaper plan, including yearly price rises.</p>
<div class="grid-2">{col("a", "Option A: carrier deal", 1099, 400, 85, 0, 36, 3)}{col("b", "Option B: unlocked phone + budget plan", 799, 250, 30, 0, 36, 0)}</div></div>
<div class="tool-out" aria-live="polite"><p class="small">Option A total</p><p class="big-out" id="tco-a">$0</p><p class="small" id="tco-a-m"></p>
<p class="small">Option B total</p><p class="big-out" id="tco-b">$0</p><p class="small" id="tco-b-m"></p><p id="tco-verdict" class="tip"></p></div>
</div>"""


def tool_refurb():
    return f"""<div class="tool" id="tool-refurb">
<div class="tool-in"><h2>Refurbished vs new</h2>
<div class="field"><label for="rf-new">New price</label><input id="rf-new" type="number" min="0" value="799"></div>
{range_field("rf-disc", "Refurbished discount", None, 10, 70, 1, 35, "%")}
<div class="field"><label class="check"><input type="checkbox" id="rf-batt"> <span>Add a new battery</span></label></div>
<div class="field"><label for="rf-batt-cost">Battery replacement cost</label><input id="rf-batt-cost" type="number" min="0" value="89"></div>
</div>
<div class="tool-out" aria-live="polite"><p class="small">You save</p><p class="big-out" id="rf-out">$0</p><ul class="result-list" id="rf-detail"></ul>
<p class="small">Typical refurbished discounts run 30–70% depending on age and grade.</p></div>
</div>"""


def tool_tradein():
    return f"""<div class="tool" id="tool-tradein">
<div class="tool-in"><h2>Trade-in value estimator</h2>
<div class="field"><label for="ti-phone">Your phone</label><select id="ti-phone"><option>Loading phones…</option></select></div>
<div class="grid-2"><div class="field"><label for="ti-price">Launch price (USD)</label><input id="ti-price" type="number" min="0" value="799"></div>
<div class="field"><label for="ti-storage">Storage</label><select id="ti-storage"><option value="1">Base storage</option><option value="1.08">Double the base</option><option value="1.15">Four times the base or more</option></select></div></div>
{range_field("ti-age", "Age", None, 0, 72, 1, 14, " mo")}
<div class="grid-2"><div class="field"><label for="ti-cond">Condition</label><select id="ti-cond"><option value="flawless">Flawless</option><option value="good" selected>Good: light scratches</option><option value="fair">Fair: visible wear</option><option value="cracked">Cracked or faulty</option></select></div>
<div class="field"><label class="check" style="margin-top:34px"><input type="checkbox" id="ti-locked"> <span>Still carrier-locked</span></label></div></div>
</div>
<div class="tool-out" aria-live="polite"><p class="small">Estimated cash value today</p><p class="big-out" id="ti-out">$0</p><p class="small" id="ti-note"></p>
<form data-md-form="Trade-in quote request" data-success="Request received. We will send you competing offers from buyback partners within two business days.">
<h3>Get real offers for this phone</h3>
<div class="field"><label for="ti-name">Name</label><input id="ti-name" name="name" type="text" required autocomplete="name"></div>
<div class="field"><label for="ti-email">Email</label><input id="ti-email" name="email" type="email" required autocomplete="email"></div>
<input type="hidden" name="estimate" id="ti-summary">{HONEY}
{consent()}
<button class="btn btn-gold" type="submit">Send me offers</button><p class="form-status" role="status"></p></form>
</div>
</div>"""


def tool_esim():
    return """<div class="tool" id="tool-esim">
<div class="tool-in"><h2>eSIM compatibility checker</h2>
<div class="grid-2"><div class="field"><label for="es-brand">Brand</label><select id="es-brand"></select></div>
<div class="field"><label for="es-model">Model</label><select id="es-model"></select></div></div>
<h3>The 10-second test for any phone</h3>
<p>Open the phone app and dial <strong>*#06#</strong>. If an <strong>EID</strong> (a 32-digit number) appears, your phone supports eSIM. The phone must also be unlocked to add an eSIM from another provider.</p>
</div>
<div class="tool-out" aria-live="polite"><p class="small">Result</p><p id="es-out" class="big-out" style="font-size:1.6rem"></p><p id="es-note"></p>
<a class="btn" href="{r}esim.html">Plan a trip with eSIM</a></div>
</div>"""


def tool_bands():
    return """<div class="tool" id="tool-bands">
<div class="tool-in"><h2>Will my phone work abroad?</h2><p class="small">Matches your phone's 4G and 5G bands against the bands operators use in each country.</p>
<div class="field"><label for="bd-country">Country</label><select id="bd-country"></select></div>
<div class="field"><label for="bd-preset">Your phone</label><select id="bd-preset"></select></div>
<div class="field" id="bd-custom-wrap" hidden><label for="bd-custom">Your phone's bands</label><input id="bd-custom" type="text" placeholder="e.g. 1 3 7 20 28 n78"><p class="small">Copy them from the spec sheet. Plain numbers are 4G bands; prefix 5G bands with n.</p></div>
</div>
<div class="tool-out" aria-live="polite"><p class="small">Verdict</p><p id="bd-out" class="big-out" style="font-size:1.6rem"></p><ul class="result-list" id="bd-detail"></ul>
<p class="small">Indicative only. Operators change spectrum over time, so confirm with the operator before you travel.</p></div>
</div>"""


def tool_imei():
    return """<div class="tool" id="tool-imei">
<div class="tool-in"><h2>IMEI validator</h2><p class="small">Checks the IMEI's built-in check digit in your browser. Nothing is sent or stored.</p>
<div class="field"><label for="imei-in">IMEI (dial *#06# to see it)</label><input id="imei-in" type="text" inputmode="numeric" autocomplete="off" maxlength="17" placeholder="15 digits"></div>
<h3>Then check an official blocklist</h3>
<ul><li>United States: <a href="https://www.stolenphonechecker.org/" rel="nofollow noopener" target="_blank">Stolen Phone Checker</a></li>
<li>Australia: <a href="https://www.lost.amta.org.au/" rel="nofollow noopener" target="_blank">AMTA lost and stolen register</a></li>
<li>India: <a href="https://www.sancharsaathi.gov.in/" rel="nofollow noopener" target="_blank">Sanchar Saathi</a></li>
<li>Elsewhere: ask any local carrier to check the IMEI.</li></ul>
</div>
<div class="tool-out" aria-live="polite"><p class="small">Result</p><p id="imei-out" class="big-out" style="font-size:1.6rem">Enter 15 digits</p><p id="imei-note"></p>
<a class="btn btn-ghost" href="{r}guides/buying-used-phone-safely.html">Used-phone safety checklist</a></div>
</div>"""


def tool_roam():
    return """<div class="tool" id="tool-roam">
<div class="tool-in"><h2>Roaming vs travel eSIM</h2>
<div class="grid-2"><div class="field"><label for="ro-days">Trip length (days)</label><input id="ro-days" type="number" min="1" value="7"></div>
<div class="field"><label for="ro-gb">Daily data use</label><select id="ro-gb"><option value="0.3">Light: maps and messages (0.3 GB)</option><option value="0.8" selected>Moderate: social and photos (0.8 GB)</option><option value="1.5">Heavy: video and calls (1.5 GB)</option><option value="3">Hotspot for a laptop (3 GB)</option></select></div></div>
<div class="grid-3"><div class="field"><label for="ro-pass">Carrier day pass, per day</label><input id="ro-pass" type="number" min="0" step="0.5" value="12"></div>
<div class="field"><label for="ro-pergb">Travel eSIM, price per GB</label><input id="ro-pergb" type="number" min="0" step="0.1" value="4.5"></div>
<div class="field"><label for="ro-unl">Unlimited eSIM, per day</label><input id="ro-unl" type="number" min="0" step="0.1" value="6"></div></div>
<p class="small">Defaults are typical market prices; replace them with real quotes for your trip.</p></div>
<div class="tool-out" aria-live="polite"><p class="small">Cheapest option</p><p class="big-out" id="ro-out">$0</p><p id="ro-best"></p><ul class="result-list" id="ro-detail"></ul></div>
</div>"""


def tool_split():
    return f"""<div class="tool" id="tool-split">
<div class="tool-in"><h2>Family plan bill splitter</h2>
<div class="grid-2"><div class="field"><label for="sp-total">Total monthly bill</label><input id="sp-total" type="number" min="0" value="140"></div>
<div>{range_field("sp-share", "Share of the bill split by data use", None, 0, 100, 5, 50, "%")}</div></div>
<div id="sp-rows"></div><button type="button" class="btn btn-ghost btn-sm" id="sp-add">Add a line</button></div>
<div class="tool-out" aria-live="polite"><p class="small">Each person pays</p><ul class="result-list" id="sp-detail"></ul>
<p class="small">The rest of the bill is split equally, so light users still pay their share of the base cost.</p></div>
</div>"""


def tool_signal():
    return """<div class="tool" id="tool-signal">
<div class="tool-in"><h2>Signal strength interpreter</h2>
<p class="small">Find the numbers on Android under Settings, About phone, SIM status (or a network info app). On iPhone, the Field Test mode shows them.</p>
<div class="grid-3"><div class="field"><label for="sg-rsrp">RSRP (dBm)</label><input id="sg-rsrp" type="number" step="1" value="-95"></div>
<div class="field"><label for="sg-rsrq">RSRQ (dB)</label><input id="sg-rsrq" type="number" step="0.5" value="-11"></div>
<div class="field"><label for="sg-sinr">SINR (dB)</label><input id="sg-sinr" type="number" step="0.5" value="10"></div></div></div>
<div class="tool-out" aria-live="polite"><p class="small">Overall connection</p><p id="sg-out" class="big-out" style="font-size:1.6rem"></p><ul class="result-list" id="sg-detail"></ul><p id="sg-advice" class="tip"></p></div>
</div>"""


def tool_trip():
    return f"""<div class="tool" id="tool-trip">
<div class="tool-in"><h2>Travel eSIM planner</h2>
<div class="field"><label for="tr-country">Destination</label><select id="tr-country"></select></div>
<div class="grid-2"><div class="field"><label for="tr-days">Days</label><input id="tr-days" type="number" min="1" value="10"></div>
<div class="field"><label for="tr-use">How you use data</label><select id="tr-use"><option value="0.3">Light: maps and messages</option><option value="0.8" selected>Moderate: social, photos, some video</option><option value="1.5">Heavy: video and calls</option><option value="3">Hotspot for a laptop</option></select></div></div>
<ul class="result-list" id="tr-bands"></ul><p class="small"><a id="tr-bandlink" href="{{r}}tools.html#bands">Check your phone against these bands</a></p>
</div>
<div class="tool-out" aria-live="polite"><p class="small">Data to buy (20% buffer included)</p><p class="big-out" id="tr-out">0 GB</p><p id="tr-rec"></p>
<form data-md-form="eSIM trip plan request" data-success="Sent. Your trip plan and the best current eSIM offers for it are on their way.">
<h3>Email me this trip plan with current offers</h3>
<div class="field"><label for="tr-email">Email</label><input id="tr-email" name="email" type="email" required autocomplete="email"></div>
<input type="hidden" name="trip" id="tr-summary">{HONEY}
{consent("I agree that Mobile.Direct may email me about this trip plan and related offers. I can opt out at any time.")}
<button class="btn btn-gold" type="submit">Email my trip plan</button><p class="form-status" role="status"></p></form>
</div>
</div>"""


# ---------- dynamic blocks ----------

def news_block(limit, r=""):
    items = load("news.json").get("items", [])[:limit]
    if not items:
        return ('<ul class="news-list" id="news-list"><li data-empty><time></time><div>Headlines refresh automatically every six hours. '
                'While they load, read our <a href="%sguides.html">guides</a>.</div></li></ul>' % r)
    lis = []
    for n in items:
        d = n.get("date", "")
        try:
            label = datetime.fromisoformat(d.replace("Z", "+00:00")).strftime("%b %d").replace(" 0", " ")
        except ValueError:
            label = ""
        lis.append('<li data-tags="%s"><time datetime="%s">%s</time><div><a href="%s" rel="nofollow noopener" target="_blank">%s</a><span class="src">%s</span></div></li>' % (
            e(" ".join(n.get("tags", []))), e(d), label, e(n["link"]), e(n["title"]), e(n.get("source", ""))))
    return '<ul class="news-list" id="news-list">%s</ul>' % "".join(lis)


def videos_block(limit):
    v = load("videos.json")
    figs = []
    for it in v.get("videos", [])[:limit]:
        thumb = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % it["id"]
        figs.append('<figure class="video"><div class="frame"><button type="button" data-yt="%s" aria-label="Play: %s" style="background-image:url(\'%s\')"><span></span></button></div>'
                    '<figcaption><strong>%s</strong>%s</figcaption></figure>' % (e(it["id"]), e(it["title"]), thumb, e(it["title"]), e(it.get("channel", ""))))
    if len(figs) < limit:
        for ch in v.get("channels", [])[: limit - len(figs)]:
            up = "UU" + ch["id"][2:]
            figs.append('<figure class="video"><div class="frame"><button type="button" data-list="%s" aria-label="Play latest uploads from %s"><span></span><em>%s</em></button></div>'
                        '<figcaption><strong>Latest from %s</strong>%s</figcaption></figure>' % (up, e(ch["name"]), e(ch["name"]), e(ch["name"]), e(ch.get("topic", ""))))
    return '<div class="video-grid">%s</div>' % "".join(figs)


def phone_rows(phones):
    out = []
    for i, p in enumerate(phones):
        s = p["_s"]
        out.append('<li class="phone-row"><span class="rank">%d</span><div><h3>%s</h3><span class="small">Released %s. eSIM: %s</span></div>'
                   '<div class="specs">%s%s</div><div><div class="score">%s %.1f</div><span class="small">%s%s</span></div>'
                   '<div class="acts"><button type="button" class="btn btn-sm btn-ghost" data-compare="%s" aria-pressed="false">Compare</button>'
                   '<button type="button" class="btn btn-sm btn-ghost" data-open-dialog="alert-dialog" data-item="%s">Price alert</button></div></li>' % (
                       i + 1, e(pname(p)), e(p["released"]), e(p["esim"]), e(spec_line(p)),
                       (", " + p["ip"]) if p.get("ip") else "", bars(s["match"] / 2.5), s["match"], money(p["price"]),
                       (" (%s)" % e(p["priceNote"])) if p.get("priceNote") else "", p["id"], e(pname(p))))
    return "".join(out)


# ---------- build ----------

def build():
    phones = load("phones.json")["phones"]
    for p in phones:
        p["_s"] = pscore(p)
    carriers = load("carriers.json")["countries"]
    bands = load("bands.json")["countries"]
    meta = load("meta.json")
    live_date = meta.get("lastUpdated", CONTENT_DATE)[:10]
    n_carriers = sum(len(c["carriers"]) for c in carriers.values())
    ctx = dict(phones=phones, carriers=carriers, bands=bands, n_carriers=n_carriers, n_countries=len(bands),
               GUIDES=GUIDES, tools=dict(data=tool_data, tco=tool_tco, refurb=tool_refurb, tradein=tool_tradein, esim=tool_esim,
                                         bands=tool_bands, imei=tool_imei, roam=tool_roam, split=tool_split, signal=tool_signal, trip=tool_trip),
               news_block=news_block, videos_block=videos_block, phone_rows=phone_rows, pname=pname, page_head=page_head, consent=consent,
               HONEY=HONEY, bars=bars, money=money, faq_html=faq_html, e=e, load=load, OWNER_LINK=OWNER_LINK)

    for spec in PAGES_CONTENT:
        body = spec["body"](ctx)
        ld = list(spec.get("ld", []))
        if spec["path"] != "index.html" and spec.get("crumb"):
            ld.append(crumbs_ld([(spec["path"], spec["crumb"])]))
        if spec.get("faq"):
            ld.append(faq_ld(spec["faq"]))
        dynamic = spec.get("dynamic")
        render(spec["path"], spec["title"], spec["desc"], body, scripts=spec.get("scripts", ()), ld=ld,
               active=spec.get("active"), priority=spec.get("priority", "0.6"),
               lastmod=live_date if dynamic else CONTENT_DATE, body_attr=spec.get("body_attr", ""),
               sitemap=spec.get("sitemap", True), robots=spec.get("robots", "index,follow"),
               base_script=spec.get("base_script", ""))

    # Guides
    for g in GUIDES:
        path = "guides/%s.html" % g["slug"]
        tools_links = "".join('<li><a href="{r}%s">%s</a></li>' % (u, e(n)) for u, n in g["tools"])
        others = "".join('<li><a href="{r}guides/%s.html">%s</a></li>' % (o["slug"], e(o["title"])) for o in GUIDES if o["slug"] != g["slug"])
        body = f"""<section class="section" style="padding-top:36px"><div class="wrap article-wrap">
<article class="prose">
<p class="crumbs"><a href="{{r}}index.html">Home</a> / <a href="{{r}}guides.html">Guides</a> / {e(g["title"])}</p>
<h1 style="font-size:clamp(2rem,4.2vw,3.1rem)">{e(g["title"])}</h1>
<p class="byline">Mobile.Direct editorial team. Updated <time datetime="{g["updated"]}">{datetime.fromisoformat(g["updated"]).strftime("%d %B %Y").lstrip("0")}</time>. {g["minutes"]}-minute read.</p>
<div class="takeaways"><h2>Key takeaways</h2><ul>{"".join("<li>%s</li>" % e(t) for t in g["takeaways"])}</ul></div>
{g["body"]}
<div class="ad-slot" data-slot="inArticle"></div>
<h2>Frequently asked questions</h2>
{faq_html(g["faq"])}
<div class="notice" style="margin-top:28px">Spotted something out of date? <a href="{{r}}contact.html">Send a correction</a> and we will update the guide.</div>
</article>
<aside><div class="aside-sticky">
<div class="aside-box"><h2 style="font-size:1.1rem">Tools for this guide</h2><ul>{tools_links}</ul></div>
<div class="sim"><div class="sim-body"><p class="quiz-q" style="font-size:1.15rem">Find your best-fit plan</p><p class="small">Six questions. See an estimated yearly saving before you share anything.</p><a class="btn" href="{{r}}get-matched.html">Start the plan match</a></div></div>
<div class="aside-box" style="margin-top:32px"><h2 style="font-size:1.1rem">More guides</h2><ul>{others}</ul></div>
</div></aside>
</div></section>"""
        article = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
                   "datePublished": g["updated"], "dateModified": g["updated"], "author": {"@type": "Organization", "name": "Mobile.Direct"},
                   "publisher": {"@type": "Organization", "name": "Mobile.Direct", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/icon-512.png"}},
                   "mainEntityOfPage": SITE + "/" + path, "image": SITE + "/assets/img/og.png"}
        render(path, g["title"], g["desc"], body, ld=[article, faq_ld(g["faq"]), crumbs_ld([("guides.html", "Guides"), (path, g["title"])])],
               active="guides.html", og_type="article", priority="0.7")

    # sitemap
    urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (
        SITE, "" if p == "index.html" else p, lm, pr) for p, lm, pr in SITEMAP)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls, encoding="utf-8")
    print("Built %d pages" % (len(SITEMAP) + 1))


if __name__ == "__main__":
    build()
