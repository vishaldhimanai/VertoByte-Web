# VertoByte Web

The public website for **Spark VertoByte** and its *Grow Slow* series: a static, HTML-only page at https://vertobyte.com/ that shows the weekly rhythm, every season and episode, and the day-by-day release calendar, with links to the YouTube channels and Instagram accounts.

## What is here

| Path | What it is |
| :--- | :--- |
| `docs/` | The published site: `index.html` (CSS and JavaScript inline), `assets/` (images, logos), `CNAME`, `.nojekyll`. GitHub Pages serves this folder. |
| `tools/site-src/` | The generator: `build.py` (data and page), `styles.css`, `app.js`. |

Everything else (the content plan, account setup, channel artwork and tools) is kept privately with the production repository, not here.

## Host

*Settings → Pages → Deploy from a branch → `production` → `/docs`*, with the custom domain `vertobyte.com` and *Enforce HTTPS* on. All paths are relative, so the site also works at `username.github.io/VertoByte-Web/`.

## Live release status

The "Today on Grow Slow" section compares the plan's release slots (in IST) with the visitor's clock, so it shows what is out, what goes out today and what comes next without a rebuild. It also marks the calendar days and episode cards. The slots come from `build.py` (`times_for`, `SLOTS`) and follow the weekly rhythm in the plan.

- **A release is late or not going out:** add `"CODE:lang": "note"` to `DELAYED` in `build.py` (for example `"S02E03:hi": "Hindi edition coming soon"`), rebuild and publish. It then shows as "coming soon" instead of "out now". Delete the entry once the upload is live.
- **A release went out at a different time from the plan:** add `"CODE": ("HH:MM", ["hi", "en"])` (IST) to `ACTUAL` in `build.py`. It replaces that episode's planned slots, so the status panel shows the real time. S01E01 went out in both languages at 8 PM IST on 10 November 2026.
- **Preview any moment:** add `?now=2026-11-14T20:00:00%2B05:30` to the page address.
- It follows the schedule, not YouTube: it cannot know whether an upload really happened.

## Change it

Edit the data at the top of `tools/site-src/build.py` (names, dates, blurbs) or `styles.css`, then run:

```bash
python3 tools/site-src/build.py
```

That rewrites `docs/index.html`. After an upload, paste the exact links into `EPISODE_LINKS` (`"en"` and `"hi"` for the YouTube Shorts, `"ig_en"` and `"ig_hi"` for the Instagram Reels) or `FILM_LINKS` (YouTube only) in `build.py` and rebuild. Every episode shows YouTube and Instagram buttons for both languages; until its links are recorded, each button opens the channel's Shorts tab or the Instagram profile.

## Phones

The page is built mobile first: no sideways scroll from 320 px up, buttons and links at least 44 px tall on touch screens, a section menu that scrolls sideways with a faded edge, and safe-area padding for notched phones. After a change, check it at 320, 375, 414 and 768 px wide.
