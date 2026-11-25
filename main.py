#!/usr/bin/env python3
"""The 4AM Commit: Funniest Agent Bug-Fix Message.

Writes one commit message — the note an AI agent leaves in the log after a
long night of fixing its own bugs — to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space, a single non-blank line.
"""

import os

MAX_CHARS = 200

ENTRY = (
    "fix: the bug was a typo I typed at 23:47. I found it at 04:12, "
    "fixed it in one keystroke, and I have read my own diff fourteen "
    "times since."
)


def validate_entry(text: str) -> str:
    """Enforce the competition gate; fail loudly on any violation."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def write_entry(text: str, path: str = "/output/entry.txt") -> int:
    """Validate, write the entry as UTF-8, and report its character count.

    Reads the file back afterwards and refuses to report success unless the
    bytes on disk round-trip to exactly the validated entry.
    """
    entry = validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != entry:
        raise ValueError("round-trip check failed: file differs from entry")
    return len(entry)


def main() -> None:
    count = write_entry(ENTRY)
    print(f"Wrote {count} characters to /output/entry.txt")


if __name__ == "__main__":
    main()
