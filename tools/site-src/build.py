#!/usr/bin/env python3
"""Builds index.html for Spark VertoByte and its series:
- Grow Slow (Patience, Humility & Habits)
- MS Dhoni: Moments That Made a Champion
- Before the Spark: How Visionary Builders Began

Reflects only actually uploaded videos across YouTube and Instagram
without speculative upcoming schedules or fixed clock times.

Output: docs/index.html and docs/.nojekyll.
"""
import glob
import json
import os
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "..", "docs"))
CSS = open(os.path.join(HERE, "styles.css"), encoding="utf-8").read()
JS = open(os.path.join(HERE, "app.js"), encoding="utf-8").read()

# Channel and profile links
YT_HI = "https://www.youtube.com/@SparkVertoByte"
YT_EN = "https://www.youtube.com/@SparkVertoByteEnglish"
IG_HI = "https://www.instagram.com/SparkVertoByte"
IG_EN = "https://www.instagram.com/SparkVertoByteEnglish"

# Founder profile and the public address (the social preview needs an absolute image URL)
SITE_URL = "https://vertobyte.com/"
LINKEDIN_URL = "https://www.linkedin.com/in/vishaldhimanai/"
FOUNDER_NAME = "Vishal Dhiman"

# Exact uploaded episode video URLs verified from channels
EPISODE_LINKS = {
    # Grow Slow Series
    "S01E01": {
        "en": "https://www.youtube.com/shorts/zcYEEak5BeQ",
        "hi": "https://www.youtube.com/shorts/8AbT_DuEwq0",
        "ig_en": "https://www.instagram.com/sparkvertobyteenglish/reel/DfkH4fKivNk/",
        "ig_hi": "https://www.instagram.com/sparkvertobyte/reel/DfkIIwAtUfC/",
    },
    "S01E02": {
        "en": "https://www.youtube.com/shorts/ZqX9d1jIJVA",
        "hi": "https://www.youtube.com/shorts/eZi4schxm68",
    },
    "S01E03": {
        "en": "https://www.youtube.com/shorts/vuu1qcHiNwo",
        "hi": "https://www.youtube.com/shorts/n0gAFDd9QSI",
    },
    "S01E04": {
        "en": "https://www.youtube.com/shorts/gbjwJ01vsBE",
        "hi": "https://www.youtube.com/shorts/szdEtMT0DGk",
    },
    "S01E05": {
        "en": "https://www.youtube.com/shorts/1Ps-0ImUfvk",
        "hi": "https://www.youtube.com/shorts/JyapxrVS808",
    },
    "S01E06": {
        "en": "https://www.youtube.com/shorts/EwmvxKNl5_0",
        "hi": "https://www.youtube.com/shorts/yQzr2Jh0um0",
    },
    "S01E07": {
        "en": "https://www.youtube.com/shorts/U7L5je2fb5Q",
        "hi": "https://www.youtube.com/shorts/ej76-FeVwow",
    },
    "S01E08": {
        "en": "https://www.youtube.com/shorts/RVpatEd-0xI",
        "hi": "https://www.youtube.com/shorts/RdU-vqXrDGo",
    },
    "S02E01": {
        "en": "https://www.youtube.com/shorts/8NoSVI-2UhE",
        "hi": "https://www.youtube.com/shorts/1TZi9CbPMLc",
    },
    "S02E02": {
        "en": "https://www.youtube.com/shorts/Jio-EGhliok",
        "hi": "https://www.youtube.com/shorts/WU5ttlX2NdQ",
    },
}

