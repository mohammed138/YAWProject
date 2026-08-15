#!/usr/bin/env python3
"""Builds the YAW STUDIO home page — cinematic editorial portfolio."""
import pathlib, re

OUT = pathlib.Path(__file__).parent

MARK = '<img class="mark" src="assets/logo/yaw-logo-ink.png" alt="" aria-hidden="true" width="924" height="458">'
MARK_WHITE = MARK
FAVICON = 'assets/logo/favicon-512.png'

NAV = [("index.html","Films"), ("story.html","Stories"), ("work.html","Frames"),
       ("archive.html","Archive"), ("licensing.html","Access"), ("contact.html","Contact")]

def ph(tone, src, alt, wm=False):
    w = ('<span class="wm">' + MARK_WHITE + '</span>') if wm else ''
    t = f' {tone}' if tone else ''
    return f'<div class="ph{t}"><img src="images/{src}" alt="{alt}" loading="lazy">{w}</div>'

FILMS = [
 ("film-01.jpg","Sixty-One Days","Documentary","2026","48 min",
  "A hospital wing rebuilt twice in one year, told through the three technicians who never left it.","featured",""),
 ("film-02.jpg","The Class of Forty-Two","Documentary","2025","31 min",
  "One teacher, forty-two children and a warehouse. A school year measured in what is missing.","wide","c"),
 ("film-03.jpg","What the Hands Remember","Documentary","2025","22 min",
  "A prosthetics workshop, and the slow argument between a body and the thing built to replace it.","narrow","b"),
 ("film-04.jpg","North of the Road","Documentary","2024","54 min",
  "Three families move south, then north, then south again, over eleven months.","narrow","d"),
]

STORIES = [
 ("story-01.jpg","Morning Water Queue","Khan Younis","02 Feb 2026","YAW-PS-0410",
  "The hour before the tanks arrive",
  "Every morning the line forms at five. By six it has folded twice around the block, and by seven the "
  "argument about who was first has already been settled by whoever is oldest.",
  "It is not a story about water. It is a story about the order people build when nothing else is ordered.",""),
 ("story-02.jpg","The Prosthetics Workshop","Rafah","27 Nov 2025","YAW-PS-0418",
  "Eight months after the roof came down",
  "The room was a storage bay. It has running water, which the east wing no longer has, and so it became "
  "the place where limbs are made.",
  "Forty-one children are on the list. Most have waited since the summer, when the casting material stopped at the crossing.","b"),
 ("story-03.jpg","Class of Forty-Two","Gaza City","11 Dec 2025","YAW-PS-0421",
  "A school year with no building",
  "The warehouse has one window and no door. The teacher brings the door with her, a sheet of plywood she "
  "leans across the opening when the wind comes off the sea.",
  "She has taught the same forty-two children for three years, in four different buildings.","c"),
]

FRAMES = [
 ("frame-01.jpg","Clinic corridor, second week","Gaza City","14 Mar 2026","YAW-P-2261","Documentary","",""),
 ("frame-02.jpg","Water tanks on the roof","Khan Younis","02 Feb 2026","YAW-P-2298","Reportage","b","pos-2"),
 ("frame-03.jpg","Nurse on a night shift","Rafah","09 Feb 2026","YAW-P-2291","Humanitarian","c","pos-3"),
 ("frame-04.jpg","Bread before dawn","Gaza City","30 Oct 2025","YAW-P-2326","Daily life","d","pos-4"),
 ("frame-01.jpg","Clinic corridor, second week","Gaza City","14 Mar 2026","YAW-P-2261","Archive","b","pos-5"),
]

PUBS = [
 ("The Guardian", "12%", "8%"),
 ("Le Monde", "58%", "18%"),
 ("NPR", "72%", "22%"),
 ("ARTE", "38%", "42%"),
 ("Der Spiegel", "18%", "58%"),
 ("Al Jazeera", "68%", "62%"),
 ("The Economist", "28%", "78%"),
 ("Channel 4", "78%", "82%"),
]

