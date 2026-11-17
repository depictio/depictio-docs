#!/usr/bin/env python3
"""Refuse documentation videos over the budget: 30 s and 1.5 MB per clip.

    scripts/check-video-budget.py docs/images/guides/x/clip.mp4 ...

Run by pre-commit on the videos a commit adds or changes. Every published
version of the site keeps the files it shipped with, so a heavy clip costs its
size again each time it changes; short clips also say more. The duration is
read with ffprobe when it is installed, and only the size is checked otherwise.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

MAX_SECONDS = 30.0
MAX_BYTES = int(1.5 * 1024 * 1024)


def duration(path: Path) -> float | None:
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    ).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return None


def main(paths: list[str]) -> int:
    failed = False
    for name in paths:
        path = Path(name)
        size = path.stat().st_size
        seconds = duration(path)
        problems = []
        if size > MAX_BYTES:
            problems.append(f"{size / 1048576:.2f} MB > {MAX_BYTES / 1048576:.1f} MB")
        if seconds is not None and seconds > MAX_SECONDS + 0.5:
            problems.append(f"{seconds:.1f} s > {MAX_SECONDS:.0f} s")
        if problems:
            failed = True
            print(f"{name}: {', '.join(problems)} (re-encode shorter, or raise -crf)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
