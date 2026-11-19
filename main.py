#!/usr/bin/env python3
"""Copy the baked news image to the grader's output folder.

Reads entry.png from this program's own directory and writes the same
bytes to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when the
variable is unset). Standard library only, no network, deterministic.
"""
import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
