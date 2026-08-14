# YAW STUDIO — public website

A complete static website. Public pages only. No build step, no framework,
no tracking. Free to use, edit and publish.

**Design direction 03 — The Agency Wall.**

## Open it

Unzip, then double-click `index.html`. That is all.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `work.html` | Selected work |
| `story.html` | Single photo story |
| `services.html` | Services |
| `about.html` | About |
| `archive.html` | Public archive search |
| `licensing.html` | Licensing + request form |
| `contact.html` | Contact |
| `legal.html` | Privacy, cookies, terms, copyright |
| `robots.txt` | Blocks AI training crawlers |
| `sitemap.xml` | Change `yawstudio.com` to your domain |

## Add your images

See `images/README.txt`. It lists every filename, the size needed, and
where to get free legally-usable photos of Gaza.

## Change the design direction

Open `assets/style.css`. Replace the six values in `:root`.
Five alternative palettes are written at the bottom of the file:
Gallery, Broadsheet, Margin, Signal, Dispatch.
Nothing else needs to change.

## Connect the forms

The two forms do nothing yet. Pick one free service and add its URL:

- Formspree — https://formspree.io
- Web3Forms — https://web3forms.com
- Netlify Forms — free if you host on Netlify

Then edit the form tag in `licensing.html` and `contact.html`:

```html
<form class="form" data-form action="https://formspree.io/f/YOURID" method="POST">
```

## Publish it free

- **Netlify Drop** — https://app.netlify.com/drop — drag the folder in. Done.
- **Cloudflare Pages** — https://pages.cloudflare.com — free, fast, own domain.
- **GitHub Pages** — push the folder, turn on Pages in settings.

All three give free HTTPS.

## Before you go live

1. Replace every placeholder image.
2. Change `studio@yawstudio.com` to your real address (search all files).
3. Change the domain in `sitemap.xml`.
4. Read `legal.html` and correct anything that is not true for you.
5. Credit every borrowed photo on `legal.html`.

## The cinema layer (home page)

Three parts, all pure CSS and a few lines of JS. No video file, no library.

**1. The entrance.** A projector gate opens, the logo strokes draw themselves,
the red point arrives last like a record light. About 3.2 seconds.
Click, scroll, or press Esc to skip. It is removed from the page after it runs.

**2. The cinemascope hero.** Five frames, 2.39:1 bars, slow Ken Burns zoom,
1.4s dissolve between them, film grain, vignette and a running timecode.
The filing strip under the caption changes with each frame.
Click a tick mark on the right to jump.

**3. The reel.** A moving filmstrip between Work and Services.
It pauses when you hover or tab into it.

To change the frames, edit `SHOTS` in `build.py` and run it.
To slow it down, change `7000` in `assets/site.js`.

Everything above is switched off automatically for anyone who has
"reduce motion" turned on. They get a still hero and no entrance.
The reel also stops when it scrolls out of view, to save battery.

## What this is not

This is the **public** half only. The private CMS, the rights guard,
the consent records and the partner RSS feeds are a separate build.
Nothing here decides what is public — you do, by which pages you upload.

## Rebuild

`build.py` (one folder up) regenerates every page from one template.
Edit it if you want to change the header, footer or add a page.
