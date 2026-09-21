# YouTube — everything needed to publish

One file per episode, plus the playlist. Each file is paste-ready: title, description,
tags, chapters, thumbnail, pinned comment.

| File | Covers |
|---|---|
| [playlist.md](playlist.md) | Playlist title + description, and playlist settings |
| [ep00a/](ep00a/README.md) | Ep 0a — What This Series Is (and Who It's For) |
| [ep00b/](ep00b/README.md) | Ep 0b — Setting Up Your Machine |
| [ep01/](ep01/README.md) | Ep 1 — What Wagtail Actually Is |
| [ep02/](ep02/README.md) | Ep 2 — Opening the Box: Every File Explained |
| [ep03/](ep03/README.md) | Ep 3 — The Page Model & the Tree |
| [ep04/](ep04/README.md) | Ep 4 — Templates & Static Files |
| [ep05/](ep05/README.md) | Ep 5 — StreamField, Properly |
| [ep06/](ep06/README.md) | Ep 6 — Images & Documents |
| [ep07/](ep07/README.md) | Ep 7 — Blog: Parent & Child Pages |
| [ep08/](ep08/README.md) | Ep 8 — Snippets & Reusable Content |
| [ep09/](ep09/README.md) | Ep 9 — Navigation & Site Settings |
| [ep10/](ep10/README.md) | Ep 10 — Forms That Work |
| [channel.md](channel.md) | Channel-level settings that apply to every upload |

## Published

| Ep | Title | URL |
|---|---|---|
| 0a | What This Series Is (and Who It's For) | https://www.youtube.com/watch?v=ck4T3lnkhqs |
| 0b | Setting Up Your Machine | https://www.youtube.com/watch?v=7AtlyySq4l4 |
| 01 | What Wagtail Actually Is | https://www.youtube.com/watch?v=X7FgE9j1XLY |
| 02 | Opening the Box: Every File Explained | https://www.youtube.com/watch?v=FoElBiKp_fI |
| 03 | The Page Model & the Tree | https://www.youtube.com/watch?v=1Oxev2holT4 |
| 04 | Templates & Static Files | https://www.youtube.com/watch?v=e-FeE6O9AhM |
| 05 | StreamField, Properly | https://www.youtube.com/watch?v=8_wrJLU57Qw |
| 06 | Images & Documents | https://www.youtube.com/watch?v=YYxtwAx4a0w |
| 07 | Blog: Parent & Child Pages | https://www.youtube.com/watch?v=lvWFyLOHSBo |
| 08 | Snippets & Reusable Content | https://www.youtube.com/watch?v=L9A5RAPO5uI |

## Titles

Front-loaded with the phrase people actually search, then the series marker. The
`Wagtail Tutorial #N` suffix repeats on purpose -- "wagtail tutorial" is itself a
search term, and the number keeps the series legible in a sidebar.

All are under 80 characters so they survive truncation.

| Ep | Target search | Title |
|---|---|---|
| 0a | `what is wagtail cms` | What Is Wagtail CMS and Should You Learn It? | Wagtail Tutorial #0 |
| 0b | `wagtail setup / python virtualenv` | Wagtail Setup: Install Python, Git and Virtualenv | Wagtail Tutorial #0b |
| 01 | `how to install wagtail` | How to Install Wagtail and Create Your First Project | Wagtail Tutorial #1 |
| 02 | `wagtail project structure` | Wagtail Project Structure Explained: Every File | Wagtail Tutorial #2 |
| 03 | `wagtail page model` | Wagtail Page Model Explained: Custom Page Types | Wagtail Tutorial #3 |
| 04 | `wagtail templates` | Wagtail Templates and Static Files Explained | Wagtail Tutorial #4 |
| 05 | `wagtail streamfield tutorial` | Wagtail StreamField Tutorial: Blocks and StructBlock | Wagtail Tutorial #5 |
| 06 | `wagtail images / renditions` | Wagtail Images and Documents: Renditions and Uploads | Wagtail Tutorial #6 |
| 07 | `wagtail blog tutorial` | Build a Blog in Wagtail: Parent and Child Pages | Wagtail Tutorial #7 |
| 08 | `wagtail snippets` | Wagtail Snippets Tutorial: Reusable Content | Wagtail Tutorial #8 |
| 09 | `wagtail menu / site settings` | Wagtail Navigation Menus and Site Settings | Wagtail Tutorial #9 |
| 10 | `wagtail forms / contact form` | Wagtail Forms Tutorial: Build a Contact Page | Wagtail Tutorial #10 |
| 11 | `wagtail search` | Wagtail Search Tutorial: Index Pages and Search | Wagtail Tutorial #11 |
| 12 | `wagtail hooks / customize admin` | Customize the Wagtail Admin: Hooks and Panels | Wagtail Tutorial #12 |
| 13 | `wagtail postgres / production` | Wagtail Production Settings: Postgres and Security | Wagtail Tutorial #13 |
| 14 | `deploy wagtail` | How to Deploy a Wagtail Site to Production | Wagtail Tutorial #14 |

**These are the YouTube titles.** The short titles on the intro cards and in the
episode tables are deliberately different -- a 74-character title does not fit on a
poster, and a card is design, not search. Card titles live in `video/brand.py`.

Renaming an already-published video is free and does not reset its ranking, so the
published episodes can be updated to these at any time.

## Settings that are the same for every episode

| Field | Value |
|---|---|
| **Category** | Education |
| **Language** | English |
| **License** | Standard YouTube License |
| **Playlist** | Wagtail Unboxed (add at upload time, not later) |
| **Audience** | "No, it's not made for kids" |
| **Altered content** | No |
| **Comments** | On |
| **Visibility** | Public, or scheduled |
| **Resolution** | 1920x1080, 30fps, H.264 + AAC |

## Assets per episode

Rendered by `python video/cards.py`, output in `youtube/epNN/assets/`:

- `assets/intro.png` — 1920x1080 opening poster (already burned into the video)
- `assets/thumb.png` — 1280x720 thumbnail to upload
- `assets/end.png` — 1920x1080 closing frame (already burned in)

## Upload checklist

1. Render the episode: `python video/build.py epNN`
2. Upload the MP4 from `youtube/epNN/out/epNN.mp4`
3. Title + description + tags — paste from this folder's `epNN.md`
4. Upload `assets/thumb.png` as the custom thumbnail
5. Upload `youtube/epNN/out/epNN.srt` as subtitles — **do this, it is the single
   cheapest win available.** Auto-captions mangle "Wagtail", "StreamField" and
   "treebeard" in exactly the words people search for
6. Add to the **Wagtail Unboxed** playlist
7. Set category, language, audience (table above)
8. Add end screen elements over the last ~7 seconds — the end card leaves its right
   third clear for them
9. Publish, then post the pinned comment from `epNN.md`
10. Push the matching git tag so the code link works: `git push origin epNN-end`

Step 10 matters more than it looks. A viewer who checks out a tag that is not pushed
gets an error, and it reads as the series being broken.

## Things worth knowing

- **YouTube rejects `<` and `>`** anywhere in a title or description. The error just
  says "not valid input" and does not name the character. Everything in this folder is
  already clean; keep it that way if you edit.
- **Tags have a 500-character total budget**, not a count limit. The tag lists here fit.
- **The first two lines of a description** are all that show before "show more". They
  carry the hook and the Django prerequisite on purpose.
- **Playlist thumbnail comes from the first video in it**, so ep 0a's thumbnail doubles
  as the playlist cover.
- **External links may be blocked** until the channel is phone-verified. If a
  description is rejected and the text is clean, that is the likely cause.