CAPABILITIES = [
 ("01","Documentary film","Long-form films from development to broadcast delivery.","hero.jpg",""),
 ("02","Field production","Crew, access, permits and logistics for visiting teams.","w04.jpg","b"),
 ("03","Cinematography","Camera direction and visual language for documentary and editorial.","film-02.jpg","c"),
 ("04","Photography","Assignment stills, captioned to agency standard.","w02.jpg","d"),
]

MENU = [
 ("index.html","Films","Long form &middot; 2024&ndash;2026","film-02.jpg",""),
 ("work.html","Photography","Single photographs &middot; frames","frame-03.jpg","c"),
 ("story.html","Stories","Reported &middot; written &middot; photographed","story-01.jpg","b"),
 ("about.html","About","YAW Studio &middot; Gaza","portrait.jpg","d"),
 ("archive.html","Archive","Search the cleared record","frame-01.jpg",""),
 ("contact.html","Contact","Gaza &middot; UTC+2","film-04.jpg","b"),
]

CINE_SHOTS = [
 ("hero.jpg","Clinic corridor, second week","Gaza City","14 Mar 2026","YAW-P-2261","Available to licence",""),
 ("portrait.jpg","YAW Studio","Gaza","2026","YAW-P-0001","Director &middot; Cinematographer","c"),
 ("w03.jpg","Class of forty-two","Gaza City","11 Dec 2025","YAW-P-2277","Available to licence","c"),
 ("w09.jpg","The prosthetics workshop","Rafah","27 Nov 2025","YAW-PS-0418","Contact first","b"),
]

def room():
    items, views = [], []
    for i,(href,name,desc,src,tone) in enumerate(MENU):
        items.append(f'<a href="{href}" data-i="{i}"><span class="k">{str(i+1).zfill(2)}</span>'
                     f'<span class="w"><b>{name}</b></span><span class="d">{desc}</span></a>')
        views.append(f'<div class="lay{" on" if i==0 else ""}">{ph(tone, src, name)}</div>')
    return f'''<div class="overlay" id="menuRoom" aria-hidden="true">
  <div class="sweep"></div>
  <div class="top">
    {MARK_WHITE.replace('class="mark"','')}
    <button class="close" id="menuClose" type="button">Close &times;</button>
  </div>
  <div class="list">{"".join(items)}</div>
  <div class="view">{"".join(views)}</div>
  <div class="foot"><span>YAW Studio</span>
  <span>studio@yawstudio.com</span><span>Gaza, Palestine</span></div>
</div>'''

def header(cur="index.html"):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="brand" href="index.html" aria-label="YAW STUDIO — home">
    {MARK}
  </a>
  <div class="hdr-actions">
    <a class="hdr-cta" href="contact.html">Work with YAW Studio &rarr;</a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="menuRoom" aria-label="Open menu">
      <span class="menu-frame"><span class="menu-line"></span><span class="menu-line short"></span><span class="menu-tag">Menu</span></span>
    </button>
  </div>
  <nav aria-label="Main" hidden>{links}</nav>
</header>
{room()}'''

INTRO = f'''<div class="intro" role="presentation">
  <div class="gate t"></div><div class="gate b"></div>
  <div class="slate"><span class="rec">REC</span><span>YAW &middot; GAZA</span><span></span></div>
  <div class="stage">{MARK_WHITE}
  <div class="sub">YAW Studio</div>
  <div class="sub2">Director &middot; Cinematographer &middot; Photographer</div></div>
  <button class="skip" type="button">Skip</button>
</div>'''

def cinema():
    n = len(CINE_SHOTS)
    shots = "".join(
      f'<figure class="shot" data-ref="{r}" data-place="{p}" data-date="{d}" data-rights="{g}">'
      f'{ph(t, s, ti)}</figure>' for s,ti,p,d,r,g,t in CINE_SHOTS)
    return f'''<section class="cine hero-cine" id="top">
  <div class="reel">{shots}</div>
  <div class="grain"></div><div class="vig"></div>
  <div class="cap">
    <p class="hero-eyebrow">YAW STUDIO &middot; Gaza</p>
    <h1>YAW Studio</h1>
    <div class="role">Director &middot; Cinematographer &middot; Photographer</div>
  </div>
  <div class="cine-foot">
    <a class="explore" href="#films">Explore work &rarr;</a>
    <span class="hero-cnt" aria-live="polite">01 / {str(n).zfill(2)}</span>
  </div>
