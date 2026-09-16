"""Single source of truth for series branding.

Everything the intro and end cards display comes from here, so changing a URL
or a handle is one edit and a re-render -- not fifteen hand-edited images.

Anything left as FILL_ME renders in amber on the card so it cannot be missed.
An empty string ("") means "deliberately hidden" and drops the row entirely.
"""

from __future__ import annotations

FILL_ME = "FILL_ME"

BRAND = {
    # ---- identity -------------------------------------------------------
    "series": "Wagtail Unboxed",
    "tagline": "Learning by Building",
    "channel": "@apequaltowork",

    # ---- where to find things -------------------------------------------
    # Display forms, not clone URLs -- these get read off a screen.
    "repo": "github.com/apequaltowork/wagtail-unbox",
    "website": "apequaltowork.github.io/ashish-pitroda",
    "email": "apequaltowork@gmail.com",

    # ---- socials ("" hides the row) -------------------------------------
    "youtube": "@apequaltowork",
    "x": "",
    "linkedin": "in/ashish-pitroda",

    # ---- stack strip, shown on the intro card ---------------------------
    "stack": "Wagtail 7.4.3 &nbsp;&middot;&nbsp; Django 6.1.1 &nbsp;&middot;&nbsp; Python 3.12",
}

# Full URLs, for descriptions and docs rather than for cards.
URLS = {
    "repo": "https://github.com/apequaltowork/wagtail-unbox",
    "repo_ssh": "git@github.com:apequaltowork/wagtail-unbox.git",
    "channel": "https://www.youtube.com/@apequaltowork",
    "website": "https://apequaltowork.github.io/ashish-pitroda/",
    "linkedin": "https://www.linkedin.com/in/ashish-pitroda/",
}

# Episode number -> title, for the intro card. Keep in step with README.md.
EPISODES: dict[str, str] = {
    "0a": "What This Series Is (and Who It's For)",
    "0b": "Setting Up Your Machine",
    "01": "What Wagtail Actually Is",
    "02": "Opening the Box: Every File Explained",
    "03": "The Page Model & the Tree",
    "04": "Templates & Static Files",
    "05": "StreamField, Properly",
    "06": "Images & Documents",
    "07": "Blog: Parent & Child Pages",
    "08": "Snippets & Reusable Content",
    "09": "Navigation & Site Settings",
    "10": "Forms That Work",
    "11": "Search",
    "12": "Editor Experience Polish",
    "13": "Production Settings",
    "14": "Deploy It",
}


def value(key: str) -> str | None:
    """Return a brand value, or None when it is still a placeholder."""
    v = BRAND.get(key, FILL_ME)
    return None if v == FILL_ME else v


def show(key: str) -> str:
    """Render a value, a loud amber placeholder, or "" for a deliberately hidden row."""
    v = BRAND.get(key, FILL_ME)
    if v == FILL_ME:
        return f'<span class="todo">{key.upper()}?</span>'
    return v


def missing() -> list[str]:
    return [k for k, v in BRAND.items() if v == FILL_ME]
