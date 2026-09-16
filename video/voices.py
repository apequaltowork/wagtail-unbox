"""Render voice samples so you can pick one before committing episodes to it.

    python video/voices.py            # 15 candidates, one comparison reel + individual files
    python video/voices.py --line "custom text to read"
    python video/voices.py --rate -8%

Output: video/out/voice-samples/
    _comparison.mp3    all candidates back to back, each announcing itself
    <voice>.mp3        each one on its own
"""

from __future__ import annotations

import argparse
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out" / "voice-samples"

# A real line from the ep 0a script -- judge the voice on the actual material.
LINE = ("Wagtail is a content management system built on Django. "
        "If you already write Django, you already know seventy percent of Wagtail. "
        "This series is about the other thirty.")

# name, voice id, one-line note on where it sits
CANDIDATES: list[tuple[str, str, str]] = [
    ("Andrew",      "en-US-AndrewNeural",       "US male - warm, conversational"),
    ("Brian",       "en-US-BrianNeural",        "US male - approachable, casual, sincere"),
    ("Christopher", "en-US-ChristopherNeural",  "US male - reliable, authoritative"),
    ("Eric",        "en-US-EricNeural",         "US male - rational, even, understated"),
    ("Steffan",     "en-US-SteffanNeural",      "US male - rational, slightly brighter (SERIES VOICE)"),
    ("Guy",         "en-US-GuyNeural",          "US male - more energy, more projection"),
    ("Roger",       "en-US-RogerNeural",        "US male - lively, upbeat"),
    ("Ryan",        "en-GB-RyanNeural",         "UK male - crisp, friendly"),
    ("Thomas",      "en-GB-ThomasNeural",       "UK male - measured, more formal"),
    ("Connor",      "en-IE-ConnorNeural",       "Irish male - warm"),
    ("William",     "en-AU-WilliamMultilingualNeural", "Australian male - relaxed"),
    ("Ava",         "en-US-AvaNeural",          "US female - expressive, friendly"),
    ("Emma",        "en-US-EmmaNeural",         "US female - cheerful, clear"),
    ("Aria",        "en-US-AriaNeural",         "US female - confident, newsy"),
    ("Sonia",       "en-GB-SoniaNeural",        "UK female - calm, measured"),
]


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"{tool} not found on PATH.")
    return path


async def render(line: str, rate: str) -> list[Path]:
    import edge_tts

    OUT.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []
    sem = asyncio.Semaphore(4)

    async def one(name: str, voice: str, note: str) -> None:
        async with sem:
            # Each sample announces itself in its own voice, so the reel is self-labelling.
            text = f"{name}. {line}"
            dest = OUT / f"{voice}.mp3"
            for attempt in range(3):
                try:
                    await edge_tts.Communicate(text, voice, rate=rate).save(str(dest))
                    made.append(dest)
                    print(f"  {name:<12} {voice:<34} {note}")
                    return
                except Exception as exc:
                    if attempt == 2:
                        print(f"  {name:<12} FAILED: {exc}")
                        return
                    await asyncio.sleep(1.5 * (attempt + 1))

    await asyncio.gather(*(one(n, v, d) for n, v, d in CANDIDATES))
    # Keep the listed order, not the order they finished in.
    order = {v: i for i, (_, v, _) in enumerate(CANDIDATES)}
    return sorted(made, key=lambda p: order[p.stem])


def reel(parts: list[Path]) -> Path:
    """Stitch the samples together with a beat of silence between each."""
    ffmpeg = need("ffmpeg")
    gap = OUT / "_gap.mp3"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=24000:cl=mono", "-t", "0.9", str(gap)], check=True)

    listing = OUT / "_concat.txt"
    lines = []
    for p in parts:
        lines.append(f"file '{p.as_posix()}'\n")
        lines.append(f"file '{gap.as_posix()}'\n")
    listing.write_text("".join(lines), encoding="utf-8")

    dest = OUT / "_comparison.mp3"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-b:a", "192k", str(dest)], check=True)
    return dest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--line", default=LINE)
    ap.add_argument("--rate", default="-4%")
    args = ap.parse_args()

    print(f"\nRendering {len(CANDIDATES)} voice samples ...\n")
    parts = asyncio.run(render(args.line, args.rate))
    if not parts:
        sys.exit("No samples rendered.")
    dest = reel(parts)
    print(f"\n  reel: {dest}")
    print(f"  individual files: {OUT}\n")


if __name__ == "__main__":
    main()
