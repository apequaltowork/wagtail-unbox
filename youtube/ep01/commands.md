# Ep 1 — Commands

Every command in order. Windows first (what's on screen), macOS/Linux after.

## 1. Make the project folder

**Windows (PowerShell)**
```powershell
cd D:\   # or wherever you keep projects
mkdir wagtail-unboxed
cd wagtail-unboxed
```

**macOS / Linux**
```bash
cd ~/projects
mkdir wagtail-unboxed
cd wagtail-unboxed
```

## 2. Virtualenv

**Windows**
```powershell
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Prompt should now start with `(.venv)`. If not, stop — see ep 0b.

## 3. Install Wagtail

```bash
python -m pip install --upgrade pip
pip install "wagtail==7.4.3" "Django==6.1.1"
```

Pinned on purpose: Wagtail 7.4 declares only `Django>=5.2` with no upper bound, so an
unpinned install drifts away from what's on screen.

Confirm:
```bash
wagtail --version
python -c "import django; print(django.__version__)"
```
Expect `Wagtail 7.4.3` and `6.1.1`.

## 4. Create the project

```bash
wagtail start studio site
```

- `studio` = the **Django project package** name (our site is a design studio).
- `site` = the **folder** to create it in.

> ⚠️ Do **not** name the package `site`. Python has a built-in module called `site`, and
> shadowing it causes confusing import errors later. Same goes for `test`, `json`, `email`.

## 5. Migrate and create your login

```bash
cd site
python manage.py migrate
python manage.py createsuperuser
```

`createsuperuser` prompts for username, email and password. The password is invisible as you
type it — that's normal, keep typing. In development you can accept a "too short/common" warning.

## 6. Run it

```bash
python manage.py runserver
```

- Site: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/

`Ctrl+C` to stop.

## 7. Save your requirements

```bash
cd ..
```

Create `requirements.txt` in the repo root:
```
wagtail==7.4.3
Django==6.1.1
```

## 8. git

```bash
git init -b main
```

Create `.gitignore` in the repo root:
```gitignore
.venv/
*.sqlite3
media/
staticfiles/
__pycache__/
*.py[cod]
.env
.vscode/
.idea/
.DS_Store
```

Then:
```bash
git add -A
git commit -m "ep01: pristine `wagtail start studio` output"
git tag ep01-end
```

We commit the generated project **untouched** — episode 2 is a tour of exactly this tree.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `'wagtail' is not recognized` | venv not activated. See step 2. |
| `Port 8000 is already in use` | `python manage.py runserver 8001` |
| `ModuleNotFoundError: No module named 'site'`-style weirdness | You named the package `site`. Delete and redo step 4 with another name. |
| `wagtail start` says the directory exists and isn't empty | Use an empty folder name, or delete the folder first. |
| Password "too common" on createsuperuser | Fine in dev — accept the bypass, or use a longer password. |
