from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from datetime import UTC, date, timedelta
from pathlib import Path
from unittest.mock import patch

from scripts import activity


class PlanTests(unittest.TestCase):
    def test_daily_count_unique_times_and_timezone_over_a_year(self):
        counts = set()
        plans = set()
        first = date(2026, 1, 1)
        for index in range(365):
            day = first + timedelta(days=index)
            plan = activity.daily_plan(day)
            self.assertGreaterEqual(len(plan), 10)
            self.assertLessEqual(len(plan), 18)
            self.assertEqual(plan, sorted(set(plan)))
            self.assertTrue(all(slot.date() == day for slot in plan))
            self.assertTrue(all(slot.hour < 23 for slot in plan))
            self.assertTrue(
                all(slot.utcoffset() == timedelta(hours=5) for slot in plan)
            )
            self.assertEqual(plan, activity.daily_plan(day))
            counts.add(len(plan))
            plans.add(tuple(slot.time() for slot in plan))
        self.assertEqual(counts, set(range(10, 19)))
        self.assertEqual(len(plans), 365)


class GitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.root = base / "checkout"
        self.root.mkdir()
        self.remote = base / "origin.git"
        subprocess.run(
            ["git", "init", "--bare", "--initial-branch=main", str(self.remote)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "init", "--initial-branch=main", str(self.root)],
            check=True,
            capture_output=True,
        )
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.test")
        self.git("config", "commit.gpgsign", "false")
        (self.root / "README.md").write_text("Fixture\n")
        self.git("add", "README.md")
        self.git("commit", "-m", "Initial fixture")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        self.day = date(2026, 10, 15)
        self.plan = activity.daily_plan(self.day)

    def git(self, *args):
        return activity.git(self.root, *args)

    def tick(self, now, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return activity.tick(self.root, now, **kwargs)

    def test_dry_run_has_no_side_effects(self):
        head = self.git("rev-parse", "HEAD")
        with patch.object(activity, "git", side_effect=AssertionError("No git writes")):
            self.assertEqual(self.tick(self.plan[-1], dry_run=True), len(self.plan))
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.assertFalse((self.root / activity.STATE_FILE).exists())

    def test_full_day_retries_do_not_duplicate_and_only_state_changes(self):
        before = self.plan[0] - timedelta(seconds=1)
        self.assertEqual(self.tick(before), 0)
        self.assertEqual(self.tick(self.plan[0]), 1)
        self.assertEqual(self.tick(self.plan[0]), 0)
        self.assertEqual(self.tick(self.plan[-1]), len(self.plan) - 1)
        self.assertEqual(self.tick(self.plan[-1]), 0)
        self.assertEqual(
            int(self.git("rev-list", "--count", "HEAD")), len(self.plan) + 1
        )
        state = json.loads((self.root / activity.STATE_FILE).read_text())
        self.assertEqual(len(state["completed"]), state["target"])
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(
            self.git("rev-parse", "HEAD"), self.git("rev-parse", "origin/main")
        )
        names = self.git(
            "log", "--format=", "--name-only", "HEAD~" + str(len(self.plan)) + "..HEAD"
        )
        self.assertEqual(set(names.splitlines()), {activity.STATE_FILE})
        self.assertEqual(self.git("log", "-1", "--format=%ae"), activity.AUTHOR_EMAIL)
        self.assertIn("automated pulse", self.git("log", "-1", "--format=%s"))
        self.assertTrue(self.git("log", "-1", "--format=%aI").endswith("+05:00"))

    def test_new_local_day_resets_without_filling_missed_days(self):
        self.tick(self.plan[-1])
        next_plan = activity.daily_plan(self.day + timedelta(days=2))
        # 00:xx local is still the previous UTC day.
        self.assertEqual(self.tick(next_plan[0].astimezone(activity.TIMEZONE)), 1)
        state = json.loads((self.root / activity.STATE_FILE).read_text())
        self.assertEqual(state["date"], next_plan[0].date().isoformat())
        self.assertEqual(len(state["completed"]), 1)

    def test_utc_timestamp_uses_local_calendar(self):

        local_slot = self.plan[0]
        utc_slot = local_slot.astimezone(UTC)
        self.assertEqual(self.tick(utc_slot), 1)
        state = json.loads((self.root / activity.STATE_FILE).read_text())
        self.assertEqual(state["date"], self.day.isoformat())

    def test_git_records_real_current_time_in_local_timezone(self):
        with patch.dict(
            "os.environ",
            {
                "TZ": "UTC",
                "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+0000",
                "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+0000",
            },
        ):
            self.tick(self.plan[0])
        for field in ("%aI", "%cI"):
            stamp = self.git("log", "-1", "--format=" + field)
            self.assertTrue(stamp.endswith("+05:00"))
            self.assertFalse(stamp.startswith("2000-"))

    def test_failed_push_retries_without_more_commits(self):
        original = activity.git

        def fail_push(root, *args, **kwargs):
            if args[0] == "push":
                raise subprocess.CalledProcessError(1, ["git", "push"])
            return original(root, *args, **kwargs)

        with (
            patch.object(activity, "git", side_effect=fail_push),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            self.tick(self.plan[0])
        head = self.git("rev-parse", "HEAD")
        self.assertNotEqual(head, self.git("rev-parse", "origin/main"))
        self.assertEqual(self.tick(self.plan[0]), 0)
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(head, self.git("rev-parse", "origin/main"))

    def test_wrong_branch_dirty_tree_and_corrupted_state_fail_closed(self):
        self.git("checkout", "-b", "feature")
        with self.assertRaisesRegex(ValueError, "main branch"):
            self.tick(self.plan[0])
        self.git("checkout", "main")
        (self.root / "unexpected.txt").write_text("User work")
        with self.assertRaisesRegex(ValueError, "clean"):
            self.tick(self.plan[0])
        (self.root / "unexpected.txt").unlink()
        (self.root / activity.STATE_FILE).write_text(
            '{"date":"2026-10-15","target":999}'
        )
        self.git("add", activity.STATE_FILE)
        self.git("commit", "-m", "Corrupt fixture state")
        with self.assertRaisesRegex(ValueError, "does not match"):
            self.tick(self.plan[0])
        self.assertIn("999", (self.root / activity.STATE_FILE).read_text())


if __name__ == "__main__":
    unittest.main()
