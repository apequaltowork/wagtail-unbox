# Ep 10 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues. `wagtail.contrib.forms` was installed from day one.
- `ContactPage(AbstractEmailForm)` + `FormField` in `home/models.py`, at `/contact/`,
  4 editor-defined fields: Your name, Email, Budget (dropdown), About the project.
- Contact appears in the menu on its own — `show_in_menus_default = True` from episode 9.
- All tests below used Django's `locmem` email backend and the test client.

| Test | Result |
|---|---|
| Valid POST | **302** → `/contact/?sent=1`, 1 submission, 1 email to `hello@studio.example` |
| Refresh the thank-you page twice | still **1** submission, **1** email |
| Honeypot filled (`website=…`) | **302** → same thank-you URL, **0** stored, **0** emailed |
| Invalid POST | **200**, errors: "This field is required." ×2, "Enter a valid email address." |
| POST without CSRF token | **403** |
| Optional budget left blank | stored as `''` |

Email body, as sent:

```
Your name: Sam
Email: sam@example.com
Budget: £5k–£15k
About the project: A new site.
```

The honeypot key never appears in stored `form_data`.

## ⭐ Gotcha 1 — no landing template: a 500 that already succeeded

Stock form page, `contact_page_landing.html` not yet written:

```
POST status: 500
TemplateDoesNotExist: home/contact_page_landing.html
submissions saved: 1 | emails sent: 1
```

The visitor sees an error page and tries again. The studio gets two enquiries. The landing
template name is derived from the page template: `contact_page.html` →
`contact_page_landing.html`, in the same folder.

## ⭐ Gotcha 2 — refresh resubmits

Stock `serve()` renders the thank-you page as the **response to the POST** (200, not a
redirect). Refreshing it makes the browser repeat the POST:

```
POST status: 200 (not a redirect)
after one refresh -> submissions: 2 | emails: 2
```

Fixed with Post/Redirect/Get: `render_landing_page` returns `redirect(self.url + "?sent=1")`,
and `serve()` renders the landing template for `GET ?sent=1`. Wagtail's own docstring on
`render_landing_page` says overriding it to redirect is expected.

## ⭐ Gotcha 3 — optional dropdowns have no blank choice

Wagtail's `create_dropdown_field` builds choices from the editor's list and nothing else. An
optional dropdown therefore shows **"Under £5k"** selected, and a browser submits it — every
enquiry would record a budget the person never chose. `StudioFormBuilder` prepends
`("", "Choose one (optional)")` for non-required dropdowns; blank then stores as `''`.

## The honeypot

A plain text input named `website`, moved off-screen with CSS, `tabindex="-1"`,
`aria-hidden="true"` on its wrapper. **Not** `type="hidden"` — bots skip hidden inputs.
A filled honeypot gets the normal redirect and thank-you page: nothing stored, nothing sent,
and the bot learns nothing. `process_form_submission` pops the key before saving.

It stops naive bots, not a determined person. Rate limiting and CAPTCHA are production
concerns.

## Where email goes

`studio/settings/dev.py` already has `EMAIL_BACKEND = "…console.EmailBackend"`, so in
development the email prints in the `runserver` terminal. Real sending is episode 13.

## Not done, deliberately
- CAPTCHA (`wagtail-django-recaptcha`) — third-party, and a privacy decision for the client.
- File upload fields — Wagtail's form builder doesn't include them; a separate lesson.
- Rate limiting — production, ep 13.
