#!/usr/bin/env python3
"""Pull fresh mobile headlines and YouTube uploads into data/*.json.

Standard library only, so it runs on any GitHub Actions runner without installs.
Feeds that fail are skipped; existing data is kept when nothing new arrives.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UA = "Mozilla/5.0 (compatible; MobileDirectBot/1.0; +https://mobile.direct/about.html)"

NEWS_FEEDS = [
    ("GSMArena", "https://www.gsmarena.com/rss-news-reviews.php3"),
    ("Android Authority", "https://www.androidauthority.com/feed/"),
    ("9to5Mac", "https://9to5mac.com/feed/"),
    ("9to5Google", "https://9to5google.com/feed/"),
    ("MobileSyrup", "https://mobilesyrup.com/feed/"),
    ("Android Central", "https://www.androidcentral.com/feed"),
    ("MacRumors", "https://feeds.macrumors.com/MacRumors-All"),
    ("Light Reading", "https://www.lightreading.com/rss.xml"),
]

# General tech feeds: keep only headlines about phones, networks and mobile services.
FILTERED = {"9to5Mac", "9to5Google", "MacRumors", "MobileSyrup", "Light Reading"}

TAGS = {
    "iphone": r"\biphone|\bios\b|\bapple\b",
    "android": r"\bandroid\b",
    "samsung": r"\bsamsung|\bgalaxy\b",
    "pixel": r"\bpixel\b",
    "5g": r"\b5g\b|\b6g\b|spectrum",
    "esim": r"\besim|\bsim card|roaming",
    "carriers": r"verizon|at&t|t-mobile|rogers|bell\b|telus|vodafone|\bee\b|\bo2\b|jio|airtel|carrier|mvno|plan\b|plans\b|telstra|optus",
    "deals": r"\bdeal|discount|\bsale\b|price drop|save \$|\boff\b",
}
MOBILE_HINT = re.compile(r"phone|iphone|android|galaxy|pixel|5g|esim|sim\b|carrier|mobile|wireless|oneplus|xiaomi|motorola|nothing|foldable|ios|tablet|smartwatch|verizon|t-mobile|at&t|rogers|telus|bell\b|vodafone|jio|airtel|roaming|network", re.I)


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def text(el, *names):
    for n in names:
        x = el.find(n)
        if x is not None:
            if x.text and x.text.strip():
                return x.text.strip()
            href = x.get("href")
            if href:
                return href
    return ""


def parse_date(s):
    if not s:
        return datetime.now(timezone.utc)
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return datetime.now(timezone.utc)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def clean(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:180]


def tags_for(title):
    t = title.lower()
    return [k for k, rx in TAGS.items() if re.search(rx, t)]


def refresh_news():
    items = []
    atom = "{http://www.w3.org/2005/Atom}"
    for source, url in NEWS_FEEDS:
        try:
            root = ET.fromstring(fetch(url))
        except Exception as ex:  # noqa: BLE001
            print("news skip %s: %s" % (source, ex), file=sys.stderr)
            continue
        entries = root.findall(".//item") or root.findall(".//%sentry" % atom)
        for it in entries[:25]:
            title = clean(text(it, "title", atom + "title"))
            link = text(it, "link", atom + "link")
            if not title or not link.startswith("http"):
                continue
            if source in FILTERED and not MOBILE_HINT.search(title):
                continue
            d = parse_date(text(it, "pubDate", atom + "published", atom + "updated", "{http://purl.org/dc/elements/1.1/}date"))
            items.append({"title": title, "link": link, "source": source, "date": d.strftime("%Y-%m-%dT%H:%M:%SZ"), "tags": tags_for(title)})
    seen, out = set(), []
    for n in sorted(items, key=lambda x: x["date"], reverse=True):
        key = re.sub(r"\W+", "", n["title"].lower())[:70]
        if key in seen:
            continue
        seen.add(key)
        out.append(n)
    return out[:80]


def refresh_videos(channels):
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    vids, alive = [], []
    for ch in channels:
        try:
            root = ET.fromstring(fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + ch["id"]))
        except Exception as ex:  # noqa: BLE001
            print("video skip %s: %s" % (ch["name"], ex), file=sys.stderr)
            continue
        alive.append(ch)
        for en in root.findall("a:entry", ns)[:4]:
            vid = en.findtext("yt:videoId", default="", namespaces=ns)
            title = clean(en.findtext("a:title", default="", namespaces=ns))
            pub = en.findtext("a:published", default="", namespaces=ns)
            link = en.find("a:link", ns)
            href = link.get("href", "") if link is not None else ""
            if not vid or "/shorts/" in href:
                continue
            vids.append({"id": vid, "title": title, "channel": ch["name"], "published": pub})
    uniq = {}
    for v in vids:
        uniq.setdefault(v["id"], v)
    vids = sorted(uniq.values(), key=lambda v: v["published"], reverse=True)
    # Keep the newest video from each channel first, then fill by date.
    first, rest, used = [], [], set()
    for v in vids:
        (rest if v["channel"] in used else first).append(v)
        used.add(v["channel"])
    return (first + rest)[:18], alive


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    news_path, vid_path = DATA / "news.json", DATA / "videos.json"
    news_old = json.loads(news_path.read_text())
    vids_old = json.loads(vid_path.read_text())

    news = refresh_news()
    changed = False
    if news and [n["link"] for n in news] != [n["link"] for n in news_old.get("items", [])]:
        news_path.write_text(json.dumps({"updated": now, "items": news}, indent=1, ensure_ascii=False) + "\n")
        changed = True

    vids, alive = refresh_videos(vids_old["channels"])
    if vids and [v["id"] for v in vids] != [v["id"] for v in vids_old.get("videos", [])]:
        vids_old["videos"] = vids
        vids_old["updated"] = now
        if alive:
            vids_old["channels"] = alive
        vid_path.write_text(json.dumps(vids_old, indent=1, ensure_ascii=False) + "\n")
        changed = True

    if changed:
        n = json.loads(news_path.read_text())
        v = json.loads(vid_path.read_text())
        (DATA / "meta.json").write_text(json.dumps({"lastUpdated": now, "newsCount": len(n["items"]), "videoCount": len(v["videos"])}, indent=1) + "\n")
    print("refresh: changed=%s news=%d videos=%d" % (changed, len(news), len(vids)))


if __name__ == "__main__":
    main()
