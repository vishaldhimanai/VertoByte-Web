#!/usr/bin/env python3
"""Builds index.html for the Grow Slow release-plan site.

Edit the data below (names, dates, blurbs), then run:  python3 build.py
Output: ../../docs/index.html with the CSS and JS inlined, so the site is HTML only and the docs/ folder
can be hosted as is (GitHub Pages, branch + /docs). No packages needed.
Thumbnails in docs/assets/thumbs/ are first-shot landscape artwork, one per episode,
named <code>-<slug>.webp (for example s01e01-one-small-step.webp).
"""
import glob
import os
from datetime import date, timedelta
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "..", "docs"))  # publishable folder: index.html, assets/, .nojekyll, CNAME
CSS = open(os.path.join(HERE, "styles.css"), encoding="utf-8").read()
JS = open(os.path.join(HERE, "app.js"), encoding="utf-8").read()
MONDAY0 = date(2026, 11, 9)  # Monday of launch week. Shorts start Tue 10 Nov 2026.

SEASONS = [
    dict(n=1, name="Before the First Leaf", theme="Patience", runtime="4:49",
         phrase="He Kept Watering. Nothing Grew.",
         blurb="Eight tiny stories for anyone who is doing the work before anyone can see it working.",
         eps=["One Small Step", "Deep Roots", "Her Little Seed", "A Cup a Day", "Ten Seeds", "Find Your Light", "Stop Digging", "Pull Them Small"]),
    dict(n=2, name="When the Fruit Comes", theme="Humility", runtime="5:01",
         phrase="The Tree Finally Bloomed. He Barely Looked.",
         blurb="Eight short stories about what comes after the wait: the first flowers, the first fruit and the first big offer.",
         eps=["The Pumpkin Next Door", "Count the Blossoms", "The Bees", "The First Fruit", "The Bowing Branch", "Market Apples", "Save Some Seeds", "The Offer"]),
    dict(n=3, name="Drought and Flood", theme="Resilience", runtime="4:19",
         phrase="Someone Was Snapping His Branches at Night",
         blurb="Eight short stories about setbacks: a fall, a drought, a flood and a visitor in the night.",
         eps=["The Fall", "Too Proud to Ask", "The Magic Powder", "The Dry Well", "The Broken Sapling", "The Fallen Giant", "The Night Visitor", "The Flood"]),
    dict(n=4, name="Many Hands", theme="Community", runtime="4:26",
         phrase="Who Stays When the Fruit Is Gone?",
         blurb="Eight short stories about people: new kids, promises, shared work and the friends who stay.",
         eps=["The New Kid", "Grow What You Love", "The Promise", "The Treehouse", "After the Fruit", "The Hardest Patch", "Careless Words", "Bend the Road"]),
    dict(n=5, name="Let the Light In", theme="Perspective", runtime="4:36",
         phrase="Some Blessings Arrive Looking Like Rain",
         blurb="Eight short stories about rest, letting go and doing good work that nobody notices.",
         eps=["The Resting Field", "The Pruning", "Rain on Kite Day", "The Fence", "Two Fruits", "No One Clapped", "Who Is It For?", "The Second Seed"]),
    dict(n=6, name="The Forest", theme="Legacy", runtime="4:32",
         phrase="Plant for People You’ll Never Meet",
         blurb="Eight short stories about growing up, growing old and passing the watering can on.",
         eps=["Roots in the City", "The Two-Fruit Tree", "The Student Again", "Enough", "Grandpa’s Chair", "Shade He’ll Never Sit In", "Pass the Can", "The Forest"]),
]
# Day offsets from the week's Monday for E01..E08. Week 1 starts on Tuesday, with E02 and E03 sharing Wednesday.
OFFSETS_WEEK1 = [1, 2, 2, 3, 4, 5, 6, 6]
OFFSETS = [0, 1, 2, 3, 4, 5, 6, 6]
FILM_OFFSET = 5  # Saturday night
PROMOS = 7  # countdown Shorts in the final week

