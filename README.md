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

## Change it

Edit the data at the top of `tools/site-src/build.py` (names, dates, blurbs) or `styles.css`, then run:

```bash
python3 tools/site-src/build.py
```

That rewrites `docs/index.html`. After an upload, paste the exact video link into `EPISODE_LINKS` or `FILM_LINKS` in `build.py` and rebuild; until then each button opens the channel's Shorts tab or channel page.
