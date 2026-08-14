#!/usr/bin/env python3
"""Generates the YAW STUDIO public website. Run: python3 build.py"""
import os, pathlib

OUT = pathlib.Path(__file__).parent / "yaw-studio"

NAV = [("index.html","Home"),("work.html","Work"),("services.html","Services"),
       ("about.html","About"),("archive.html","Archive"),("licensing.html","Licensing"),
       ("contact.html","Contact")]


# ---------------------------------------------------------------- logo
# Concept A — the YW ligature. W = V + V, Y = the centre stem.
# Mirror-symmetric about x=104 by construction. Red dot = focus point.
MARK = '<img class="mark" src="assets/logo/yaw-logo-ink.png" alt="" aria-hidden="true" width="924" height="458">'
WATERMARK = '<span class="wm">' + '<img class="mark" src="assets/logo/yaw-logo-ink.png" alt="" aria-hidden="true">' + '</span>'
MARK_WHITE = MARK

# Solid slab version — used for the favicon and the photo watermark,
# because a line drawing breaks up at small size and over busy images.
FAVICON = 'assets/logo/favicon-512.png'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900'
 '&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,200..700;1,6..72,200..600&display=swap" rel="stylesheet">')

def header(cur):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="brand" href="index.html" aria-label="YAW STUDIO — home">
    {MARK}
    <span class="bt"><strong>YAW STUDIO</strong><small>DOCUMENTARY &amp; MEDIA PRODUCTION</small></span>
  </a>
  <nav aria-label="Main">{links}</nav>
  <a class="btn fill" href="contact.html">Enquire</a>
</header>'''

FOOTER = f'''<footer class="ftr">
  <div>{MARK_WHITE}&copy; 2026 Yasser Abu Wazna Documentary &amp; Media Production</div>
  <nav aria-label="Legal">
    <a href="legal.html#privacy">Privacy</a><a href="legal.html#cookies">Cookies</a>
    <a href="legal.html#terms">Terms</a><a href="legal.html#copyright">Copyright</a>
  </nav>
  <div>Gaza, Palestine &middot; studio@yawstudio.com</div>
</footer>
<script src="assets/site.js"></script>'''

def page(fn, title, desc, body):
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; YAW STUDIO</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — YAW STUDIO">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{FONTS}
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="{FAVICON}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{header(fn)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>'''
    (OUT / fn).write_text(html, encoding="utf-8")
    print("wrote", fn)

def ph(cls, src, alt, extra="", wm=False):
    return (f'<div class="ph {cls}"{extra}>'
            f'<img src="images/{src}" alt="{alt}" loading="lazy">'
            f'{WATERMARK if wm else ""}</div>')

# ---------------------------------------------------------------- shared data
WALL = [
 ("w01.jpg","Clinic corridor, second week","Gaza City","YAW-P-2261","go","Available","tall",""),
 ("w02.jpg","Morning water queue","Khan Younis","YAW-P-2270","go","Available","","b"),
 ("w03.jpg","Class of forty-two","Gaza City","YAW-P-2277","go","Available","","c"),
 ("w04.jpg","Vaccination day","North Gaza","YAW-P-2284","go","Available","wide","d"),
 ("w05.jpg","Nurse on a night shift","Rafah","YAW-P-2291","ask","Ask first","",""),
 ("w06.jpg","Water tanks on the roof","Khan Younis","YAW-P-2298","go","Available","","b"),
 ("w07.jpg","Pharmacy stock count","Gaza City","YAW-P-2305","go","Available","tall","c"),
 ("w08.jpg","Fishermen, first light","Gaza port","YAW-P-2312","go","Available","","d"),
 ("w09.jpg","The prosthetics workshop","Rafah","YAW-PS-0418","ask","Ask first","",""),
 ("w10.jpg","Bread before dawn","Gaza City","YAW-PS-0402","go","Available","wide","b"),
 ("w11.jpg","Winter shelter, day one","Khan Younis","YAW-P-2326","go","Available","","c"),
 ("w12.jpg","A school in a warehouse","Deir al-Balah","YAW-P-2333","go","Available","","d"),
]

