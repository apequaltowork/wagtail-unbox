# Ep 0b — Setting Up Your Machine

**Target: 15 min.** Ends with every viewer at an identical, verified starting line.

> Open by telling experienced viewers to leave: *"If you already have Python 3.12, git, and
> you know what a virtualenv is — skip to episode 1, I'll see you there."* Respecting their
> time earns the subscribe.

## Beats

### 0:00–0:50 — What we're installing, and what we're not
**[SCREEN: a four-item checklist]**
Python 3.12 · an editor · git · a terminal. That's it.

Say the two things that stop people quitting at setup:
- **No database to install.** Episodes 1–12 use SQLite, which ships inside Python. Postgres shows up in episode 13 and we install it there.
- **No Node.js.** Ever. There's no front-end build step in this series.

### 0:50–4:00 — Python 3.12
**[SCREEN: python.org → downloads]**
- **Windows:** download the 3.12 installer. **Tick "Add python.exe to PATH"** on the first screen — the single most common setup failure. Show it being ticked, deliberately.
- **macOS:** `brew install python@3.12`, or the python.org installer. Note the system Python is old — don't use it.
- **Linux:** `sudo apt install python3.12 python3.12-venv` (the `-venv` package is separate on Debian/Ubuntu and people miss it).

Verify — and show what *failure* looks like too, because that's the frame people will pause on:
```
py --version        # Windows  →  Python 3.12.10
python3 --version   # macOS / Linux
```

> "If that says 'command not found' on Windows, you didn't tick the PATH box. Re-run the installer, choose Modify, tick it."

### 4:00–5:30 — An editor
**[SCREEN: VS Code + Python extension]**
- VS Code, free, cross-platform. Install the **Python** extension.
- One sentence of honesty: any editor works — PyCharm, Neovim, Sublime. VS Code is just what's on my screen.
- Don't detour into themes and plugins. Install it, move on.

### 5:30–7:00 — git
**[SCREEN: git-scm.com, then a terminal]**
- Windows: git-scm.com installer, accept the defaults.
- macOS: `xcode-select --install` or `brew install git`. Linux: `sudo apt install git`.
```
git --version
```
- Why you need it: the episode tags. Show one checkout so it's concrete, not theoretical.

### 7:00–8:00 — Your terminal
**[SCREEN: PowerShell open]**
- Windows: PowerShell (what's on screen). Not cmd.exe.
- macOS/Linux: Terminal, bash or zsh.
- The only commands you need: `cd`, listing files, and running a thing. Show `cd` into a folder.

### 8:00–13:00 — Virtual environments (the important part)
**[SCREEN: terminal, whiteboard-style aside]**
This is the concept, not just the command. Spend the time.

> "A virtualenv is a folder holding one project's packages. Without it, every Python project on
> your machine shares one set of libraries, and two projects that need different Wagtail
> versions will fight. With it, they never meet."

Live, in a throwaway folder:
```
py -m venv .venv
.venv\Scripts\activate
```
- Point at the `(.venv)` prefix in the prompt. **That prefix is the whole lesson** — it means you're inside.
- `pip list` — nearly empty. That's the point.
- `deactivate` — prefix gone.
- Re-activate. Emphasise: **new terminal = activate again.** This is the #1 thing that breaks people in episode 3 when a command "suddenly" can't find Wagtail.

**Windows execution-policy gotcha** — hit it deliberately on camera if it appears:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 13:00–14:15 — Verify the starting line
Run the checklist together; everyone should see the same three answers:
```
py --version
git --version
py -m venv --help      # exits cleanly = venv support present
```
**[SCREEN: all three succeeding, side by side]**

### 14:15–15:00 — Close
- Nothing Wagtail-specific has been installed yet — that's episode 1's first command, on purpose.
- Delete the throwaway folder; the real project starts fresh next episode.
- If anything failed, comment with your OS and the exact error.

## Tone notes
- Setup episodes are where channels lose people. Every failure mode gets shown, not just the happy path.
- Don't apologise for the episode's existence. It's short, it's skippable, and it's said so up front.
