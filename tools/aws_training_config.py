# SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
# SPDX-License-Identifier: MIT

"""Load and validate this repository's non-secret operator configuration."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import re
import sys
import tomllib
from types import MappingProxyType
from typing import Any, Mapping


CONFIG_ENVIRONMENT_VARIABLE = "AWS_TRAINING_CONFIG"
DEFAULT_CONFIG_FILENAME = ".aws-training.local.toml"
DEFAULT_STATE_DIRECTORY_NAME = "aws-training"
SUPPORTED_SCHEMA_VERSION = 1


class ConfigError(ValueError):
    """Raised when operator-local configuration is absent or invalid."""


class UnsupportedSchemaVersionError(ConfigError):
    """Raised when configuration uses an unsupported contract version."""


@dataclass(frozen=True)
class AwsProfiles:
    """Named AWS CLI profiles; credential-provider details remain external."""

    operator: str
    maintainer_recovery: str | None = None
    examiner: str | None = None
    drillmaster: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {
            "operator": self.operator,
            "maintainer_recovery": self.maintainer_recovery,
            "examiner": self.examiner,
            "drillmaster": self.drillmaster,
        }


@dataclass(frozen=True)
class TrainingConfig:
    """Normalized, validated operator-local parameters."""

    schema_version: int
    repository_root: Path
    source_path: Path
    expected_account_id: str
    account_label: str | None
    primary_region: str
    profiles: AwsProfiles
    resource_prefix: str
    resource_tags: Mapping[str, str]
    require_free_plan: bool
    max_out_of_pocket_usd: int | float
    state_directory: Path

    def as_dict(self) -> dict[str, Any]:
        """Return normalized values using JSON-compatible types."""

        return {
            "schema_version": self.schema_version,
            "repository_root": str(self.repository_root),
            "source_path": str(self.source_path),
            "aws": {
                "expected_account_id": self.expected_account_id,
                "account_label": self.account_label,
                "primary_region": self.primary_region,
                "profiles": self.profiles.as_dict(),
            },
            "resources": {
                "prefix": self.resource_prefix,
                "tags": dict(self.resource_tags),
            },
            "cost": {
                "require_free_plan": self.require_free_plan,
                "max_out_of_pocket_usd": self.max_out_of_pocket_usd,
            },
            "state": {"directory": str(self.state_directory)},
        }


def find_repository_root(start: Path | None = None) -> Path:
    """Find the Git working-tree root containing this training repository."""

    candidate = (start or Path(__file__)).resolve()
    if candidate.is_file():
        candidate = candidate.parent

    for directory in (candidate, *candidate.parents):
        if (directory / ".git").exists() and (directory / "CODEX.md").is_file():
            return directory

    raise ConfigError(
        f"cannot locate the aws-training repository root from {candidate}"
    )


def load_config(
    config_path: str | Path | None = None,
    *,
    repository_root: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> TrainingConfig:
    """Load and validate the shared TOML contract without contacting AWS."""

    root = (repository_root or find_repository_root()).resolve()
    environment = os.environ if environ is None else environ
    source = _resolve_config_path(config_path, root, environment)

    try:
        with source.open("rb") as config_file:
            document = tomllib.load(config_file)
    except FileNotFoundError as error:
        raise ConfigError(
            f"configuration file not found: {source}; initialize it with "
            "'cp .aws-training.example.toml .aws-training.local.toml'"
        ) from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"invalid TOML in {source}: {error}") from error
    except OSError as error:
        raise ConfigError(
            f"cannot read configuration file {source}: {error}"
        ) from error

    schema_version = document.get("schema_version")
    if type(schema_version) is not int:
        raise ConfigError("schema_version must be the integer 1")
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        raise UnsupportedSchemaVersionError(
            f"unsupported configuration schema_version {schema_version}; "
            f"supported version is {SUPPORTED_SCHEMA_VERSION}"
        )

    _reject_unknown(
        document,
        {"schema_version", "aws", "resources", "cost", "state"},
        "root",
    )

    aws = _required_table(document, "aws", "root")
    _reject_unknown(
        aws,
        {"expected_account_id", "account_label", "primary_region", "profiles"},
        "aws",
    )
    expected_account_id = _required_string(aws, "expected_account_id", "aws")
    if re.fullmatch(r"[0-9]{12}", expected_account_id) is None:
        raise ConfigError("aws.expected_account_id must contain exactly 12 digits")

    account_label = _optional_string(aws, "account_label", "aws")
    primary_region = _required_string(aws, "primary_region", "aws")

    profiles_table = _required_table(aws, "profiles", "aws")
    _reject_unknown(
        profiles_table,
        {"operator", "maintainer_recovery", "examiner", "drillmaster"},
        "aws.profiles",
    )
    profiles = AwsProfiles(
        operator=_required_string(profiles_table, "operator", "aws.profiles"),
        maintainer_recovery=_optional_string(
            profiles_table, "maintainer_recovery", "aws.profiles"
        ),
        examiner=_optional_string(profiles_table, "examiner", "aws.profiles"),
        drillmaster=_optional_string(
            profiles_table, "drillmaster", "aws.profiles"
        ),
    )

    resources = _required_table(document, "resources", "root")
    _reject_unknown(resources, {"prefix", "tags"}, "resources")
    resource_prefix = _required_string(resources, "prefix", "resources")
    tags_table = _required_table(resources, "tags", "resources")
    if not tags_table:
        raise ConfigError("resources.tags must contain at least one tag")
    resource_tags: dict[str, str] = {}
    for key, value in tags_table.items():
        if not key.strip():
            raise ConfigError("resources.tags keys must be non-empty")
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(f"resources.tags.{key} must be a non-empty string")
        resource_tags[key] = value.strip()

    cost = _required_table(document, "cost", "root")
    _reject_unknown(
        cost, {"require_free_plan", "max_out_of_pocket_usd"}, "cost"
    )
    require_free_plan = cost.get("require_free_plan")
    if not isinstance(require_free_plan, bool):
        raise ConfigError("cost.require_free_plan must be a boolean")

    maximum_cost = cost.get("max_out_of_pocket_usd")
    if (
        isinstance(maximum_cost, bool)
        or not isinstance(maximum_cost, (int, float))
        or not math.isfinite(maximum_cost)
    ):
        raise ConfigError("cost.max_out_of_pocket_usd must be a finite number")
    if maximum_cost < 0:
        raise ConfigError(
            "cost.max_out_of_pocket_usd must be greater than or equal to zero"
        )
    if require_free_plan and maximum_cost != 0:
        raise ConfigError(
            "cost.max_out_of_pocket_usd must be zero when "
            "cost.require_free_plan is true"
        )

    state = document.get("state", {})
    if not isinstance(state, dict):
        raise ConfigError("state must be a TOML table")
    _reject_unknown(state, {"directory"}, "state")
    state_directory = _resolve_state_directory(state, source, root, environment)

    return TrainingConfig(
        schema_version=schema_version,
        repository_root=root,
        source_path=source,
        expected_account_id=expected_account_id,
        account_label=account_label,
        primary_region=primary_region,
        profiles=profiles,
        resource_prefix=resource_prefix,
        resource_tags=MappingProxyType(resource_tags),
        require_free_plan=require_free_plan,
        max_out_of_pocket_usd=maximum_cost,
        state_directory=state_directory,
    )


def _resolve_config_path(
    config_path: str | Path | None,
    repository_root: Path,
    environ: Mapping[str, str],
) -> Path:
    raw_path = config_path
    if raw_path is None:
        configured_path = environ.get(CONFIG_ENVIRONMENT_VARIABLE)
        if configured_path is not None and not configured_path.strip():
            raise ConfigError(f"{CONFIG_ENVIRONMENT_VARIABLE} must not be empty")
        raw_path = configured_path or DEFAULT_CONFIG_FILENAME

    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = repository_root / path
    return path.resolve()


def _resolve_state_directory(
    state: Mapping[str, Any],
    source_path: Path,
    repository_root: Path,
    environ: Mapping[str, str],
) -> Path:
    configured_directory = state.get("directory")
    if configured_directory is not None:
        if (
            not isinstance(configured_directory, str)
            or not configured_directory.strip()
        ):
            raise ConfigError("state.directory must be a non-empty string")
        state_directory = Path(configured_directory).expanduser()
        if not state_directory.is_absolute():
            state_directory = source_path.parent / state_directory
    else:
        xdg_state_home = environ.get("XDG_STATE_HOME")
        if xdg_state_home is not None and not xdg_state_home.strip():
            xdg_state_home = None
        state_home = (
            Path(xdg_state_home).expanduser()
            if xdg_state_home is not None
            else Path.home() / ".local" / "state"
        )
        if not state_home.is_absolute():
            raise ConfigError("XDG_STATE_HOME must resolve to an absolute path")
        state_directory = state_home / DEFAULT_STATE_DIRECTORY_NAME

    resolved_state_directory = state_directory.resolve()
    if _is_within(resolved_state_directory, repository_root):
        raise ConfigError(
            "state.directory must resolve outside the Git working tree: "
            f"{resolved_state_directory}"
        )
    return resolved_state_directory


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def _required_table(
    parent: Mapping[str, Any], key: str, parent_name: str
) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ConfigError(f"{parent_name}.{key} must be a TOML table")
    return value


def _required_string(parent: Mapping[str, Any], key: str, parent_name: str) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{parent_name}.{key} must be a non-empty string")
    return value.strip()


def _optional_string(
    parent: Mapping[str, Any], key: str, parent_name: str
) -> str | None:
    if key not in parent:
        return None
    return _required_string(parent, key, parent_name)


def _reject_unknown(
    table: Mapping[str, Any], allowed: set[str], table_name: str
) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        joined = ", ".join(unknown)
        raise ConfigError(f"unsupported {table_name} field(s): {joined}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="validate and print normalized aws-training configuration"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help=(
            "configuration path relative to the repository root; otherwise use "
            f"${CONFIG_ENVIRONMENT_VARIABLE} or {DEFAULT_CONFIG_FILENAME}"
        ),
    )
    arguments = parser.parse_args(argv)

    try:
        configuration = load_config(arguments.config)
    except UnsupportedSchemaVersionError as error:
        print(f"unsupported configuration schema: {error}", file=sys.stderr)
        return 3
    except ConfigError as error:
        print(f"configuration error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(configuration.as_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
