"""Intro and end cards -- the two branded frames every episode shares.

    python video/cards.py                 # every episode's cards
    python video/cards.py --ep 05         # just episode 05

Output: youtube/epNN/assets/
    intro.png     1920x1080 opening poster (build.py burns this into the video)
    end.png       1920x1080 closing frame (likewise)
    thumb.png     1280x720 YouTube thumbnail, uploaded by hand

Everything displayed comes from brand.py. Fill that in once.

The end card leaves the RIGHT THIRD clear on purpose: that is where YouTube
overlays its clickable end-screen elements (next video, subscribe). Text placed
there gets covered up.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brand import BRAND, EPISODES, missing, show, value  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
EPISODE_ROOT = REPO / "youtube"


def folder_key(number: str) -> str:
    """Card numbers are "0a"/"01"; episode folders are ep00a/ep01."""
    return f"ep0{number}" if number in ("0a", "0b") else f"ep{number}"


def assets_dir(number: str) -> Path:
    """Each episode owns its own assets folder: youtube/epNN/assets/."""
    d = EPISODE_ROOT / folder_key(number) / "assets"
    d.mkdir(parents=True, exist_ok=True)
    return d
THEME = HERE / "theme.css"
WIDTH, HEIGHT = 1920, 1080

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

CARD_CSS = """
.todo { color: var(--amber); font-weight: 700; letter-spacing: 1px; }

/* ---------- shared mark: an opened box ---------- */
.mark { width: 104px; height: 104px; display: block; }

/* ---------- intro card ---------- */
.intro {
  width: 1920px; height: 1080px; position: relative;
  background:
    radial-gradient(1200px 700px at 78% 18%, rgba(67,177,176,.16), transparent 60%),
    linear-gradient(160deg, #0f1117 0%, #141826 58%, #0f1117 100%);
  display: flex; flex-direction: column; justify-content: center;
  padding: 0 140px; overflow: hidden;
}
/* faint grid, so the flat background has some texture */
.intro::after {
  content: ""; position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.028) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.028) 1px, transparent 1px);
  background-size: 80px 80px;
  mask-image: radial-gradient(900px 620px at 72% 30%, #000 0%, transparent 78%);
}
.intro > * { position: relative; z-index: 2; }

.brandline { display: flex; align-items: center; gap: 30px; margin-bottom: 76px; }
.brandline .word { font-size: 40px; letter-spacing: 9px; text-transform: uppercase; font-weight: 600; }
.brandline .word b { color: var(--teal); }
.brandline .tag {
  font-size: 26px; color: var(--muted); letter-spacing: 3px;
  text-transform: uppercase; padding-left: 30px; border-left: 3px solid var(--line);
}

.epline { display: flex; align-items: flex-start; gap: 56px; }
.epnum {
  font-size: 220px; font-weight: 800; line-height: .82; letter-spacing: -8px;
  color: transparent; -webkit-text-stroke: 4px var(--teal); flex: none;
}
.epwrap { padding-top: 14px; }
.epwrap .kicker {
  font-size: 30px; letter-spacing: 7px; text-transform: uppercase;
  color: var(--teal); margin-bottom: 26px; font-weight: 600;
}
.eptitle { font-size: 92px; font-weight: 700; line-height: 1.06; letter-spacing: -2.5px; max-width: 1260px; }

.stack {
  position: absolute; left: 140px; bottom: 92px; z-index: 2;
  font-family: var(--mono); font-size: 27px; color: var(--muted);
}
.intro .accent { position: absolute; left: 0; top: 0; bottom: 0; width: 14px;
  background: linear-gradient(180deg, var(--teal), var(--teal-dim)); z-index: 3; }
.repoline {
  position: absolute; right: 140px; bottom: 92px; z-index: 2;
  font-family: var(--mono); font-size: 27px; color: var(--muted);
}