</section>'''

def act_films():
    pieces = []
    for src,title,cat,year,run,syn,layout,tone in FILMS:
        pieces.append(f'''<a class="film-scene {layout}" href="index.html#films">
  <div class="film-frame">
    {ph(tone, src, title)}
    <div class="film-veil"></div>
    <div class="film-meta">
      <span class="film-cat">{cat} &middot; {year} &middot; {run}</span>
      <h3>{title}</h3>
      <p class="film-desc">{syn}</p>
      <span class="film-cta">View film <span class="arr">&rarr;</span></span>
    </div>
  </div>
</a>''')
    return f'''<section class="act films-act" id="films">
  <header class="act-head">
    <span class="seq-num">01</span>
    <div class="act-head-copy">
      <h2>Films</h2>
      <p>Four documentaries made in Gaza &mdash; each one shot over months, not days, with the same families across the whole of it.</p>
    </div>
    <a class="act-all" href="index.html#films">View all films &rarr;</a>
  </header>
  <div class="film-reel">{"".join(pieces)}</div>
</section>'''

def act_stories():
    blocks = []
    for i,(src,title,place,date,ref,head,p1,p2,tone) in enumerate(STORIES):
        alt = "odd" if i % 2 else "even"
        blocks.append(f'''<a class="story-editorial {alt}" href="story.html">
  <div class="story-media">{ph(tone, src, title)}<div class="story-veil"></div></div>
  <div class="story-text">
    <span class="story-kicker">Story {str(i+1).zfill(2)} &mdash; {place}</span>
    <h3>{head}</h3>
    <p class="story-lede">{p1}</p>
    <p class="story-pull"><em>{p2}</em></p>
    <div class="story-foot"><span>{date}</span><span>{ref}</span></div>
    <span class="story-cta">Read story <span class="arr">&rarr;</span></span>
  </div>
</a>''')
    return f'''<section class="act stories-act" id="stories">
  <header class="act-head compact">
    <span class="seq-num">02</span>
    <div class="act-head-copy"><h2>Stories</h2></div>
  </header>
  <div class="story-mag">{"".join(blocks)}</div>
</section>'''

def act_frames():
    items = []
    for src,title,place,date,ref,cat,tone,pos in FRAMES:
        pclass = pos or "pos-1"
        items.append(f'''<a class="cursor-frame {pclass}" href="work.html" data-x="0" data-y="0">
  <div class="cursor-frame-inner">
    {ph(tone, src, title)}
    <div class="cursor-frame-cap">
      <h4>{title}</h4>
      <span>{place} &middot; {date}</span>
      <span class="cursor-frame-go">View frame &rarr;</span>
    </div>
  </div>
</a>''')
    return f'''<section class="act frames-act" id="frames">
  <header class="act-head compact">
    <span class="seq-num">03</span>
    <div class="act-head-copy"><h2>Frames</h2><p>Photography from Gaza &mdash; explore by moving through the field.</p></div>
  </header>
  <div class="cursor-gallery" id="cursorGallery">
    <div class="cursor-label" id="cursorLabel" aria-hidden="true">View</div>
    <div class="cursor-stage">{"".join(items)}</div>
  </div>
</section>'''

def act_publications():
    items = "".join(
        f'<span class="credit-item" style="--lx:{lx};--ty:{ty}" data-i="{i}">{name}</span>'
        for i,(name,lx,ty) in enumerate(PUBS))
    return f'''<section class="act credits-act" id="publications">
  <header class="act-head compact centered">
    <span class="seq-num">04</span>
    <div class="act-head-copy"><h2>Selected publications</h2></div>
  </header>
  <div class="credits-field" id="creditsField">
    <p class="credits-tag">Featured &middot; Published &middot; Broadcast</p>
    {items}
  </div>
