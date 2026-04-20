#!/usr/bin/env bash
# Convenience wrapper that runs any command inside the NCS v3.2.0
# toolchain environment (Zephyr SDK, west, ninja, cmake all on PATH).
#
# Usage:
#   tools/ncs.sh west build -b nrf5340dk/nrf5340/cpuapp app -d build -p always
#   tools/ncs.sh west flash -d build
#   tools/ncs.sh bash            # drop into a sub-shell
set -euo pipefail

NCS_VERSION="v3.2.0"
NCS_INSTALL_DIR="${NCS_INSTALL_DIR:-/opt/nordic/ncs/$NCS_VERSION}"
NRFUTIL_BIN="${NRFUTIL_BIN:-$HOME/.nrfutil/bin/nrfutil}"

if [[ ! -x "$NRFUTIL_BIN" ]]; then
    echo "nrfutil not found at $NRFUTIL_BIN" >&2
    exit 1
fi

# ZEPHYR_BASE lets `west build` resolve extension commands even though we
# run from outside the NCS workspace (this app is freestanding).
export ZEPHYR_BASE="$NCS_INSTALL_DIR/zephyr"

exec "$NRFUTIL_BIN" toolchain-manager launch --ncs-version "$NCS_VERSION" -- "$@"