def wall(items, link="story.html"):
    out = ['<div class="wall">']
    for src,title,place,ref,st,lbl,span,tone in items:
        out.append(
          f'<a class="cell {span}" href="{link}">'
          f'{ph(tone,src,title)}'
          f'<div class="meta"><b>{title}</b>{place} &middot; {ref}'
          f'<br><span class="dot {st}"></span><i>{lbl}</i></div></a>')
    out.append('</div>')
    return "\n".join(out)

SERVICES = [
 ("S/01","Field production","Crew, camera, sound, transport, permits and local contacts for visiting teams.","Lead time 3–7 days"),
 ("S/02","Documentary production","Development, filming, edit supervision and delivery to broadcast spec.","Project based"),
 ("S/03","Humanitarian communication","Field reporting for programme and appeal use, with written consent for each participant.","Consent pack included"),
 ("S/04","Photography","Assignment stills, portraits and photo stories, captioned and keyworded on delivery.","Delivery in 48 hours where possible"),
 ("S/05","Research &amp; facilitation","Verification, case-finding, translation and coordination with local authorities.","Half-day and full-day rates"),
 ("S/06","Archive licensing","Existing stills and footage, cleared and released under a written licence.","Reply within two working days"),
]

def cards(items):
    out = ['<div class="cards">']
    for num,h,p,fine in items:
        out.append(f'<div class="card"><div class="num">{num}</div><h3>{h}</h3><p>{p}</p><div class="fine">{fine}</div></div>')
    out.append('</div>')
    return "\n".join(out)


INTRO = f'''<div class="intro" role="presentation">
  <div class="gate t"></div><div class="gate b"></div>
  <div class="slate">
    <span class="rec">REC</span>
    <span>YAW STUDIO &middot; GAZA</span>
    <span>DOC / 2026 / 24 FPS</span>
  </div>
  <div class="stage">
    {MARK_WHITE}
    <div class="name">YAW STUDIO</div>
    <div class="sub">Documentary &amp; Media Production</div>
  </div>
  <button class="skip" type="button">Skip</button>
</div>'''

SHOTS = [
 ("hero.jpg","Clinic corridor, second week","Gaza City","14 Mar 2026","YAW-P-2261","Available to licence",""),
 ("w03.jpg","Class of forty-two","Gaza City","11 Dec 2025","YAW-P-2277","Available to licence","c"),
 ("w09.jpg","The prosthetics workshop","Rafah","27 Nov 2025","YAW-PS-0418","Contact first","b"),
 ("w02.jpg","Morning water queue","Khan Younis","02 Feb 2026","YAW-P-2270","Available to licence","d"),
 ("w12.jpg","A school in a warehouse","Deir al-Balah","19 Jan 2026","YAW-P-2333","Available to licence",""),
]

def cinema():
    shots, ticks = [], []
    for n,(src,title,place,date,ref,rights,tone) in enumerate(SHOTS):
        shots.append(
          f'<figure class="shot" data-ref="{ref}" data-place="{place}" data-date="{date}" '
          f'data-rights="{rights}">{ph(tone, src, title)}</figure>')
        ticks.append(f'<button type="button" aria-label="Frame {n+1}"></button>')
    return f'''<section class="cine">
  <div class="reel">{"".join(shots)}</div>
  <div class="grain"></div><div class="vig"></div>
  <div class="bar t"></div><div class="bar b"></div>
  <div class="hud"><span>YAW STUDIO &mdash; SELECTED FRAMES</span><span class="tc">00:00:00</span></div>
  <div class="cap">
    <div class="kick">Gaza &middot; documentary &amp; field production</div>
    <h1>Filed from the ground, cleared for use.</h1>
    <p>Documentary film, video journalism and photography produced in Gaza &mdash; with consent, credit and licence recorded for every frame.</p>
    <div class="now"></div>
  </div>
  <div class="ticks">{"".join(ticks)}</div>
  <div class="cue">Scroll</div>
</section>'''

