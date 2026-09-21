"""Make a readable transcript and clean captions for every rendered episode.

    python video/transcripts.py            # every episode with out/<key>.srt
    python video/transcripts.py ep05       # just one

Reads youtube/<key>/out/<key>.srt -- the subtitles written by build.py in the
same render as the MP4, so the timings match the video -- and writes two files
next to the episode's other docs:

    youtube/<key>/transcript.md    readable, one paragraph per scene, timestamped
    youtube/<key>/captions.srt     the same cues with written spellings, for YouTube

The narration is written for the voice, not the eye: "U R L", "C S S",
"four oh four", "manage dot py". SPOKEN_TO_WRITTEN turns those back into what a
reader expects. Order matters -- longer phrases first.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "youtube"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brand import EPISODES as TITLES  # noqa: E402

SPOKEN_TO_WRITTEN: list[tuple[str, str]] = [
    # multi-word numbers and status codes
    (r"\boh oh oh four\b", "0004"),
    (r"\bthree hundred and seventy five\b", "375"),
    (r"\bnine hundred and ninety nine\b", "999"),
    (r"\btwo hundred and seventeen\b", "217"),
    (r"\ba hundred and eighty four\b", "184"),
    (r"\bfour oh four\b", "404"),
    (r"\bfour oh three\b", "403"),
    (r"\bthree oh two\b", "302"),
    (r"\bfive hundred\b", "500"),
    (r"\bfour hundred\b", "400"),
    (r"\beight hundred pixel\b", "800-pixel"),
    (r"\bsixteen hundred\b", "1600"),
    (r"(?<=everything is )two hundred\b", "200"),
    # spelled-out acronyms
    (r"\bH T T P S\b", "HTTPS"),
    (r"\bH T T P\b", "HTTP"),
    (r"\bH S T S\b", "HSTS"),
    (r"\bH T M L\b", "HTML"),
    (r"\bC S R F\b", "CSRF"),
    (r"\bW S G I\b", "WSGI"),
    (r"\bU R Ls\b", "URLs"),
    (r"\bU R L\b", "URL"),
    (r"\bU R\b", "URL"),
    (r"\bC S S\b", "CSS"),
    (r"\bC M S\b", "CMS"),
    (r"\bS E O\b", "SEO"),
    (r"\bJ SON\b", "JSON"),
    (r"\bc s s\b", "css"),                       # lower-case, inside a path
    (r"\bhttp colon slash slash\b ?", "http://"),
    (r"\bhttps colon slash slash\b ?", "https://"),
    (r"\bd b dot sqlite three\b", "db.sqlite3"),
    (r"\bgit dash s c m dot com\b", "git-scm.com"),
    (r"\bpython dot e x e\b", "python.exe"),
    # code read aloud
    (r"\b[Pp]age dot content panels\b", "Page.content_panels"),
    (r"\b[Pp]age dot objects\b", "Page.objects"),
    (r"\bpage dot get parent\b", "page.get_parent"),
    (r"\bpage dot url\b", "page.url"),
    (r"\bnot url path\b", "not url_path"),
    (r"\b[Vv]alue dot (quote|attribution)\b", r"value.\1"),
    (r"\bdot (specific|live)\b", r".\1"),
    (r"\bplus underscore landing\b", "plus _landing"),
    (r"\b([a-z]+) underscore ([a-z]+)\b", r"\1_\2"),
    (r"\bapp slash model name dot html\b", "app/model_name.html"),
    # file names read aloud; the name is lower-cased because a sentence may
    # start with it ("Base dot html ...")
    (r"\b([A-Za-z_]+) dot pie\b", lambda m: f"{m.group(1).lower()}.py"),
    (r"\bstudio dot settings dot dev\b", "studio.settings.dev"),
    (r"\b([A-Za-z_]+) dot (html|py|css|com|org|txt|CSS|HTML)\b",
     lambda m: f"{m.group(1).lower()}.{m.group(2).lower()}"),
    (r"\bdot venv\b", ".venv"),
    (r"\bslash\b ?", "/"),
]


def written(text: str) -> str:
    for pattern, repl in SPOKEN_TO_WRITTEN:
        text = re.sub(pattern, repl, text)
    text = re.sub(r" +/ *", "/", text)          # "studio / static" -> "studio/static"
    return text


def parse_srt(path: Path) -> list[tuple[str, str, str]]:
    cues = []
    for block in path.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        start, end = lines[1].split(" --> ")
        cues.append((start, end, " ".join(lines[2:]).strip()))
    return cues


MAX_LINE = 84  # about two lines of YouTube captions at normal size


def caption_lines(text: str) -> list[str]:
    """Split at sentence ends, then at commas, so no line exceeds MAX_LINE."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    lines = []
    for part in parts:
        while len(part) > MAX_LINE:
            cut = part.rfind(", ", 0, MAX_LINE)
            if cut < MAX_LINE // 3:
                cut = part.rfind(" ", 0, MAX_LINE)
            else:
                cut += 1  # keep the comma on this line
            lines.append(part[:cut].strip())
            part = part[cut:].strip()
        if part:
            lines.append(part)
    return lines