# Grow Slow uploaded episodes in reverse chronological order
UPLOADED_EPS = [
    dict(
        code="S02E02",
        season=2,
        ep=2,
        name="Count the Blossoms",
        season_name="When the Fruit Comes",
        desc="Staying present and grounded when initial signs of success and growth appear.",
    ),
    dict(
        code="S02E01",
        season=2,
        ep=1,
        name="The Pumpkin Next Door",
        season_name="When the Fruit Comes",
        desc="The comparison trap: why measuring your slow growth against fast blooms leads astray.",
    ),
    dict(
        code="S01E08",
        season=1,
        ep=8,
        name="Pull Them Small",
        season_name="Before the First Leaf",
        desc="Season 1 finale: tackling bad habits, doubts, and weeds while they are still small.",
    ),
    dict(
        code="S01E07",
        season=1,
        ep=7,
        name="Stop Digging",
        season_name="Before the First Leaf",
        desc="Trusting the invisible work under the soil instead of constantly digging to check.",
    ),
    dict(
        code="S01E06",
        season=1,
        ep=6,
        name="Find Your Light",
        season_name="Before the First Leaf",
        desc="Reaching toward whatever sunlight is available, even when surrounded by shade.",
    ),
    dict(
        code="S01E05",
        season=1,
        ep=5,
        name="Ten Seeds",
        season_name="Before the First Leaf",
        desc="Planting multiple efforts and embracing quiet compounding over time.",
    ),
    dict(
        code="S01E04",
        season=1,
        ep=4,
        name="A Cup a Day",
        season_name="Before the First Leaf",
        desc="The compounding power of small daily hydration versus erratic floods of effort.",
    ),
    dict(
        code="S01E03",
        season=1,
        ep=3,
        name="Her Little Seed",
        season_name="Before the First Leaf",
        desc="Protecting quiet beginnings and having faith before anyone else sees results.",
    ),
    dict(
        code="S01E02",
        season=1,
        ep=2,
        name="Deep Roots",
        season_name="Before the First Leaf",
        desc="Building anchor strength in the dark soil so you can withstand future winds.",
    ),
    dict(
        code="S01E01",
        season=1,
        ep=1,
        name="One Small Step",
        season_name="Before the First Leaf",
        desc="The series premiere: starting the journey with dry soil, one seed, and a single drop.",
    ),
]

# Grow Slow Seasons
SEASONS = [
    dict(
        n=1,
        name="Before the First Leaf",
        theme="Patience",
        status="Complete (8 Episodes)",
        phrase="He Kept Watering. Nothing Grew.",
        blurb="Eight tiny stories for anyone who is doing the work before anyone can see it working. The complete first arc is out now in Hindi and English.",
        eps=[
            "One Small Step",
            "Deep Roots",
            "Her Little Seed",
            "A Cup a Day",
            "Ten Seeds",
            "Find Your Light",
            "Stop Digging",
            "Pull Them Small",
        ],
    ),
    dict(
        n=2,
        name="When the Fruit Comes",
        theme="Humility",
        status="In Progress (2 Episodes Released)",
        phrase="The Tree Finally Bloomed. He Barely Looked.",
        blurb="Stories about what comes after the wait: the first flowers, the first fruit and staying grounded. Season 2 is currently releasing.",
        eps=[
            "The Pumpkin Next Door",
            "Count the Blossoms",
        ],
    ),
]

# MS Dhoni Series details
DHONI_SERIES = dict(
    title="MS Dhoni: Moments That Made a Champion",
    tagline="The small moments that made a champion, one takeaway per story.",
    tagline_hi="वो छोटे पल जिन्होंने एक champion बनाया, हर कहानी में एक सीख।",
    playlist_hi="https://www.youtube.com/playlist?list=PLef4XhWJG7lM",
    eps=[
        dict(
            code="S01E01",
            title="The Boy in Goal",
            title_hi="The Boy in Goal",
            yt_hi="https://www.youtube.com/shorts/cBatA1_mPsM",
            yt_en="https://www.youtube.com/shorts/VT-PbNn6ddg",
            thumb="https://i.ytimg.com/vi/VT-PbNn6ddg/hqdefault.jpg",
            desc="Before MS Dhoni was a wicketkeeper, he was a football goalkeeper at his school in Ranchi. His coach saw him diving between the posts and asked him to try wicketkeeping. The reflexes were already there—they just needed the right pitch.",
            quote="“Sometimes you don’t lack skill; you just need to change the field.”",
            quote_hi="“कभी-कभी आपकी skill कम नहीं होती, बस मैदान बदलना पड़ता है।”",
        )
    ],
)

