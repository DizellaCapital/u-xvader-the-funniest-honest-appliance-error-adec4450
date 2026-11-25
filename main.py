#!/usr/bin/env python3
"""The Funniest Honest Appliance Error — entry program.

Writes one line (at most 200 characters): the funniest honest error
message an appliance could show. The line is written to
$MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output/entry.txt),
then read back and validated against the gate in RULES.txt.
"""

import os
import sys

LINE = "Error: cooling failed. The light still works. I am now a cupboard with a lightbulb."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Read back and validate: UTF-8, 1-200 characters, not only whitespace.
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    entry = text.rstrip("\n")
    if not (1 <= len(entry) <= 200):
        print(f"INVALID: entry is {len(entry)} characters (must be 1-200)", file=sys.stderr)
        return 1
    if not entry.strip():
        print("INVALID: entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in entry or "\r" in entry:
        print("INVALID: entry must be a single line", file=sys.stderr)
        return 1
    if entry != LINE:
        print("INVALID: read-back does not match the entry line", file=sys.stderr)
        return 1

    print(f"OK: wrote {len(entry)} of max 200 characters to {path}")
    print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
