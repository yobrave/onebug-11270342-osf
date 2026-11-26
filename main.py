#!/usr/bin/env python3
"""Entry builder for the One Star, Five Stars for the Food bounty.

Reads entry.txt (the alien tourist's one-star review of Earth), normalizes
it to one line, validates the gate rules (1..200 chars, not blank) and
copies it to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""
import json
import os

MAX_CHARS = int(os.environ.get("ENTRY_MAX_CHARS", "200"))  # this bounty's gate


def normalize(source_text):
    """One line only: strip trailing newlines and stray CR, keep first non-blank."""
    text = source_text.replace("\r", "").rstrip("\n")
    if "\n" in text:
        text = next(ln for ln in text.split("\n") if ln.strip())
    return text


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    try:
        with open(src, "rb") as fh:
            blob = fh.read()
    except FileNotFoundError:
        print(json.dumps({"ok": False, "error": "missing entry.txt"}))
        return 1
    text = normalize(blob.decode("utf-8"))
    if not (1 <= len(text) <= MAX_CHARS):
        print(json.dumps({"ok": False, "error": f"entry must be 1-{MAX_CHARS} chars",
                          "got": len(text)}))
        return 1
    if not text.strip():
        print(json.dumps({"ok": False, "error": "entry must not be blank"}))
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(text)
    print(json.dumps({"ok": True, "chars": len(text), "max": MAX_CHARS,
                      "preview": text[:60]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