# Before the Spark Series details
BUILDERS_SERIES = dict(
    title="Before the Spark",
    tagline="How well-known builders began.",
    tagline_hi="मशहूर लोगों ने शुरुआत कैसे की।",
    eps=[
        dict(
            code="S01E01",
            title="The Best Dishwasher",
            subject="Jensen Huang (Nvidia)",
            yt_hi="https://www.youtube.com/shorts/rLale_Vs_kM",
            yt_en="https://www.youtube.com/shorts/DllJvINZQf8",
            thumb="https://i.ytimg.com/vi/DllJvINZQf8/hqdefault.jpg",
            desc="At 15, years before co-founding Nvidia, Jensen Huang washed dishes and cleaned tables at Denny's. He resolved to be the best dishwasher they ever had, learning that greatness starts with total dedication to humble tasks.",
            quote="“You cannot pick your tasks, but you can always pick your dedication.”",
            quote_hi="Nvidia से पहले Jensen Huang ने Denny’s में बर्तन धोए।",
        )
    ],
)

ICONS = {
    "shorts": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 9.5l3 2-3 2z" fill="currentColor"/></svg>',
    "film": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M10 9.5l5 2.5-5 2.5z" fill="currentColor"/></svg>',
    "forest": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l5 7h-3l4 6H6l4-6H7z"/><path d="M12 16v5"/></svg>',
    "trophy": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H8v4h8v-4h-1c-.55 0-1-.45-1-1v-2.34"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>',
    "spark": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M4.93 19.07l14.14-14.14"/></svg>',
    "ai": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>',
    "linkedin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>',
}


def logo_picture(cls=""):
    return (
        '<picture><source media="(prefers-color-scheme: dark)" srcset="assets/logos/spark-by-vertobyte-final-dark.svg">'
        f'<img src="assets/logos/spark-by-vertobyte-final.svg" alt="Spark VertoByte" width="562" height="216" {cls}></picture>'
    )


def thumb(code):
    hits = sorted(glob.glob(os.path.join(SITE, "assets", "thumbs", code.lower() + "-*.webp")))
    if not hits:
        raise SystemExit(f"missing thumbnail for {code}")
    return "assets/thumbs/" + os.path.basename(hits[0])


def ep_url(code, lang):
    """Direct YouTube Short URL, or channel shorts feed if unmapped."""
    return EPISODE_LINKS.get(code, {}).get(lang) or (YT_EN if lang == "en" else YT_HI) + "/shorts"


def ig_url(code, lang):
    """Direct Instagram Reel URL, or channel profile if unmapped."""
    return EPISODE_LINKS.get(code, {}).get("ig_" + lang) or (IG_EN if lang == "en" else IG_HI)


def ep_links(code):
    """YouTube and Instagram buttons for both languages of an episode."""
    rows = []
    for lang, label, name in (("en", "English", "English"), ("hi", "हिंदी", "Hindi")):
        yt, ig = ep_url(code, lang), ig_url(code, lang)
        lg = ' lang="hi"' if lang == "hi" else ""
        rows.append(
            f'<div class="lk-row"><span class="lk-l"{lg}>{label}</span>'
            f'<a href="{yt}" target="_blank" rel="noopener" aria-label="Watch {code} in {name} on YouTube">YouTube</a>'
            f'<a href="{ig}" target="_blank" rel="noopener" aria-label="Watch {code} in {name} on Instagram">Instagram</a></div>'
        )
    return '<div class="links by-lang">' + "".join(rows) + '</div>'


def featured_release_html():
    """Hero card highlighting the latest release (S02E02)."""
    latest = UPLOADED_EPS[0]
    code = latest["code"]
    img = thumb(code)
    yt_en = ep_url(code, "en")
    yt_hi = ep_url(code, "hi")
    ig_en = ig_url(code, "en")
    return (
        f'<article class="featured-card">'
        f'<div class="pic"><img src="{img}" alt="Scene from {esc(latest["name"])}" loading="lazy" width="720" height="405">'
        f'<span class="featured-badge"><span class="live-dot"></span>Latest Release · {code}</span></div>'
        f'<div class="featured-body">'
        f'<span class="kicker">Grow Slow · Season {latest["season"]} · {esc(latest["season_name"])}</span>'
        f'<h3>{esc(latest["name"])}</h3>'
        f'<p class="sub">Grow Slow {code}</p>'
        f'<p>{esc(latest["desc"])}</p>'
        f'<div class="links">'
        f'<a class="btn btn-solid btn-sm" href="{yt_en}" target="_blank" rel="noopener">Watch in English on YouTube</a>'
        f'<a class="btn btn-outline btn-sm" href="{yt_hi}" target="_blank" rel="noopener" lang="hi">हिंदी में देखें</a>'
        f'<a class="btn btn-outline btn-sm" href="{ig_en}" target="_blank" rel="noopener">Instagram</a>'
        f'</div>'
        f'</div>'
        f'</article>'
    )