def reel():
    fr = []
    for src,title,place,date,ref,rights,tone in SHOTS + SHOTS:
        fr.append(f'<div class="fr">{ph(tone, src, title)}<div class="lb">{ref} &middot; {place}</div></div>')
    return '<div class="strip-reel" aria-hidden="true"><div class="track">' + "".join(fr) + '</div></div>'

BAND = '''<section class="band">
  <h2 class="disp">Need coverage from Gaza, or a cleared file for publication?</h2>
  <a class="btn" href="contact.html">Start an enquiry</a>
</section>'''

# ---------------------------------------------------------------- 1. HOME
page("index.html","Home",
 "Documentary film, video journalism and photography produced in Gaza. Field production, humanitarian media and a licensed archive.",
f'''{INTRO}

{cinema()}

<div class="strip">
  <div><b>Now showing</b>5 selected frames</div>
  <div><b>Format</b>2.39:1 &middot; documentary</div>
  <div><b>Rights</b><span class="dot go"></span>Cleared before publication</div>
  <div><b>Credit</b>&copy; YAW STUDIO / Yasser Abu Wazna</div>
</div>

<div class="btnrow" style="padding-top:26px">
  <a class="btn fill" href="work.html">See selected work</a>
  <a class="btn" href="licensing.html">Licensing terms</a>
</div>

<section class="sec flush">
  <div class="sec-head">
    <div><p class="eyebrow">01 &mdash; Selected work</p><h2 class="disp">Recent files.</h2></div>
    <a class="btn" href="work.html">All work</a>
  </div>
  {wall(WALL[:8])}
</section>

{reel()}

<section class="sec flush">
  <div class="sec-head">
    <div><p class="eyebrow">02 &mdash; Services</p><h2 class="disp">What we can take on.</h2></div>
    <a class="btn" href="services.html">Details &amp; lead times</a>
  </div>
  {cards(SERVICES)}
</section>

<section class="sec">
  <div class="split">
    <div>
      <p class="eyebrow">03 &mdash; For editors</p>
      <h2 class="disp" style="font-size:clamp(22px,3.4vw,40px);margin:8px 0 18px">Every frame arrives with its paperwork.</h2>
      <p style="font-family:var(--read);font-size:18px;line-height:1.6;color:#31363B;max-width:52ch">
        Location, date, caption, consent, credit line and permitted use are recorded before anything is published.
        If a restriction applies, you see it before you ask.</p>
      <p style="margin-top:22px"><a class="btn" href="archive.html">Search the archive</a></p>
    </div>
    <div>
      <div class="rights">
        <b>Typical record</b>
        CONSENT &middot; Documented, signed release on file<br>
        PERMITTED USE &middot; Editorial, education, non-profit reporting<br>
        TERRITORY &amp; TERM &middot; Worldwide, one year from licence date<br>
        RESTRICTION &middot; Credit line must not be cropped
      </div>
    </div>
  </div>
</section>

{BAND}''')

# ---------------------------------------------------------------- 2. WORK
page("work.html","Selected work",
 "Documentary photography, photo stories and video journalism produced in Gaza between 2025 and 2026.",
f'''<section class="sec flush" style="border-top:0;padding-top:clamp(28px,4vw,52px)">
  <div class="sec-head">
    <div><p class="eyebrow">Selected work</p><h2 class="disp">Contact sheet &mdash; 2025 / 2026</h2></div>
  </div>
  <div class="chips" data-filter>
    <button class="chip" aria-pressed="true">All</button>
    <button class="chip" aria-pressed="false">Documentary</button>
    <button class="chip" aria-pressed="false">Photography</button>
    <button class="chip" aria-pressed="false">Video journalism</button>
    <button class="chip" aria-pressed="false">Humanitarian</button>
  </div>
  <div class="strip">
    <div>12 published files</div>
    <div>Sorted by newest</div>
    <div><span class="dot go"></span>Available &nbsp; <span class="dot ask"></span>Ask first &nbsp; <span class="dot no"></span>Not available</div>
  </div>
  {wall(WALL)}
  <p class="figcap" style="padding-top:16px">Published files only. The rest of the archive stays private until it is cleared.</p>
</section>

{BAND}''')

