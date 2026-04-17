#!/usr/bin/env python3
"""
qmd_refresh.py — refresh the QMD index for the Agent Memory vault.

Stdout contract:
- `status: success | qmd_update: done | qmd_embed: done`
- `status: failed | step: <update|embed> | stderr: <first line>`
"""

import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    update = run(["qmd", "update"])
    if update.returncode != 0:
        print(f"status: failed | step: update | stderr: {(update.stderr or '').strip().splitlines()[:1][0] if (update.stderr or '').strip() else 'unknown'}")
        sys.exit(update.returncode)

    embed = run(["qmd", "embed"])
    if embed.returncode != 0:
        print(f"status: failed | step: embed | stderr: {(embed.stderr or '').strip().splitlines()[:1][0] if (embed.stderr or '').strip() else 'unknown'}")
        sys.exit(embed.returncode)

    print("status: success | qmd_update: done | qmd_embed: done")


if __name__ == "__main__":
    main()
