#!/usr/bin/env python3
"""Six Words, One Story - make.fun entry (program/v1).

Writes one complete story in exactly six words to /output/entry.txt.

The story is picked by scoring a shortlist against the judge brief,
in the brief's own order of importance:
  1. a complete story in exactly six words,
  2. a turn, a surprise, or a whole life implied,
  3. every word earning its place,
  4. clean rhythm when read aloud,
  5. something left unsaid for the reader to fill in.
"""

import sys
from pathlib import Path

# (text, complete, twist, tight, rhythm, unsaid) - each scored 0-5.
CANDIDATES = [
    ("Came home early. She wasn't alone.", 5, 5, 5, 5, 5),
    ("He proposed. She paused. Then left.", 4, 4, 5, 4, 4),
    ("Funeral over, her phone rang: him.", 4, 5, 4, 3, 5),
    ("She kept his letters. He never wrote.", 4, 4, 4, 4, 4),
    ("The lighthouse blinked. Nobody came home.", 4, 3, 4, 4, 4),
    ("She waited years. He married Tuesday.", 4, 4, 4, 4, 4),
]

# Weights follow the judge brief: completeness first, then the turn,
# then tightness, rhythm, and what is left unsaid.
WEIGHTS = (5, 4, 3, 2, 1)


def word_count(text):
    """Count words the way a reader does: split on whitespace."""
    return len(text.split())


def is_valid_entry(text):
    """The sealed gate: UTF-8 text, 1-60 chars, exactly six words."""
    if not text or not text.strip():
        return False
    if not 1 <= len(text) <= 60:
        return False
    return word_count(text) == 6


def score(candidate):
    """Weighted score of one candidate against the five criteria."""
    _, complete, twist, tight, rhythm, unsaid = candidate
    marks = (complete, twist, tight, rhythm, unsaid)
    return sum(mark * weight for mark, weight in zip(marks, WEIGHTS))


def pick_story(candidates):
    """Return the highest-scoring candidate that passes the gate."""
    valid = [c for c in candidates if is_valid_entry(c[0])]
    if not valid:
        raise SystemExit("no candidate passes the six-word gate")
    return max(valid, key=score)[0]


def output_path():
    """The grader mounts /output; fall back to a local folder to test."""
    try:
        Path("/output").mkdir(parents=True, exist_ok=True)
        return Path("/output/entry.txt")
    except OSError:
        local = Path(__file__).resolve().parent / "output"
        local.mkdir(parents=True, exist_ok=True)
        return local / "entry.txt"


def main():
    story = pick_story(CANDIDATES)
    target = output_path()
    target.write_text(story, encoding="utf-8")
    print(f"wrote {word_count(story)} words to {target}: {story}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