# ---------------------------------------------------------------- 3. STORY
page("story.html","The prosthetics workshop",
 "A workshop rebuilt inside a damaged hospital wing in Rafah, where technicians fit limbs for children.",
f'''<div class="story">
  <div class="col-a">
    {ph("","story-01.jpg","A technician checks the fit of a prosthetic socket", wm=True)}
    <p class="figcap">Preview &middot; watermarked &middot; 1600px. The master file is not available from this page.</p>
    <div class="prose">
      <p>The room was a storage bay eight months ago. It has running water, which the east wing no longer has, and so it became the place where limbs are made.</p>
      <p>Three technicians work here. Forty-one children are on the waiting list, and most have been waiting since the summer, when the last shipment of casting material stopped at the crossing and did not move for eleven weeks.</p>
      <div class="pull">A caption is a promise. If it cannot be checked, it should not be published.</div>
      <p>I photographed here across four days. Every family gave written consent before I began. Two asked that their children not appear in campaign material, and that condition is attached to the file &mdash; it travels with the photograph wherever it goes.</p>
      <p>The workshop opens at seven. By nine the corridor outside is full, and it stays full until the material runs out.</p>
    </div>
    <div class="thumbs">
      {ph("b","story-02.jpg","Corridor outside the workshop")}
      {ph("c","story-03.jpg","Casting material on a workbench")}
      {ph("d","story-04.jpg","A child waiting with a guardian")}
      {ph("","story-05.jpg","Finished sockets on a shelf")}
    </div>
  </div>
  <div class="col-b">
    <p class="eyebrow" style="color:var(--signal)">Photo story &middot; 12 frames</p>
    <h1 class="disp">The prosthetics workshop</h1>
    <p style="font-family:var(--read);font-size:17px;line-height:1.6;color:#31363B">
      A workshop rebuilt inside a damaged hospital wing, where three technicians fit limbs for children who have been waiting since the spring.</p>
    <div class="rights">
      <b>Rights</b>
      STATUS &middot; Contact first<br>
      PERMITTED USE &middot; Editorial, education, non-profit reporting<br>
      RESTRICTION &middot; Faces of minors must not be cropped out of context<br>
      CREDIT &middot; &copy; YAW STUDIO / Yasser Abu Wazna
    </div>
    <div class="btnrow" style="padding:0">
      <a class="btn fill" href="licensing.html">Request a licence</a>
      <a class="btn" href="work.html">Back to work</a>
    </div>
    <p class="fine" style="margin-top:14px">The high-resolution file is sent only after a licence is agreed.</p>
    <dl class="facts">
      <div><dt>Reference</dt><dd>YAW-PS-0418</dd></div>
      <div><dt>Location</dt><dd>Rafah, Gaza</dd></div>
      <div><dt>Captured</dt><dd>27 November 2025</dd></div>
      <div><dt>Project</dt><dd>Health after the ceasefire</dd></div>
      <div><dt>Topics</dt><dd>Health &middot; Disability &middot; Children</dd></div>
      <div><dt>Language</dt><dd>Arabic audio &middot; English captions</dd></div>
    </dl>
  </div>
</div>

{BAND}''')

