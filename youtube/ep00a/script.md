# Ep 0a — What This Series Is (and Who It's For)

**Target: 8 min. No code.**

> ⚠️ **RECORD THIS EPISODE LAST.** The cold open shows the *finished* studio site, which
> doesn't exist until ep 14. Script it now so the series' promise is fixed and every later
> episode stays honest to it — but shoot it at the end.

## Beats

### 0:00–0:35 — Cold open: the payoff
**[SCREEN: finished studio site — PLACEHOLDER FOOTAGE UNTIL EP 14]**
Scroll the live site. Home, services, a blog post, the contact form. Then cut to the Wagtail
admin and edit a heading live, save, refresh — the change appears.

> "That's a real website, and that's a client editing it without touching code. By the end of
> this series you'll have built that, from an empty folder, and you'll understand every file in it."

### 0:35–1:30 — What Wagtail actually is
**[SCREEN: simple diagram — Django at the base, Wagtail as a layer on top]**
- Wagtail is a **CMS built on Django**. Not a fork, not a framework of its own — a set of Django apps.
- Your Django knowledge transfers directly. Models are models. Templates are templates.
- What it adds: a page tree, a genuinely good editor interface, images with renditions, a content-block system called StreamField.

> "If you already write Django, you already know 70% of Wagtail. This series is about the other 30%."

### 1:30–2:45 — Who this is for, honestly
**[SCREEN: the three audiences, one at a time]**
1. **Django developers** who keep getting asked "can the client edit this?"
2. **Agency / freelance developers** who build sites for people who are not developers.
3. **People leaving WordPress** who want the editor experience without the PHP plugin ecosystem.

Then the hard part — say it plainly:

> "You need to know Django. Not deeply. But models, migrations, templates and settings.py have
> to be familiar. If they aren't, pause here, go do the official Django tutorial — it's a
> weekend — and come back. You'll get far more out of this, and you won't spend fourteen
> episodes copying code you can't change."

Full list is in the description and in `docs/prerequisites.md`. Don't read it all out loud.

**Also say out loud:** recording on **Windows**. Mac and Linux commands are in `commands.md`
in the repo for every episode. Nothing in the series is Windows-only.

### 2:45–4:30 — What we're building, and the shape of the series
**[SCREEN: the episode table from the README]**
- **Act 1, eps 1–3 — Unboxing.** Create the project and read every single file Wagtail generates. Most tutorials skip this. It's why people stay confused.
- **Act 2, eps 4–11 — Building.** Templates, StreamField, images, blog, snippets, navigation, forms, search.
- **Act 3, eps 12–14 — Shipping.** Editor polish, production settings, deploy to a real domain.

One concept per episode, 15–25 minutes. Nothing gets hand-waved.

### 4:30–5:45 — How to follow along (the repo)
**[SCREEN: the GitHub repo, then a terminal doing the checkout]**
- Every episode ends on a **tag**: `ep01-end`, `ep02-end`, …
- Want to start at episode 7? `git checkout ep06-end` and you have exactly the code episode 7 starts from.
- The database isn't committed — you make your own content. That's deliberate; making content is how the admin stops being abstract.

### 5:45–7:00 — What this series is not
Being clear here saves the comments section:
- **Not** a Django tutorial.
- **Not** a front-end course. No React, no Tailwind, no Node. Plain CSS, written by hand, so the episodes stay about Wagtail.
- **Not** a headless/API series. We use Wagtail the way most people ship it — server-rendered templates. (Maybe a separate series later.)
- **Not** a "clone this repo and you're done" series. You'll type the code.

### 7:00–8:00 — Close
- Wagtail **7.4.3**, Django **6.1.1**, Python **3.12** — pinned, so the code on screen is the code you get. (8.0 exists; we're on 7.4 on purpose — better package compatibility, ages slower.)
- Next episode: getting your machine set up. If you already have Python, a venv habit and git, **skip straight to episode 1** — say this explicitly, don't make experienced viewers sit through setup.
- Subscribe / repo link / prerequisites link.

## Tone notes
- Don't oversell. The honest "you need Django first" moment is the most valuable 30 seconds in the episode.
- No "hey guys welcome back" — this is episode zero, nobody is back yet.
- Keep the diagram count to one. This is a talking episode; the finished-site footage carries it.
