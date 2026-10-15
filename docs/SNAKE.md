# Contribution snake

`.github/workflows/snake.yml` generates an animated SVG from the repository owner's
GitHub contribution calendar with [Platane/snk](https://github.com/Platane/snk).
The orange snake matches the profile wordmark and supports light and dark themes.

The workflow runs daily at **03:23 UTC (08:23 Yekaterinburg)**, can be started with
**Actions → Contribution snake → Run workflow**, and runs when its workflow file
changes on `main`. Scheduled runs can be delayed by GitHub.

Generated files live on the separate `snake` branch:

- `github-snake.svg` — light theme.
- `github-snake-dark.svg` — dark theme.

Only changed SVGs create a commit, attributed to `github-actions[bot]`. The workflow
does not create user contributions. It uses the built-in `GITHUB_TOKEN` through
checkout's persisted credentials; no personal access token is required. Publishing
uses a normal push to `snake`, preserving its history and leaving `main` untouched.

Actions are pinned to official release commits: checkout `v7.0.1` and the SVG-only
snake action `v3.5.0`. Both were resolved through the official GitHub API.

The image URLs for the profile README are:

```text
https://raw.githubusercontent.com/afterburnerr/afterburnerr/snake/github-snake.svg
https://raw.githubusercontent.com/afterburnerr/afterburnerr/snake/github-snake-dark.svg
```

They become available after the first successful run. A missing image is usually
explained by the latest workflow log or a missing `snake` branch. If publishing is
denied, check repository Actions permissions and rules applying to that branch.