# ---------------------------------------------------------------- 4. SERVICES
page("services.html","Services",
 "Field production, documentary production, humanitarian media, photography, research and archive licensing from Gaza.",
f'''<section class="sec flush" style="border-top:0">
  <div class="sec-head">
    <div><p class="eyebrow">Services</p><h2 class="disp">What we can take on.</h2></div>
  </div>
  <p class="lede">Each service lists what is included and the usual lead time. Ask for anything that is not listed &mdash; if we cannot do it, we will say so and suggest who can.</p>
  {cards(SERVICES)}
</section>

<section class="sec">
  <div class="split">
    <div>
      <p class="eyebrow">How we work</p>
      <h2 class="disp" style="font-size:clamp(22px,3.2vw,36px);margin:8px 0 18px">Three rules that do not change.</h2>
    </div>
    <div>
      <dl class="facts" style="margin-top:0">
        <div><dt>Consent first</dt><dd>Nobody is filmed or photographed before they understand where the material may appear.</dd></div>
        <div><dt>No payment for testimony</dt><dd>We cover costs. We do not pay for a story.</dd></div>
        <div><dt>Restrictions travel</dt><dd>If a family sets a condition, it is recorded on the file and applies to every later use.</dd></div>
      </dl>
    </div>
  </div>
</section>

{BAND}''')

# ---------------------------------------------------------------- 5. ABOUT
page("about.html","About",
 "YAW STUDIO is the production name of Yasser Abu Wazna, a documentary film-maker and photojournalist based in Gaza.",
f'''<div class="story">
  <div class="col-a">
    {ph("c","portrait.jpg","Portrait of Yasser Abu Wazna","")}
  </div>
  <div class="col-b">
    <p class="eyebrow" style="color:var(--signal)">About</p>
    <h1 class="disp">A studio based where the work happens.</h1>
    <p style="font-family:var(--read);font-size:17.5px;line-height:1.65;color:#2A2F34">
      YAW STUDIO is the production name of Yasser Abu Wazna, a documentary film-maker and photojournalist working in Gaza.
      The studio produces its own films and works as a local partner for broadcasters, agencies, NGOs and universities.</p>
    <p style="font-family:var(--read);font-size:17.5px;line-height:1.65;color:#2A2F34;margin-top:16px">
      Everything is filed the same way: caption, location, date, consent and credit. That record is what makes an archive
      usable years later, and what lets an editor publish without doubt.</p>
    <dl class="facts">
      <div><dt>Based in</dt><dd>Gaza, Palestine</dd></div>
      <div><dt>Working languages</dt><dd>Arabic, English</dd></div>
      <div><dt>Legal entity</dt><dd>Yasser Abu Wazna Documentary &amp; Media Production</dd></div>
      <div><dt>Reply time</dt><dd>Within two working days</dd></div>
    </dl>
    <div class="btnrow" style="padding:22px 0 0">
      <a class="btn fill" href="contact.html">Get in touch</a>
    </div>
  </div>
</div>

{BAND}''')

# ---------------------------------------------------------------- 6. ARCHIVE
page("archive.html","Archive",
 "Search released photographs, photo stories and video from Gaza by topic, place, date and rights status.",
f'''<section class="sec flush" style="border-top:0">
  <div class="sec-head">
    <div><p class="eyebrow">Public archive</p><h2 class="disp">Search released material.</h2></div>
  </div>
  <form class="search" role="search" onsubmit="return false">
    <label class="skip" for="q">Search the archive</label>
    <input id="q" type="search" placeholder="Search caption, location, project or reference…">
    <button class="btn fill" type="submit">Search</button>
  </form>
  <div class="chips" data-filter>
    <button class="chip" aria-pressed="true">All types</button>
    <button class="chip" aria-pressed="false">Photograph</button>
    <button class="chip" aria-pressed="false">Photo story</button>
    <button class="chip" aria-pressed="false">Video</button>
    <button class="chip" aria-pressed="false">Health</button>
    <button class="chip" aria-pressed="false">Education</button>
    <button class="chip" aria-pressed="false">Gaza City</button>
    <button class="chip" aria-pressed="false">Rafah</button>
    <button class="chip" aria-pressed="true">Available only</button>
  </div>
  <div class="strip">
    <div>12 results</div>
    <div>Sorted by newest</div>
    <div><span class="dot go"></span>Available &nbsp; <span class="dot ask"></span>Ask first &nbsp; <span class="dot no"></span>Not available</div>
  </div>
  {wall(WALL)}
  <p class="figcap" style="padding-top:16px">
    Not finding it? The public archive is a small part of the full record. <a href="contact.html">Ask us directly</a>.</p>
</section>

{BAND}''')

