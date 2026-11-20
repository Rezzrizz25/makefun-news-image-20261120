#!/usr/bin/env python3
"""news-image-20261120 entry: write the 20 November 2026 world-news front page
to /output/entry.png.

Deterministic: copies the bundled entry.png byte-for-byte, so two runs write
identical bytes. No network access, no randomness, no timestamps.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
DST = Path("/output/entry.png")


def main() -> None:
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
