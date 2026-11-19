# Original long-form guides for Mobile.Direct. Each guide renders to guides/<slug>.html
GUIDES = [
{
"slug": "how-to-choose-a-phone-plan",
"title": "How to choose a phone plan without overpaying",
"desc": "A five-step method for picking the right cell phone plan: check coverage, measure your data, compare total cost, weigh inclusions and stack discounts.",
"updated": "2026-11-18",
"minutes": 7,
"takeaways": [
  "Start with coverage where you actually spend time, then shop on price.",
  "Measure your real data use before paying for unlimited.",
  "Compare total cost over the contract, including price rises and fees.",
  "Budget brands often use the same towers as the big networks."
],
"tools": [("tools.html#data", "Data usage calculator"), ("get-matched.html", "Plan match questionnaire"), ("tools.html#tco", "Total cost calculator")],
"body": """
<p>Most people pick a phone plan once, then forget about it for years. That is exactly why so many overpay: plans change every few months, while the habits that decide which plan fits you change slowly. A good choice comes down to five questions asked in the right order.</p>

<h2>1. Which network actually works where you are?</h2>
<p>Coverage comes first because a cheap plan with no signal at home is not cheap. Every country has a small number of companies that own radio networks, and many more brands that resell access to them. Before comparing prices, find out which network is strongest at your home, your workplace and your commute.</p>
<ul>
<li>Ask neighbours and co-workers which network they use and whether calls drop indoors.</li>
<li>Check a crowdsourced map built from real speed tests, not only the carrier's own marketing map.</li>
<li>If you can, borrow a SIM or try an eSIM trial on a second line for a week.</li>
</ul>
<p>Once you know the best network, every brand that runs on it becomes a candidate. That usually multiplies your options.</p>

<h2>2. How much data do you really use?</h2>
<p>Open your phone's settings and look at mobile data used over the last few billing cycles. Most people land between 5 and 15 GB a month. Video is the big driver: standard-definition streaming uses around 1 GB an hour and HD can use about 3 GB an hour, while music streaming at high quality uses roughly 0.15 GB an hour.</p>
<p>If your usage is under 20 GB, a fixed-data plan is usually cheaper than unlimited. If you regularly use a hotspot for a laptop, or stream on the commute every day, unlimited starts to pay off. Our <a href="../tools.html#data">data usage calculator</a> turns your habits into a monthly figure.</p>

<h2>3. What is the total cost, not the headline price?</h2>
<p>The advertised monthly price is rarely what you pay. Add these before comparing:</p>
<ul>
<li><strong>Annual price rises</strong> written into some contracts.</li>
<li><strong>Taxes and regulatory fees</strong>, which some carriers include and others add on top.</li>
<li><strong>Activation or connection fees.</strong></li>
<li><strong>Device payments</strong> bundled into the bill, and any promotional credits that disappear if you leave early.</li>
</ul>
<p>Multiply the real monthly cost by the number of months you plan to stay, then subtract any trade-in value. The <a href="../tools.html#tco">total cost calculator</a> compares two options side by side, including yearly increases.</p>

<h2>4. Which inclusions matter to you?</h2>
<p>Inclusions are where plans differentiate once price and coverage are similar. Decide which of these you would actually use:</p>
<ul>
<li>Hotspot data and whether it is capped separately.</li>
<li>Roaming in other countries, and whether it is included or sold by the day.</li>
<li>Priority data, which keeps your speed up when towers are congested.</li>
<li>Streaming subscriptions, cloud storage or device insurance bundled in.</li>
<li>Calling and texting to other countries.</li>
</ul>
<p>Perks only count if they replace something you would otherwise pay for.</p>

<h2>5. Which discounts can you stack?</h2>
<p>Common discounts include paying by automatic payment, adding lines for family members, paying several months in advance, and employer, student, senior or military programmes. Multi-month prepaid plans often deliver the lowest effective monthly price if you can pay upfront.</p>

<h2>Prepaid or postpaid?</h2>
<p>Prepaid plans are paid in advance, usually need no credit check and are easy to leave. Postpaid plans are billed after use, often bundle phone financing and can include more perks. If you bring your own unlocked phone, prepaid is usually the better deal.</p>

<h2>A simple decision rule</h2>
<table>
<thead><tr><th>Your situation</th><th>Usually the best fit</th></tr></thead>
<tbody>
<tr><td>Under 5 GB, mostly on Wi-Fi</td><td>Low-cost prepaid plan on the strongest local network</td></tr>
<tr><td>5–20 GB, one or two lines</td><td>Budget brand or MVNO with a mid-size data bucket</td></tr>
<tr><td>Heavy streaming or hotspot use</td><td>Unlimited plan with a generous hotspot allowance</td></tr>
<tr><td>Frequent international travel</td><td>Plan with included roaming, or a cheap home plan plus travel eSIMs</td></tr>
<tr><td>Family of four or more</td><td>Multi-line plan with per-line discounts</td></tr>
</tbody>
</table>
<p>Still unsure? Answer six questions in our <a href="../get-matched.html">plan match</a> and get a recommendation with an estimated yearly saving.</p>
""",
"faq": [
  ("Is unlimited data worth it?", "Only if you regularly use more than roughly 25–30 GB a month or rely on a hotspot. Below that, a fixed-data plan is almost always cheaper."),
  ("Do budget brands have worse coverage?", "They use the same towers as their host network, so coverage is the same. During congestion, their data may be slowed before the host network's own premium customers."),
  ("How often should I review my plan?", "Once a year, or whenever your usage changes. Plan prices and promotions change several times a year.")
]
},
{
"slug": "mvno-vs-major-carrier",
"title": "MVNO vs major carrier: what you really give up",
"desc": "Mobile virtual network operators can cut your bill by a third or more. Here is what changes when you switch: priority, hotspot, roaming and support.",
"updated": "2026-11-18",
"minutes": 6,
"takeaways": [
  "An MVNO rents capacity on a big network, so coverage maps are the same.",
  "The main trade-off is data priority during congestion.",
  "Check hotspot rules, roaming and phone compatibility before switching.",
  "For single lines and light users, the saving is often 30–50%."
],
"tools": [("plans.html", "Carrier directory"), ("get-matched.html", "Plan match questionnaire")],
"body": """
<p>A mobile virtual network operator, or MVNO, is a phone company that does not own radio towers. It buys capacity wholesale from a network owner and sells plans under its own brand. Some MVNOs are independent; others are budget brands owned by the network itself, often called sub-brands or flanker brands.</p>

<h2>Why MVNOs are cheaper</h2>
<p>MVNOs skip the costs that make big carriers expensive: national store networks, heavy advertising, device subsidies and premium perks. Many run online only, with app-based support. The network owner sells them spare capacity because it earns money from towers that would otherwise sit idle at quiet times.</p>

<h2>What stays the same</h2>
<ul>
<li><strong>Coverage.</strong> If the MVNO runs on a network, you get that network's towers. Rural coverage is identical in normal conditions.</li>
<li><strong>Your number.</strong> You can port your existing number in.</li>
<li><strong>Your phone.</strong> Most unlocked phones work, as long as they support the host network's bands.</li>
</ul>

<h2>What can change</h2>
<h3>Data priority</h3>
<p>When a tower is congested, for example at a stadium or a busy station at rush hour, networks decide whose data goes first. MVNO and prepaid customers are often placed behind the network's own premium customers. In daily use most people never notice; in crowded places, speeds can drop.</p>
<h3>Hotspot limits</h3>
<p>Some MVNOs cap tethering separately or slow hotspot speeds. If you work from a laptop on mobile data, read the hotspot terms first.</p>
<h3>Roaming</h3>
<p>Big carriers more often include roaming in neighbouring countries. Many MVNOs offer limited or paid roaming. If you travel, pair a cheap MVNO with a <a href="../esim.html">travel eSIM</a>.</p>
<h3>Support and extras</h3>
<p>Expect app or chat support rather than a store. Perks like streaming bundles are less common, and phone financing may be limited.</p>

<h2>Who should switch</h2>
<table>
<thead><tr><th>Profile</th><th>MVNO fit</th></tr></thead>
<tbody>
<tr><td>Single line, under 20 GB, owns an unlocked phone</td><td>Excellent</td></tr>
<tr><td>Family that wants the cheapest per-line price</td><td>Good: many MVNOs offer multi-line discounts</td></tr>
<tr><td>Heavy hotspot user</td><td>Check the hotspot cap first</td></tr>
<tr><td>Frequent traveller</td><td>Good with travel eSIMs</td></tr>
<tr><td>Needs in-person support or phone financing</td><td>A network-owned plan may suit better</td></tr>
</tbody>
</table>

<h2>How to switch safely</h2>
<ol>
<li>Confirm your phone is unlocked and supports the host network's bands.</li>
<li>Note your account number and request a transfer or port-out PIN from your current provider.</li>
<li>Sign up with the new provider, choose to keep your number, and enter the details.</li>
<li>Keep the old SIM until the port completes, usually within hours.</li>
</ol>
<p>Our <a href="../plans.html">carrier directory</a> shows which brands run on which networks in the US, Canada, the UK, India and Australia.</p>
""",
"faq": [
  ("Is an MVNO the same as prepaid?", "Not exactly. Most MVNOs sell prepaid plans, but some offer postpaid billing. Network-owned brands also sell prepaid plans."),
  ("Will my 5G work on an MVNO?", "Usually yes if your phone and plan both support 5G on the host network. Some plans limit the fastest 5G to premium tiers.")
]
},
{
"slug": "what-is-esim",
"title": "eSIM explained: setup, transfer and travel",
"desc": "What an eSIM is, how to check if your phone supports one, how to install or move it, and when to keep a physical SIM.",
"updated": "2026-11-18",
"minutes": 6,
"takeaways": [
  "An eSIM is a SIM built into the phone that you download instead of insert.",
  "Dial *#06#: if an EID appears, your phone supports eSIM.",
  "Most phones store several eSIMs and use one or two at a time.",
  "Move your eSIM before you wipe or sell a phone."
],
"tools": [("tools.html#esim", "eSIM compatibility checker"), ("esim.html", "Travel eSIM planner")],
"body": """
<p>An eSIM (embedded SIM) is a chip soldered inside your phone that can hold mobile network profiles. Instead of inserting a plastic card, you download your plan by scanning a QR code, opening the carrier's app or tapping a link. The phone then connects exactly as it would with a physical SIM.</p>

<h2>Does my phone support eSIM?</h2>
<p>The quickest test works on almost every phone: open the dialler and type <strong>*#06#</strong>. If the screen shows an <strong>EID</strong> (a long 32-digit number) alongside your IMEI, the phone has an eSIM chip. Most iPhones from the XR and XS onward, Google Pixel phones from the Pixel 3 onward, Samsung Galaxy S20 and later, and recent foldables support eSIM, but regional versions differ. Our <a href="../tools.html#esim">compatibility checker</a> covers the common models.</p>
<p>The phone also needs to be <a href="unlocked-phones.html">unlocked</a> if you want to add an eSIM from a different carrier than the one that sold it.</p>

<h2>Installing an eSIM</h2>
<ol>
<li>Connect to Wi-Fi. The profile downloads over the internet.</li>
<li>On iPhone, go to Settings, then Mobile or Cellular, then Add eSIM. On Android, go to Settings, Network and internet, then SIMs, and add an eSIM.</li>
<li>Scan the QR code, use the carrier's app, or accept the eSIM your carrier pushes to your phone.</li>
<li>Label the line (for example "Home" and "Travel") and choose which line handles data.</li>
</ol>
<p>Keep the QR code private. Some can only be used once; a deleted profile may need a new code from the carrier.</p>

<h2>Moving an eSIM to a new phone</h2>
<p>Many carriers support transferring an eSIM directly between phones of the same platform during setup. If that is not available, ask the carrier for a new eSIM QR code for the new device. Do this before you erase the old phone, and never delete an eSIM profile you still need until the new one works.</p>

<h2>Why eSIM is great for travel</h2>
<p>You can keep your home number active for calls and verification texts while a travel eSIM handles data. You buy the plan before you leave, it activates when you land, and there is no airport SIM counter. Our <a href="../esim.html">eSIM planner</a> estimates how much data a trip needs and lists providers to compare.</p>

<h2>When a physical SIM still makes sense</h2>
<ul>
<li>Your phone or tablet has no eSIM chip.</li>
<li>You swap SIMs between devices often.</li>
<li>Your local carrier still charges for eSIM or handles it only in store.</li>
</ul>

<h2>Security</h2>
<p>eSIM removes one theft risk: a thief cannot pop the SIM out to stop the phone being tracked. Protect your carrier account with a PIN, because a criminal who controls your account could request a new eSIM for your number.</p>
""",
"faq": [
  ("How many eSIMs can a phone hold?", "Most phones can store several profiles, typically eight or more, and use one or two at the same time depending on the model."),
  ("Can I use an eSIM and a physical SIM together?", "Yes, on dual-SIM phones that still have a SIM tray. Phones sold without a tray in some markets use two eSIMs instead.")
]
},
{
"slug": "travel-data-roaming-vs-esim",
"title": "Travel data: roaming vs local SIM vs travel eSIM",
"desc": "Compare the three ways to get mobile data abroad, with a simple cost formula and a checklist for before you fly.",
"updated": "2026-11-18",
"minutes": 6,
"takeaways": [
  "Day passes are simplest but get expensive after a few days.",
  "Travel eSIMs usually cost a fraction of daily roaming for the same data.",
  "Local SIMs are cheapest for long stays but need a shop visit.",
  "Check your phone is unlocked and supports local bands first."
],
"tools": [("tools.html#roam", "Roaming vs eSIM calculator"), ("tools.html#bands", "Will my phone work abroad?"), ("esim.html", "Travel eSIM planner")],
"body": """
<p>There are three ways to stay connected abroad. Each wins in a different situation, and the right answer depends mostly on the length of your trip and how much data you use.</p>

<h2>Option 1: your carrier's roaming</h2>
<p>Many carriers sell a daily pass that lets you use your home plan abroad, or include roaming in certain regions. It is the easiest choice: nothing to install, and your number works normally. The catch is cost. A pass charged every day adds up quickly over a long trip, and some passes slow data after a daily allowance.</p>
<p><strong>Best for:</strong> short trips of one to three days, or plans that already include roaming at no extra cost.</p>

<h2>Option 2: a travel eSIM</h2>
<p>Travel eSIM providers sell data-only plans for a country, region or the whole world. You install the eSIM before leaving and switch data to it when you land, while your home line stays active for calls and texts.</p>
<ul>
<li><strong>Fixed-data plans</strong> (for example 5 GB for 15 days) are best when you know your usage.</li>
<li><strong>Unlimited plans</strong> suit heavy users but usually slow down after a daily fair-use threshold.</li>
<li>Check whether hotspot sharing is allowed if you need to connect a laptop.</li>
</ul>
<p><strong>Best for:</strong> most trips of three days or more.</p>

<h2>Option 3: a local SIM or eSIM</h2>
<p>Buying from a local operator after you arrive usually gives the lowest price per gigabyte and a local number. Many countries require ID registration, which can take time, and you may need a physical SIM slot.</p>
<p><strong>Best for:</strong> stays of several weeks, or when you need a local number.</p>

<h2>Quick cost formula</h2>
<p>Estimate total data as daily use multiplied by days, plus a 20% buffer. Then compare:</p>
<table>
<thead><tr><th>Option</th><th>Cost</th></tr></thead>
<tbody>
<tr><td>Day pass</td><td>Daily price × days</td></tr>
<tr><td>Fixed travel eSIM</td><td>Price of the smallest plan above your total data</td></tr>
<tr><td>Unlimited travel eSIM</td><td>Daily or plan price for your trip length</td></tr>
</tbody>
</table>
<p>The <a href="../tools.html#roam">roaming calculator</a> does this for you.</p>

<h2>Before you fly</h2>
<ol>
<li>Confirm your phone is <a href="unlocked-phones.html">unlocked</a>.</li>
<li>Check it supports the destination's main 4G bands with our <a href="../tools.html#bands">band checker</a>.</li>
<li>Install the travel eSIM at home on Wi-Fi, but leave it switched off.</li>
<li>Turn off data roaming on your home line so it cannot run up charges.</li>
<li>Download offline maps and translation packs as a backup.</li>
</ol>
""",
"faq": [
  ("Will I keep my phone number with a travel eSIM?", "Yes. Keep your home line enabled for calls and texts, and set the travel eSIM as the data line. Incoming calls on your home line may still incur roaming charges, so check your carrier's rates."),
  ("Do travel eSIMs work for messaging apps?", "Yes. Messaging and calling apps work over the data connection like any other app.")
]
},
{
"slug": "unlocked-phones",
"title": "Unlocked phones: how to check and how to unlock",
"desc": "What carrier locking means, how to check if your phone is unlocked, and the rules in the US, Canada, the UK, India and Australia.",
"updated": "2026-11-18",
"minutes": 5,
"takeaways": [
  "A locked phone only works with the carrier that sold it.",
  "Test by inserting or adding a SIM from a different carrier.",
  "Canada and the UK ban the sale of locked phones; the US relies on carrier policies.",
  "Paying off a financed phone is usually required before unlocking."
],
"tools": [("tools.html#imei", "IMEI validator"), ("tools.html#bands", "Band checker")],
"body": """
<p>Carriers sometimes lock the phones they sell so they only accept that carrier's SIM. A lock protects the carrier while the phone is being paid off. An unlocked phone accepts a SIM or eSIM from any compatible network, which lets you switch plans freely and use local SIMs when travelling.</p>

<h2>How to check if your phone is unlocked</h2>
<ul>
<li><strong>Swap test:</strong> insert a SIM from a different carrier (borrow one from a friend). If you can make a call, the phone is unlocked.</li>
<li><strong>iPhone:</strong> go to Settings, General, About. Next to Carrier Lock (or Network Provider Lock) it says "No SIM restrictions" when unlocked.</li>
<li><strong>Android:</strong> look for a SIM lock or network unlock section in Settings, or try adding a second carrier's eSIM.</li>
<li><strong>Ask:</strong> your carrier can confirm the status from your IMEI.</li>
</ul>

<h2>The rules by country</h2>
<table>
<thead><tr><th>Country</th><th>What applies</th></tr></thead>
<tbody>
<tr><td>Canada</td><td>The national Wireless Code requires phones to be sold unlocked and bans unlocking fees.</td></tr>
<tr><td>United Kingdom</td><td>The regulator stopped providers selling locked phones from December 2021.</td></tr>
<tr><td>United States</td><td>Carriers follow their own unlocking policies under industry commitments: typically once the device is paid off and the account is in good standing, or after a set period. Some unlock automatically.</td></tr>
<tr><td>India</td><td>Most phones are sold unlocked through retail.</td></tr>
<tr><td>Australia</td><td>Carriers unlock on request; most phones are now sold unlocked.</td></tr>
</tbody>
</table>
<p>Policies change, so always confirm on your carrier's own unlocking page.</p>

<h2>How to request an unlock</h2>
<ol>
<li>Pay off any device balance.</li>
<li>Find your IMEI by dialling *#06#.</li>
<li>Submit the carrier's online unlock form or call support.</li>
<li>Restart the phone with the new SIM once the carrier confirms.</li>
</ol>

<h2>Unlocked does not mean compatible</h2>
<p>An unlocked phone still needs to support the bands the new network uses. Phones built for one market may miss key low-frequency bands in another, which shows up as weak indoor signal. Use our <a href="../tools.html#bands">band checker</a> before switching or travelling.</p>

<h2>Avoid "unlock code" scams</h2>
<p>Paid third-party unlock services range from legitimate to fraudulent. A phone that is reported lost, stolen or unpaid can be blocked again later. Use your carrier's official process whenever you can.</p>
""",
"faq": [
  ("Does unlocking void my warranty?", "An official carrier unlock does not affect the manufacturer's warranty."),
  ("Is a carrier lock the same as an activation lock?", "No. Activation lock (Find My or Google account protection) ties the phone to the owner's account and must be removed by the owner. It is separate from carrier locking.")
]
},
{
"slug": "sell-or-trade-in-your-phone",
"title": "How to sell or trade in your phone for the most money",
"desc": "Compare carrier trade-ins, buyback sites and private sales; prepare your phone; and time the sale to beat the price drop.",
"updated": "2026-11-18",
"minutes": 6,
"takeaways": [
  "Get at least three quotes; offers for the same phone vary widely.",
  "Carrier trade-in credits are often paid over 24–36 months.",
  "Sell before a new model launches, when used prices dip.",
  "Remove your account lock, back up and erase before you ship."
],
"tools": [("trade-in.html", "Trade-in value estimator"), ("tools.html#imei", "IMEI validator")],
"body": """
<p>An old phone in a drawer loses value every month. Selling it at the right time, through the right channel, can fund a large part of your next phone.</p>

<h2>Your four options</h2>
<table>
<thead><tr><th>Channel</th><th>Typical payout</th><th>Effort</th><th>Watch out for</th></tr></thead>
<tbody>
<tr><td>Carrier trade-in</td><td>High headline value on promotions</td><td>Low</td><td>Paid as bill credits over the contract; you lose the rest if you leave early</td></tr>
<tr><td>Manufacturer trade-in</td><td>Fair, as credit toward a new device</td><td>Low</td><td>Store credit only</td></tr>
<tr><td>Buyback websites</td><td>Good, paid in cash</td><td>Low</td><td>Re-grading on arrival; read the condition rules</td></tr>
<tr><td>Private sale or marketplace</td><td>Highest</td><td>High</td><td>Fees, scams, time spent answering buyers</td></tr>
</tbody>
</table>
<p>Comparison sites that collect quotes from many buyback companies regularly show large differences between the best and worst offer for the same model and condition, so a few minutes of comparison pays.</p>

<h2>Timing</h2>
<p>Used prices fall fastest when a new generation launches. For iPhones that is usually September; for Samsung Galaxy S models it is early in the year. Selling two to four weeks before a launch typically beats selling after it. Our <a href="../trade-in.html">estimator</a> shows how value declines with age.</p>

<h2>Grade your phone honestly</h2>
<ul>
<li><strong>Flawless:</strong> no visible marks.</li>
<li><strong>Good:</strong> light scratches, everything works.</li>
<li><strong>Fair:</strong> visible scratches or scuffs, everything works.</li>
<li><strong>Broken:</strong> cracked glass, faulty buttons or battery issues.</li>
</ul>
<p>Over-grading leads to a lower revised offer after inspection. Photograph the phone before shipping.</p>

<h2>Prepare the phone</h2>
<ol>
<li>Back up photos, messages and authenticator apps.</li>
<li>Move your eSIM or remove the physical SIM.</li>
<li>Sign out of Apple ID with Find My turned off, or remove your Google account on Android.</li>
<li>Erase all content and settings.</li>
<li>Check the phone is carrier-unlocked; unlocked phones fetch more.</li>
</ol>

<h2>Broken phones still sell</h2>
<p>Many buyers accept cracked screens and pay a reduced price. Get a quote before paying for a repair; the repair often costs more than the value it adds.</p>
""",
"faq": [
  ("Can I sell a phone that is still on a payment plan?", "You can, but most buyers require the phone to be paid off and not blocklisted. Pay it off first to get a fair price."),
  ("Is it safe to send my phone by post?", "Use a buyer with a clear inspection process and tracked shipping, and keep photos of the phone's condition.")
]
},
{
"slug": "refurbished-phone-buying-guide",
"title": "Refurbished phones: grades, battery and what to check",
"desc": "How refurbished grading works, the battery health to insist on, warranties and returns, and when refurbished beats new.",
"updated": "2026-11-18",
"minutes": 5,
"takeaways": [
  "Grades describe looks, not function, on reputable marketplaces.",
  "Ask for battery health of at least 85%, or a new battery.",
  "Insist on a warranty of 12 months and a return window.",
  "Last year's flagship refurbished often beats a new mid-range phone."
],
"tools": [("tools.html#refurb", "Refurbished vs new calculator"), ("phones.html", "Phone finder")],
"body": """
<p>A refurbished phone has been returned, inspected, repaired where needed, cleaned and resold. Bought from a reputable seller, it works like new and usually costs 30–70% less, depending on age and condition.</p>

<h2>How grading works</h2>
<p>Large refurbished marketplaces grade phones by cosmetic condition. All grades must pass the same functional tests.</p>
<table>
<thead><tr><th>Grade</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Excellent / Premium</td><td>Looks new; marks invisible with the screen on</td></tr>
<tr><td>Good</td><td>Light scratches visible up close</td></tr>
<tr><td>Fair</td><td>Visible scratches or scuffs on body or screen</td></tr>
</tbody>
</table>
<p>If you use a case and screen protector, "Good" is often the best value.</p>

<h2>Battery health matters most</h2>
<p>Lithium-ion batteries lose capacity with charge cycles. Reputable sellers guarantee a minimum capacity (often 80%), and some offer a new battery as an option. For a phone you plan to keep two years or more, ask for 85% or higher, or budget for a battery replacement.</p>

<h2>Warranty and returns</h2>
<ul>
<li>Look for at least a 12-month warranty.</li>
<li>A 14–30 day return window lets you test properly.</li>
<li>Confirm the phone is unlocked and not blocklisted.</li>
<li>Check what is in the box; many come with a cable but no charger.</li>
</ul>

<h2>What to test on day one</h2>
<ol>
<li>Calls on speaker and earpiece, and the microphone.</li>
<li>Every camera, including video and focus.</li>
<li>Face or fingerprint unlock.</li>
<li>Charging with a cable and wirelessly if supported.</li>
<li>Wi-Fi, Bluetooth, GPS and mobile data.</li>
<li>Battery health in settings.</li>
</ol>

<h2>Refurbished or new?</h2>
<p>Refurbished wins when you want flagship cameras and performance on a mid-range budget. New wins when you want the longest software support, or when a launch promotion brings the new price close to refurbished. The <a href="../tools.html#refurb">refurbished vs new calculator</a> shows the real saving including a battery swap.</p>
<p>Buying refurbished also cuts electronic waste: reusing a phone avoids most of the raw materials and emissions of manufacturing a new one.</p>
""",
"faq": [
  ("Is refurbished the same as used?", "No. Used phones are sold as-is by their owner. Refurbished phones are tested, repaired if needed and usually come with a warranty."),
  ("How many years of updates will a refurbished phone get?", "Updates depend on the model's launch date. Check the manufacturer's support policy and subtract the phone's age.")
]
},
{
"slug": "buying-used-phone-safely",
"title": "Buying a used phone safely: IMEI, blocklists and locks",
"desc": "A step-by-step checklist for buying a second-hand phone: verify the IMEI, check official blocklists, avoid activation locks and test before paying.",
"updated": "2026-11-18",
"minutes": 5,
"takeaways": [
  "Check the IMEI on an official lost-and-stolen database before paying.",
  "Make sure the seller's account lock is removed in front of you.",
  "Unpaid financed phones can be blocked after you buy them.",
  "Meet in a public place and test every function."
],
"tools": [("tools.html#imei", "IMEI validator"), ("tools.html#bands", "Band checker")],
"body": """
<p>Private sales get you the lowest prices, but they carry risks a shop takes on for you. These steps remove most of them.</p>

<h2>1. Get the IMEI and verify it</h2>
<p>Ask the seller to dial *#06# and show you the screen. Compare it with the IMEI in settings and on the SIM tray or box. All should match. Run it through our <a href="../tools.html#imei">IMEI validator</a>: an IMEI that fails the check-digit test has been mistyped or altered.</p>

<h2>2. Check official blocklists</h2>
<p>Many countries share lost and stolen phone databases between carriers. A blocked phone cannot connect to networks.</p>
<ul>
<li>United States: the industry Stolen Phone Checker at <a href="https://www.stolenphonechecker.org/" rel="nofollow noopener" target="_blank">stolenphonechecker.org</a>.</li>
<li>Australia: the industry lost and stolen register at <a href="https://www.lost.amta.org.au/" rel="nofollow noopener" target="_blank">lost.amta.org.au</a>.</li>
<li>India: the government's Sanchar Saathi portal at <a href="https://www.sancharsaathi.gov.in/" rel="nofollow noopener" target="_blank">sancharsaathi.gov.in</a>.</li>
<li>Elsewhere: ask a local carrier to check the IMEI.</li>
</ul>

<h2>3. Remove the account lock</h2>
<p>An iPhone with Find My turned on, or an Android phone still signed in to a Google account, is tied to its owner. Ask the seller to sign out and erase the phone while you watch. If they cannot, walk away.</p>

<h2>4. Confirm it is paid off and unlocked</h2>
<p>A phone sold while still on a payment plan can be blocklisted later for non-payment. Ask whether it is fully paid, and test with your own SIM to confirm it is unlocked.</p>

<h2>5. Test before paying</h2>
<ol>
<li>Make a call with your SIM.</li>
<li>Test cameras, speakers, microphone and buttons.</li>
<li>Check battery health and charging.</li>
<li>Look for screen burn-in on a plain grey background.</li>
<li>Check face or fingerprint unlock works for you after setup.</li>
</ol>

<h2>6. Pay safely</h2>
<p>Meet in a public place, ideally a carrier store or a police "safe exchange" spot. Use a payment method with a record. Avoid deals that seem far below market value.</p>
""",
"faq": [
  ("What is a TAC?", "The first eight digits of an IMEI form the Type Allocation Code, which identifies the manufacturer and model."),
  ("Can a blocked phone be fixed?", "Only the original owner or carrier can remove a block legitimately, for example if a lost phone is found.")
]
},
{
"slug": "5g-explained",
"title": "5G explained: bands, speeds and what you actually get",
"desc": "Low-band, mid-band and mmWave 5G; standalone vs non-standalone; and whether 5G is worth paying for.",
"updated": "2026-11-18",
"minutes": 5,
"takeaways": [
  "Mid-band 5G gives the best mix of speed and coverage.",
  "mmWave is extremely fast but only over very short distances.",
  "Many networks still anchor 5G on 4G (non-standalone).",
  "A 5G icon does not guarantee faster speeds than good 4G."
],
"tools": [("tools.html#signal", "Signal strength interpreter"), ("tools.html#bands", "Band checker")],
"body": """
<p>5G is the fifth generation of mobile networks. What you experience depends far more on which frequencies your carrier uses near you than on the 5G label itself.</p>

<h2>Three kinds of 5G</h2>
<table>
<thead><tr><th>Type</th><th>Frequencies</th><th>Speed</th><th>Coverage</th></tr></thead>
<tbody>
<tr><td>Low-band</td><td>Below 1 GHz</td><td>Similar to good 4G</td><td>Wide, good indoors</td></tr>
<tr><td>Mid-band</td><td>Roughly 1–6 GHz, including the popular 3.5 GHz range (band n78) and C-band (n77)</td><td>Fast, often hundreds of Mbps</td><td>City and suburban</td></tr>
<tr><td>mmWave</td><td>24 GHz and above (n257–n261)</td><td>Very fast</td><td>A block or less; blocked by walls</td></tr>
</tbody>
</table>

<h2>Standalone vs non-standalone</h2>
<p>Non-standalone (NSA) 5G uses a 4G connection to manage the link while 5G carries data. Standalone (SA) 5G runs end to end on a 5G core, which enables lower latency and features like network slicing. Many networks run both.</p>

<h2>Is 5G worth it?</h2>
<ul>
<li>If your carrier has mid-band 5G where you live, you will likely see a real speed gain.</li>
<li>If you mostly use Wi-Fi, 5G matters little.</li>
<li>5G can use more battery in weak signal areas; most phones switch intelligently to save power.</li>
<li>Almost every phone sold today supports 5G, so you rarely pay extra for the phone.</li>
</ul>

<h2>Read your real signal</h2>
<p>Bars on the status bar are a rough guide. Your phone's diagnostic screens show RSRP (signal power), RSRQ (quality) and SINR (signal to noise). Enter them in our <a href="../tools.html#signal">signal interpreter</a> to see whether slow speed is a signal problem or congestion.</p>
""",
"faq": [
  ("Why does my phone show 5G but feel slow?", "You may be on low-band 5G, on a congested cell, or on a plan with lower data priority."),
  ("Do I need a new SIM for 5G?", "Usually not. Some carriers require a newer SIM or eSIM profile for standalone 5G.")
]
},
{
"slug": "cut-your-phone-bill",
"title": "Cut your phone bill in half: a practical playbook",
"desc": "Ten proven ways to lower your mobile bill, ranked by how much they usually save, with the order to do them in.",
"updated": "2026-11-18",
"minutes": 6,
"takeaways": [
  "Switching to a budget brand on the same network is the biggest single saving.",
  "Pay for the data you use, not the data you fear using.",
  "Bring your own unlocked phone instead of financing a new one.",
  "Re-check your plan every year."
],
"tools": [("get-matched.html", "Plan match"), ("tools.html#data", "Data calculator"), ("tools.html#split", "Family bill splitter")],
"body": """
<p>Most households can cut their phone bill significantly without losing coverage. Work through these steps in order; the first three deliver most of the saving.</p>

<h2>1. Find out what you use</h2>
<p>Look at the last three months of data, minutes and roaming. Use our <a href="../tools.html#data">data calculator</a> if you want a projection. Write down the number.</p>

<h2>2. Move to a budget brand on the same network</h2>
<p>Sub-brands and MVNOs run on the same towers as the big networks. For single lines and light to moderate users, the saving is often a third or more. See which brands run on which network in our <a href="../plans.html">carrier directory</a>.</p>

<h2>3. Right-size your data</h2>
<p>If you use 8 GB, a 15 GB plan is enough. Unlimited plans make sense mainly above about 25–30 GB or for heavy hotspot use.</p>

<h2>4. Keep your phone longer, or buy unlocked</h2>
<p>Financed phones can hide in the monthly bill for years. Buying unlocked, or refurbished, separates the phone from the plan so you can switch freely.</p>

<h2>5. Pay upfront for several months</h2>
<p>Multi-month prepaid plans often cost noticeably less per month than paying monthly.</p>

<h2>6. Stack discounts</h2>
<p>Autopay, paperless billing, employer, student, senior and military discounts can each take a few dollars off per line.</p>

<h2>7. Drop insurance you do not need</h2>
<p>Many credit cards include phone protection when you pay your bill with them. Compare the deductible before keeping carrier insurance.</p>

<h2>8. Use Wi-Fi calling and Wi-Fi data</h2>
<p>Wi-Fi calling fixes weak indoor signal for free and saves data at home and work.</p>

<h2>9. Combine lines fairly</h2>
<p>A family plan lowers the per-line price. Use our <a href="../tools.html#split">bill splitter</a> to divide the cost fairly by usage.</p>

<h2>10. Ask your current carrier</h2>
<p>Once you have a cheaper offer in hand, call your current carrier's retention team. They may match it, which saves you the switch.</p>
""",
"faq": [
  ("Will switching affect my credit?", "Prepaid plans usually need no credit check. Postpaid applications may involve one."),
  ("Do I lose my number when switching?", "No. You can port your number to the new provider in most countries.")
]
},
{
"slug": "business-mobile-plans",
"title": "Business mobile plans: fleets, BYOD and device management",
"desc": "How to choose business mobile service: company-paid vs BYOD, pooled data, device management, eSIM provisioning and international coverage.",
"updated": "2026-11-18",
"minutes": 6,
"takeaways": [
  "Decide between company-owned phones and bring-your-own-device first.",
  "Pooled data plans avoid paying for unused allowances.",
  "Device management keeps company data safe on every phone.",
  "Get at least two competing quotes; business pricing is negotiable."
],
"tools": [("business.html", "Business quote request"), ("tools.html#tco", "Total cost calculator")],
"body": """
<p>Business mobile service is less about the cheapest plan and more about control: who owns the number, who owns the device, how data is protected and how costs are tracked.</p>

<h2>Company-owned or bring your own device?</h2>
<table>
<thead><tr><th></th><th>Company-owned</th><th>BYOD</th></tr></thead>
<tbody>
<tr><td>Control</td><td>Full: the company owns the phone and number</td><td>Partial: work profile only</td></tr>
<tr><td>Cost</td><td>Device and plan</td><td>Monthly stipend or partial reimbursement</td></tr>
<tr><td>Security</td><td>Easier to enforce</td><td>Relies on work profiles and app policies</td></tr>
<tr><td>Best for</td><td>Field teams, regulated industries</td><td>Office staff, small teams</td></tr>
</tbody>
</table>

<h2>Plan structures</h2>
<ul>
<li><strong>Per-line unlimited:</strong> simple, predictable, good for heavy users.</li>
<li><strong>Pooled or shared data:</strong> one data bucket across all lines; efficient when usage varies.</li>
<li><strong>Data-only lines:</strong> for tablets, hotspots, vehicles and sensors.</li>
</ul>

<h2>Device management</h2>
<p>Mobile device management (MDM) lets you enrol phones automatically, push apps and Wi-Fi settings, enforce passcodes and wipe lost devices. Apple and Google both offer zero-touch enrolment programmes that work with MDM software, so new phones configure themselves on first boot.</p>

<h2>eSIM for fleets</h2>
<p>eSIM lets you provision or switch lines remotely, without shipping SIM cards. It is especially useful for remote staff and for moving devices between users.</p>

<h2>Questions to ask every provider</h2>
<ol>
<li>What is the total monthly cost per line after discounts, and how long is the term?</li>
<li>Is data pooled, and what happens when the pool runs out?</li>
<li>What roaming is included for staff who travel?</li>
<li>Is there a dedicated account manager and business support line?</li>
<li>What are the early termination terms?</li>
</ol>
<p>Want competing quotes without the sales calls? Use our <a href="../business.html">business mobility request</a> and we will match your requirements to suitable providers.</p>
""",
"faq": [
  ("How many lines count as a business account?", "Many carriers open business accounts from a single line with a registered business, though the best pricing usually starts at five or more lines."),
  ("Can employees keep their number when they leave?", "Company-liable numbers belong to the company. Agree a porting policy in advance.")
]
},
{
"slug": "keep-your-number-porting",
"title": "Keep your number when switching: porting guide by country",
"desc": "How number porting works in the US, Canada, the UK, India and Australia, what details you need, and how long it takes.",
"updated": "2026-11-18",
"minutes": 5,
"takeaways": [
  "Do not cancel your old plan before the port completes.",
  "You need your account number and usually a transfer PIN or code.",
  "Most wireless ports complete within hours.",
  "The new provider starts the port, not the old one."
],
"tools": [("get-matched.html", "Plan match"), ("plans.html", "Carrier directory")],
"body": """
<p>Number porting moves your phone number from one provider to another. In nearly every country you have a legal right to keep your number, and the process is quick when you have the right details ready.</p>

<h2>The universal rule</h2>
<p>Start the switch with your <strong>new</strong> provider, and keep your old service active until the new SIM works. Cancelling first can release your number.</p>

<h2>United States</h2>
<ul>
<li>You need your account number and a number transfer PIN, which most carriers generate in their app or online account.</li>
<li>Give these to the new carrier during sign-up.</li>
<li>Wireless-to-wireless ports usually complete within hours.</li>
</ul>

<h2>Canada</h2>
<ul>
<li>Have your account number and the phone's IMEI ready.</li>
<li>The new carrier requests the port; wireless ports are normally completed within a few hours.</li>
</ul>

<h2>United Kingdom</h2>
<ul>
<li>Text <strong>PAC</strong> to 65075 to receive your Porting Authorisation Code by text. It is valid for 30 days.</li>
<li>Give the code to your new provider; the switch usually happens the next working day.</li>
<li>To leave without keeping your number, text STAC to 75075.</li>
</ul>

<h2>India</h2>
<ul>
<li>SMS <strong>PORT</strong> followed by your 10-digit mobile number to 1900 to receive a Unique Porting Code.</li>
<li>Visit or contact the new operator with the code and your ID.</li>
<li>The change usually completes within a few working days.</li>
</ul>

<h2>Australia</h2>
<ul>
<li>Provide your account number (prepaid customers may use date of birth) to the new provider.</li>
<li>Ports often complete the same day.</li>
</ul>

<h2>If something goes wrong</h2>
<ol>
<li>Check the name and account details match exactly.</li>
<li>Confirm the PIN or code has not expired.</li>
<li>Ask the new provider for the port status and any rejection reason.</li>
</ol>
<p>Protect your account with a PIN so nobody else can port your number away. Number hijacking is a common route to account takeover.</p>
""",
"faq": [
  ("Will porting cancel my old plan?", "Yes, once the port completes your old service ends automatically. You may still owe any remaining device payments or final bill."),
  ("Can I port a prepaid number?", "Yes. Prepaid numbers can be ported in all the countries listed here.")
]
}
]