# ---------------------------------------------------------------- 7. LICENSING
LIC = [
 ("STEP 01","Tell us the use","Publication, programme, territory and how long you need it.",""),
 ("STEP 02","We check the rights","Consent, restrictions and any embargo on that specific asset.",""),
 ("STEP 03","Licence and fee","A short written licence with the exact credit line and any conditions.",""),
 ("STEP 04","File delivery","A time-limited private link. The delivery is recorded against the asset.",""),
]
page("licensing.html","Licensing",
 "How to licence photography and video from the YAW STUDIO archive: permitted uses, credit, restrictions and the request process.",
f'''<section class="sec flush" style="border-top:0">
  <div class="sec-head">
    <div><p class="eyebrow">Licensing</p><h2 class="disp">How to use this material.</h2></div>
  </div>
  <p class="lede">Nothing on this site is free to reuse. A preview is not a licence. Send the details below and you will get a written answer within two working days.</p>
  {cards(LIC)}
</section>

<section class="sec">
  <div class="split">
    <div>
      <p class="eyebrow">Terms in short</p>
      <dl class="facts" style="margin-top:14px">
        <div><dt>Permitted use</dt><dd>Editorial, education and non-profit reporting, unless the file says otherwise.</dd></div>
        <div><dt>Credit</dt><dd>The exact credit line on the file must appear with the image. It must not be cropped.</dd></div>
        <div><dt>Not permitted</dt><dd>Advertising, political campaigning, AI training, or any use that identifies a protected person.</dd></div>
        <div><dt>Master files</dt><dd>Sent only after a licence is agreed, through a link that expires.</dd></div>
      </dl>
    </div>
    <div>
      <p class="eyebrow">Licence request</p>
      <form class="form" style="padding:14px 0 0" data-form>
        <div class="full"><label for="ref">Asset reference</label><input id="ref" name="ref" value="YAW-PS-0418"></div>
        <div><label for="org">Organisation</label><input id="org" name="org" placeholder="Broadcaster, publisher, NGO"></div>
        <div><label for="em">Email</label><input id="em" name="email" type="email"></div>
        <div class="full"><label for="use">Intended use</label>
          <select id="use" name="use">
            <option>Editorial — news</option><option>Editorial — feature</option>
            <option>Education / teaching</option><option>Screening / festival</option>
            <option>Campaign / fundraising</option>
          </select></div>
        <div><label for="ter">Territory</label><input id="ter" name="territory" placeholder="Worldwide"></div>
        <div><label for="term">Term</label><input id="term" name="term" placeholder="One year"></div>
        <div class="full"><label for="det">Publication details</label><textarea id="det" name="details" placeholder="Where it will appear, and when"></textarea></div>
        <div class="full"><button class="btn fill" type="submit">Send request</button>
          <p class="fine" style="margin-top:12px">Sending a request does not grant any right to use the file.</p></div>
      </form>
    </div>
  </div>
</section>''')

