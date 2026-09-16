# Channel-level details

Applies to every upload in the series. Set once.

## Identity

| | |
|---|---|
| Channel | https://www.youtube.com/@apequaltowork |
| Handle | @apequaltowork |
| Repo | https://github.com/apequaltowork/wagtail-unbox |
| Website | https://apequaltowork.github.io/ashish-pitroda/ |
| Email | apequaltowork@gmail.com |
| LinkedIn | https://www.linkedin.com/in/ashish-pitroda/ |

Kept in sync with `video/brand.py`, which drives the intro and end cards. Change it
there first, then re-render, then update here.

## Standard description footer

Paste at the bottom of every episode description so the links are consistent:

```
📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.
```

## Series-wide tag base

These go on every episode, then each episode adds its own specifics. Keep the combined
list under the 500-character total budget.

```
wagtail, wagtail cms, wagtail tutorial, django cms, django, python, wagtail 7, python web development, wagtail unboxed
```

## Channel settings worth doing once

- **Verify the channel by phone.** Unlocks custom thumbnails and external links in
  descriptions. Without it, half of what is in this folder cannot be used.
- **Upload defaults** (Studio → Settings → Upload defaults): pre-set category Education,
  language English, the tag base above, and the description footer. Saves repeating it
  fifteen times.
- **Set the series as a Show/Season** if the option appears on the account — it enables
  proper episode numbering.
- **Channel keywords**: wagtail, django, python, cms, web development, tutorial.

## Consistency rules for the series

- Every title ends with the episode marker: `| Wagtail Unboxed #N`
- Every description opens with a one-line hook, then the Django prerequisite
- Every description carries the `git checkout epNN-end` line
- Every episode gets its `.srt` uploaded
- Every episode is added to the playlist at upload time