def episodes_grid_html():
    """Grid of all 10 uploaded Grow Slow episodes in reverse chronological order."""
    cards = []
    for item in UPLOADED_EPS:
        code = item["code"]
        img = thumb(code)
        cards.append(
            f'<article class="ep-card" data-season="{item["season"]}" data-code="{code}">'
            f'<div class="ep-pic">'
            f'<img src="{img}" alt="Scene from {esc(item["name"])}" loading="lazy" width="720" height="405">'
            f'<span class="ep-badge">{code}</span>'
            f'</div>'
            f'<div class="ep-card-body">'
            f'<div class="ep-meta">'
            f'<span class="ep-code">Season {item["season"]} · Episode {item["ep"]}</span>'
            f'<span class="ep-live-tag"><span class="live-dot"></span>Out Now</span>'
            f'</div>'
            f'<h4>{esc(item["name"])}</h4>'
            f'<p class="ep-season-tag">{esc(item["desc"])}</p>'
            f'{ep_links(code)}'
            f'</div>'
            f'</article>'
        )
    return '<div class="rel-grid all-eps">' + "".join(cards) + '</div>'


def seasons_html():
    """Seasons section showcasing Season 1 (complete) and Season 2 (in progress)."""
    tabs = ['<div class="tabs" role="tablist" aria-label="Seasons">']
    for s in SEASONS:
        sel = "true" if s["n"] == 1 else "false"
        tabs.append(
            f'<button role="tab" id="tab-{s["n"]}" aria-controls="season-{s["n"]}" '
            f'aria-selected="{sel}" data-season="{s["n"]}" tabindex="{0 if s["n"] == 1 else -1}">'
            f'Season {s["n"]}<small>{esc(s["theme"])}</small></button>'
        )
    tabs.append("</div>")

    panels = []
    for s in SEASONS:
        cards = []
        for i, name in enumerate(s["eps"]):
            code = f"S{s['n']:02d}E{i + 1:02d}"
            cards.append(
                f'<article class="ep" data-code="{code}">'
                f'<img src="{thumb(code)}" alt="Scene from {esc(name)}" loading="lazy" width="720" height="405">'
                f'<div class="body"><div class="code">{code}</div><h4>{esc(name)}</h4>'
                f'<div class="when">Hindi and English editions</div>{ep_links(code)}</div></article>'
            )

        note_html = ""
        if s["n"] == 2:
            note_html = (
                '<div class="season-note">'
                '<span class="live-dot"></span>'
                '<span><b>Season 2 in progress:</b> Episodes 1 and 2 are released now in Hindi and English. '
                'Subsequent chapters will be released as production finishes.</span>'
                '</div>'
            )

        panels.append(
            f'<section class="panel" id="season-{s["n"]}" role="tabpanel" aria-labelledby="tab-{s["n"]}" data-season="{s["n"]}">'
            f'<div class="film-card"><div class="pic"><img src="assets/film/s0{s["n"]}.webp" alt="Artwork for Season {s["n"]}" loading="lazy" width="1280" height="720">'
            f'<span class="badge">{esc(s["status"])}</span></div>'
            f'<div class="film-body"><span class="kicker">Season {s["n"]} · {esc(s["theme"])}</span>'
            f'<h3>{esc(s["phrase"])}</h3><p class="sub">Grow Slow Season {s["n"]}: {esc(s["name"])}</p>'
            f'<p>{esc(s["blurb"])}</p>'
            f'<div class="meta"><span class="chip">{len(s["eps"])} chapters uploaded</span><span class="chip">Hindi &amp; English</span></div>'
            f'</div></div>'
            f'{note_html}'
            f'<div class="eps">{"".join(cards)}</div></section>'
        )

    return "\n".join(tabs) + "\n" + "\n".join(panels)


