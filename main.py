#!/usr/bin/env python3
"""One Star, Five Stars for the Food — entry builder.

An alien tourist files a one-star review of Earth and still praises the
food. This script squeezes repo entry.txt into that single line, checks it
against the sealed gate (UTF-8, 1..CAP chars, non-blank), then drops the
verdict text where the sandbox expects it.
"""
import json
import os
import sys
from pathlib import Path

CAP = int(os.environ.get("ENTRY_CAP", "200"))  # gate ceiling for this bounty
ARTIFACT = "entry.txt"


def squeeze(raw_bytes):
    """Collapse the review to one physical line; CR and blank leads go."""
    body = raw_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    for cand in body.split("\n"):
        if cand.strip():
            return cand
    return ""


def verdict(review):
    """Return (ok, reason) for the gate: length window and non-blank."""
    if not review:
        return False, "review came back empty after squeezing"
    if len(review) > CAP:
        return False, f"review spans {len(review)} chars, gate ceiling is {CAP}"
    return True, f"{len(review)} chars inside the 1..{CAP} window"


def emit(review, receipt):
    """Hand the artifact to the sandbox dir, defaulting to /output."""
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target.mkdir(parents=True, exist_ok=True)
    (target / ARTIFACT).write_text(review + "\n", encoding="utf-8",
                                   newline="\n")
    print(json.dumps(receipt))
    return 0


def main():
    home = Path(__file__).resolve().parent
    source = home / ARTIFACT
    if not source.is_file():
        print(json.dumps({"ok": False, "why": f"{ARTIFACT} not found beside main.py"}))
        return 1
    review = squeeze(source.read_bytes())
    good, why = verdict(review)
    if not good:
        print(json.dumps({"ok": False, "why": why}))
        return 1
    assert "star" in review.lower(), "review must mention its star verdict"
    sentences = len([s for s in review.replace("!.", ".").split(". ") if s.strip()])
    return emit(review, {"ok": True, "why": why, "cap": CAP,
                         "sentences": sentences, "head": review[:48]})


if __name__ == "__main__":
    sys.exit(main())
