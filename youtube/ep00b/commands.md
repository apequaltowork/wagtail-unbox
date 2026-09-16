# Ep 0b — Commands

Nothing here is Wagtail-specific. We install Wagtail in episode 1.

## 1. Check what you already have

**Windows (PowerShell)**
```powershell
py --version
git --version
```

**macOS / Linux**
```bash
python3 --version
git --version
```

Want: Python **3.12.x**, git **2.x**.

## 2. Install Python 3.12

**Windows** — https://www.python.org/downloads/
On the first installer screen, tick **"Add python.exe to PATH"**. If you already installed
without it: re-run the installer → **Modify** → tick it.

**macOS**
```bash
brew install python@3.12
```

**Linux (Debian/Ubuntu)**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```
`python3.12-venv` is a separate package on Debian/Ubuntu. Without it, `python3 -m venv` fails.

**Linux (Fedora)**
```bash
sudo dnf install python3.12
```

## 3. Install git

**Windows** — https://git-scm.com/download/win (accept the defaults)

**macOS**
```bash
xcode-select --install     # or: brew install git
```

**Linux**
```bash
sudo apt install git       # Debian/Ubuntu
sudo dnf install git       # Fedora
```

Set your identity once:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 4. Install VS Code (optional)

https://code.visualstudio.com/ — then install the **Python** extension (`ms-python.python`).
Any editor works.

## 5. Practise a virtualenv

Throwaway folder. We delete it at the end.

**Windows (PowerShell)**
```powershell
mkdir venv-practice
cd venv-practice
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
mkdir venv-practice
cd venv-practice
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. That prefix means you're inside it.

```bash
pip list        # nearly empty — that's the point
deactivate      # prefix disappears
```

**Remember: a new terminal window starts deactivated. Activate again every time.**

### Windows: "running scripts is disabled on this system"

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Answer `Y`. Then run `.venv\Scripts\activate` again. This affects your user account only.

## 6. Verify your starting line

**Windows**
```powershell
py --version
git --version
py -m venv --help
```

**macOS / Linux**
```bash
python3 --version
git --version
python3 -m venv --help
```

All three succeed → you're ready for episode 1.

## 7. Clean up

```bash
deactivate
cd ..
```
Then delete the `venv-practice` folder. Episode 1 starts from an empty directory.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `'py' is not recognized` (Windows) | PATH box not ticked | Re-run installer → Modify → tick "Add python.exe to PATH" |
| `running scripts is disabled` (Windows) | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `No module named venv` (Linux) | Missing `-venv` package | `sudo apt install python3.12-venv` |
| `python` opens the Microsoft Store (Windows) | Store alias shim | Use `py` instead, or turn off the alias in Settings → App execution aliases |
| Package installs but "isn't found" | venv not activated in this terminal | Activate again — see step 5 |
| `python3 --version` shows 3.9 (macOS) | That's the old system Python | Use `python3.12`, or install via Homebrew |