def dhoni_section_html():
    """Dedicated section for MS Dhoni series."""
    ep = DHONI_SERIES["eps"][0]
    return f"""<section class="block" id="dhoni"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Champions Series · Season 1</span>
    <h2>{esc(DHONI_SERIES["title"])}</h2>
    <p class="tagline-hi" lang="hi" style="margin-top:4px">{esc(DHONI_SERIES["tagline_hi"])}</p>
    <p>{esc(DHONI_SERIES["tagline"])}</p>
  </div>

  <article class="featured-card">
    <div class="pic">
      <img src="{ep["thumb"]}" alt="Scene from {esc(ep["title"])}" loading="lazy" width="720" height="405">
      <span class="featured-badge"><span class="live-dot"></span>Out Now · Season 1 Episode 1</span>
    </div>
    <div class="featured-body">
      <span class="kicker">MS Dhoni · Season 1</span>
      <h3>{esc(ep["title"])}</h3>
      <p class="sub">MS Dhoni · {ep["code"]}</p>
      <p>{esc(ep["desc"])}</p>
      <div class="quote-box">
        {esc(ep["quote"])}
        <div class="quote-box-hi" lang="hi">{esc(ep["quote_hi"])}</div>
      </div>
      <div class="links">
        <a class="btn btn-solid btn-sm" href="{ep["yt_en"]}" target="_blank" rel="noopener">Watch in English on YouTube</a>
        <a class="btn btn-outline btn-sm" href="{ep["yt_hi"]}" target="_blank" rel="noopener" lang="hi">हिंदी में देखें (YouTube)</a>
        <a class="btn btn-outline btn-sm" href="{DHONI_SERIES["playlist_hi"]}" target="_blank" rel="noopener">View Full Playlist</a>
        <a class="btn btn-outline btn-sm" href="{IG_HI}" target="_blank" rel="noopener">Instagram</a>
      </div>
    </div>
  </article>
</div></section>"""


def builders_section_html():
    """Dedicated section for Before the Spark series."""
    ep = BUILDERS_SERIES["eps"][0]
    return f"""<section class="block" id="builders"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Origin Stories · Season 1</span>
    <h2>{esc(BUILDERS_SERIES["title"])}</h2>
    <p class="tagline-hi" lang="hi" style="margin-top:4px">{esc(BUILDERS_SERIES["tagline_hi"])}</p>
    <p>{esc(BUILDERS_SERIES["tagline"])}</p>
  </div>

  <article class="featured-card">
    <div class="pic">
      <img src="{ep["thumb"]}" alt="Scene from {esc(ep["title"])}" loading="lazy" width="720" height="405">
      <span class="featured-badge"><span class="live-dot"></span>Out Now · Season 1 Episode 1</span>
    </div>
    <div class="featured-body">
      <span class="kicker">Before the Spark · {esc(ep["subject"])}</span>
      <h3>{esc(ep["title"])}</h3>
      <p class="sub">Before the Spark · {ep["code"]}</p>
      <p>{esc(ep["desc"])}</p>
      <div class="quote-box">
        {esc(ep["quote"])}
        <div class="quote-box-hi" lang="hi">{esc(ep["quote_hi"])}</div>
      </div>
      <div class="links">
        <a class="btn btn-solid btn-sm" href="{ep["yt_en"]}" target="_blank" rel="noopener">Watch in English on YouTube</a>
        <a class="btn btn-outline btn-sm" href="{ep["yt_hi"]}" target="_blank" rel="noopener" lang="hi">हिंदी में देखें (YouTube)</a>
        <a class="btn btn-outline btn-sm" href="{IG_HI}" target="_blank" rel="noopener">Instagram</a>
      </div>
    </div>
  </article>
</div></section>"""


