YAW STUDIO — IMAGE SLOTS
========================

Drop your files here with these exact names. Nothing else to change.
If a file is missing, the page still looks correct: a dark gradient
shows in its place instead of a broken icon.

FILE            USED ON             SUGGESTED SIZE     SHAPE
-------------------------------------------------------------------
hero.jpg        Home hero           2400 x 1350        wide 16:9
w01.jpg         Home + Work + Archive  1200 x 2400     tall  1:2
w02.jpg         "                   1200 x 1200        square
w03.jpg         "                   1200 x 1200        square
w04.jpg         "                   2400 x 1200        wide  2:1
w05.jpg         "                   1200 x 1200        square
w06.jpg         "                   1200 x 1200        square
w07.jpg         Work + Archive      1200 x 2400        tall  1:2
w08.jpg         "                   1200 x 1200        square
w09.jpg         "                   1200 x 1200        square
w10.jpg         "                   2400 x 1200        wide  2:1
w11.jpg         "                   1200 x 1200        square
w12.jpg         "                   1200 x 1200        square
story-01.jpg    Story page, main    2400 x 1600        3:2
story-02..05    Story page, strip   900 x 600          3:2
portrait.jpg    About page          1400 x 1750        4:5

BEFORE YOU UPLOAD
-----------------
1. Resize the long edge to 1600px. Quality 70. Never upload a master.
2. Remove GPS data:  exiftool -gps:all= *.jpg
3. Add your credit:  exiftool -Copyright="© YAW STUDIO" -Artist="Yasser Abu Wazna" *.jpg
4. Convert to WebP if you can — about half the file size.


WHERE TO GET FREE, LEGAL IMAGES OF GAZA
=======================================

A. NO ATTRIBUTION NEEDED — easiest
   Pixabay        https://pixabay.com/images/search/gaza/
   Pexels         https://www.pexels.com/search/palestine/
   Unsplash       https://unsplash.com/s/photos/palestine

B. FREE, BUT YOU MUST CREDIT (Creative Commons)
   Wikimedia Commons  https://commons.wikimedia.org/wiki/Category:Gaza_Strip
   EU / ECHO on Flickr (humanitarian field photos)
       https://www.flickr.com/photos/69583224@N05/collections/72157645399556883/
       Credit format:  Photo credit: EC/ECHO/(Photographer Name)
   Creative Commons — Gaza tag
       https://creativecommons.org/tag/gaza/
   Creative Commons — Palestine tag
       https://creativecommons.org/tag/palestine/

   CC BY / CC BY-SA means you MUST:
     - name the photographer
     - link to the licence
     - say if you changed the file
   Put every credit on legal.html under "Photographs on this build".


IMPORTANT — READ THIS
=====================
This is a website about rights and consent. Using an image you do not
have the right to use would damage the studio more than an empty page.

- Replace every placeholder with YOUR OWN photographs as soon as you can.
- Never take an image from Google Images or from a news site.
- Never use a photograph of an identifiable person from a CC pool as if
  it were your own work, and never in a way that suggests a story about
  that person that is not true.
- If in doubt, publish with the gradient placeholders. An empty slot is
  honest. A stolen photo is not.


================================================================
THE IMAGES CURRENTLY IN THIS FOLDER ARE NOT PHOTOGRAPHS
================================================================
They were drawn by code — depth layers, haze, raking light, film
grain. They exist for one reason only: so the cinematic motion
(slow zoom, dissolve, clip-path reveal, grain, vignette) can be
judged with something that behaves like a photograph.

They are NOT pictures of Gaza. They are NOT pictures of any real
place, event or person. Do not publish them as if they were.

Replace every one with your own work before the site goes live.
Run  python3 plates.py  to regenerate them if you need to.
