# Ep 13 — Production Settings

Transcript of the narration.

Code at the end of this episode: `git checkout ep13-end`

---

**[0:00]** Production settings.

**[0:04]** Here is what wagtail start gave us for production. Debug off, one storage setting, and an import of a local settings file that does not exist. Django's deploy check finds six issues. And there is no secret key at all.

**[0:21]** And before any of that, the biggest one. The Dockerfile that wagtail start generates runs gunicorn on the WSGI file, and never says which settings to use. So I loaded it exactly the way gunicorn would. Development settings. Debug on. Any host. And the secret key that is committed to git.

**[0:45]** Deployed as generated, any error on the live site shows a full traceback, settings included, to anyone. So the WSGI file now defaults to production, and the Dockerfile says so explicitly. And production refuses to start without a secret. If something is missing, the server stops, with a message saying what. That is failing closed. manage.py still defaults to development, so nothing changes on your laptop.

**[1:17]** Everything secret or host specific now comes from environment variables, so nothing sensitive is in git and the same code runs on any host. Two are required. The secret key, and the allowed hosts. An empty hosts list would start perfectly happily and then answer every single request with a 400, so we refuse to start instead.

**[1:41]** The database is one variable. Database URL. Set it to a Postgres address and it parses to Django's Postgres backend. Leave it unset and you get the local SQLite file, which means you can try these production settings on a laptop before any server exists.

**[2:01]** Point it at Postgres, and it fails before it even tries to connect. On Postgres, Wagtail's search switches to Postgres full text search, and that needs Django's Postgres app installed. So add it when the engine is Postgres. And while testing with no server listening, a wrong address took more than two minutes to fail. A ten second connect timeout, and the same mistake shows up in twelve seconds.

**[2:29]** Now run the site with production settings, before collecting static files. The home page, 500. The admin login, 500. Even the 404 page is a 500. Missing static files manifest entry.

**[2:47]** The manifest storage will not render a static tag for any file it has not seen. So without collect static, every page on the site breaks, including the admin login you would use to investigate. Collect static. Two hundred and seventeen files. And now everything is 200, and a missing page is a real 404.

**[3:11]** Which means, back in episode four, I promised this. The 404 template that extends our base, finally showing up, because debug is off.

**[3:23]** With debug off, Django stops serving static files, so without help the stylesheet is a 404. White noise serves it from the app itself, compressed. And look at the file name. It has a hash in it, so the browser is told to cache it for ten years. Change the CSS and the hash changes. That is the permanent fix for the cache trap that cost us ten minutes in episode four.

**[3:51]** But look at the hero. Broken. Uploaded images are media, not static files, and with debug off nothing serves them. White noise deliberately does not. You can see the alt text from episode six doing its job, at least. How media is served depends on the host, so that is decided in the next episode.

**[4:15]** And HTTPS. The host terminates the encryption and forwards plain requests with a header, so Django is told to trust it. Plain HTTP now redirects. A request for somebody else's hostname is refused. Cookies are secure only. And HSTS starts at one hour. It is a promise browsers keep. Set a year, then break your certificate, and nobody can reach the site until the year is up. Raise it once HTTPS is proven.

**[4:48]** Django's deploy check. Six issues down to two, and both of those are about committing harder to HSTS, which we are not doing until the real domain exists.

**[5:01]** And one more from the generated files. The requirements file that the Dockerfile installs still caps Django below six point one. Every episode has run on six point one point one. So a production image would have been a different Django from anything we ever tested. Both requirements files now pin exactly the same versions.

**[5:25]** And to be straight about it. The Postgres address, the driver, the system checks and the timeout are all verified. A live Postgres connection is not, because there is no database server on this machine, and neither is building the Docker image. Both happen against the real host, next episode.

**[5:46]** Commit, and tag.

**[5:49]** Next episode, the last one. A real host, a real database, media that works, and the first live edit.

**[5:59]** Next episode, we deploy it. Thanks for watching.
