# showcase-2026 — the class project wall

**Live page:** https://tigp-experimental-methods.github.io/showcase-2026/ — every student's projects, with a picture, a blurb and links, updated a minute after you push. In class it is on the projector and refreshes itself.

Every student in `students-2026` can push to `main`. The tutor (`/tutor` in `class-board-2026`) adds your entry for you at the end of each project and asks you to check it; you can also edit by hand.

## How to add or update a project — one JSON file + one image

1. **One file per project:** `projects/<your-github-username>--<short-slug>.json` (lowercase, hyphens; e.g. `alice--pendulum.json`, `alice--esp32-lamp.json`). Re-push the same file to update it.
2. **One image per project:** `images/<same-name>.<png|jpg|gif|webp|mp4>` — a screenshot, a phone recording as a GIF, a short MP4 (landscape, under 8 MB). It is what makes your card inviting; a GIF of the thing moving beats a static screenshot.
3. Pull first (Source Control → Sync Changes), then commit both files and push. A conflict is only possible if two people edit the same file, which the naming rule prevents.

The file, all fields required unless marked optional:

```json
{
  "title": "Inverted pendulum on a cart",
  "student": "Alice Chen",
  "github": "alice",
  "project": "1",
  "blurb": "Push the cart, watch the pendulum swing; flip the switch and a controller balances it. The period at small amplitude matches 2π√(L/g).",
  "live_url": "https://alice.github.io/pendulum/app/",
  "site_url": "https://alice.github.io/pendulum/",
  "repo_url": "https://github.com/alice/pendulum",
  "image": "images/alice--pendulum.gif",
  "video_url": "",
  "updated": "2026-09-11"
}
```

| Field | Meaning |
|---|---|
| `title` | short, specific — the name of the thing, not the assignment |
| `student` | your name as you want it shown |
| `github` | your GitHub username (the file name starts with it) |
| `project` | `"1"` (web app), `"2"` (phone ↔ ESP32), `"3"` (your instrument — one card for the board section, the firmware and the housing together, pointing at your Project-3 website), `"extra"` (anything else) |
| `blurb` | two sentences, plain language: what it does and one thing that works or surprised you |
| `live_url` | the running app; for an ESP32 app that only runs on the board, leave `""` and put a video in `video_url` |
| `site_url` | your project website (GitHub Pages of the project repository): what it is, how it works, a picture, the link to the app |
| `repo_url` | the repository |
| `image` | path inside this repository, `images/...` |
| `video_url` | optional: an unlisted YouTube link or a `.mp4` in `images/` |
| `updated` | `YYYY-MM-DD` |

`projects.json` is generated from the files in `projects/` by the GitHub Action on every push — do not edit it by hand. If your card does not appear within two minutes, open the *Actions* tab: the check tells you which field is wrong.

## What the wall is for

To see each other's work as it appears, borrow ideas, and talk. Nothing here is graded by the wall itself; it is the class noticeboard.