# Channel and profile links. They work once the accounts exist with these handles.
YT_HI = "https://www.youtube.com/@SparkVertoByte"
YT_EN = "https://www.youtube.com/@SparkVertoByteEnglish"
IG_HI = "https://www.instagram.com/SparkVertoByte"
IG_EN = "https://www.instagram.com/SparkVertoByteEnglish"
# After an upload, paste the exact video link here and the matching button opens that video, e.g.
# EPISODE_LINKS = {"S01E01": {"en": "https://www.youtube.com/shorts/...", "hi": "https://www.youtube.com/shorts/..."}}
# FILM_LINKS = {1: "https://www.youtube.com/watch?v=...", "complete": "https://www.youtube.com/watch?v=..."}
EPISODE_LINKS = {}
FILM_LINKS = {}


def ep_links(code):
    en = EPISODE_LINKS.get(code, {}).get("en") or YT_EN + "/shorts"
    hi = EPISODE_LINKS.get(code, {}).get("hi") or YT_HI + "/shorts"
    return ('<div class="links">'
            f'<a href="{en}" target="_blank" rel="noopener" aria-label="Watch {code} in English on YouTube">Watch in English</a>'
            f'<a href="{hi}" target="_blank" rel="noopener" lang="hi" aria-label="Watch {code} in Hindi on YouTube">हिंदी में देखें</a></div>')


def film_link_html(key):
    url = FILM_LINKS.get(key) or YT_EN
    return f'<div class="meta"><a class="btn btn-primary btn-sm" href="{url}" target="_blank" rel="noopener">Watch the film on YouTube</a></div>'

def fmt(d, with_year=False):
    s = f"{d:%a} {d.day} {d:%b}"
    return s + (f" {d.year}" if with_year else "")

def thumb(code):
    hits = sorted(glob.glob(os.path.join(SITE, "assets", "thumbs", code.lower() + "-*.webp")))
    if not hits:
        raise SystemExit(f"missing thumbnail for {code}")
    return "assets/thumbs/" + os.path.basename(hits[0])

# ---- build the event map -------------------------------------------------
events = {}  # date -> list of dict
for s in SEASONS:
    monday = MONDAY0 + timedelta(days=7 * (s["n"] - 1))
    offs = OFFSETS_WEEK1 if s["n"] == 1 else OFFSETS
    s["monday"] = monday
    s["dates"] = []
    for i, name in enumerate(s["eps"]):
        d = monday + timedelta(days=offs[i])
        code = f"S{s['n']:02d}E{i + 1:02d}"
        s["dates"].append(d)
        events.setdefault(d, []).append(dict(kind="short", code=code, name=name, season=s["n"], img=thumb(code)))
    s["film"] = monday + timedelta(days=FILM_OFFSET)
    events.setdefault(s["film"], []).append(dict(kind="film", season=s["n"], label=f"Season {s['n']} film", runtime=s["runtime"], img=f"assets/film/s0{s['n']}.webp"))
week7 = MONDAY0 + timedelta(days=7 * 6)
FINALE = week7 + timedelta(days=FILM_OFFSET)
for i in range(PROMOS):
    events.setdefault(week7 + timedelta(days=i), []).append(dict(kind="promo", n=i + 1))
events.setdefault(FINALE, []).append(dict(kind="film", season=0, label="The complete series", runtime="27:43", img="assets/film/complete.webp"))

# ---- html helpers --------------------------------------------------------
ICONS = {
    "shorts": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 9.5l3 2-3 2z" fill="currentColor"/></svg>',
    "film": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M10 9.5l5 2.5-5 2.5z" fill="currentColor"/></svg>',
    "forest": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l5 7h-3l4 6H6l4-6H7z"/><path d="M12 16v5"/></svg>',
    "ai": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>',
}

def logo_picture(cls=""):
    return ('<picture><source media="(prefers-color-scheme: dark)" srcset="assets/logos/spark-by-vertobyte-final-dark.svg">'
            f'<img src="assets/logos/spark-by-vertobyte-final.svg" alt="Spark VertoByte" width="562" height="216" {cls}></picture>')