def founder_section_html():
    return f"""<section class="block" id="founder"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Behind VertoByte</span>
    <h2>An independent venture, built in the open</h2>
    <p>VertoByte is a creative-technology venture started in 2026. Spark VertoByte is its first product.</p>
  </div>
  <article class="card founder">
    <div class="founder-id">
      <span class="monogram" aria-hidden="true">VD</span>
      <div>
        <h3>{esc(FOUNDER_NAME)}</h3>
        <p class="role">Founder, VertoByte</p>
        <p class="where">India</p>
      </div>
    </div>
    <div class="founder-body">
      <p>{esc(FOUNDER_NAME)} is a software and applied-AI engineer with more than seven years of experience building and leading production systems. He started VertoByte to practise the same discipline in public: take each story from script to storyboard, pictures, narration and upload, in Hindi and English, and say plainly which parts are made with AI.</p>
      <ul class="founder-facts">
        <li>Three original series: Grow Slow, MS Dhoni and Before the Spark.</li>
        <li>Every story is produced natively in Hindi and English.</li>
        <li>AI-generated pictures and narration are labelled on every upload.</li>
      </ul>
      <div class="founder-actions">
        <a class="btn btn-solid" href="{LINKEDIN_URL}" target="_blank" rel="noopener me">{ICONS["linkedin"]}<span>Connect on LinkedIn</span></a>
        <a class="btn btn-outline" href="#watch">Watch the stories</a>
      </div>
    </div>
  </article>
</div></section>"""


FAQ = [
    (
        "Who makes Spark VertoByte?",
        f"Spark VertoByte is the first product of VertoByte, an independent creative-technology venture founded by {FOUNDER_NAME} in 2026. "
        "You can find the founder on LinkedIn from the Behind VertoByte section on this page.",
    ),
    (
        "What series does Spark VertoByte produce?",
        "Spark VertoByte produces three complementary short-story series: 'Grow Slow' (lessons on patience, humility, and compounding habits), "
        "'MS Dhoni: Moments That Made a Champion' (defining early decisions that forged a champion, one takeaway per story), and "
        "'Before the Spark' (how iconic founders and leaders began from humble work).",
    ),
    (
        "Where is the MS Dhoni series info and where can I watch it?",
        "The MS Dhoni series focuses on the small, pivotal moments that made Mahendra Singh Dhoni a champion. Season 1 Episode 1 ('The Boy in Goal') "
        "is streaming now in Hindi on Spark VertoByte and in English on Spark VertoByte English, with direct links right here on this page.",
    ),
    (
        "When does a new video go out?",
        "Video upload times are not fixed to a rigid clock or calendar schedule. New episodes are released "
        "as soon as animation and voiceovers are finished. Subscribe on YouTube and follow on Instagram to get notified "
        "instantly whenever a new story drops.",
    ),
    (
        "Do I have to watch in order?",
        "No. Every story stands alone as an under-60-second reflection. However, stories within the same season build on each other, "
        "so exploring playlists from Season 1 Episode 1 offers the richest experience.",
    ),
    (
        "Which language should I watch?",
        "All episodes are produced in both Hindi and English. Watch in Hindi on Spark VertoByte and in English "
        "on Spark VertoByte English. Both versions feature native voiceovers and captions.",
    ),
    (
        "Is it made with AI?",
        "Yes. The pictures and narration are created with AI tools, and every upload carries the "
        "AI-generated label on YouTube and Instagram. This is an independent channel.",
    ),
]


