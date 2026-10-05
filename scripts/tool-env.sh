#!/usr/bin/env bash
# Source this file before invoking the pinned TH03 headless analyzer by hand.

th03_repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export GHIDRA_HOME="$th03_repo_root/.tools/ghidra"
export JAVA_HOME="$th03_repo_root/.tools/jdk"
export XDG_CONFIG_HOME="$th03_repo_root/.analysis/ghidra/config"
export XDG_CACHE_HOME="$th03_repo_root/.analysis/ghidra/cache"
export XDG_DATA_HOME="$th03_repo_root/.analysis/ghidra/data"
export PATH="$GHIDRA_HOME/support:$JAVA_HOME/bin:$PATH"
unset th03_repo_root

# All local tool invocations are headless.
export DISPLAY=""
export WAYLAND_DISPLAY=""
export JAVA_TOOL_OPTIONS="-Djava.awt.headless=true"