def ev_html(ev):
    if ev["kind"] == "short":
        label = f'{ev["code"]} {ev["name"]}'
        return (f'<a class="ev short" href="#seasons" data-goto-season="{ev["season"]}" title="{esc(label)}">'
                f'<img src="{ev["img"]}" alt="" loading="lazy" width="720" height="405">'
                f'<span class="tag">{ev["code"]}</span><span class="nm">{esc(ev["name"])}</span></a>')
    if ev["kind"] == "film":
        goto = f' href="#{"season-%d" % ev["season"] if ev["season"] else "finale"}"'
        data = f' data-goto-season="{ev["season"]}"' if ev["season"] else ""
        return (f'<a class="ev film"{goto}{data} title="{esc(ev["label"])}, {ev["runtime"]}, 7:00 PM IST">'
                f'<img src="{ev["img"]}" alt="" loading="lazy" width="1280" height="720">'
                f'<span class="tag">FILM · 7 PM</span><span class="nm">{esc(ev["label"])} · {ev["runtime"]}</span></a>')
    return f'<div class="ev promo"><b>Countdown</b><span>Short {ev["n"]} of {PROMOS}</span></div>'

# ---- calendar ------------------------------------------------------------
def calendar_html():
    out = ['<div class="cal-head" aria-hidden="true">' + "".join(f"<span>{d}</span>" for d in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")) + "</div>"]
    for w in range(7):
        monday = MONDAY0 + timedelta(days=7 * w)
        if w < 6:
            s = SEASONS[w]
            head = f'<h3>Week {w + 1}</h3><span>Season {s["n"]} · {esc(s["name"])} · film on {fmt(s["film"])}</span>'
        else:
            head = f'<h3>Week 7</h3><span>The complete series · film on {fmt(FINALE)}</span>'
        out.append(f'<div class="week-label">{head}</div><div class="week">')
        for i in range(7):
            d = monday + timedelta(days=i)
            evs = events.get(d, [])
            classes = "day" + (" has-film" if any(e["kind"] == "film" for e in evs) else "") + (" is-empty" if not evs else "")
            month = f" {d:%b}" if (d.day == 1 or i == 0 or d == MONDAY0) else f" {d:%b}"
            body = "".join(ev_html(e) for e in sorted(evs, key=lambda e: {"short": 0, "promo": 0, "film": 1}[e["kind"]])) if evs else '<span class="empty-note">Before launch</span>'
            out.append(f'<div class="{classes}"><div class="date"><span class="wd">{d:%a}</span><b>{d.day}</b><span>{d:%b}</span></div><div class="evs">{body}</div></div>')
        out.append("</div>")
    return "\n".join(out)

# ---- seasons -------------------------------------------------------------
def seasons_html():
    tabs = ['<div class="tabs" role="tablist" aria-label="Seasons">']
    for s in SEASONS:
        sel = "true" if s["n"] == 1 else "false"
        tabs.append(f'<button role="tab" id="tab-{s["n"]}" aria-controls="season-{s["n"]}" aria-selected="{sel}" data-season="{s["n"]}" tabindex="{0 if s["n"] == 1 else -1}">Season {s["n"]}<small>{esc(s["theme"])}</small></button>')
    tabs.append("</div>")
    panels = []
    for s in SEASONS:
        cards = []
        for i, name in enumerate(s["eps"]):
            code = f"S{s['n']:02d}E{i + 1:02d}"
            cards.append(
                f'<article class="ep"><img src="{thumb(code)}" alt="Scene from {esc(name)}" loading="lazy" width="720" height="405">'
                f'<div class="body"><div class="code">{code}</div><h4>{esc(name)}</h4>'
                f'<div class="when">{fmt(s["dates"][i])} · Hindi and English</div>{ep_links(code)}</div></article>')
        hindi = '<p class="note">Hindi editions of this season follow once their recordings are finished.</p>' if s["n"] >= 4 else ""
        panels.append(
            f'<section class="panel" id="season-{s["n"]}" role="tabpanel" aria-labelledby="tab-{s["n"]}" data-season="{s["n"]}">'
            f'<div class="film-card"><div class="pic"><img src="assets/film/s0{s["n"]}.webp" alt="Scene from Season {s["n"]}" loading="lazy" width="1280" height="720">'
            f'<span class="badge">Season film</span></div>'
            f'<div class="film-body"><span class="kicker">Season {s["n"]} · {esc(s["theme"])}</span>'
            f'<h3>{esc(s["phrase"])}</h3><p class="sub">Grow Slow Season {s["n"]}: {esc(s["name"])}</p>'
            f'<p>{esc(s["blurb"])}</p>'
            f'<div class="meta"><span class="chip">{fmt(s["film"], True)} · 7:00 PM IST</span><span class="chip">{s["runtime"]} · English</span><span class="chip">8 chapters</span></div>{film_link_html(s["n"])}</div></div>'
            f'<div class="eps">{"".join(cards)}</div>{hindi}</section>')
    return "\n".join(tabs) + "\n" + "\n".join(panels)

# ---- page ----------------------------------------------------------------
TZ_ROWS = [
    ("1:00 PM IST", "Hindi Shorts and Reels, Monday to Friday; both languages on Saturday and the first Sunday slot", ("1:00 PM", "11:30 AM", "3:30 PM", "7:30 AM", "2:30 AM")),
    ("7:00 PM IST", "English Shorts and Reels, Monday to Friday; the Saturday-night season film; the Sunday finale Short", ("7:00 PM", "5:30 PM", "9:30 PM", "1:30 PM", "8:30 AM")),
]

def rhythm_html():
    def day(name, slots, film=False):
        s = "".join(f'<div class="slot{" film" if f else ""}"><b>{esc(t)}</b>{esc(txt)}</div>' for t, txt, f in slots)
        return f'<div class="rh-day{" is-film" if film else ""}"><h4>{name}</h4>{s}</div>'
    wk = [("1:00 PM IST", "Episodes 1 to 5, one a day · Hindi", False), ("7:00 PM IST", "Episodes 1 to 5, one a day · English", False)]
    return '<div class="rhythm">' + "".join([
        day("Monday to Friday", wk),
        day("Saturday", [("1:00 PM IST", "Episode 6 · both languages", False), ("7:00 PM IST", "Season film · English", True)], film=True),
        day("Sunday", [("1:00 PM IST", "Episode 7 · both languages", False), ("7:00 PM IST", "Episode 8, the finale · both languages", False)]),
    ]) + "</div>"

def tz_html():
    head = "<tr><th>Slot</th><th>What goes out</th><th>India</th><th>Gulf</th><th>Singapore</th><th>UK</th><th>US East</th></tr>"
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{esc(b)}</td>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" for a, b, cells in TZ_ROWS)
    return f'<div class="tz"><table><thead>{head}</thead><tbody>{rows}</tbody></table></div>'

FAQ = [
    ("What is Grow Slow?", "A series of short animated stories about patience, humility, resilience, community and legacy. It begins with one boy and one seed in dry soil, and by the sixth season there is a whole forest."),
    ("Do I have to watch in order?", "No. Every story stands alone, and each season film collects its eight stories in one sitting. They do build on each other, so starting from Season 1 rewards you."),
    ("Which language should I watch?", "Shorts and Reels come in Hindi on Spark VertoByte and in English on Spark VertoByte English. The season films and the complete film are in English. Hindi editions of Seasons 4 to 6 will follow."),
    ("Is it made with AI?", "Yes. The pictures and the narration are created with AI tools, and every upload is marked as AI-generated."),
    ("When does a new episode go out?", "One episode a day from Monday to Friday, then episode 6 and the season film on Saturday and episodes 7 and 8 on Sunday. Times are in the table above."),
    ("Can the dates change?", "This is a plan, not a promise. Dates and times can move, and the channels always show the real schedule."),
]

def page():
    watch = [
        ("YouTube", "Spark VertoByte", "@SparkVertoByte", "Hindi Shorts, one a day, in Hindi with Devanagari captions.", YT_HI, YT_HI + "?sub_confirmation=1"),
        ("YouTube", "Spark VertoByte English", "@SparkVertoByteEnglish", "English Shorts, one a day, in English with English captions.", YT_EN, YT_EN + "?sub_confirmation=1"),
        ("Instagram", "Spark VertoByte", "@SparkVertoByte", "Hindi Reels for India, released alongside the Shorts.", IG_HI, None),
        ("Instagram", "Spark VertoByte English", "@SparkVertoByteEnglish", "English Reels for everyone else, released alongside the Shorts.", IG_EN, None),
    ]
    watch_html = "".join(
        f'<article class="card channel"><span class="plat">{p}</span><h3>{esc(n)}</h3><span class="handle">{h}</span><p class="what">{esc(w)}</p>'
        f'<div class="actions"><a class="btn btn-solid btn-sm" href="{u}" target="_blank" rel="noopener">Open on {p}</a>'
        + (f'<a class="btn btn-outline btn-sm" href="{sub}" target="_blank" rel="noopener">Subscribe</a>' if sub else '')
        + '</div></article>'
        for p, n, h, w, u, sub in watch)
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    last_sun = MONDAY0 + timedelta(days=7 * 7 - 1)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grow Slow: the release plan | Spark VertoByte</title>
<meta name="description" content="48 short animated stories in Hindi and English, six season films and one 27-minute finale, released from 10 November 2026. See the full plan.">
<meta name="theme-color" content="#163a2d">
<meta property="og:title" content="Grow Slow: the release plan">
<meta property="og:description" content="Little stories about big habits. 48 episodes, six season films and one 27-minute finale.">
<link rel="icon" href="assets/logos/spark-mark-final.svg" type="image/svg+xml">
<style>
{CSS}
</style>
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="brand" href="#top" aria-label="Spark VertoByte, home">{logo_picture()}</a>
  <nav class="nav" aria-label="Sections">
    <a href="#plan">The plan</a><a href="#rhythm">A week</a><a href="#seasons">Seasons</a><a href="#calendar">Calendar</a><a href="#finale">Finale</a><a href="#watch">Where to watch</a><a href="#faq">FAQ</a>
  </nav>
</div></header>

<main id="top">
<section class="hero"><div class="wrap">
  <span class="eyebrow">A VertoByte story series · Hindi and English</span>
  <h1>Grow Slow</h1>
  <p class="tagline">Little stories about big habits.</p>
  <p class="tagline-hi" lang="hi">बड़ी आदतों की छोटी कहानियाँ।</p>
  <p class="lede">Forty-eight short animated stories, six season films and one 27-minute finale, released over seven weeks from Tuesday 10 November 2026.</p>
  <div class="cta-row"><a class="btn btn-primary" href="{YT_EN}" target="_blank" rel="noopener">Watch in English on YouTube</a><a class="btn btn-ghost" href="{YT_HI}" target="_blank" rel="noopener" lang="hi">हिंदी में देखें</a><a class="btn btn-ghost" href="#calendar">See the release calendar</a></div>
</div></section>

<div class="stats"><div class="wrap"><ul>
  <li><b>48</b><span>episodes, each in Hindi and English</span></li>
  <li><b>6</b><span>season films, every Saturday night</span></li>
  <li><b>27:43</b><span>complete film on {fmt(FINALE)}</span></li>
  <li><b>7</b><span>weeks, {fmt(MONDAY0 + timedelta(days=1))} to {fmt(last_sun)}</span></li>
</ul></div></div>

<section class="block" id="plan"><div class="wrap">
  <div class="section-head"><span class="eyebrow">The plan at a glance</span><h2>Three ways to watch, one story</h2>
  <p>Every week follows the same pattern, so you always know what comes next and when.</p></div>
  <div class="glance">
    <article class="card"><div class="icon">{ICONS["shorts"]}</div><h3>A story every day</h3><p>One short episode a day on YouTube Shorts and Instagram Reels, in Hindi and in English. Each one stands alone in under a minute.</p></article>
    <article class="card"><div class="icon">{ICONS["film"]}</div><h3>A film every Saturday night</h3><p>At 7:00 PM IST each season arrives as one film: eight stories, about five minutes, with chapters so you can jump to your favourite.</p></article>
    <article class="card"><div class="icon">{ICONS["forest"]}</div><h3>One finale on {fmt(FINALE)}</h3><p>All 48 stories in a single 27-minute film, from one seed in dry soil to a whole forest.</p></article>
  </div>
</div></section>

<section class="block" id="rhythm"><div class="wrap">
  <div class="section-head"><span class="eyebrow">A week with Grow Slow</span><h2>The weekly rhythm</h2>
  <p>Monday to Friday bring one episode a day. Saturday is film night. Sunday closes the season with its last two stories.</p></div>
  {rhythm_html()}
  {tz_html()}
  <p class="fineprint">Times shown are for November and December 2026, with the US on Eastern Standard Time and the UK on GMT. The first week starts on Tuesday 10 November, so Wednesday 11 November carries two episodes.</p>
</div></section>

<section class="block" id="seasons"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Six seasons, one forest</span><h2>Every season, every episode</h2>
  <p>Each season is eight stories and a film. Pick a season to see its episodes and when they arrive.</p></div>
  {seasons_html()}
</div></section>

<section class="block" id="calendar"><div class="wrap">
  <div class="section-head"><span class="eyebrow">The release calendar</span><h2>Seven weeks, day by day</h2>
  <p>Every episode and film on its release day. Select a thumbnail to jump to its season.</p></div>
  <div class="legend"><span><i></i>Episode, Hindi and English</span><span><i class="film"></i>Season film, 7:00 PM IST</span><span><i class="promo"></i>Countdown Short</span></div>
  {calendar_html()}
</div></section>

<section class="block" id="finale"><div class="wrap">
  <div class="finale">
    <div class="copy"><span class="eyebrow" style="color:#ffd479">The grand finale · {fmt(FINALE, True)} · 7:00 PM IST</span>
    <h2>One Boy, One Seed, a Whole Forest</h2>
    <p>All 48 Grow Slow stories in one watch, from one seed in dry soil to a whole forest. Twenty-seven minutes, 48 chapters, and the whole story in order.</p>
    <p>The week before, seven countdown Shorts build up to the film.</p>
    <div class="meta"><span class="chip">27:43</span><span class="chip">English</span><span class="chip">48 chapters</span></div>{film_link_html("complete")}</div>
    <div class="pic"><img src="assets/film/complete.webp" alt="A green valley with a forest of trees at sunset" loading="lazy" width="1280" height="720"></div>
  </div>
</div></section>

<section class="block" id="watch"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where to watch</span><h2>Two channels, two languages</h2>
  <p>Hindi has its own home and so does English. The season films are in English and go out on YouTube.</p></div>
  <div class="channels">{watch_html}</div>
</div></section>

<section class="block" id="faq"><div class="wrap">
  <div class="ai-note">{ICONS["ai"]}<p><b>Made with AI, and we say so.</b> The pictures and the narration in Grow Slow are generated with AI tools, and every upload carries the AI-generated label.</p></div>
  <div class="section-head" style="margin-top:56px"><span class="eyebrow">Questions</span><h2>Good to know</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>
</main>

<footer class="site-footer"><div class="wrap">
  <div>{logo_picture().replace('<picture>', '<picture>').replace('final.svg', 'final-dark.svg')}<p>Grow Slow is a story series by Spark VertoByte, from VertoByte. Little stories about big habits.</p></div>
  <ul><li>YouTube · <a href="{YT_HI}" target="_blank" rel="noopener">@SparkVertoByte</a> · <a href="{YT_EN}" target="_blank" rel="noopener">@SparkVertoByteEnglish</a></li><li>Instagram · <a href="{IG_HI}" target="_blank" rel="noopener">@SparkVertoByte</a> · <a href="{IG_EN}" target="_blank" rel="noopener">@SparkVertoByteEnglish</a></li><li>Hindi and English · AI-generated pictures and voice</li></ul>
  <p class="legal">© 2026 VertoByte. This page shows the planned release schedule; dates and times may change.</p>
</div></footer>
<script>
{JS}
</script>
</body>
</html>
'''

if __name__ == "__main__":
    html = page()
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    open(os.path.join(SITE, ".nojekyll"), "w").close()  # GitHub Pages: serve files as they are
    n_ev = sum(len(v) for v in events.values())
    print(f"index.html written: {len(html) // 1024} KB, {n_ev} calendar tiles, finale {fmt(FINALE, True)}")
