# Page bodies for Mobile.Direct. Each entry's body(ctx) returns HTML; "{r}" is replaced with the relative root.
import json

SITE = "https://mobile.direct"


def _sec(inner, cls="section", attrs=""):
    return '<section class="%s"%s><div class="wrap">%s</div></section>' % (cls, attrs, inner)


def _head(title, desc_p, more=None):
    m = '<a class="more" href="{r}%s">%s</a>' % more if more else ""
    return '<div class="section-head"><div><h2>%s</h2><p>%s</p></div>%s</div>' % (title, desc_p, m)


# ---------------- HOME ----------------
def home(c):
    e = c["e"]
    top = sorted(c["phones"], key=lambda p: p["released"], reverse=True)[:6]
    rows = "".join(
        '<tr><td><strong>%s</strong><br><span class="small">Released %s</span></td><td class="num">%s</td><td>%s"</td><td>%s</td><td>%s %.1f</td></tr>' % (
            e(c["pname"](p)), p["released"], c["money"](p["price"]), p["display"], e(p["chipset"]),
            c["bars"](p["_s"]["match"] / 2.5), p["_s"]["match"]) for p in top)
    guides = "".join('<li><a href="{r}guides/%s.html"><h3>%s</h3><p>%s</p></a></li>' % (g["slug"], e(g["title"]), e(g["desc"])) for g in c["GUIDES"][:6])
    return f"""
<section class="hero"><div class="wrap">
<div>
<h1>Phones, plans and eSIMs. Compared directly.</h1>
<p class="lede">Find the phone worth buying, the plan worth switching to, the cheapest way to stay online abroad and what your old phone is worth. {len(c["phones"])} current phones, {c["n_carriers"]} carriers in 5 countries and 13 free tools. No carrier pays for a ranking.</p>
<div class="seg"><a class="btn" href="{{r}}phones.html">Compare phones</a><a class="btn btn-ghost" href="{{r}}tools.html">Open the tools</a></div>
</div>
<div class="sim" id="hero-quiz"><div class="sim-body">
<div class="progress"><span style="width:8%"></span></div>
<p class="small">Plan match, question 1 of 6</p>
<p class="quiz-q" id="hq">How many lines do you need?</p>
<div class="seg" role="group" aria-labelledby="hq"><button type="button" data-lines="1">1</button><button type="button" data-lines="2">2</button><button type="button" data-lines="3">3</button><button type="button" data-lines="4">4</button><button type="button" data-lines="5">5 or more</button></div>
<ul class="trust"><li>Free</li><li>See results before sharing anything</li><li>About a minute</li></ul>
</div></div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
<nav class="routes" aria-label="What you can do here">
<a href="{{r}}phones.html"><h3>Pick the right phone</h3><p>Rank current phones by what you care about and compare up to three side by side.</p></a>
<a href="{{r}}plans.html"><h3>Pay less for your plan</h3><p>See which budget brands run on which network, and what a fair price looks like.</p></a>
<a href="{{r}}esim.html"><h3>Travel without roaming bills</h3><p>Work out how much data a trip needs and whether your phone takes an eSIM.</p></a>
<a href="{{r}}trade-in.html"><h3>Sell your old phone well</h3><p>Estimate its value today and get competing cash offers.</p></a>
</nav>
</div></section>

<section class="section" id="data"><div class="wrap">
{_head("How much data do you actually need?", "Most people pay for more than they use. Move the sliders; the answer updates as you go.", ("tools.html", "All 13 tools"))}
{c["tools"]["data"]()}
<p class="tip"><strong>Tip of the day:</strong> <span data-tip>Dial *#06# on any phone. If an EID appears, the phone supports eSIM.</span></p>
</div></section>

<section class="section"><div class="wrap">
{_head("Newest phones, scored", "Scores combine performance, camera, battery, display and value from published specs. Set your own weights in the phone finder.", ("phones.html", "Open the phone finder"))}
<div class="table-wrap"><table><thead><tr><th scope="col">Phone</th><th scope="col" class="num">Launch price</th><th scope="col">Screen</th><th scope="col">Chipset</th><th scope="col">Score</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>

<section class="section"><div class="wrap">
<div class="ad-slot" data-slot="footer"></div>
{_head("Latest mobile headlines", "Collected from leading mobile news sites and refreshed every six hours.", ("news.html", "All headlines"))}
{c["news_block"](6, "{r}")}
</div></section>

<section class="section"><div class="wrap">
{_head("Guides that save you money", "Plain-English answers to the questions people ask before they switch, buy or travel.", ("guides.html", "All guides"))}
<ul class="guide-list">{guides}</ul>
</div></section>

<section class="section band"><div class="wrap lead-grid">
<div><h2>Running phones for a team?</h2><p class="muted">Tell us your line count, devices and coverage needs. We match you with business mobility providers and send competing quotes, without a round of sales calls.</p></div>
<div><a class="btn btn-gold" href="{{r}}business.html">Request business quotes</a></div>
</div></section>

<section class="section" style="padding-top:clamp(48px,7vw,88px)"><div class="wrap">
{_head("Watch before you buy", "Recent reviews and tests from respected mobile reviewers. Videos load only when you press play.", ("videos.html", "More videos"))}
{c["videos_block"](3)}
</div></section>

<section class="section"><div class="wrap">
{_head("Help build Mobile.Direct", "We are independent and reader-funded as well as ad-supported. Here is how to get involved.")}
<nav class="routes" aria-label="Get involved">
<a href="{{r}}support.html"><h3>Support us</h3><p>Chip in for hosting, research, promotions and new tools.</p></a>
<a href="{{r}}contests.html"><h3>Enter the monthly contest</h3><p>This month: best phone photo. Prizes every month.</p></a>
<a href="{{r}}careers.html"><h3>Write, film or research</h3><p>Paid and volunteer roles for mobile enthusiasts.</p></a>
<a href="{{r}}advertise.html"><h3>Advertise or partner</h3><p>Sponsorships, white-label tools and lead partnerships.</p></a>
</nav>
</div></section>
"""


HOME_LD = [
    {"@context": "https://schema.org", "@type": "Organization", "name": "Mobile.Direct", "url": SITE + "/",
     "logo": SITE + "/assets/img/icon-512.png", "description": "Independent tools and guides for choosing phones, plans and eSIMs."},
    {"@context": "https://schema.org", "@type": "WebSite", "name": "Mobile.Direct", "url": SITE + "/"},
]


# ---------------- GET MATCHED (lead gen) ----------------
GM_FAQ = [
    ("Is the plan match free?", "Yes. You see your recommendation and estimated saving without entering any personal details."),
    ("Where do the price ranges come from?", "From typical published prices for each plan type in your country, reviewed regularly. Always confirm the final price on the provider's site."),
    ("What happens after I request the report?", "We email your shortlist and, only if you ask, a plan specialist or up to three matched providers contact you. You can opt out at any time."),
]