</section>'''

def act_production():
    rows, imgs = [], []
    for k,name,desc,src,tone in CAPABILITIES:
        active = " active" if k == "01" else ""
        rows.append(f'''<button type="button" class="prod-row{active}" data-cap="{k}">
  <span class="prod-k">{k}</span>
  <span class="prod-name">{name}</span>
  <span class="prod-desc">{desc}</span>
  <span class="prod-arr">&rarr;</span>
</button>''')
        imgs.append(f'<div class="prod-img{" on" if k == "01" else ""}" data-cap="{k}">{ph(tone, src, name)}</div>')
    return f'''<section class="act prod-act" id="work">
  <header class="act-head">
    <span class="seq-num">05</span>
    <div class="act-head-copy">
      <h2>Work with YAW Studio</h2>
      <p class="prod-lead">From the first frame<br>to the final cut.</p>
    </div>
  </header>
  <div class="prod-reel">
    <div class="prod-visual">{"".join(imgs)}</div>
    <div class="prod-list">{"".join(rows)}</div>
  </div>
</section>'''

def act_final():
    return f'''<section class="act final-act" id="contact">
  <div class="final-visual">{ph("c", "film-04.jpg", "North of the Road")}<div class="final-veil"></div></div>
  <div class="final-copy">
    <h2>What are you making?</h2>
    <a class="final-cta" href="contact.html">Start a project <span class="arr">&rarr;</span></a>
    <a class="final-mail" href="mailto:studio@yawstudio.com">studio@yawstudio.com</a>
  </div>
</section>'''

FOOTER = f'''<footer class="endcard endcard-min">
  <div class="end-min-inner">
    <div class="end-brand">
      <img class="lock" src="assets/logo/yaw-logo-ink.png" alt="YAW STUDIO" width="924" height="458">
      <p class="end-name">YAW Studio</p>
      <p class="end-roles">Director &middot; Cinematographer &middot; Photographer</p>
    </div>
    <nav class="end-nav" aria-label="Footer">
      <a href="index.html">Films</a>
      <a href="story.html">Stories</a>
      <a href="work.html">Frames</a>
      <a href="archive.html">Archive</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="end-contact">
      <a href="mailto:studio@yawstudio.com">studio@yawstudio.com</a>
      <span>Gaza, Palestine &middot; UTC+2</span>
    </div>
  </div>
  <div class="end-min-base">
    <div><a href="legal.html#privacy">Privacy</a><a href="legal.html#cookies">Cookies</a><a href="legal.html#terms">Terms</a></div>
    <div>&copy; 2026 YAW STUDIO &middot; All rights reserved</div>
  </div>
</footer>
<script src="assets/site.js"></script>
<script src="assets/home.js"></script>'''

PAGE = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>YAW STUDIO &mdash; documentary &amp; photography, Gaza</title>
<meta name="description" content="Documentary film, reported photo stories and a cleared archive, produced in Gaza.">
<meta property="og:title" content="YAW STUDIO — documentary and media production, Gaza">
<meta property="og:description" content="Films, stories and frames made in Gaza, with consent, credit and licence recorded for every frame.">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,200..700;1,6..72,200..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/home.css">
</head>
<body class="home fs-cine">
{header()}
<main id="main">
{INTRO}

{cinema()}

{act_films()}

{act_stories()}

{act_frames()}

{act_publications()}

{act_production()}

{act_final()}
</main>
{FOOTER}
</body>
</html>'''

(OUT / "index.html").write_text(PAGE, encoding="utf-8")
print("index.html written:", len(PAGE)//1024, "kb")

for fn in ["work.html","story.html","services.html","about.html","archive.html",
           "licensing.html","contact.html","legal.html"]:
    p = OUT / fn
    if not p.exists():
        continue
    h = p.read_text(encoding="utf-8")
    h = re.sub(
        r'<a class="skip" href="#main">.*?</div>\s*(?=<main)',
        header(fn) + '\n',
        h, count=1, flags=re.S
    )
    h = h.replace('<body class="home fs-cine">', '<body>')
    h = h.replace('<body class="home">', '<body>')
    h = h.replace('width="924" height="574"', 'width="924" height="458"')
    p.write_text(h, encoding="utf-8")
print("headers + logos updated on secondary pages")
