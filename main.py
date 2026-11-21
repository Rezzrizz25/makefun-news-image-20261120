#!/usr/bin/env python3
"""news-image-20261120 entry: write the 20 November 2026 world-news front page
to /output/entry.png.

Deterministic: copies the bundled entry.png byte-for-byte, so two runs write
identical bytes. No network access, no randomness, no timestamps.
"""

import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
DST = Path("/output/entry.png")

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate_png(path: Path) -> None:
    """Verify *path* is a 1024x1024 PNG.

    Checks the 8-byte PNG signature, then parses the IHDR chunk and
    verifies width == 1024 and height == 1024. Raises ValueError with
    a clear message on any mismatch.
    """
    data = path.read_bytes()
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path}: bad PNG signature")
    if len(data) < 33:
        raise ValueError(f"{path}: truncated PNG file (missing IHDR chunk)")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        raise ValueError(f"{path}: missing or malformed IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width != 1024 or height != 1024:
        raise ValueError(
            f"{path}: wrong dimensions {width}x{height}, expected 1024x1024"
        )


def main() -> None:
    try:
        validate_png(SRC)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    try:
        validate_png(DST)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
