"""The Router Confesses.

Writes one line in which a home Wi-Fi router excuses itself for
dropping the connection at the climax of a movie, to /output/entry.txt.
Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "I watched the ending before you did, and honestly, you're better off not knowing."

MAX_CHARS = 200


def main():
    # Empty string counts as unset: fall back to the default output dir.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate: 1-200 chars, single line, not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print("gate failed: line is %d chars, over %d" % (len(LINE), MAX_CHARS),
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    # Second verification: the file must be exactly one line with no
    # trailing whitespace (a trailing newline or stray space would fail
    # the single-line gate even when the byte check above passes).
    lines = text.splitlines()
    if len(lines) != 1 or lines[0] != LINE or lines[0] != lines[0].rstrip():
        print("verification failed: file is not exactly one clean line",
              file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
