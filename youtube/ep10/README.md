# Ep 10 — Forms That Work

| | |
|---|---|
| **Video file** | `youtube/ep10/out/ep10.mp4` |
| **Subtitles** | `youtube/ep10/out/ep10.srt` |
| **Captions (upload these)** | `youtube/ep10/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep10/assets/thumb.png` |
| **Runtime** | 4:05 |
| **Git tag** | `ep10-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Ready to upload |
| **URL** | — |

---

## Title

```
Wagtail Forms Tutorial: Build a Contact Page That Works | Wagtail Tutorial #10
```

Target search: `wagtail forms` / `wagtail contact form`. 78 characters.

**Alternatives:**

```
Wagtail AbstractEmailForm: Stop Duplicate Form Submissions | Wagtail Tutorial #10
Wagtail Contact Form with a Honeypot for Spam | Wagtail Tutorial #10
```

---

## Description

```
A contact form the editor builds field by field, that emails the studio and stores every
submission. And the three things Wagtail's defaults get wrong, every one measured.

Submit it before writing a thank-you template and the visitor sees a 500 error, but the
submission was saved and the email was sent. Refresh the thank-you page and it sends
again. And an optional dropdown quietly records a choice nobody made.

WHAT YOU'LL LEARN
• AbstractEmailForm and AbstractFormField: forms the editor builds
• The form template, and the 403 you get without csrf_token
• The 500 that already succeeded: the missing landing template
• Why refreshing the thank-you page resubmits, and the Post/Redirect/Get fix
• Why an optional dropdown has no blank choice, and a custom FormBuilder that adds one
• A honeypot for spam, and why it must not be type="hidden"
• Where the email goes in development
• FormSubmissionsPanel: submissions and CSV export in the admin

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep10/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep10-end

Starting from the previous episode? git checkout ep09-end

CHAPTERS
0:00 A studio you can't contact
0:20 Forms the editor builds
0:40 The template, and csrf_token
0:56 A 500 that already worked
1:11 Why the visitor sends it twice
1:31 Refresh sends it again
1:47 Post, redirect, get
2:08 The dropdown that lies
2:30 A custom FormBuilder
2:45 A honeypot for spam
3:14 Where the email goes
3:29 The contact form
3:39 The thank-you page
3:46 Commit and tag
3:50 Next episode

NEXT → Ep 11: Search — the search app from episode 2, finally doing something.

📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.

#wagtail #django #python #cms #webdev
```

---

## Tags

```
wagtail forms, wagtail contact form, wagtail abstractemailform, wagtail form builder, wagtail form submissions, wagtail landing page template, post redirect get django, duplicate form submission, django honeypot, wagtail spam protection, wagtail formbuilder dropdown, wagtail form email, wagtail tutorial, wagtail cms, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep10/assets/thumb.png`

Best hook: the red **500** with "submissions saved: 1" underneath. Overlay: **IT WORKED. IT SAID 500.**

---

## Pinned comment

```
The three from this episode, all measured on the running site:

1) At 0:56 — no contact_page_landing.html yet. The POST returns a 500, but the
submission WAS saved and the email WAS sent. The visitor retries, you get two.
Write the landing template first: page template name + _landing, same folder.

2) At 1:31 — Wagtail renders the thank-you page as the POST response (200, not a
redirect), so refreshing it resubmits. Override render_landing_page to redirect to
?sent=1 and render the landing template on that GET. Refresh twice: still 1.

3) At 2:08 — an optional dropdown has no blank choice, so the browser submits the
first option. A small FormBuilder subclass that prepends ("", "Choose one") fixes it.

Honeypot: a text input moved off-screen with CSS. Not type="hidden" — bots skip those.
```

---

## Before publishing

```bash
git push origin ep10-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 11
- Link element → the repo
