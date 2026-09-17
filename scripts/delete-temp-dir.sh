#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
# SPDX-License-Identifier: MIT

set -o pipefail

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  local command_name="$1"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    die "Required command not found: $command_name"
  fi
}

main() {
  local input_path
  local temp_root_input="${TMPDIR:-/tmp}"
  local temp_root
  local target_path
  local checked_path

  if (($# != 1)); then
    die "Usage: $0 ABSOLUTE_TEMP_DIRECTORY"
  fi
  input_path="$1"

  if [[ "$input_path" != /* ]]; then
    die "Target path must be absolute: $input_path"
  fi

  require_command realpath
  require_command find

  if [[ ! -d "$temp_root_input" ]]; then
    die "Temp root is not a directory: $temp_root_input"
  fi
  if ! temp_root="$(realpath -e -- "$temp_root_input")"; then
    die "Could not resolve temp root: $temp_root_input"
  fi
  if [[ "$temp_root" == / ]]; then
    die "Temp root may not be the filesystem root"
  fi

  if ! target_path="$(realpath -m -- "$input_path")"; then
    die "Could not resolve target path: $input_path"
  fi
  if [[ "$target_path" == "$temp_root" ]]; then
    die "Refusing to delete the temp root: $temp_root"
  fi
  case "$target_path" in
    "$temp_root"/*) ;;
    *)
      die "Target is outside the temp root: $target_path"
      ;;
  esac

  if [[ ! -e "$target_path" && ! -L "$target_path" ]]; then
    printf 'Temp directory already absent: %s\n' "$target_path"
    return 0
  fi
  if [[ ! -d "$target_path" ]]; then
    die "Target is not a directory: $target_path"
  fi

  if ! checked_path="$(realpath -e -- "$target_path")"; then
    die "Could not recheck target path: $target_path"
  fi
  if [[ "$checked_path" != "$target_path" ]]; then
    die "Target path changed while it was checked: $target_path"
  fi
  case "$checked_path" in
    "$temp_root"/*) ;;
    *)
      die "Rechecked target is outside the temp root: $checked_path"
      ;;
  esac

  if ! find -P "$checked_path" -xdev -depth -delete; then
    die "Could not delete temp directory: $checked_path"
  fi
  if [[ -e "$checked_path" || -L "$checked_path" ]]; then
    die "Temp directory still exists after deletion: $checked_path"
  fi

  printf 'Deleted temp directory: %s\n' "$checked_path"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
