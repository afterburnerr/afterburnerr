# Daily activity

[`scripts/activity.py`](../scripts/activity.py) makes **10–18 automated commits per calendar day** in `Asia/Yekaterinburg` (UTC+5), in this repository's `main` branch. Commits update only `activity.json`; messages explicitly label them as automation. Nothing is backdated and no access token is stored in the repository.

A stable random plan is derived from the date and repository name. A new date gets a new count and new times between 00:00 and 23:00. The final hour gives delayed jobs time to finish. The committed state prevents duplicate commits when a workflow is retried or started manually. The state keeps only today's records; previous days remain in Git history.

[The workflow](../.github/workflows/activity.yml) checks due times twice an hour, at :17 and :47 UTC. Overdue slots from the current day are committed together. Thus actual commits land on workflow runs, not at exact second-level timestamps in the plan. The first run can catch up on today's earlier slots. After a completely missed day, the script starts a new plan; it does not fabricate past commits.

GitHub can delay or drop scheduled runs, so 10–18 is the daily target when Actions is available, not a guaranteed service level. [GitHub schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

The author uses the account's verified GitHub `noreply` address. GitHub may take up to 24 hours to show eligible commits in the contribution graph. [GitHub contribution requirements](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference).

## Commands

Python 3.11+ with the standard library is sufficient; no packages to install.

```bash
python3 scripts/activity.py --plan
python3 scripts/activity.py --dry-run
# Creates due commits and pushes main; requires a clean checkout and Git credentials:
python3 scripts/activity.py
# Starts the same job remotely:
gh workflow run activity.yml --repo afterburnerr/afterburnerr
# Stops future scheduled commits:
gh workflow disable activity.yml --repo afterburnerr/afterburnerr
```

Development checks:

```bash
python3 -m unittest discover -s tests -v
uvx ruff check scripts tests
uvx ruff format --check scripts tests
uvx ty check scripts tests
```
