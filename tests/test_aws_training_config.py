# SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from tools.aws_training_config import (
    ConfigError,
    UnsupportedSchemaVersionError,
    find_repository_root,
    load_config,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

VALID_CONFIG = """\
schema_version = 1

[aws]
expected_account_id = "123456789012"
primary_region = "us-east-1"

[aws.profiles]
operator = "operator-profile"

[resources]
prefix = "aws-training"

[resources.tags]
Project = "aws-training"

[cost]
require_free_plan = true
max_out_of_pocket_usd = 0
"""


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory(
            prefix=".aws-training-test-", dir=REPOSITORY_ROOT
        )
        self.addCleanup(temporary_directory.cleanup)
        self.temporary_directory = Path(temporary_directory.name)

    def write_config(self, content: str) -> Path:
        config_path = self.temporary_directory / "config.toml"
        config_path.write_text(content, encoding="utf-8")
        return config_path

    def test_finds_repository_root(self) -> None:
        self.assertEqual(
            find_repository_root(self.temporary_directory), REPOSITORY_ROOT
        )

    def test_tracked_example_is_valid(self) -> None:
        config = load_config(
            REPOSITORY_ROOT / ".aws-training.example.toml",
            repository_root=REPOSITORY_ROOT,
            environ={},
        )

        self.assertEqual(config.schema_version, 1)
        self.assertEqual(config.expected_account_id, "123456789012")
        self.assertEqual(config.profiles.operator, "aws-training-operator")
        self.assertIsNone(config.profiles.examiner)
        self.assertIsNone(config.profiles.drillmaster)
        self.assertTrue(config.require_free_plan)
        self.assertEqual(config.max_out_of_pocket_usd, 0)
        self.assertFalse(
            config.state_directory.is_relative_to(REPOSITORY_ROOT)
        )

    def test_environment_override_and_normalization(self) -> None:
        config_path = self.write_config(VALID_CONFIG)
        config = load_config(
            repository_root=REPOSITORY_ROOT,
            environ={"AWS_TRAINING_CONFIG": str(config_path)},
        )

        self.assertEqual(config.resource_tags, {"Project": "aws-training"})
        self.assertEqual(config.max_out_of_pocket_usd, 0)

    def test_missing_configuration_fails_with_initialization_help(self) -> None:
        missing = self.temporary_directory / "missing.toml"

        with self.assertRaisesRegex(ConfigError, "cp .aws-training.example.toml"):
            load_config(
                missing, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_malformed_toml_is_rejected(self) -> None:
        config_path = self.write_config("[aws\n")

        with self.assertRaisesRegex(ConfigError, "invalid TOML"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_missing_schema_version_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace("schema_version = 1\n\n", "")
        )

        with self.assertRaisesRegex(ConfigError, "schema_version must be"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_unsupported_schema_version_is_distinct(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                "schema_version = 1",
                'schema_version = 2\nfuture_contract_field = "future-value"',
            )
        )

        with self.assertRaisesRegex(
            UnsupportedSchemaVersionError,
            "unsupported configuration schema_version 2",
        ):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_malformed_account_id_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace("123456789012", "1234")
        )

        with self.assertRaisesRegex(ConfigError, "exactly 12 digits"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_empty_region_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                'primary_region = "us-east-1"', 'primary_region = ""'
            )
        )

        with self.assertRaisesRegex(ConfigError, "aws.primary_region"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_empty_profile_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace('operator = "operator-profile"', 'operator = ""')
        )

        with self.assertRaisesRegex(ConfigError, "aws.profiles.operator"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_free_plan_with_positive_ceiling_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                "max_out_of_pocket_usd = 0", "max_out_of_pocket_usd = 1"
            )
        )

        with self.assertRaisesRegex(ConfigError, "must be zero when"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_paid_plan_with_zero_ceiling_is_accepted(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                "require_free_plan = true", "require_free_plan = false"
            )
        )

        config = load_config(
            config_path, repository_root=REPOSITORY_ROOT, environ={}
        )

        self.assertFalse(config.require_free_plan)
        self.assertEqual(config.max_out_of_pocket_usd, 0)

    def test_paid_plan_with_positive_finite_ceiling_is_accepted(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                "require_free_plan = true", "require_free_plan = false"
            )
            .replace("max_out_of_pocket_usd = 0", "max_out_of_pocket_usd = 25.50")
        )

        config = load_config(
            config_path, repository_root=REPOSITORY_ROOT, environ={}
        )

        self.assertEqual(config.max_out_of_pocket_usd, 25.5)

    def test_negative_cost_ceiling_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                "max_out_of_pocket_usd = 0", "max_out_of_pocket_usd = -1"
            )
        )

        with self.assertRaisesRegex(ConfigError, "greater than or equal to zero"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_non_finite_cost_ceiling_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG.replace(
                "max_out_of_pocket_usd = 0", "max_out_of_pocket_usd = inf"
            )
        )

        with self.assertRaisesRegex(ConfigError, "finite number"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_external_state_directory_override_is_resolved(self) -> None:
        external_state = REPOSITORY_ROOT.parent / "aws-training-test-state"
        config_path = self.write_config(
            VALID_CONFIG
            + f'\n[state]\ndirectory = "{external_state}"\n'
        )

        config = load_config(
            config_path, repository_root=REPOSITORY_ROOT, environ={}
        )

        self.assertEqual(config.state_directory, external_state.resolve())
        self.assertFalse(external_state.exists())

    def test_state_directory_inside_working_tree_is_rejected(self) -> None:
        config_path = self.write_config(
            VALID_CONFIG + '\n[state]\ndirectory = "runtime-state"\n'
        )

        with self.assertRaisesRegex(ConfigError, "outside the Git working tree"):
            load_config(
                config_path, repository_root=REPOSITORY_ROOT, environ={}
            )

    def test_relative_xdg_state_home_is_rejected(self) -> None:
        config_path = self.write_config(VALID_CONFIG)

        with self.assertRaisesRegex(ConfigError, "XDG_STATE_HOME"):
            load_config(
                config_path,
                repository_root=REPOSITORY_ROOT,
                environ={"XDG_STATE_HOME": "relative-state"},
            )


if __name__ == "__main__":
    unittest.main()