# ---------------------------------------------------------------- 8. CONTACT
page("contact.html","Contact",
 "Commission field production, documentary work or humanitarian media from Gaza, or ask about an archive licence.",
f'''<section class="sec flush" style="border-top:0">
  <div class="sec-head">
    <div><p class="eyebrow">Contact</p><h2 class="disp">Tell us the assignment.</h2></div>
  </div>
  <p class="lede">The more you give here, the faster the answer. If dates are not fixed yet, say so &mdash; we can still tell you what is possible.</p>
</section>

<section class="sec" style="border-top:0;padding-top:0">
  <div class="split">
    <div>
      <form class="form" style="padding:0" data-form>
        <div><label for="n">Your name</label><input id="n" name="name"></div>
        <div><label for="o">Organisation</label><input id="o" name="org"></div>
        <div><label for="e">Email</label><input id="e" name="email" type="email"></div>
        <div><label for="s">Service needed</label>
          <select id="s" name="service">
            <option>Field production</option><option>Documentary</option>
            <option>Humanitarian media</option><option>Photography</option>
            <option>Archive licence</option><option>Something else</option>
          </select></div>
        <div><label for="l">Location</label><input id="l" name="location" placeholder="Gaza City, Rafah…"></div>
        <div><label for="d">Dates</label><input id="d" name="dates" placeholder="Approximate is fine"></div>
        <div class="full"><label for="m">Message</label><textarea id="m" name="message" placeholder="What are you making, and what do you need from us?"></textarea></div>
        <div class="full"><button class="btn fill" type="submit">Send enquiry</button>
          <p class="fine" style="margin-top:12px">We keep only what we need to answer you. See the <a href="legal.html#privacy">privacy policy</a>.</p></div>
      </form>
    </div>
    <div>
      <dl class="facts" style="margin-top:0">
        <div><dt>Email</dt><dd>studio@yawstudio.com</dd></div>
        <div><dt>Reply time</dt><dd>Within two working days</dd></div>
        <div><dt>Time zone</dt><dd>UTC+2 / UTC+3</dd></div>
        <div><dt>Based in</dt><dd>Gaza, Palestine</dd></div>
        <div><dt>Legal entity</dt><dd>Yasser Abu Wazna Documentary &amp; Media Production</dd></div>
      </dl>
      <div class="rights" style="margin-top:26px">
        <b>Before you write</b>
        For a licence, use the <a href="licensing.html">licensing form</a> instead &mdash; it asks for the details we need.
      </div>
    </div>
  </div>
</section>''')

# ---------------------------------------------------------------- 9. LEGAL
page("legal.html","Legal",
 "Privacy policy, cookie notice, terms of use and copyright information for YAW STUDIO.",
'''<section class="sec flush" style="border-top:0">
  <div class="sec-head"><div><p class="eyebrow">Legal</p><h2 class="disp">Privacy, cookies, terms, copyright.</h2></div></div>
</section>

<div class="prose">
  <h2 id="privacy">Privacy policy</h2>
  <p>We collect only what you type into the contact and licence forms: your name, organisation, email and the details of your request. We use it to answer you and to record the licence if one is agreed. We do not sell it and we do not share it with anyone outside the studio.</p>
  <p>Request records are kept for as long as the licence is valid, plus three years. Ask us and we will tell you what we hold about you, or delete it.</p>

  <h2 id="cookies">Cookies</h2>
  <p>This site sets no advertising or tracking cookies. If analytics are enabled, they are anonymous and count visits only. You can block cookies in your browser and the site will still work.</p>

  <h2 id="terms">Terms of use</h2>
  <p>You may look at this site freely. You may not copy, download, scrape, republish or use any image, video or text from it without a written licence.</p>
  <p>Preview images on this site are low resolution and watermarked. A preview is not a licence, and it is not permission of any kind. Automated collection of this site&rsquo;s content, including for training machine-learning systems, is not permitted.</p>

  <h2 id="copyright">Copyright and credit</h2>
  <p>All photographs, video and text are &copy; Yasser Abu Wazna Documentary &amp; Media Production, unless a different rights holder is named on the file.</p>
  <p>Where a licence is granted, the exact credit line shown on the asset page must appear with the material. It must not be shortened, moved out of view or cropped away.</p>
  <p>If you believe something here infringes your rights, write to studio@yawstudio.com with the page address and we will answer within five working days.</p>

  <h2>Photographs on this build</h2>
  <p>If this site is published with images that are not our own, each one must be credited on this page with its photographer and licence. See <code>images/README.txt</code> in the site folder.</p>
</div>''')

print("done")