/* ---------- end card ---------- */
.end {
  width: 1920px; height: 1080px; position: relative;
  background:
    radial-gradient(900px 640px at 22% 76%, rgba(67,177,176,.15), transparent 62%),
    linear-gradient(200deg, #0f1117 0%, #141826 60%, #0f1117 100%);
  padding: 110px 140px; overflow: hidden;
  display: flex; flex-direction: column; justify-content: space-between;
}
.end .accent { position: absolute; left: 0; top: 0; bottom: 0; width: 14px;
  background: linear-gradient(180deg, var(--teal), var(--teal-dim)); }
/* YouTube drops its clickable end-screen widgets over the right third. */
.safe {
  position: absolute; right: 0; top: 0; width: 620px; height: 1080px;
  border-left: 2px dashed rgba(255,255,255,.07);
}
.safe .note {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%) rotate(-90deg);
  white-space: nowrap; font-size: 22px; letter-spacing: 6px; text-transform: uppercase;
  color: rgba(255,255,255,.13);
}
.end .inner { max-width: 1120px; position: relative; z-index: 2; }
.end h1 { font-size: 88px; line-height: 1.05; letter-spacing: -2px; margin: 0 0 22px; }
.end .sub2 { font-size: 36px; color: var(--muted); margin-bottom: 64px; }

.links { display: flex; flex-direction: column; gap: 30px; }
.link { display: flex; align-items: center; gap: 26px; }
.link .lbl {
  font-size: 22px; letter-spacing: 3px; text-transform: uppercase; color: var(--teal);
  width: 180px; flex: none; font-weight: 600;
}
/* 32px keeps the longest value (the repo URL) on one line inside .inner. */
.link .val { font-family: var(--mono); font-size: 32px; color: var(--fg); white-space: nowrap; }

.endfoot {
  position: relative; z-index: 2; display: flex; align-items: center;
  gap: 30px; color: var(--muted); font-size: 28px;
}
.endfoot .word { font-size: 30px; letter-spacing: 7px; text-transform: uppercase; color: var(--fg); }
.endfoot .word b { color: var(--teal); }
"""

MARK = """
<svg class="mark" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 22 L32 10 L58 22 L32 34 Z" stroke="#43b1b0" stroke-width="3"
        stroke-linejoin="round" fill="rgba(67,177,176,.16)"/>
  <path d="M6 22 V45 L32 57 V34" stroke="#43b1b0" stroke-width="3" stroke-linejoin="round"/>
  <path d="M58 22 V45 L32 57" stroke="#2b6f6e" stroke-width="3" stroke-linejoin="round"/>
  <path d="M32 30 V4 M32 4 L25 11 M32 4 L39 11" stroke="#eef1f7" stroke-width="3"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def find_chrome() -> Path:
    for p in CHROME_CANDIDATES:
        if p.exists():
            return p
    sys.exit("No Chrome or Edge found -- needed to rasterise cards.")