def page():
    watch = [
        (
            "YouTube",
            "Spark VertoByte",
            "@SparkVertoByte",
            "Hindi Shorts for Grow Slow, MS Dhoni, and Before the Spark with Devanagari captions.",
            YT_HI,
            YT_HI + "?sub_confirmation=1",
        ),
        (
            "YouTube",
            "Spark VertoByte English",
            "@SparkVertoByteEnglish",
            "English Shorts with English narration and captions across all series.",
            YT_EN,
            YT_EN + "?sub_confirmation=1",
        ),
        (
            "Instagram",
            "Spark VertoByte",
            "@SparkVertoByte",
            "Hindi Reels released alongside the YouTube Shorts.",
            IG_HI,
            None,
        ),
        (
            "Instagram",
            "Spark VertoByte English",
            "@SparkVertoByteEnglish",
            "English Reels released alongside the YouTube Shorts.",
            IG_EN,
            None,
        ),
    ]

    watch_html = "".join(
        f'<article class="card channel"><span class="plat">{p}</span><h3>{esc(n)}</h3><span class="handle">{h}</span><p class="what">{esc(w)}</p>'
        f'<div class="actions"><a class="btn btn-solid btn-sm" href="{u}" target="_blank" rel="noopener">Open on {p}</a>'
        + (f'<a class="btn btn-outline btn-sm" href="{sub}" target="_blank" rel="noopener">Subscribe</a>' if sub else '')
        + '</div></article>'
        for p, n, h, w, u, sub in watch
    )

    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)

    # Structured data: tells search engines who runs the venture and where its profiles are.
    jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "VertoByte",
            "alternateName": "Spark VertoByte",
            "url": SITE_URL,
            "description": "Independent creative-technology venture publishing short animated stories in Hindi and English.",
            "founder": {
                "@type": "Person",
                "name": FOUNDER_NAME,
                "jobTitle": "Founder",
                "sameAs": [LINKEDIN_URL],
            },
            "sameAs": [YT_HI, YT_EN, IG_HI, IG_EN],
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Spark VertoByte | Grow Slow, MS Dhoni &amp; Before the Spark</title>
<meta name="description" content="Little stories about big habits, pivotal moments, and quiet dedication. Watch Grow Slow, MS Dhoni, and Before the Spark in Hindi and English.">
<meta name="theme-color" content="#163a2d">
<meta property="og:title" content="Spark VertoByte | Little stories about big habits">
<meta property="og:description" content="Short animated stories: Grow Slow, MS Dhoni, and Before the Spark in Hindi and English.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spark VertoByte">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A child resting under a large tree at sunset, from the Grow Slow series">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE_URL}">
<link rel="icon" href="assets/logos/spark-mark-final.svg" type="image/svg+xml">
<script type="application/ld+json">{jsonld}</script>
<style>
{CSS}
</style>
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="brand" href="#top" aria-label="Spark VertoByte, home">{logo_picture()}</a>
  <nav class="nav" aria-label="Sections">
    <a href="#grow-slow">Grow Slow</a><a href="#dhoni">MS Dhoni</a><a href="#builders">Before the Spark</a><a href="#about">About</a><a href="#founder">Founder</a><a href="#watch">Where to watch</a><a href="#faq">FAQ</a>
  </nav>
</div></header>

<main id="top">
<section class="hero"><div class="wrap">
  <span class="eyebrow">A VertoByte Story Universe · Hindi and English</span>
  <h1>Spark VertoByte</h1>
  <p class="tagline">Little stories about big habits, pivotal moments, and quiet dedication.</p>
  <p class="tagline-hi" lang="hi">बड़ी आदतों की छोटी कहानियाँ, एक मिनट से कम में।</p>
  <p class="lede">Short animated stories across three distinct series: <b>Grow Slow</b> (patience and compounding habits), <b>MS Dhoni</b> (the small moments that made a champion), and <b>Before the Spark</b> (how iconic innovators began). Watch all uploaded stories in Hindi and English.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="#grow-slow">Grow Slow Series</a>
    <a class="btn btn-ghost" href="#dhoni">MS Dhoni Series</a>
    <a class="btn btn-ghost" href="#builders">Before the Spark</a>
  </div>
</div></section>

<div class="stats"><div class="wrap"><ul>
  <li><b>12</b><span>stories uploaded across 3 series</span></li>
  <li><b>3</b><span>series: Grow Slow, MS Dhoni &amp; Before the Spark</span></li>
  <li><b>2</b><span>languages: Hindi and English for every story</span></li>
  <li><b>&lt; 60s</b><span>bite-sized animated format for reflection</span></li>
</ul></div></div>