def get_matched(c):
    return f"""
{c["page_head"]("Find the plan that fits, and see what you could save", "Answer six quick questions. You get a best-fit plan type, the carriers to compare first and an estimated yearly saving, before you share anything.")}
<section class="section" id="quiz" style="padding-top:8px"><div class="wrap lead-grid">
<div class="sim"><div class="sim-body" id="matcher">
<div class="progress" id="quiz-progress"><span></span></div>
<p class="small" id="quiz-count">Question 1 of 6</p>
<div id="quiz-step" aria-live="polite"></div>
<button type="button" class="btn btn-ghost btn-sm" id="quiz-back" hidden>Back</button>
</div></div>
<div>
<div id="lead-why">
<h2>Why people use the plan match</h2>
<ul class="result-list">
<li><span>Carriers covered</span><strong>{c["n_carriers"]} in 5 countries</strong></li>
<li><span>Time to answer</span><strong>About a minute</strong></li>
<li><span>Cost</span><strong>Free</strong></li>
<li><span>Personal details needed to see results</span><strong>None</strong></li>
</ul>
<p class="small" style="margin-top:16px">We recommend plan types and carriers on fit alone. Partners cannot buy a higher position.</p>
</div>
<form id="lead-form" data-md-form="Plan match lead" hidden data-success="Your plan report is on its way. Check your inbox (and spam folder) in the next few minutes.">
<h2 tabindex="-1">Get your full plan report</h2>
<p>We email a side-by-side shortlist for your answers, current promotions worth knowing about and an alert when a better deal appears. Want a hand switching? A plan specialist can call you.</p>
<div class="grid-2"><div class="field"><label for="lf-name">Name</label><input id="lf-name" name="name" type="text" required autocomplete="name"></div>
<div class="field"><label for="lf-email">Email</label><input id="lf-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="grid-2"><div class="field"><label for="lf-phone">Phone (optional)</label><input id="lf-phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="lf-zip">ZIP or postal code</label><input id="lf-zip" name="postal_code" type="text" autocomplete="postal-code" required></div></div>
<div class="field"><label for="lf-pref">How should we follow up?</label><select id="lf-pref" name="follow_up"><option>Email my report only</option><option>Email the report and call me to help me switch</option><option>Send me offers from matched providers</option></select></div>
<input type="hidden" name="answers" id="lead-summary">{c["HONEY"]}
{c["consent"]()}
<button class="btn btn-gold" type="submit">Email my plan report</button>
<ul class="trust"><li>No spam</li><li>Unsubscribe in one click</li><li>Your answers stay private</li></ul>
<p class="form-status" role="status"></p>
</form>
</div>
</div></section>
<section class="section"><div class="wrap">
<h2>How the plan match works</h2>
<ol class="cols-2">
<li><strong>You describe your usage.</strong> Lines, data, what matters most and your current bill.</li>
<li><strong>We match a plan type.</strong> Budget brand, network plan, travel setup or premium unlimited.</li>
<li><strong>We price it locally.</strong> Using typical prices for that plan type in your country.</li>
<li><strong>You compare the shortlist.</strong> With direct links to each carrier's own site.</li>
</ol>
<h2 style="margin-top:40px">Questions</h2>
{c["faq_html"](GM_FAQ)}
</div></section>
"""


# ---------------- PHONES ----------------
PH_FAQ = [
    ("How are phone scores calculated?", "Each phone gets five sub-scores from published specs: performance from its chipset tier, camera from lens count, telephoto and sensor resolution, battery from capacity with an efficiency adjustment, display from size and refresh rate, and value from overall quality relative to launch price. Your weights decide how they combine."),
    ("Are these lab test results?", "No. Scores are spec-based and meant for shortlisting. Read hands-on reviews before you buy."),
]


def phones_page(c):
    ps = sorted(c["phones"], key=lambda p: p["_s"]["match"], reverse=True)
    w = "".join('<div><label for="w-%s">%s <output>3</output></label><input type="range" id="w-%s" name="%s" min="0" max="5" step="1" value="3"></div>' % (k, l, k, k)
                for k, l in [("perf", "Performance"), ("camera", "Camera"), ("battery", "Battery"), ("display", "Display"), ("value", "Value")])
    return f"""
{c["page_head"]("Phone finder", "Rank %d current phones by what matters to you, then compare up to three side by side. Set a weight to zero to ignore it." % len(ps), [("phones.html", "Phone finder")])}
<section class="section" style="padding-top:0"><div class="wrap" id="phone-app">
<h2 class="visually-hidden">Your priorities</h2>
<div class="weights" id="weights">{w}</div>
<div class="filters" id="phone-filters">
<div class="field"><label for="f-q">Search</label><input id="f-q" type="search" placeholder="Model or chipset"></div>
<div class="field"><label for="f-brand">Brand</label><select id="f-brand"><option value="">All brands</option></select></div>
<div class="field"><label for="f-price">Max price: <output id="f-price-out">Any</output></label><input id="f-price" type="range" min="150" max="2000" step="50" value="2000"></div>
<div class="field"><label for="f-size">Size</label><select id="f-size"><option value="">Any size</option><option value="compact">Compact (6.3" or less)</option><option value="large">Large (6.6"+)</option><option value="fold">Foldable</option></select></div>
<div class="field"><label for="f-sort">Sort by</label><select id="f-sort"><option value="match">Match score</option><option value="price">Lowest price</option><option value="newest">Newest</option><option value="battery">Biggest battery</option></select></div>
</div>
<p class="small"><span id="phone-count">{len(ps)} phones</span>. Launch prices in USD. Battery figures marked ~ are from regulatory filings.</p>
<ul class="phone-list" id="phone-list">{c["phone_rows"](ps)}</ul>
<section id="compare-section" hidden style="margin-top:40px"><h2>Side-by-side comparison</h2><p class="small">The winning value in each row is marked. Share this comparison by copying the page address.</p><div class="table-wrap" id="compare-table"></div></section>
</div></section>
<div class="compare-bar" id="compare-bar"><div class="wrap"><span>Comparing: <strong id="compare-names"></strong></span><span class="seg"><button type="button" class="btn btn-gold btn-sm" id="compare-go">Compare now</button><button type="button" class="btn btn-sm" id="compare-clear" style="border-color:var(--on-ink)">Clear</button></span></div></div>
<dialog id="alert-dialog" aria-labelledby="alert-title"><div class="dlg-body">
<form data-md-form="Price drop alert" data-success="Alert set. We will email you when the price drops.">
<h2 id="alert-title">Price drop alert</h2>
<p>Get an email when <strong data-item-label></strong> drops in price or a strong deal appears.</p>
<input type="hidden" name="item">
<div class="field"><label for="al-email">Email</label><input id="al-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="al-target">Alert me below (optional)</label><input id="al-target" name="target_price" type="number" min="0" placeholder="e.g. 650"></div>
{c["HONEY"]}{c["consent"]("I agree to receive price alerts and related deals by email. I can unsubscribe at any time.")}
<div class="seg"><button class="btn btn-gold" type="submit">Set alert</button><button class="btn btn-ghost" type="button" data-close>Close</button></div>
<p class="form-status" role="status"></p>
</form></div></dialog>
<section class="section"><div class="wrap">
<div class="ad-slot" data-slot="inArticle"></div>
<h2>How the scores work</h2>
{c["faq_html"](PH_FAQ)}
<p style="margin-top:20px">Not sure which phone or plan? <a href="{{r}}get-matched.html">Take the plan match</a> or read <a href="{{r}}guides/refurbished-phone-buying-guide.html">why last year's flagship refurbished often beats a new mid-range phone</a>.</p>
</div></section>
"""


# ---------------- PLANS ----------------
PL_FAQ = [
    ("Are these prices live?", "No. They are typical ranges for each plan type, reviewed regularly. Promotions change often, so always confirm on the carrier's site."),
    ("What is a sub-brand?", "A budget brand owned by a network operator, sold at lower prices with fewer perks. It uses the parent network's towers."),
]


