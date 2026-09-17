# SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DELETE_TEMP_DIR = REPOSITORY_ROOT / "scripts" / "delete-temp-dir.sh"


class DeleteTempDirTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_root_context = tempfile.TemporaryDirectory(
            prefix="aws-training-delete-root-"
        )
        self.addCleanup(temp_root_context.cleanup)
        self.temp_root = Path(temp_root_context.name)

        outside_context = tempfile.TemporaryDirectory(
            prefix="aws-training-delete-outside-"
        )
        self.addCleanup(outside_context.cleanup)
        self.outside_root = Path(outside_context.name)

    def run_helper(
        self, *arguments: object, temp_root: Path | str | None = None
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["TMPDIR"] = str(
            self.temp_root if temp_root is None else temp_root
        )
        return subprocess.run(
            [str(DELETE_TEMP_DIR), *(str(argument) for argument in arguments)],
            cwd=REPOSITORY_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )

    def assert_succeeded(
        self, result: subprocess.CompletedProcess[str]
    ) -> None:
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assert_failed(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_deletes_nested_directory(self) -> None:
        target = self.temp_root / "target"
        nested = target / "nested"
        nested.mkdir(parents=True)
        (target / "file.txt").write_text("top level\n", encoding="utf-8")
        (nested / "file.txt").write_text("nested\n", encoding="utf-8")

        result = self.run_helper(target)

        self.assert_succeeded(result)
        self.assertFalse(target.exists())
        self.assertIn(f"Deleted temp directory: {target}", result.stdout)

    def test_already_absent_target_succeeds(self) -> None:
        target = self.temp_root / "absent"

        result = self.run_helper(target)

        self.assert_succeeded(result)
        self.assertIn(f"Temp directory already absent: {target}", result.stdout)

    def test_does_not_follow_symlink_inside_target(self) -> None:
        sentinel = self.outside_root / "sentinel.txt"
        sentinel.write_text("retain\n", encoding="utf-8")
        target = self.temp_root / "target"
        target.mkdir()
        (target / "outside-link").symlink_to(
            self.outside_root, target_is_directory=True
        )

        result = self.run_helper(target)

        self.assert_succeeded(result)
        self.assertFalse(target.exists())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "retain\n")

    def test_rejects_missing_argument(self) -> None:
        result = self.run_helper()

        self.assert_failed(result)
        self.assertIn("Usage:", result.stderr)

    def test_rejects_multiple_arguments(self) -> None:
        result = self.run_helper(
            self.temp_root / "first", self.temp_root / "second"
        )

        self.assert_failed(result)
        self.assertIn("Usage:", result.stderr)

    def test_rejects_relative_target(self) -> None:
        result = self.run_helper("relative-target")

        self.assert_failed(result)
        self.assertIn("Target path must be absolute", result.stderr)

    def test_rejects_temp_root(self) -> None:
        sentinel = self.temp_root / "sentinel.txt"
        sentinel.write_text("retain\n", encoding="utf-8")

        result = self.run_helper(self.temp_root)

        self.assert_failed(result)
        self.assertIn("Refusing to delete the temp root", result.stderr)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "retain\n")

    def test_rejects_filesystem_root_as_temp_root(self) -> None:
        result = self.run_helper("/tmp/not-used", temp_root="/")

        self.assert_failed(result)
        self.assertIn("Temp root may not be the filesystem root", result.stderr)

    def test_rejects_target_outside_temp_root(self) -> None:
        target = self.outside_root / "target"
        target.mkdir()
        sentinel = target / "sentinel.txt"
        sentinel.write_text("retain\n", encoding="utf-8")

        result = self.run_helper(target)

        self.assert_failed(result)
        self.assertIn("Target is outside the temp root", result.stderr)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "retain\n")

    def test_rejects_regular_file(self) -> None:
        target = self.temp_root / "file.txt"
        target.write_text("retain\n", encoding="utf-8")

        result = self.run_helper(target)

        self.assert_failed(result)
        self.assertIn("Target is not a directory", result.stderr)
        self.assertEqual(target.read_text(encoding="utf-8"), "retain\n")

    def test_rejects_symlink_resolving_outside_temp_root(self) -> None:
        sentinel = self.outside_root / "sentinel.txt"
        sentinel.write_text("retain\n", encoding="utf-8")
        target = self.temp_root / "outside-link"
        target.symlink_to(self.outside_root, target_is_directory=True)

        result = self.run_helper(target)

        self.assert_failed(result)
        self.assertIn("Target is outside the temp root", result.stderr)
        self.assertTrue(target.is_symlink())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "retain\n")

    def test_rejects_nonexistent_temp_root(self) -> None:
        missing_temp_root = self.temp_root / "missing"

        result = self.run_helper(
            missing_temp_root / "target", temp_root=missing_temp_root
        )

        self.assert_failed(result)
        self.assertIn("Temp root is not a directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
