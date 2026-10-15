#!/usr/bin/env python3
"""Make 10–18 explicitly automated commits per day, at randomly planned times."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Yekaterinburg")
REPOSITORY = "afterburnerr/afterburnerr"
AUTHOR_EMAIL = "123447337+afterburnerr@users.noreply.github.com"
STATE_FILE = "activity.json"
ROOT = Path(__file__).resolve().parents[1]


def daily_plan(day: date, repository: str = REPOSITORY) -> list[datetime]:
    """Stable per-day randomness; reserve the final hour for delayed runners."""
    seed = hashlib.sha256(f"activity-v1:{repository}:{day}".encode()).digest()
    rng = random.Random(seed)
    count = rng.randint(10, 18)
    midnight = datetime.combine(day, time.min, tzinfo=TIMEZONE)
    return [
        midnight + timedelta(seconds=second)
        for second in sorted(rng.sample(range(23 * 60 * 60), count))
    ]


def read_state(root: Path, plan: list[datetime]) -> dict:
    day = plan[0].date().isoformat()
    path = root / STATE_FILE
    if not path.exists():
        previous = None
    else:
        previous = json.loads(path.read_text())
        if not isinstance(previous, dict) or not isinstance(previous.get("date"), str):
            raise ValueError("Invalid activity state; refusing to overwrite it")
        previous_day = date.fromisoformat(previous["date"])
        if previous_day > plan[0].date():
            raise ValueError("Activity state is from the future")
        if previous_day < plan[0].date():
            previous = None
    if previous is None:
        return {
            "date": day,
            "timezone": str(TIMEZONE),
            "target": len(plan),
            "completed": [],
        }
    if previous.get("timezone") != str(TIMEZONE) or previous.get("target") != len(plan):
        raise ValueError("Activity plan does not match stored state")
    records = previous.get("completed")
    if not isinstance(records, list):
        raise TypeError("Invalid completed activity records")
    slots = [record["planned_at"] for record in records]
    expected = [slot.isoformat() for slot in plan]
    if len(set(slots)) != len(slots) or slots != expected[: len(slots)]:
        raise ValueError("Stored activity slots do not match the daily plan")
    return previous


def git(root: Path, *args: str, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )
    return result.stdout.strip()


def tick(root: Path, now: datetime, *, dry_run: bool = False) -> int:
    if now.utcoffset() is None:
        raise ValueError("Current time must include a timezone")
    now = now.astimezone(TIMEZONE)
    plan = daily_plan(now.date())
    if not dry_run:
        if git(root, "branch", "--show-current") != "main":
            raise ValueError("Run activity.py only on the main branch")
        if git(root, "status", "--porcelain"):
            raise ValueError("Working tree must be clean before running activity.py")
        git(root, "fetch", "origin", "main")
        git(root, "merge", "--ff-only", "origin/main")
    state = read_state(root, plan)
    completed = len(state["completed"])
    due = [slot for slot in plan[completed:] if slot <= now]
    print(
        json.dumps(
            {
                "date": state["date"],
                "timezone": str(TIMEZONE),
                "target": len(plan),
                "completed": completed,
                "due": [slot.isoformat() for slot in due],
                "dry_run": dry_run,
            },
            indent=2,
        )
    )
    if dry_run:
        return len(due)
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "afterburnerr",
        "GIT_AUTHOR_EMAIL": AUTHOR_EMAIL,
        "GIT_COMMITTER_NAME": "afterburnerr",
        "GIT_COMMITTER_EMAIL": AUTHOR_EMAIL,
        "TZ": str(TIMEZONE),
    }
    # Never inherit a backdated timestamp from the caller's environment.
    env.pop("GIT_AUTHOR_DATE", None)
    env.pop("GIT_COMMITTER_DATE", None)
    for slot in due:
        state["completed"].append(
            {"planned_at": slot.isoformat(), "executed_at": now.isoformat()}
        )
        (root / STATE_FILE).write_text(json.dumps(state, indent=2) + "\n")
        git(root, "add", "--", STATE_FILE)
        git(
            root,
            "commit",
            "-m",
            f"chore(activity): automated pulse {slot:%Y-%m-%d %H:%M:%S}",
            env=env,
        )
    # Also retry a previous failed push when there are no newly due slots.
    if git(root, "rev-list", "--count", "origin/main..HEAD") != "0":
        git(root, "push", "origin", "HEAD:main")
    return len(due)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print due slots without changing anything",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Print today's full plan without changing anything",
    )
    args = parser.parse_args()
    now = datetime.now(TIMEZONE)
    if args.plan:
        print("\n".join(slot.isoformat() for slot in daily_plan(now.date())))
    else:
        tick(ROOT, now, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
