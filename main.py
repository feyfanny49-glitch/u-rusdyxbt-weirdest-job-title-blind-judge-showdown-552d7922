#!/usr/bin/env python3
"""Write and verify the judged text artifact for the Weirdest Job Title contest.

House gate: /output/entry.txt must be UTF-8 text, 1..60 characters, not only
whitespace. We write exactly the entry bytes (no trailing newline, no BOM),
atomically via a temp file + os.replace, then read the file back and re-check
every gate condition against the bytes actually on disk before reporting success.
"""

import hashlib
import os
import tempfile

ENTRY = "Houseplant Divorce Mediator"
OUTPUT = "/output/entry.txt"


def validate(data: bytes) -> str:
    """Return the decoded text, or raise if the bytes fail any gate rule."""
    text = data.decode("utf-8")  # rejects invalid UTF-8 (and a surprise BOM body)
    if not data:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if not 1 <= len(text) <= 60:
        raise ValueError(f"entry is {len(text)} chars, must be 1..60")
    if data.endswith((b"\n", b"\r")):
        raise ValueError("entry must not end with a newline")
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("entry must not carry a UTF-8 BOM")
    return text


def main() -> None:
    data = ENTRY.encode("utf-8")
    validate(data)  # fail before writing if the source text is invalid

    out_dir = os.path.dirname(OUTPUT)
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, OUTPUT)  # atomic: the grader never sees a partial file
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

    # Improvement over the first version: verify what is actually on disk.
    with open(OUTPUT, "rb") as handle:
        on_disk = handle.read()
    text = validate(on_disk)
    if on_disk != data:
        raise ValueError("on-disk bytes differ from the intended entry")

    digest = hashlib.sha256(on_disk).hexdigest()
    print(f"entry : {text}")
    print(f"file  : {OUTPUT}")
    print(f"bytes : {len(on_disk)}  chars: {len(text)}  (gate: 1..60, UTF-8)")
    print(f"newline at end: no   BOM: no   atomic write: yes")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
