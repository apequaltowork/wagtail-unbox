# Ep 10 — Forms That Work

Start from `git checkout ep09-end`. Everything quoted here was run — see `notes.md`.

## Beats

### Cold open — a studio you can't contact
A menu, a journal, a team. No way to get in touch.

### The editor builds the form
`AbstractEmailForm` + an `AbstractFormField` with a `ParentalKey`. The editor adds fields in
the admin — label, type, required, choices. Each submission is stored; if `to_address` is set,
it's emailed.

### The form template
Loop over `form`, `{% csrf_token %}`. Without the token: **403**.

### ⭐ The 500 that already worked
Submit before writing `contact_page_landing.html`: **500**, `TemplateDoesNotExist`. But the
submission **was saved** and the email **was sent**. The visitor retries; the studio gets two.

### ⭐ Refresh sends it again
Wagtail renders the thank-you page as the POST response. Refresh → the browser re-POSTs →
2 submissions, 2 emails. Fix: Post/Redirect/Get. Redirect to `?sent=1`, render the landing
page on that GET. Refresh twice → still 1.

### ⭐ The dropdown that lies
An optional Budget dropdown has no blank option, so the browser submits the first choice.
Every enquiry says "Under £5k". A custom `FormBuilder` adds "Choose one (optional)".

### A honeypot
A text input off-screen. People never fill it; bots fill everything. Filled → same thank-you
page, nothing stored, nothing sent. Not `type="hidden"` — bots skip those.

### Where the email goes
`dev.py` already uses the console backend. The email prints in the runserver terminal. Real
sending is ep 13.

### Submissions in the admin
`FormSubmissionsPanel` on the edit screen: count, link, CSV export.

### Before and after
The form. The thank-you page.

### Next
Ep 11: search — the `search/` app from episode 2, finally doing something.
