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

- **A release is late or not going out:** add `"CODE:lang": "note"` to `DELAYED` in `build.py` (for example `"S01E01:hi": "Hindi edition coming soon"`), rebuild and publish. It then shows as "coming soon" instead of "out now". Delete the entry once the upload is live.
- **Preview any moment:** add `?now=2026-11-14T20:00:00%2B05:30` to the page address.
- It follows the schedule, not YouTube: it cannot know whether an upload really happened.

## Change it

Edit the data at the top of `tools/site-src/build.py` (names, dates, blurbs) or `styles.css`, then run:

```bash
python3 tools/site-src/build.py
```

That rewrites `docs/index.html`. After an upload, paste the exact video link into `EPISODE_LINKS` or `FILM_LINKS` in `build.py` and rebuild; until then each button opens the channel's Shorts tab or channel page.
