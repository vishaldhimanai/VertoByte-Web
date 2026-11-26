# VertoByte Web

The public website for **Spark VertoByte** and its story series (**Grow Slow**, **MS Dhoni: Moments That Made a Champion**, and **Before the Spark**): a static, HTML-only page at https://vertobyte.com/ that showcases all released episodes and their story timelines, with links to the active Spark VertoByte accounts on YouTube and Instagram.

## What is here

| Path | What it is |
| :--- | :--- |
| `docs/` | The published site: `index.html` (CSS and JavaScript inline), `assets/` (images, logos), `CNAME`, `.nojekyll`. GitHub Pages serves this folder. |
| `tools/site-src/` | The generator: `build.py` (data and page), `styles.css`, `app.js`. |
| `wrangler.jsonc` | Tells Cloudflare's `npx wrangler deploy` to publish `docs/` as the Worker `vertobyte-web`. The name must match the Worker in the dashboard. |
| `docs/.assetsignore` | Keeps macOS `.DS_Store` files out of the Worker upload. |

Everything else (the content plan, account setup, channel artwork and tools) is kept privately with the production repository, not here.

## Host

`vertobyte.com`, `www.vertobyte.com` and `spark.vertobyte.com` are served by the Cloudflare Worker **`vertobyte-web`**, which holds a copy of `docs/` (see `wrangler.jsonc`). Pushing to GitHub updates the site only through Cloudflare's Git build: *Workers & Pages → vertobyte-web → Settings → Builds*, repository `VertoByte-Web`, production branch `production`, deploy command `npx wrangler deploy`. If that page says the project is disconnected from Git, no push reaches the site until it is reconnected (*Manage*, or *Disconnect* and connect the same repository again).

To deploy by hand from this folder (it signs in through your browser the first time):

```bash
npx wrangler login
npx wrangler deploy
```

GitHub Pages (*Settings → Pages → `production` → `/docs`*) also serves the same folder, but the custom domain does not go through it. All paths are relative, so the site also works at `username.github.io/VertoByte-Web/`.

## Released Series & Episodes

Video upload times are flexible throughout the day and episodes release as they are finished, rather than adhering to rigid clock times or speculative upcoming schedules. The site highlights all confirmed uploaded videos across Spark VertoByte's series:

- **Grow Slow:** 11 uploaded episodes (Season 1 complete with 8 episodes; Season 2 in progress with 3 episodes).
- **MS Dhoni: Moments That Made a Champion:** Season 1 episodes *The Boy in Goal* and *The Ticket Examiner* are available in Hindi.
- **Before the Spark:** Season 1 Episode 1 (*The Best Dishwasher*) is available in Hindi.
- **Parathas in the Monsoon** is a wordless short available on both platforms.
- **Grow Slow: Living Diorama** is a released YouTube preview.
- **No speculative upcoming cards:** The website only displays videos that are actually uploaded and streaming.

## Change it

Edit the data in `tools/site-src/build.py` (released episode entries, video URLs) or `styles.css`, then run:

```bash
python3 tools/site-src/build.py
```

That rewrites `docs/index.html`. After an upload, update the episode lists and paste the exact links in `tools/site-src/build.py`, then rebuild.

## Founder and link preview

The **Behind VertoByte** section, the footer line, the FAQ answer and the JSON-LD in the page head come from `founder_section_html()`, `FAQ` and `page()` in `build.py`; the LinkedIn address is `LINKEDIN_URL` at the top of that file. `docs/assets/og-image.jpg` (1200 x 630) is the picture LinkedIn, WhatsApp and similar apps show when the link is shared. After deploying, ask LinkedIn to refresh its cached preview at https://www.linkedin.com/post-inspector/.

## Phones

The page is built mobile first: no sideways scroll from 320 px up, buttons and links at least 44 px tall on touch screens, a section menu that scrolls sideways with a faded edge, and safe-area padding for notched phones. After a change, check it at 320, 375, 414 and 768 px wide.