def plans_page(c):
    e = c["e"]
    cur_sym = {"USD": "US$", "CAD": "CA$", "GBP": "£", "INR": "₹", "AUD": "A$"}
    price_rows = "".join("<tr><th scope='row'>%s</th>%s</tr>" % (
        e(v["name"]), "".join("<td>%s%d–%d</td>" % (cur_sym[v["currency"]], v["bands"][k][0], v["bands"][k][1])
                               for k in ["light", "medium", "heavy", "unlimited", "premium"])) for v in c["carriers"].values())
    dirs = []
    for code, v in c["carriers"].items():
        rows = "".join("<tr><td><a href='%s' rel='nofollow noopener' target='_blank'>%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            x["url"], e(x["name"]), x["type"], e(x["network"]),
            ", ".join({"price": "Low price", "coverage": "Coverage", "travel": "Travel", "5g": "5G", "premium": "Perks"}[b] for b in x["bestFor"]))
            for x in v["carriers"])
        dirs.append('<h3 id="carriers-%s">%s</h3><div class="table-wrap" style="margin-bottom:28px"><table><thead><tr><th scope="col">Brand</th><th scope="col">Type</th><th scope="col">Runs on</th><th scope="col">Strong for</th></tr></thead><tbody>%s</tbody></table></div>' % (code.lower(), e(v["name"]), rows))
    return f"""
{c["page_head"]("Phone plans and carriers, decoded", "What a fair price looks like for each kind of plan, and which budget brands run on which network in the US, Canada, the UK, India and Australia.", [("plans.html", "Plans")])}
<section class="section" style="padding-top:0"><div class="wrap">
<div class="lead-grid">
<div>
<h2>Five kinds of plan</h2>
<table><thead><tr><th scope="col">Plan type</th><th scope="col">Fits</th></tr></thead><tbody>
<tr><td>Light prepaid</td><td>Under 5 GB, mostly on Wi-Fi, talk and text</td></tr>
<tr><td>Mid-size data</td><td>5–20 GB, the most common need</td></tr>
<tr><td>Large data</td><td>20–50 GB, streaming on the go</td></tr>
<tr><td>Budget unlimited</td><td>Heavy use, fine with slower data at busy times</td></tr>
<tr><td>Premium unlimited</td><td>Priority data, hotspot, roaming and perks</td></tr>
</tbody></table>
</div>
<div class="sim"><div class="sim-body"><p class="quiz-q">Which one is yours?</p><p>Answer six questions and get the plan type, carriers to compare and your estimated saving.</p><a class="btn" href="{{r}}get-matched.html">Start the plan match</a><p class="small" style="margin-top:12px">Or measure your usage with the <a href="{{r}}tools.html#data">data calculator</a>.</p></div></div>
</div>
</div></section>
<section class="section"><div class="wrap">
{_head("Typical monthly price per line", "Ranges seen for each plan type in late 2026, before taxes. Multi-line plans cost less per line.")}
<div class="table-wrap"><table><thead><tr><th scope="col">Country</th><th scope="col">Light</th><th scope="col">Mid-size</th><th scope="col">Large</th><th scope="col">Budget unlimited</th><th scope="col">Premium unlimited</th></tr></thead><tbody>{price_rows}</tbody></table></div>
<p class="small">India prices are for monthly prepaid recharges; plans there are usually sold per 28 days.</p>
</div></section>
<section class="section"><div class="wrap">
{_head("Carrier directory", "Network: owns towers. Sub-brand: budget brand owned by a network. MVNO: independent brand renting capacity. All three on the same network share the same coverage map.")}
<p class="seg">{" ".join('<a class="btn btn-ghost btn-sm" href="#carriers-%s">%s</a>' % (k.lower(), e(v["name"])) for k, v in c["carriers"].items())}</p>
{"".join(dirs)}
<div class="ad-slot" data-slot="inArticle"></div>
</div></section>
<section class="section"><div class="wrap">
{_head("Plans for every kind of user", "Shortcuts for the situations people ask us about most.")}
<div class="guide-list" style="display:grid">
<div><h3>Seniors</h3><p class="muted">Light prepaid on the strongest local network, with Wi-Fi calling switched on. Ask about age-based discounts; several carriers offer them.</p></div>
<div><h3>Students</h3><p class="muted">Mid-size data from a sub-brand, paid monthly so you can switch at term breaks. Check student discounts and campus coverage.</p></div>
<div><h3>Families</h3><p class="muted">Multi-line plans where the per-line price falls as lines are added. Split fairly with our <a href="{{r}}tools.html#split">bill splitter</a>.</p></div>
<div><h3>Frequent travellers</h3><p class="muted">A plan with roaming included, or a cheap home plan plus <a href="{{r}}esim.html">travel eSIMs</a>.</p></div>
<div><h3>Newcomers</h3><p class="muted">Prepaid with no credit check gets you a local number fast. Bring an unlocked phone and check its <a href="{{r}}tools.html#bands">bands</a>.</p></div>
<div><h3>Businesses</h3><p class="muted">Pooled data, device management and an account manager. <a href="{{r}}business.html">Request competing quotes</a>.</p></div>
</div>
<h2 style="margin-top:40px">Questions</h2>
{c["faq_html"](PL_FAQ)}
</div></section>
"""


# ---------------- ESIM ----------------
ES_FAQ = [
    ("Do I need to be on Wi-Fi to install a travel eSIM?", "Yes, the profile downloads over the internet. Install it at home before you leave and switch it on when you land."),
    ("Will I still receive calls on my normal number?", "Yes, if you keep your home line enabled. Incoming calls may cost roaming charges depending on your plan."),
    ("What does fair use mean on unlimited eSIMs?", "Most unlimited travel plans slow your speed after a daily amount of high-speed data. Check the threshold on the provider's plan page."),
]