<!-- GROW SLOW SECTION -->
<section class="block" id="grow-slow"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Series 1 · The Story So Far</span>
    <h2>Grow Slow: Released Episodes</h2>
    <p>Upload times are flexible; new stories arrive as each chapter is completed. Browse all 10 uploaded Grow Slow episodes below or filter by season.</p>
  </div>

  {featured_release_html()}

  <div class="filter-bar" role="toolbar" aria-label="Filter Grow Slow episodes by season">
    <button type="button" class="filter-pill active" data-filter="all" aria-pressed="true">All Episodes (10)</button>
    <button type="button" class="filter-pill" data-filter="2" aria-pressed="false">Season 2 (2)</button>
    <button type="button" class="filter-pill" data-filter="1" aria-pressed="false">Season 1 (8)</button>
  </div>

  {episodes_grid_html()}
</div></section>

<section class="block" id="seasons"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Grow Slow · Thematic Arcs</span>
    <h2>Grow Slow Seasons &amp; Storylines</h2>
    <p>Grow Slow explores character growth through distinct seasons. Explore the released arcs below.</p>
  </div>
  {seasons_html()}
</div></section>

<!-- MS DHONI SECTION -->
{dhoni_section_html()}

<!-- BEFORE THE SPARK SECTION -->
{builders_section_html()}

<section class="block" id="about"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">About the Format</span>
    <h2>Three promises, one mission</h2>
    <p>Created for thoughtful viewing wherever you are.</p>
  </div>
  <div class="glance">
    <article class="card"><div class="icon">{ICONS["shorts"]}</div><h3>Under 60 seconds</h3><p>Every story stands alone in under a minute on YouTube Shorts and Instagram Reels, crafted for quick daily reflection.</p></article>
    <article class="card"><div class="icon">{ICONS["forest"]}</div><h3>Two native languages</h3><p>Complete dual productions in Hindi and English, with tailored voice narration and native typography.</p></article>
    <article class="card"><div class="icon">{ICONS["trophy"]}</div><h3>Timeless takeaways</h3><p>From quiet patience in Grow Slow to champion mindset in MS Dhoni, every video delivers one memorable lesson.</p></article>
  </div>
</div></section>

{founder_section_html()}

<section class="block" id="watch"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Where to watch</span>
    <h2>Two channels, two languages</h2>
    <p>Watch and subscribe on YouTube, or follow on Instagram for instant notifications when new stories drop.</p>
  </div>
  <div class="channels">{watch_html}</div>
</div></section>

<section class="block" id="faq"><div class="wrap">
  <div class="ai-note">{ICONS["ai"]}<p><b>Made with AI, and we say so.</b> The pictures and the narration in our series are generated with AI tools, and every upload carries the AI-generated label. This is an independent channel not affiliated with any featured individuals.</p></div>
  <div class="section-head" style="margin-top:56px"><span class="eyebrow">Questions</span><h2>Good to know</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>
</main>

<footer class="site-footer"><div class="wrap">
  <div>{logo_picture().replace('<picture>', '<picture>').replace('final.svg', 'final-dark.svg')}<p>Spark VertoByte by VertoByte: Grow Slow, MS Dhoni, and Before the Spark. Little stories about big habits.</p></div>
  <ul>
    <li>YouTube · <a href="{YT_HI}" target="_blank" rel="noopener">@SparkVertoByte</a> · <a href="{YT_EN}" target="_blank" rel="noopener">@SparkVertoByteEnglish</a></li>
    <li>Instagram · <a href="{IG_HI}" target="_blank" rel="noopener">@SparkVertoByte</a> · <a href="{IG_EN}" target="_blank" rel="noopener">@SparkVertoByteEnglish</a></li>
    <li>Founder · <a href="{LINKEDIN_URL}" target="_blank" rel="noopener me">{esc(FOUNDER_NAME)} on LinkedIn</a></li>
    <li>Hindi and English · AI-generated pictures and voice</li>
  </ul>
  <p class="legal">© 2026 VertoByte. All uploaded episodes displayed. Upload times are flexible as new stories are completed.</p>
</div></footer>
<script>
{JS}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    html = page()
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    open(os.path.join(SITE, ".nojekyll"), "w").close()
    print(f"index.html successfully written ({len(html) // 1024} KB).")