def seconds(tc: str) -> float:
    h, m, rest = tc.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def timecode(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def stamp(timecode: str) -> str:
    h, m, rest = timecode.split(":")
    s = rest.split(",")[0]
    return f"{int(h) * 60 + int(m)}:{s}"


def episode_code(key: str) -> str:
    """ep05 -> "05", ep00a -> "0a" -- the keys brand.EPISODES uses."""
    n = key[2:]
    return n if n.isdigit() else n[1:]


def number_of(key: str) -> str:
    code = episode_code(key)
    return str(int(code)) if code.isdigit() else code


def title_of(key: str) -> str:
    return TITLES.get(episode_code(key), key)


def published_url(key: str) -> str | None:
    readme = EPISODES / key / "README.md"
    if not readme.exists():
        return None
    m = re.search(r"\| \*\*URL\*\* \| (https://\S+) \|", readme.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def build(key: str) -> tuple[int, int]:
    srt = EPISODES / key / "out" / f"{key}.srt"
    cues = parse_srt(srt)
    title = title_of(key)
    url = published_url(key)

    md = [f"# Ep {number_of(key)} — {title}", "", "Transcript of the narration."]
    if url:
        md += ["", f"Video: {url}"]
    md += ["", f"Code at the end of this episode: `git checkout {key}-end`"
           if key not in ("ep00a", "ep00b") else "No code in this episode.", "", "---", ""]
    for start, _end, text in cues:
        md += [f"**[{stamp(start)}]** {written(text)}", ""]
    (EPISODES / key / "transcript.md").write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

    # build.py writes one cue per scene -- up to 30 seconds of speech in one
    # block, far too much to read on screen. Split each into short lines and
    # share the scene's time between them by length. Narration is read at an
    # even pace, so character count is a fair proxy for when each line is said.
    out, n = [], 0
    for start, end, text in cues:
        t0, t1 = seconds(start), seconds(end)
        lines = caption_lines(written(text))
        total = sum(len(line) for line in lines) or 1
        clock = t0
        for line in lines:
            span = (t1 - t0) * len(line) / total
            n += 1
            out.append(f"{n}\n{timecode(clock)} --> {timecode(clock + span)}\n{line}\n")
            clock += span
    (EPISODES / key / "captions.srt").write_text("\n".join(out), encoding="utf-8")
    return len(cues), sum(len(t.split()) for _, _, t in cues)


def main(argv: list[str]) -> None:
    keys = argv or sorted(p.parent.parent.name for p in EPISODES.glob("ep*/out/ep*.srt"))
    for key in keys:
        cues, words = build(key)
        print(f"{key:6}  {cues:3} cues  {words:5} words  -> transcript.md, captions.srt")


if __name__ == "__main__":
    main(sys.argv[1:])
