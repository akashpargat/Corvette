# Pickleball Manager

A phone app for running a pickleball group: keep everyone's contact, ask who's in for a
given day, track the YES/NO replies, and remind the people who said yes.

It's a web app — no app store, no build step, no server. Open it on your phone, add it to
your home screen, and it behaves like a normal app (own icon, full screen, works offline).
All data lives on your phone in browser storage; nothing is uploaded anywhere.

## The loop it's built around

1. **Add your people** — name and mobile number. Type them in or paste a list.
2. **Make groups** — "Morning regulars", "Weekend crew". Picking a group picks everyone in it.
3. **Create a play date** — Wed / Fri / Sat shortcuts, a time, a place, and how many
   players you need (8 fills two doubles courts).
4. **Ask** — each person gets their own text with their own name in it:
   *"Hi Ravi! Pickleball on Wednesday Aug 19 at 6:00 AM, the pickleball facility. Are you
   in? Reply YES or NO 🎾"*. Tap a name, your messaging app opens with the draft ready, you
   hit send, you come back. A progress bar tracks who's been asked.
5. **Mark the replies** — as answers come in, tap **Yes** or **No** next to the name. The
   counts update live: *5 in · 4 waiting · 1 out — need 3 more players to hit 8*.
6. **Remind the players** — one button texts only the people who said yes. **Save yes list
   as a group** turns that crew into a reusable group, and **Group thread** opens one
   message thread with all of them.

## The one thing it can't do

**It cannot read incoming texts.** No web app can, on any phone — browsers have no access
to SMS, on Android or iPhone. So replies are marked with one tap per person instead of
being detected automatically. Everything downstream of that tap is automatic.

Sending has the same boundary: the app opens a *prefilled draft* in your messaging app and
you press send. It never sends anything silently, and texts come from your own number.

If fully automatic reply tracking matters more than any of the above, that needs either a
native Android app (Android lets an app read SMS with permission) or a Twilio number that
receives replies on your behalf. Both are bigger builds with real trade-offs — an unfamiliar
sending number for Twilio, sideloading for Android.

## Running it

**On your phone (the real way).** The app needs to be served over HTTPS for offline mode
and home-screen install to work. With GitHub Pages:

1. Repo **Settings → Pages → Build and deployment → Deploy from a branch**, pick the branch
   holding this folder and `/ (root)`.
2. Open `https://<your-user>.github.io/<repo>/pickleball/` on your phone.
3. **Android/Chrome:** menu → *Add to Home screen*. **iPhone/Safari:** Share → *Add to Home
   Screen*.

Any static host works the same way (Netlify, Vercel, your own server) — it's plain files.

**On a computer, to try it out:**

```sh
cd pickleball
python3 -m http.server 8777
# then open http://localhost:8777/
```

Settings → **Load sample data** fills it with ten fake players and a play date so you can
see the whole flow without typing anything in.

## Backups

Browser storage is durable but not permanent — clearing site data or browsing history
wipes it, and it doesn't follow you to a new phone. **Settings → Download backup** saves a
JSON file; **Restore backup** reads it back, either replacing everything or merging in.
Worth doing after you've entered your contacts.

## Layout

```
index.html                 app shell
manifest.webmanifest       home-screen install metadata
sw.js                      service worker (offline cache)
css/styles.css             all styling, light + dark
js/
  app.js                   routing and the shell
  router.js                hash routing
  store.js                 all data + localStorage persistence
  sms.js                   message templating and sms: links
  ui.js                    sheets, toasts, confirms
  views/
    events.js              play-date list, roster/response screen, create form
    people.js              contacts
    groups.js              groups
    picker.js              the "who?" selector
    send.js                the send sheet
    settings.js            defaults, templates, backup
tools/
  make-icons.py            regenerates the app icons
  smoke-test.mjs           end-to-end browser test (needs playwright)
```

### Message placeholders

Usable in either template, in Settings or in the send sheet itself:

| Token | Becomes |
| --- | --- |
| `{first}` | Ravi |
| `{name}` | Ravi Menon |
| `{day}` | Wednesday |
| `{date}` | Aug 19 |
| `{time}` | 6:00 AM |
| `{place}` | the pickleball facility |
| `{count}` | how many said yes so far |

In a group text there's no single recipient, so `{first}` and `{name}` become "everyone".

### Editing the code

No build, no dependencies — edit a file and reload. If you change a file, bump `CACHE` in
`sw.js` so phones that already installed the app pick up the new version.
