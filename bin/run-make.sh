#!/usr/bin/env sh
set -eu

# Prefer Poetry when available so project-pinned tool versions are used.
if command -v poetry >/dev/null 2>&1; then
    exec poetry run make "$@"
fi

# Fallback for environments where Poetry is not installed.
exec make "$@"
