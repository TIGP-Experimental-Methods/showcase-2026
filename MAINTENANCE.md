# Maintaining the wall

Notes for whoever (or whatever) next edits this repository. `README.md` is the student-facing
document and is the authority on the entry format; this file is the operational detail that
is not obvious from it.

---

## The two Actions, and the trap

A push runs **two** workflows:

1. **`build projects.json`** — validates `projects/*.json` and commits the regenerated
   `projects.json` back with `[skip ci]`.
2. **`pages build and deployment`** — publishes the site.

They start together but **(2) finishes well after (1)**. `gh run list --limit 1` returns
whichever started last, which is usually (1), so waiting on it and then loading the page
shows you the *old* site. This has already caused one false "it's live" report.

Check the live files, not the run status:

```bash
curl -s "https://tigp-experimental-methods.github.io/showcase-2026/projects.json?t=$(date +%s)"
```

and wait until what comes back is what you pushed.

---

## Ordering — it is the `updated` date, and nothing else

`index.html` and `scripts/build.py` both sort by `updated` **descending**, then `title`
descending. There is no other mechanism, on purpose: a `rank` field was tried on
2026-09-12 and removed the same day at the instructor's request. Do not reintroduce one.

The consequence worth knowing: **any card returns to the top of the wall the moment it is
touched**, because that is what the date means. That is right for student work — the wall is
a noticeboard and new work should lead.

### The instructor's own cards carry their project's start date

`shaynebennetts--load-the-train` (2026-09-10) and `shaynebennetts--pendulum-example`
(2026-09-06) are dated from when each project began, not from when the card was last
edited. Both were in fact edited on 2026-09-12.

This is deliberate, is the instructor's decision, and is the only thing keeping those two
cards below the class's work and the reference example last.

> **If you "correct" these dates to the day you edited them, both cards jump to the top of
> the projector page, above every student.** That is the outcome the dates exist to prevent.
> Leave them alone unless the instructor says otherwise.

Student cards should always carry a truthful `updated`.

---

## Adding or updating a card

1. `git pull` first. Conflicts are only possible if two people edit the same file, which the
   `<github-username>--<slug>.json` naming rule prevents.
2. Edit or create `projects/<github-username>--<slug>.json`; put the picture in `images/`
   under the same base name.
3. `python scripts/build.py` — it validates and names the file and field on any error.
4. **Do not commit `projects.json`.** The Action regenerates it. `build.py` rewrites it
   locally as a side effect of validating, so `git checkout -- projects.json` before you
   commit.
5. Commit the JSON and the image, push, then verify against the live URLs above.

### Validator rules that actually bite

- `blurb` is capped at **400 characters** — the usual first failure.
- `image` must match `images/<name>.(png|jpg|jpeg|gif|webp|mp4|webm)`, must exist in the
  repository, and must be **under 8 MB**.
- The file name must be lowercase `<github-username>--<slug>.json`, and the part before `--`
  must equal the `github` field, lowercased.
- Unknown fields are rejected outright. The schema is `REQUIRED` + `video_url` in
  `scripts/build.py`; nothing else.

---

## Before putting URLs on a card

`live_url` and `site_url` go on a page that is on the projector in class. Check them first:

```bash
for u in <site_url> <live_url>; do echo "$(curl -s -o /dev/null -w '%{http_code}' "$u")  $u"; done
```

A freshly enabled GitHub Pages site 404s for a few minutes after the repository is pushed.
Wait for the 200 rather than pushing the card and hoping.

---

## Blurbs are the student's words

Course rule, from the tutor guide: Claude drafts, the student edits. Two sentences — what it
does, and one thing that works or surprised them. The blurbs on both `shaynebennetts` cards
are currently Claude's drafts and are still waiting to be replaced.
