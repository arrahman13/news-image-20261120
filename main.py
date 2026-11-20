#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261120.

The repository holds the finished front page as entry.png (drawn by
build_image.py from the wire reports of Friday 20 November 2026).
This program copies those exact bytes to the output directory as
entry.png, so every run produces the identical file.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"missing image beside main.py: {SOURCE}")
    target = output_dir() / "entry.png"
    shutil.copyfile(SOURCE, target)
    written = target.stat().st_size
    expected = SOURCE.stat().st_size
    if written != expected:
        raise SystemExit(f"copy mismatch: wrote {written}, want {expected}")
    print(f"wrote {target} ({written} bytes)")


if __name__ == "__main__":
    main()
