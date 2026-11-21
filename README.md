# app-config

Public repo served by GitHub Pages. It holds the remote settings that every app reads at start-up
(replaces Firebase Realtime Database). **Never put secrets here** - everything in this repo is public.

```
apps.json                     registry: [{ "key", "name", "package" }]
<appKey>/ads.json             ad switches (enabled, network, intervals, placements)
<appKey>/update.json          forced / optional update
<appKey>/moreApps.json        "More apps" cards   (object keyed by id)
<appKey>/banners.json         home banners        (object keyed by id)
<appKey>/newCategories.json   categories with the red "New" badge (array of names)
<appKey>/prompts.json         content rows for card-style apps (array)
<appKey>/img/                 images uploaded from the admin page
_template/                    defaults copied by app-factory/scripts/new-app.sh
admin/index.html              admin page (GitHub-backed, app selector)
tools/split-firebase.py       splits a Firebase export into the files above
```

App URL pattern: `https://<owner>.github.io/app-config/<appKey>/ads.json`

## One-time setup
1. Repo Settings > Pages > Deploy from branch `main`, folder `/ (root)`.
2. Create a fine-grained token: GitHub > Settings > Developer settings > Fine-grained tokens,
   Repository access = only `app-config`, permission **Contents: Read and write**. Keep it private.
3. Open `https://<owner>.github.io/app-config/admin/`, enter `owner/app-config`, paste the token.

Changes reach apps after GitHub Pages redeploys (usually 1-5 minutes) - apps also cache the last copy.

## Add an app
Run `scripts/new-app.sh` in the private app-factory repo; it creates `<appKey>/` here from `_template/`
and adds the entry to `apps.json`. Or copy `_template/` by hand and edit `apps.json`.

## Prompt Book data
`prompt-book/` is a snapshot from the old backup. Before switching Prompt Book to this repo, export the
live Firebase database (Console > Realtime Database > three dots > Export JSON) and run:
`python3 tools/split-firebase.py export.json prompt-book`
Check `prompt-book/ads.json` first: the snapshot is set to network `unity` (no AdMob).
The released Prompt Book v3.4.1 still reads Firebase; keep Firebase running until a new version ships.