def esim_page(c):
    e = c["e"]
    prov = json.loads((__import__("pathlib").Path(__file__).resolve().parent.parent / "data" / "esim-providers.json").read_text())["providers"]
    rows = "".join("<tr><td><a href='%s' rel='nofollow sponsored noopener' target='_blank'>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        p["url"], e(p["name"]), e(p["plans"]), e(p["hotspot"]), e(p["fairUse"]), e(p["bestFor"])) for p in prov)
    return f"""
{c["page_head"]("Travel eSIM hub", "Work out how much data your trip needs, check your phone takes an eSIM, and compare the main providers.", [("esim.html", "eSIM")])}
<section class="section" style="padding-top:0"><div class="wrap">
{c["tools"]["trip"]()}
{c["tools"]["esim"]()}
</div></section>
<section class="section"><div class="wrap">
{_head("Travel eSIM providers compared", "What each provider sells and the terms that matter. Policies change; check the plan page before buying.")}
<div class="table-wrap"><table><thead><tr><th scope="col">Provider</th><th scope="col">Plans</th><th scope="col">Hotspot</th><th scope="col">Fair use</th><th scope="col">Best for</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Outbound links may become affiliate links. That never changes the order or the notes in this table.</p>
<div class="ad-slot" data-slot="inArticle"></div>
</div></section>
<section class="section"><div class="wrap lead-grid">
<div><h2>Before you fly</h2><ol>
<li>Confirm your phone is unlocked.</li>
<li>Check the destination's bands with the <a href="{{r}}tools.html#bands">band checker</a>.</li>
<li>Install the eSIM at home on Wi-Fi; leave it switched off.</li>
<li>Turn off data roaming on your home line.</li>
<li>Download offline maps as a backup.</li></ol>
<p>Read more: <a href="{{r}}guides/what-is-esim.html">eSIM explained</a> and <a href="{{r}}guides/travel-data-roaming-vs-esim.html">roaming vs travel eSIM</a>.</p></div>
<div><h2>Questions</h2>{c["faq_html"](ES_FAQ)}</div>
</div></section>
"""


# ---------------- TRADE-IN ----------------
def tradein_page(c):
    return f"""
{c["page_head"]("What is your old phone worth?", "Estimate today's cash value, see how fast it falls, and get competing offers from buyback partners.", [("trade-in.html", "Trade-in")])}
<section class="section" style="padding-top:0"><div class="wrap">
{c["tools"]["tradein"]()}
{c["tools"]["refurb"]()}
</div></section>
<section class="section"><div class="wrap lead-grid">
<div><h2>Before you sell</h2><ol>
<li>Back up photos, messages and authenticator apps.</li>
<li>Move your eSIM or take out the SIM.</li>
<li>Turn off Find My (iPhone) or remove your Google account (Android).</li>
<li>Erase all content and settings.</li>
<li>Photograph the phone's condition before shipping.</li></ol></div>
<div><h2>When to sell</h2><p>Used prices drop fastest when a new generation launches: September for iPhone, early in the year for Galaxy S. Selling two to four weeks before a launch usually beats waiting.</p>
<p>Carrier trade-in promotions often pay as bill credits spread over 24–36 months. Cash from a buyback buyer is yours immediately.</p>
<p><a href="{{r}}guides/sell-or-trade-in-your-phone.html">Read the full selling guide</a></p></div>
</div></section>
"""


# ---------------- TOOLS ----------------
def tools_page(c):
    idx = [("#data", "Data usage calculator", "Turns your daily habits into a monthly data figure."),
           ("#tco", "Total cost of ownership", "Carrier deal vs unlocked phone with a budget plan."),
           ("#refurb", "Refurbished vs new", "The real saving, including a new battery."),
           ("#esim", "eSIM compatibility checker", "Does your phone take an eSIM?"),
           ("#bands", "Will my phone work abroad?", "Band match for 39 countries."),
           ("#imei", "IMEI validator", "Spot mistyped or altered IMEIs before buying used."),
           ("#roam", "Roaming vs travel eSIM", "Cheapest way to get data on your trip."),
           ("#split", "Family plan bill splitter", "Split a shared bill fairly by usage."),
           ("#signal", "Signal strength interpreter", "Turn RSRP, RSRQ and SINR into plain English."),
           ("trade-in.html", "Trade-in value estimator", "What your phone is worth today."),
           ("phones.html", "Phone finder and compare", "Personal match scores and side-by-side specs."),
           ("get-matched.html", "Plan match", "Best-fit plan and estimated yearly saving."),
           ("esim.html", "Travel eSIM planner", "Data for your trip and the bands at your destination.")]
    lis = "".join('<li><a href="%s">%s</a><br><span class="small">%s</span></li>' % ("{r}tools.html" + u if u.startswith("#") else "{r}" + u, n, d) for u, n, d in idx)
    t = c["tools"]
    blocks = "".join('<div id="%s">%s</div>' % (k, t[k]()) for k in ["data", "tco", "refurb", "esim", "bands", "imei", "roam", "split", "signal"])
    return f"""
{c["page_head"]("Free mobile tools", "Thirteen calculators and checkers for choosing, paying for and travelling with a phone. Everything runs in your browser.", [("tools.html", "Tools")])}
<section class="section" style="padding-top:0"><div class="wrap">
<ul class="tool-index">{lis}</ul>
</div></section>
<section class="section"><div class="wrap">
{blocks}
<div class="ad-slot" data-slot="inArticle"></div>
</div></section>
"""


# ---------------- GUIDES INDEX ----------------
def guides_page(c):
    e = c["e"]
    lis = "".join('<li><a href="{r}guides/%s.html"><h3>%s</h3><p>%s</p></a><span class="small">%d-minute read</span></li>' % (g["slug"], e(g["title"]), e(g["desc"]), g["minutes"]) for g in c["GUIDES"])
    return f"""
{c["page_head"]("Guides", "Independent, plain-English guides to choosing plans, phones and eSIMs, written to help you decide, not to sell you something.", [("guides.html", "Guides")])}
<section class="section" style="padding-top:0"><div class="wrap"><ul class="guide-list">{lis}</ul></div></section>
"""


# ---------------- NEWS / VIDEOS ----------------
def news_page(c):
    tags = [("all", "All"), ("iphone", "iPhone"), ("android", "Android"), ("samsung", "Samsung"), ("pixel", "Pixel"),
            ("5g", "5G"), ("esim", "eSIM"), ("carriers", "Carriers"), ("deals", "Deals")]
    btns = "".join('<button type="button" data-tag="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "all" else "false", n) for k, n in tags)
    return f"""
{c["page_head"]("Mobile news", "The latest headlines from leading mobile news sites, refreshed automatically every six hours. Headlines link to the original publisher.", [("news.html", "News")])}
<section class="section" style="padding-top:0"><div class="wrap" id="news-app">
<div class="seg tag-filter" role="group" aria-label="Filter headlines">{btns}</div>
{c["news_block"](60, "{r}")}
<p class="small" style="margin-top:16px">Last refreshed <time data-last-updated>recently</time>. Headlines and links belong to their publishers.</p>
<div class="ad-slot" data-slot="footer"></div>
</div></section>
"""


def videos_page(c):
    return f"""
{c["page_head"]("Videos", "Recent phone reviews, comparisons and durability tests from respected creators. Updated automatically; videos load only when you press play.", [("videos.html", "Videos")])}
<section class="section" style="padding-top:0"><div class="wrap">
{c["videos_block"](12)}
<p class="small" style="margin-top:20px">Videos are embedded from YouTube using privacy-enhanced mode and remain the property of their creators.</p>
</div></section>
"""


# ---------------- DEALS CALENDAR ----------------
def deals_page(c):
    months = [("January", "Post-holiday clearance on last year's models; carrier promotions to win switchers."),
              ("February–March", "Samsung Galaxy S launch: pre-order bonuses and the strongest trade-in offers of the year for Galaxy owners."),
              ("April–May", "Mid-range launches (A-series phones); older flagships drop in price."),
              ("July", "Big online retail sale events: unlocked phones and accessories hit yearly lows."),
              ("August", "Back-to-school promotions and Pixel launches; student discounts peak."),
              ("September", "New iPhones: carriers push trade-in credits; previous models fall in price. Sell your old phone before launch."),
              ("October", "Holiday promotions start early; foldables often discounted."),
              ("Late November", "Black Friday and Cyber Monday: the deepest discounts on phones and plans."),
              ("December", "Holiday bundles and, in Canada and the UK, Boxing Day sales.")]
    rows = "".join("<tr><th scope='row'>%s</th><td>%s</td></tr>" % m for m in months)
    return f"""
{c["page_head"]("Deal calendar", "When phone and plan prices drop during the year, so you can time your purchase. Get alerts when it is time to act.", [("deals.html", "Deal calendar")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div><div class="table-wrap"><table><thead><tr><th scope="col">When</th><th scope="col">What usually happens</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Patterns from recent years. Exact dates vary by country and retailer.</p></div>
<div class="sim"><div class="sim-body">
<form data-md-form="Deal alert signup" data-success="You are on the list. We will email you when a deal window opens for what you chose.">
<h2>Deal alerts</h2><p>Tell us what you are shopping for and we will email you when the price is right.</p>
<div class="field"><label for="da-want">I am looking for</label><select id="da-want" name="looking_for"><option>A new iPhone</option><option>A new Samsung Galaxy</option><option>A new Pixel</option><option>A budget phone under $400</option><option>A cheaper phone plan</option><option>A travel eSIM</option></select></div>
<div class="field"><label for="da-email">Email</label><input id="da-email" name="email" type="email" required autocomplete="email"></div>
{c["HONEY"]}{c["consent"]("I agree to receive deal alerts by email. I can unsubscribe at any time.")}
<button class="btn btn-gold" type="submit">Send me deal alerts</button><p class="form-status" role="status"></p>
</form></div></div>
</div></section>
"""


# ---------------- BUSINESS (B2B lead) ----------------
BZ_FAQ = [
    ("Is the quote service free?", "Yes for businesses. Providers we work with may compensate us for introductions, which never affects which providers we recommend."),
    ("How quickly will I hear back?", "Usually within two business days, with a shortlist and quotes."),
]


def business_page(c):
    return f"""
{c["page_head"]("Business mobile quotes", "Tell us about your team once. We match you with suitable business mobility providers and send competing quotes for lines, devices and device management.", [("business.html", "Business")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div>
<h2>What we can quote</h2>
<ul class="result-list">
<li><span>Lines</span><strong>From 2 to 2,000+</strong></li>
<li><span>Plans</span><strong>Pooled, unlimited, data-only</strong></li>
<li><span>Devices</span><strong>New, refurbished, BYOD</strong></li>
<li><span>Management</span><strong>MDM, zero-touch, eSIM</strong></li>
<li><span>Extras</span><strong>Roaming, IoT, 5G hotspots</strong></li>
</ul>
<p style="margin-top:18px">New to business mobile? Read <a href="{{r}}guides/business-mobile-plans.html">fleets, BYOD and device management explained</a>.</p>
</div>
<div class="sim"><div class="sim-body">
<form data-md-form="Business mobility quote" data-success="Thanks. Your request is with us; expect a shortlist and quotes within two business days.">
<h2>Request quotes</h2>
<div class="grid-2"><div class="field"><label for="bz-company">Company</label><input id="bz-company" name="company" required autocomplete="organization"></div>
<div class="field"><label for="bz-name">Your name</label><input id="bz-name" name="name" required autocomplete="name"></div></div>
<div class="grid-2"><div class="field"><label for="bz-email">Work email</label><input id="bz-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="bz-phone">Phone</label><input id="bz-phone" name="phone" type="tel" autocomplete="tel"></div></div>
<div class="grid-2"><div class="field"><label for="bz-country">Country</label><select id="bz-country" name="country"><option>United States</option><option>Canada</option><option>United Kingdom</option><option>India</option><option>Australia</option><option>Other</option></select></div>
<div class="field"><label for="bz-lines">Number of lines</label><input id="bz-lines" name="lines" type="number" min="1" value="10" required></div></div>
<fieldset class="field" style="border:0;padding:0;margin:0 0 16px"><legend style="font-weight:650;margin-bottom:6px">You need</legend>
<label class="check"><input type="checkbox" name="needs" value="New devices"> <span>New or refurbished devices</span></label>
<label class="check"><input type="checkbox" name="needs" value="Device management (MDM)"> <span>Device management (MDM)</span></label>
<label class="check"><input type="checkbox" name="needs" value="International roaming"> <span>International roaming</span></label>
<label class="check"><input type="checkbox" name="needs" value="IoT / data-only"> <span>Data-only or IoT lines</span></label>
<label class="check"><input type="checkbox" name="needs" value="5G hotspots"> <span>5G hotspots or fixed wireless</span></label></fieldset>
<div class="grid-2"><div class="field"><label for="bz-spend">Current monthly spend</label><input id="bz-spend" name="monthly_spend" type="text" placeholder="e.g. $1,200"></div>
<div class="field"><label for="bz-when">Timeline</label><select id="bz-when" name="timeline"><option>Within 30 days</option><option>1–3 months</option><option>3–6 months</option><option>Just researching</option></select></div></div>
<div class="field"><label for="bz-msg">Anything else</label><textarea id="bz-msg" name="message" placeholder="Current carrier, contract end date, coverage problems"></textarea></div>
{c["HONEY"]}{c["consent"]()}
<button class="btn btn-gold" type="submit">Get my business quotes</button>
<ul class="trust"><li>Free for businesses</li><li>Two-day turnaround</li><li>No obligation</li></ul>
<p class="form-status" role="status"></p>
</form></div></div>
</div></section>
<section class="section"><div class="wrap"><h2>Questions</h2>{c["faq_html"](BZ_FAQ)}</div></section>
"""


# ---------------- SUPPORT / DONATE ----------------
def support_page(c):
    return f"""
{c["page_head"]("Support Mobile.Direct", "We keep every tool free and every ranking independent. Your support pays for operations, promotions, marketing, new contributors, contests and prizes.", [("support.html", "Support")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div class="sim"><div class="sim-body">
<form data-donate-form>
<h2>Make a contribution</h2>
<p class="small">One-time contribution through PayPal. Card payments work without a PayPal account in most countries.</p>
<div class="amounts seg" role="group" aria-label="Choose an amount">
<button type="button" data-amount="5" aria-pressed="false">$5</button><button type="button" data-amount="15" aria-pressed="true">$15</button><button type="button" data-amount="50" aria-pressed="false">$50</button><button type="button" data-amount="100" aria-pressed="false">$100</button></div>
<div class="grid-2"><div class="field"><label for="dn-amount">Amount (USD)</label><input id="dn-amount" name="amount" type="number" min="1" step="1" value="15"></div>
<div class="field"><label for="dn-purpose">Put it towards</label><select id="dn-purpose" name="purpose"><option>General support</option><option>Operations and hosting</option><option>Promotions and marketing</option><option>Hiring writers and creators</option><option>Contests and prizes</option></select></div></div>
<button class="btn btn-gold" type="submit">Contribute with PayPal</button>
<p class="small" style="margin-top:12px">Contributions support an independent website. They are not charitable donations and are not tax-deductible.</p>
</form></div></div>
<div>
<h2>Where the money goes</h2>
<ul class="result-list">
<li><span>Operations: data, research and hosting</span><strong>35%</strong></li>
<li><span>New contributors: writers, researchers, video</span><strong>30%</strong></li>
<li><span>Promotions and marketing</span><strong>20%</strong></li>
<li><span>Contests and prizes</span><strong>15%</strong></li>
</ul>
<p class="small" style="margin-top:12px">Target allocation; we publish a summary once a year.</p>
</div>
</div></section>
<section class="section"><div class="wrap">
{_head("Supporter levels", "Pick an amount above, or pledge a recurring or larger contribution below.")}
<div class="tiers">
<div><h3>Supporter</h3><p class="price">$5</p><p class="muted">Our thanks, plus early access to new tools.</p></div>
<div><h3>Backer</h3><p class="price">$15</p><p class="muted">Everything above, plus a say in which tool we build next.</p></div>
<div><h3>Patron</h3><p class="price">$50</p><p class="muted">Everything above, plus a thank-you mention in the newsletter.</p></div>
<div><h3>Sponsor</h3><p class="price">$100+</p><p class="muted">Your name or logo on this page for a year, if you want it.</p></div>
</div>
</div></section>
<section class="section"><div class="wrap lead-grid">
<div><h2>Pledge, sponsor or give in another way</h2><p>For recurring support, bank transfer, sponsoring a prize or funding a specific tool, send a pledge and we will reply with the details.</p></div>
<form data-md-form="Support pledge" data-success="Thank you. We will reply with the details within two business days.">
<div class="grid-2"><div class="field"><label for="pl-name">Name or organisation</label><input id="pl-name" name="name" required></div>
<div class="field"><label for="pl-email">Email</label><input id="pl-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="grid-2"><div class="field"><label for="pl-type">Type</label><select id="pl-type" name="pledge_type"><option>Monthly support</option><option>Sponsor a contest prize</option><option>Fund a new tool</option><option>One-time large contribution</option></select></div>
<div class="field"><label for="pl-amount">Amount</label><input id="pl-amount" name="amount" type="text" placeholder="e.g. $25 a month"></div></div>
<div class="field"><label for="pl-msg">Message (optional)</label><textarea id="pl-msg" name="message"></textarea></div>
{c["HONEY"]}<button class="btn" type="submit">Send pledge</button><p class="form-status" role="status"></p>
</form>
</div></section>
"""


# ---------------- CONTESTS ----------------
def contests_page(c):
    e = c["e"]
    d = c["load"]("contests.json")
    cur = d["current"]
    how = "".join("<li>%s</li>" % e(x) for x in cur["howToEnter"])
    up = "".join("<li><strong>%s</strong> (%s). %s</li>" % (e(u["title"]), e(u["month"]), e(u["summary"])) for u in d["upcoming"])
    past = "".join("<li>%s</li>" % e(p) for p in d["pastWinners"]) or "<li>The first winner will be announced on %s.</li>" % e(cur["winnerAnnounced"])
    return f"""
{c["page_head"]("Contests and prizes", "A new contest every month for people who love their phones. Free to enter, judged on merit.", [("contests.html", "Contests")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div>
<h2>{e(cur["title"])}</h2>
<p>{e(cur["summary"])}</p>
<dl class="kv"><dt>Prize</dt><dd>{e(cur["prize"])}</dd><dt>Opens</dt><dd>{e(cur["opens"])}</dd><dt>Closes</dt><dd>{e(cur["closes"])} at 23:59 Eastern Time</dd><dt>Winner announced</dt><dd>{e(cur["winnerAnnounced"])}</dd></dl>
<h3>How to enter</h3><ol>{how}</ol>
</div>
<div class="sim"><div class="sim-body">
<form data-md-form="Contest entry: {e(cur["id"])}" data-success="Your entry is in. Good luck, and watch your inbox after the closing date.">
<h2>Enter now</h2>
<div class="grid-2"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="grid-2"><div class="field"><label for="ct-country">Country</label><input id="ct-country" name="country" required autocomplete="country-name"></div>
<div class="field"><label for="ct-phone">Phone model used</label><input id="ct-phone" name="phone_model" required></div></div>
<div class="field"><label for="ct-link">Link to your photo</label><input id="ct-link" name="entry_link" type="url" required placeholder="https://"></div>
<div class="field"><label for="ct-story">The story behind it (optional)</label><textarea id="ct-story" name="story"></textarea></div>
{c["HONEY"]}
<div class="field"><label class="check"><input type="checkbox" name="rules" value="accepted" required> <span>I am 18 or over (or the age of majority where I live), the photo is my own work, and I accept the official rules below.</span></label></div>
<button class="btn btn-gold" type="submit">Submit my entry</button><p class="form-status" role="status"></p>
</form></div></div>
</div></section>
<section class="section"><div class="wrap lead-grid">
<div><h2>Coming up</h2><ul>{up}</ul><h2 style="margin-top:28px">Past winners</h2><ul>{past}</ul>
<p>Want your brand on a prize? <a href="{{r}}advertise.html">Sponsor a contest</a>.</p></div>
<div><h2 id="rules">Official rules (summary)</h2><ol class="small">
<li>No purchase or payment is necessary to enter or win. A purchase does not improve your chances.</li>
<li>Open to individuals aged 18 or over (or the age of majority where they live), where such contests are lawful. Void where prohibited or restricted. Employees of Mobile.Direct and their households are not eligible.</li>
<li>One entry per person per contest. Entries must be the entrant's original work and must not infringe anyone's rights.</li>
<li>Winners are selected by a panel of judges on merit using the criteria stated for each contest. This is a contest of skill, not chance.</li>
<li>The winner is notified by email and must reply within 14 days, or an alternate winner is selected. Prizes cannot be exchanged for cash except where required by law. Taxes are the winner's responsibility.</li>
<li>By entering, you allow Mobile.Direct to display your entry and first name with credit on this website and its social channels, without further payment. You keep ownership of your work.</li>
<li>Personal data is used only to run the contest, as described in our <a href="{{r}}privacy.html">privacy policy</a>.</li>
<li>Mobile.Direct may cancel or modify a contest if fraud or technical problems affect it. This contest is not sponsored, endorsed or administered by any social network or brand named in an entry.</li>
</ol></div>
</div></section>
"""


# ---------------- CAREERS ----------------
ROLES = [
    ("Mobile tech writer", "Freelance, remote, paid per article", "Write clear, original guides on phones, plans and eSIMs. You test things yourself and explain them without jargon."),
    ("Plans and pricing researcher", "Part-time, remote, paid hourly", "Keep our carrier directory and price ranges accurate for your country. Ideal for detail-minded people who already compare plans for fun."),
    ("Short-form video creator", "Freelance, paid per video", "Turn our tools and guides into 30–90 second explainers for social channels."),
    ("Community and contest coordinator", "Part-time, remote", "Run the monthly contest, coordinate judges and reply to readers."),
    ("Growth and partnerships", "Commission-based", "Bring in sponsors, affiliate partners and business-mobility lead buyers."),
    ("City and campus ambassador", "Volunteer with rewards", "Share Mobile.Direct locally and collect real coverage experiences. Top ambassadors get gear and paid roles first."),
]


def careers_page(c):
    e = c["e"]
    roles = "".join('<div class="role"><h3>%s</h3><p class="small">%s</p><p>%s</p></div>' % (e(t), e(k), e(d)) for t, k, d in ROLES)
    opts = "".join("<option>%s</option>" % e(t) for t, _, _ in ROLES)
    return f"""
{c["page_head"]("Work with Mobile.Direct", "We are growing a small, remote team of people who know phones and plans and want to help others choose well.", [("careers.html", "Careers")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div><h2>Open roles</h2>{roles}</div>
<div class="sim"><div class="sim-body">
<form data-md-form="Job application" data-success="Application received. If there is a fit, we will be in touch within a week.">
<h2>Apply</h2>
<div class="grid-2"><div class="field"><label for="jb-name">Name</label><input id="jb-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="jb-email">Email</label><input id="jb-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="field"><label for="jb-role">Role</label><select id="jb-role" name="role">{opts}</select></div>
<div class="grid-2"><div class="field"><label for="jb-link">Portfolio or LinkedIn</label><input id="jb-link" name="portfolio" type="url" placeholder="https://"></div>
<div class="field"><label for="jb-tz">Country and time zone</label><input id="jb-tz" name="location" required></div></div>
<div class="field"><label for="jb-hours">Hours a week you can give</label><select id="jb-hours" name="availability"><option>Under 5</option><option>5–10</option><option>10–20</option><option>20+</option></select></div>
<div class="field"><label for="jb-why">Why you, in a few lines</label><textarea id="jb-why" name="message" required></textarea></div>
{c["HONEY"]}{c["consent"]("I agree that Mobile.Direct may store my application for up to 12 months to consider me for roles.")}
<button class="btn btn-gold" type="submit">Send application</button><p class="form-status" role="status"></p>
</form></div></div>
</div></section>
"""


# ---------------- ADVERTISE / PARTNER ----------------
def advertise_page(c):
    return f"""
{c["page_head"]("Advertise and partner", "Reach people at the moment they choose a phone, a plan, an eSIM or a buyer for their old device.", [("advertise.html", "Advertise")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div>
<h2>Ways to work with us</h2>
<ul class="result-list">
<li><span>Sponsored tool ("Data calculator, presented by…")</span><strong>Monthly</strong></li>
<li><span>Category sponsorship (eSIM hub, trade-in, plans)</span><strong>Monthly</strong></li>
<li><span>Newsletter sponsorship</span><strong>Per issue</strong></li>
<li><span>Contest prize sponsorship</span><strong>Per contest</strong></li>
<li><span>White-label plan finder or calculators for your site</span><strong>Licence</strong></li>
<li><span>Qualified leads: consumer plans, business mobility, trade-in</span><strong>Per lead</strong></li>
</ul>
<p class="small" style="margin-top:12px">Sponsored placements are always labelled and never change rankings or tool results.</p>
<h2 style="margin-top:32px">Interested in this website or domain?</h2>
<p>For acquisition of the website or domain name, or a strategic partnership, contact the owner directly.</p>
<a class="btn btn-ghost" href="{c["OWNER_LINK"]}" target="_blank" rel="noopener">Contact the owner</a>
</div>
<div class="sim"><div class="sim-body">
<form data-md-form="Advertising and partnership enquiry" data-success="Thanks. We will reply with options and a media kit within two business days.">
<h2>Tell us what you have in mind</h2>
<div class="grid-2"><div class="field"><label for="ad-company">Company</label><input id="ad-company" name="company" required autocomplete="organization"></div>
<div class="field"><label for="ad-name">Your name</label><input id="ad-name" name="name" required autocomplete="name"></div></div>
<div class="grid-2"><div class="field"><label for="ad-email">Email</label><input id="ad-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="ad-site">Website</label><input id="ad-site" name="website" type="url" placeholder="https://"></div></div>
<div class="field"><label for="ad-type">Interested in</label><select id="ad-type" name="interest"><option>Sponsorship</option><option>Advertising</option><option>Lead partnership</option><option>White-label tools</option><option>Contest prize sponsorship</option><option>Website or domain acquisition</option><option>Other partnership</option></select></div>
<div class="field"><label for="ad-budget">Monthly budget</label><select id="ad-budget" name="budget"><option>Under $500</option><option>$500–$2,000</option><option>$2,000–$10,000</option><option>$10,000+</option><option>Let's discuss</option></select></div>
<div class="field"><label for="ad-msg">Message</label><textarea id="ad-msg" name="message" required></textarea></div>
{c["HONEY"]}<button class="btn btn-gold" type="submit">Send enquiry</button><p class="form-status" role="status"></p>
</form></div></div>
</div></section>
"""


# ---------------- ABOUT ----------------
def about_page(c):
    return f"""
{c["page_head"]("About Mobile.Direct", "An independent website that helps people choose phones, plans and eSIMs with clear tools and honest guides.", [("about.html", "About")])}
<section class="section" style="padding-top:0"><div class="wrap article-wrap"><div class="prose">
<h2>What we do</h2>
<p>Choosing a phone or a plan should not require a spreadsheet. Mobile.Direct turns the questions people actually ask (how much data do I need, will my phone work abroad, what is my old phone worth) into fast tools with clear answers, backed by guides written in plain English.</p>
<h2>How we make money</h2>
<p>The site is free. It is funded by advertising (Google AdSense), by reader contributions, by sponsorships that are always labelled, and by introductions: when you ask us to match you with providers or request quotes, partners may pay us for that introduction. Some outbound links may become affiliate links. None of this changes a score, a ranking or a tool result.</p>
<h2 id="methodology">How we score phones</h2>
<p>Each phone gets five sub-scores from manufacturer-published specifications:</p>
<ul>
<li><strong>Performance</strong> from the chipset's tier, informed by public benchmark rankings.</li>
<li><strong>Camera</strong> from the number of rear cameras, whether there is a telephoto lens and the main sensor's resolution.</li>
<li><strong>Battery</strong> from capacity, with an efficiency adjustment for platforms that achieve longer runtimes from smaller batteries, and a bonus for fast charging.</li>
<li><strong>Display</strong> from refresh rate and size.</li>
<li><strong>Value</strong> from the overall spec score relative to launch price.</li>
</ul>
<p>The match score is the average of these, weighted by the priorities you set. Spec-based scores are for shortlisting; read hands-on reviews before buying.</p>
<h2>How we keep information current</h2>
<ul>
<li>Headlines and videos refresh automatically every six hours.</li>
<li>Plan price ranges and the carrier directory are reviewed regularly against carriers' own sites.</li>
<li>Phone data is added when phones launch, from manufacturer specifications.</li>
<li>Every guide shows its last update date.</li>
</ul>
<h2>Independence</h2>
<p>No carrier, manufacturer or provider can pay for a better score or position. Sponsored content is labelled. If you spot an error, <a href="{{r}}contact.html">tell us</a> and we will fix it.</p>
<h2>Who we are</h2>
<p>Mobile.Direct is part of an independent network of web properties. Our contributors include writers, researchers and creators who use and test mobile services every day. <a href="{{r}}careers.html">Join us</a>.</p>
</div>
<aside><div class="aside-box"><h2 style="font-size:1.1rem">Quick links</h2><ul><li><a href="{{r}}disclaimer.html">Disclaimer and trademarks</a></li><li><a href="{{r}}privacy.html">Privacy policy</a></li><li><a href="{{r}}contact.html">Contact and corrections</a></li><li><a href="{{r}}support.html">Support us</a></li></ul></div></aside>
</div></section>
"""


# ---------------- CONTACT ----------------
def contact_page(c):
    return f"""
{c["page_head"]("Contact Mobile.Direct", "Questions, corrections, press or partnerships. We reply within two business days.", [("contact.html", "Contact")])}
<section class="section" style="padding-top:0"><div class="wrap lead-grid">
<div class="sim"><div class="sim-body">
<form data-md-form="Contact message" data-success="Message received. We reply within two business days.">
<div class="grid-2"><div class="field"><label for="cn-name">Name</label><input id="cn-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="cn-email">Email</label><input id="cn-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="field"><label for="cn-topic">Topic</label><select id="cn-topic" name="topic"><option>General question</option><option>Correction or update</option><option>Help choosing a phone or plan</option><option>Press</option><option>Partnership or sponsorship</option><option>Privacy request</option></select></div>
<div class="field"><label for="cn-msg">Message</label><textarea id="cn-msg" name="message" required></textarea></div>
{c["HONEY"]}<button class="btn btn-gold" type="submit">Send message</button><p class="form-status" role="status"></p>
</form></div></div>
<div>
<h2>Website, domain, sponsorship or partnership</h2>
<p>If you are interested in this website, the domain name, sponsorship, advertising or a partnership, contact the owner directly.</p>
<a class="btn btn-ghost" href="{c["OWNER_LINK"]}" target="_blank" rel="noopener">Contact the owner</a>
<h2 style="margin-top:32px">Looking for something specific?</h2>
<ul><li><a href="{{r}}business.html">Business mobile quotes</a></li><li><a href="{{r}}advertise.html">Advertising options</a></li><li><a href="{{r}}careers.html">Careers</a></li><li><a href="{{r}}support.html">Supporting the site</a></li></ul>
</div>
</div></section>
"""


# ---------------- LEGAL ----------------
def _legal(title, lede, crumb, html_body):
    def body(c):
        return c["page_head"](title, lede, [(crumb[0], crumb[1])]) + '<section class="section" style="padding-top:0"><div class="wrap"><div class="prose">%s</div></div></section>' % html_body
    return body


PRIVACY = """
<p><strong>Effective 19 November 2026.</strong> This policy explains what Mobile.Direct collects, why, and your choices.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Information you send us</strong> through forms: for example your name, email, phone number, postal code, quiz answers or application details. Forms are delivered to our private inbox through a form-relay service (FormSubmit).</li>
<li><strong>Tool inputs</strong> such as data-usage sliders or IMEI numbers are processed in your browser and are not sent to us unless you submit a form.</li>
<li><strong>Technical data</strong> collected automatically by our host (GitHub Pages) and by third-party services listed below, such as IP address, browser type and pages viewed.</li>
<li><strong>Settings</strong> stored in your browser's local storage, such as your theme choice and that you have seen the cookie notice.</li>
</ul>
<h2>How we use it</h2>
<ul>
<li>To reply to you, send the report, alerts or newsletter you asked for, and run contests.</li>
<li>When you request a plan match, quotes or offers and tick the consent box, to share your request with up to three relevant providers or partners so they can contact you about it.</li>
<li>To improve the site and keep it secure.</li>
</ul>
<p>We do not sell personal information for money. We keep form submissions only as long as needed for the purpose, and job applications for up to 12 months.</p>
<h2>Advertising and Google AdSense</h2>
<p>We use Google AdSense to show ads. Google and its partners use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits. You can opt out of personalised advertising at <a href="https://adssettings.google.com/" rel="noopener" target="_blank">Google Ads Settings</a>, and learn more at <a href="https://policies.google.com/technologies/ads" rel="noopener" target="_blank">how Google uses information in advertising</a>. You can also opt out of some third-party vendors' cookies at <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">aboutads.info</a>. Visitors in the European Economic Area, the UK and Switzerland are asked for consent through Google's certified consent message before personalised ads are shown.</p>
<h2>Other third-party services</h2>
<ul>
<li><strong>YouTube</strong> videos are embedded in privacy-enhanced mode and load only when you press play.</li>
<li><strong>Google Fonts</strong> delivers the site's typeface.</li>
<li><strong>PayPal</strong> processes contributions; we never see your card details.</li>
<li><strong>FormSubmit</strong> relays form messages to our inbox.</li>
</ul>
<h2>Your rights</h2>
<p>Depending on where you live (for example under the GDPR, UK GDPR, Canada's PIPEDA and Quebec's Law 25, or California's CCPA/CPRA), you can ask to access, correct or delete your personal information, withdraw consent, or opt out of sharing. Use the <a href="contact.html">contact form</a> and choose "Privacy request". We respond within 30 days.</p>
<h2>Children</h2>
<p>This site is not directed at children under 13 (16 in the EEA), and we do not knowingly collect their information.</p>
<h2>Changes</h2>
<p>We will update this page when our practices change and revise the effective date above.</p>
"""

TERMS = """
<p><strong>Effective 19 November 2026.</strong> By using Mobile.Direct you agree to these terms.</p>
<h2>Information, not advice</h2>
<p>Content and tool results are general information to help you compare options. Prices, plan details and specifications change often and may contain errors. Always confirm details with the provider before you buy. Tool results such as trade-in values, savings and data estimates are estimates, not offers.</p>
<h2>No warranty</h2>
<p>The site is provided "as is" without warranties of any kind. To the extent permitted by law, Mobile.Direct is not liable for any loss arising from use of the site or reliance on its content.</p>
<h2>Third-party links and services</h2>
<p>We link to carriers, retailers, publishers and other sites we do not control. Their terms and privacy policies apply when you use them.</p>
<h2>Your submissions</h2>
<p>You agree to give accurate information in forms and not to submit unlawful, infringing or harmful content. Contest entries are also governed by the contest rules.</p>
<h2>Contributions</h2>
<p>Contributions made through the Support page are voluntary, support an independent website, are non-refundable except where required by law, and are not tax-deductible charitable donations.</p>
<h2>Intellectual property</h2>
<p>The site's original text, tools, design and code are protected by copyright. You may share links and short quotes with attribution. Do not copy or republish substantial parts without permission.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the Province of Quebec and the federal laws of Canada applicable there, without affecting any mandatory consumer protections where you live.</p>
<h2>Changes</h2>
<p>We may update these terms; the effective date above shows the latest version.</p>
"""

DISCLAIMER = """
<h2>Trademark disclosure</h2>
<p>Mobile.Direct is an independent informational website. It is not a mobile carrier, network operator, phone manufacturer or retailer. It is <strong>not affiliated with, endorsed by, sponsored by or connected to</strong> any carrier, manufacturer, eSIM provider, retailer, or any other business, brand or trademark that uses a similar name or wording. The name "Mobile.Direct" refers only to this website and its domain.</p>
<p>All product names, company names, carrier names, logos and brands mentioned on this site (for example Apple, iPhone, Samsung, Galaxy, Google, Pixel, Android, and the carriers and providers in our directory) are trademarks or registered trademarks of their respective owners. They are used only to identify products and services for comparison purposes. Their use does not imply any affiliation or endorsement.</p>
<h2>Copyright disclosure</h2>
<p>&copy; Mobile.Direct. The original text, tools, scoring method, data compilation, design and code on this site are protected by copyright. Phone specifications are factual information published by manufacturers. News headlines link to and remain the property of their publishers. Embedded videos remain the property of their creators and are shown through YouTube's embedding service under its terms.</p>
<p>If you believe any content on this site infringes your rights, send details through our <a href="contact.html">contact form</a> and we will review and, where appropriate, remove it promptly.</p>
<h2>Affiliate and advertising disclosure</h2>
<p>Mobile.Direct is supported by advertising (including Google AdSense), sponsorships, reader contributions and introductions to providers. Some links may be affiliate links, which means we may earn a commission if you buy, at no extra cost to you. Sponsored placements are labelled. Commissions and sponsorships never change our scores, rankings or tool results.</p>
<h2>Accuracy</h2>
<p>We work to keep information accurate, but prices, plans, coverage and specifications change frequently. Estimates (savings, trade-in values, data needs, band compatibility) are approximations. Confirm all details with the provider before making a decision.</p>
<h2>Not professional advice</h2>
<p>Nothing on this site is legal, financial or technical advice.</p>
"""

COOKIES = """
<h2>What cookies and local storage we use</h2>
<table><thead><tr><th scope="col">Name or type</th><th scope="col">Set by</th><th scope="col">Purpose</th></tr></thead><tbody>
<tr><td>Advertising cookies</td><td>Google AdSense and its partners</td><td>Show and measure ads, limit repeats, and personalise ads where you have allowed it</td></tr>
<tr><td>YouTube cookies</td><td>YouTube (privacy-enhanced mode)</td><td>Set only after you press play on a video</td></tr>
<tr><td>md-theme (local storage)</td><td>Mobile.Direct</td><td>Remembers light or dark theme</td></tr>
<tr><td>md-cookie (local storage)</td><td>Mobile.Direct</td><td>Remembers that you closed the cookie notice</td></tr>
<tr><td>md-slide (session storage)</td><td>Mobile.Direct</td><td>Stops the plan-match reminder from showing twice in one visit</td></tr>
</tbody></table>
<h2>Your choices</h2>
<ul>
<li>Manage personalised ads at <a href="https://adssettings.google.com/" rel="noopener" target="_blank">Google Ads Settings</a>.</li>
<li>Opt out of some vendors at <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">aboutads.info</a> or, in Europe, <a href="https://www.youronlinechoices.eu/" rel="noopener" target="_blank">youronlinechoices.eu</a>.</li>
<li>Block or delete cookies in your browser settings. The site still works without them.</li>
</ul>
<p>Visitors in the EEA, UK and Switzerland see Google's consent message and can change their choice at any time.</p>
"""

NOT_FOUND = """
<section class="page-head"><div class="wrap"><h1>That page has no signal</h1><p class="lede">The address may be mistyped, or the page has moved. These will get you back on track.</p>
<div class="seg"><a class="btn" href="index.html">Go to the home page</a><a class="btn btn-ghost" href="tools.html">Open the tools</a><a class="btn btn-ghost" href="guides.html">Read the guides</a></div></div></section>
"""

PAGES_CONTENT = [
    dict(path="index.html", title="Mobile.Direct: compare phones, plans and travel eSIMs",
         desc="Independent tools to compare phones, find a cheaper phone plan, plan travel eSIM data and value your old phone. Free, fast and unbiased.",
         body=home, scripts=("tools.js", "matcher.js"), ld=HOME_LD, priority="1.0", dynamic=True),
    dict(path="get-matched.html", title="Plan match: find your best-fit phone plan", crumb="Plan match",
         desc="Answer six questions and get your best-fit phone plan type, the carriers to compare first and an estimated yearly saving.",
         body=get_matched, scripts=("matcher.js",), faq=GM_FAQ, priority="0.9", body_attr=" data-no-slidein"),
    dict(path="phones.html", title="Phone finder: compare and rank current phones", crumb="Phone finder", active="phones.html",
         desc="Rank current iPhone, Galaxy, Pixel, OnePlus and other phones by your own priorities and compare up to three side by side.",
         body=phones_page, scripts=("phones.js",), faq=PH_FAQ, priority="0.9"),
    dict(path="plans.html", title="Phone plans and carriers: prices and directory", crumb="Plans", active="plans.html",
         desc="Typical phone plan prices by plan type and a directory of carriers, sub-brands and MVNOs in the US, Canada, UK, India and Australia.",
         body=plans_page, faq=PL_FAQ, priority="0.9"),
    dict(path="esim.html", title="Travel eSIM hub: planner, checker and providers", crumb="eSIM", active="esim.html",
         desc="Estimate travel data for your trip, check whether your phone supports eSIM and compare travel eSIM providers.",
         body=esim_page, scripts=("tools.js", "esim.js"), faq=ES_FAQ, priority="0.9"),
    dict(path="trade-in.html", title="Trade-in value estimator: what is my phone worth?", crumb="Trade-in", active="trade-in.html",
         desc="Estimate your phone's trade-in value today, compare refurbished vs new, and get competing cash offers.",
         body=tradein_page, scripts=("tools.js",), priority="0.8"),
    dict(path="tools.html", title="Free mobile tools and calculators", crumb="Tools", active="tools.html",
         desc="Data usage calculator, total cost of ownership, eSIM checker, band checker, IMEI validator, roaming calculator and more.",
         body=tools_page, scripts=("tools.js",), priority="0.9"),
    dict(path="guides.html", title="Guides to phones, plans and eSIM", crumb="Guides", active="guides.html",
         desc="Independent guides to choosing phone plans, MVNOs, eSIM, travel data, unlocking, trade-ins, refurbished phones and 5G.",
         body=guides_page, priority="0.8"),
    dict(path="news.html", title="Mobile news: latest phone and carrier headlines", crumb="News", active="news.html",
         desc="The latest smartphone, carrier, 5G and eSIM headlines from leading mobile news sites, refreshed every six hours.",
         body=news_page, scripts=("esim.js",), priority="0.7", dynamic=True),
    dict(path="videos.html", title="Phone review videos", crumb="Videos", active="videos.html",
         desc="Recent phone reviews, comparisons and durability tests from respected creators, refreshed automatically.",
         body=videos_page, priority="0.6", dynamic=True),
    dict(path="deals.html", title="Phone deal calendar and alerts", crumb="Deal calendar",
         desc="When phone and plan prices drop during the year, and free alerts so you buy at the right time.",
         body=deals_page, priority="0.6"),
    dict(path="business.html", title="Business mobile quotes", crumb="Business",
         desc="Get competing quotes for business mobile lines, devices, device management and roaming from matched providers.",
         body=business_page, faq=BZ_FAQ, priority="0.8", body_attr=" data-no-slidein"),
    dict(path="support.html", title="Support Mobile.Direct", crumb="Support",
         desc="Contribute to keep Mobile.Direct's tools free and independent, sponsor a prize or fund a new tool.",
         body=support_page, priority="0.4"),
    dict(path="contests.html", title="Contests and prizes", crumb="Contests",
         desc="Monthly Mobile.Direct contests with prizes. Free to enter and judged on merit. Official rules included.",
         body=contests_page, priority="0.5"),
    dict(path="careers.html", title="Careers at Mobile.Direct", crumb="Careers",
         desc="Remote roles for mobile tech writers, pricing researchers, video creators, community coordinators and ambassadors.",
         body=careers_page, priority="0.4"),
    dict(path="advertise.html", title="Advertise and partner with Mobile.Direct", crumb="Advertise",
         desc="Sponsorships, newsletter placements, white-label tools and lead partnerships with Mobile.Direct.",
         body=advertise_page, priority="0.5"),
    dict(path="about.html", title="About Mobile.Direct and our methodology", crumb="About",
         desc="Who we are, how we make money, how we score phones and how we keep information current.",
         body=about_page, priority="0.5"),
    dict(path="contact.html", title="Contact Mobile.Direct", crumb="Contact",
         desc="Contact Mobile.Direct with questions, corrections, press or partnership requests.",
         body=contact_page, priority="0.5"),
    dict(path="privacy.html", title="Privacy policy", crumb="Privacy policy",
         desc="How Mobile.Direct collects, uses and protects information, including Google AdSense advertising cookies.",
         body=_legal("Privacy policy", "What we collect, why, and the choices you have.", ("privacy.html", "Privacy policy"), PRIVACY), priority="0.3"),
    dict(path="terms.html", title="Terms of use", crumb="Terms of use",
         desc="The terms that apply when you use Mobile.Direct.",
         body=_legal("Terms of use", "The ground rules for using this website.", ("terms.html", "Terms of use"), TERMS), priority="0.3"),
    dict(path="disclaimer.html", title="Disclaimer, trademark and copyright disclosure", crumb="Disclaimer",
         desc="Mobile.Direct's trademark and copyright disclosure, affiliate disclosure and accuracy disclaimer.",
         body=_legal("Disclaimer and trademark disclosure", "Who we are not affiliated with, who owns what, and how we are funded.", ("disclaimer.html", "Disclaimer"), DISCLAIMER), priority="0.3"),
    dict(path="cookies.html", title="Cookie policy", crumb="Cookie policy",
         desc="The cookies and local storage Mobile.Direct uses and how to control them.",
         body=_legal("Cookie policy", "What is stored in your browser and how to control it.", ("cookies.html", "Cookie policy"), COOKIES), priority="0.3"),
    dict(path="404.html", title="Page not found", desc="This page could not be found.", body=lambda c: NOT_FOUND,
         sitemap=False, robots="noindex,follow",
         base_script="<script>(function(){var p=location.pathname,b=p.indexOf('/mobile-direct/')===0?'/mobile-direct/':'/';document.write('<base href=\"'+b+'\">');})();</script>\n"),
]