def page(body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{THEME.as_uri()}">
<style>{CARD_CSS}{THUMB_CSS}</style></head><body>{body}</body></html>"""


def intro_html(number: str, title: str) -> str:
    return page(f"""
<div class="intro">
  <div class="accent"></div>
  <div class="brandline">
    {MARK}
    <div class="word">Wagtail <b>Unboxed</b></div>
    <div class="tag">{BRAND['tagline']}</div>
  </div>
  <div class="epline">
    <div class="epnum">{number}</div>
    <div class="epwrap">
      <div class="kicker">Episode {number}</div>
      <div class="eptitle">{title}</div>
    </div>
  </div>
  <div class="stack">{BRAND['stack']}</div>
  <div class="repoline">{show('repo')}</div>
</div>""")


def end_html() -> str:
    rows = []
    for key, label in (("repo", "Code"), ("website", "Website"), ("email", "Email"),
                       ("youtube", "YouTube"), ("x", "X"), ("linkedin", "LinkedIn")):
        # An empty value means deliberately hidden; a placeholder still shows loudly.
        if BRAND.get(key) == "":
            continue
        rows.append((label, show(key)))

    links = "\n".join(
        f'<div class="link"><div class="lbl">{lbl}</div><div class="val">{val}</div></div>'
        for lbl, val in rows
    )
    channel = show("channel")
    return page(f"""
<div class="end">
  <div class="accent"></div>
  <div class="safe"><div class="note">YouTube end-screen zone &mdash; keep clear</div></div>
  <div class="inner">
    <h1>Thanks for watching.</h1>
    <div class="sub2">Every episode ends on a git tag &mdash; start anywhere in the series.</div>
    <div class="links">{links}</div>
  </div>
  <div class="endfoot">
    {MARK}
    <div class="word">Wagtail <b>Unboxed</b></div>
    <div>&middot;</div>
    <div>{channel}</div>
  </div>
</div>""")


THUMB_CSS = """
/* 1280x720 thumbnail: same design language, but sized to survive being shown
   at roughly 360x200 in a sidebar. Everything gets bigger, not smaller. */
.thumb {
  width: 1280px; height: 720px; position: relative; overflow: hidden;
  background:
    radial-gradient(760px 460px at 80% 20%, rgba(67,177,176,.20), transparent 62%),
    linear-gradient(160deg, #0f1117 0%, #141826 58%, #0f1117 100%);
  padding: 74px 84px; display: flex; flex-direction: column; justify-content: center;
}
.thumb .accent { position: absolute; left: 0; top: 0; bottom: 0; width: 12px;
  background: linear-gradient(180deg, var(--teal), var(--teal-dim)); }
.thumb .epbig {
  position: absolute; right: 60px; top: 40px;
  font-size: 210px; font-weight: 800; letter-spacing: -8px; line-height: 1;
  color: transparent; -webkit-text-stroke: 4px rgba(67,177,176,.42);
}
.thumb .word {
  font-size: 30px; letter-spacing: 8px; text-transform: uppercase;
  font-weight: 600; margin-bottom: 30px;
}
.thumb .word b { color: var(--teal); }
.thumb h1 {
  font-size: 88px; font-weight: 800; line-height: 1.02; letter-spacing: -2.5px;
  margin: 0; max-width: 900px;
}
.thumb .hook {
  margin-top: 30px; font-size: 34px; color: var(--teal); font-weight: 600;
  letter-spacing: 1px;
}
"""

# Short, punchy overlay per episode -- a thumbnail is read in about a second,
# so this is deliberately not the full episode title.
THUMB_TEXT: dict[str, tuple[str, str]] = {
    "0a": ("Start<br>here.", "Is this series for you?"),
    "0b": ("Set up<br>once.", "Python · git · virtualenvs"),
    "01": ("What IS<br>Wagtail?", "Install to running CMS"),
    "02": ("Every<br>file.", "All 29, explained"),
    "03": ("The page<br>tree.", "How Wagtail really works"),
    "04": ("Templates<br>&amp; static.", "Making it look real"),
    "05": ("Stream<br>Field.", "Done properly"),
    "06": ("Images<br>&amp; docs.", "Renditions and uploads"),
    "07": ("Build a<br>blog.", "Parent and child pages"),
    "08": ("Snippets.", "Reusable content"),
    "09": ("Menus &amp;<br>settings.", "Navigation from the tree"),
    "10": ("Forms<br>that work.", "A real contact page"),
    "11": ("Search.", "Indexing your pages"),
    "12": ("Editor<br>polish.", "Make the client happy"),
    "13": ("Going to<br>production.", "Postgres, env vars, security"),
    "14": ("Deploy<br>it.", "Live, on a real domain"),
}


def thumb_html(number: str) -> str:
    headline, hook = THUMB_TEXT.get(number, (EPISODES[number], ""))
    return page(f"""
<div class="thumb">
  <div class="accent"></div>
  <div class="epbig">{number}</div>
  <div class="word">Wagtail <b>Unboxed</b></div>
  <h1>{headline}</h1>
  <div class="hook">{hook}</div>
</div>""")


def shoot(chrome: Path, html: str, dest: Path, size: tuple[int, int] = (WIDTH, HEIGHT)) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_{dest.stem}.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(
        [str(chrome), "--headless", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={size[0]},{size[1]}",
         f"--screenshot={dest}", str(tmp)],
        check=True, capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    if not dest.exists():
        raise RuntimeError(f"Chrome produced nothing for {dest.name}")
    print(f"  {dest.relative_to(REPO)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", default=None, help="render one episode's cards, e.g. 05")
    args = ap.parse_args()

    chrome = find_chrome()
    if args.ep and args.ep not in EPISODES:
        sys.exit(f"Unknown episode '{args.ep}'. Known: {', '.join(EPISODES)}")
    targets = {args.ep: EPISODES[args.ep]} if args.ep else EPISODES

    print("\nCards -> youtube/epNN/assets/\n")
    end = end_html()
    for num, title in targets.items():
        d = assets_dir(num)
        shoot(chrome, intro_html(num, title), d / "intro.png")
        shoot(chrome, thumb_html(num), d / "thumb.png", size=(1280, 720))
        # The end card is identical everywhere, but each folder stays self-contained.
        shoot(chrome, end, d / "end.png")

    gaps = missing()
    if gaps:
        print(f"\n  ! still placeholders in brand.py: {', '.join(gaps)}")
        print("    They render in amber on the cards. Fill them in and re-run.\n")
    else:
        print("\n  All brand details filled in.\n")


if __name__ == "__main__":
    main()
