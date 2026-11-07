"""Shared helpers for Stage 7 authoring scripts (not part of the product)."""
import re
import build

build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-12"
from build import Lesson, Exercises, q, code  # noqa: E402
import outline  # noqa: E402

register = outline.register
SCRATCH = "/private/tmp/claude-501/-Users-brandon-Documents-Java/9ea7fc9a-c1e9-4ec6-b467-8fe304dbe547/scratchpad"


def cap(name):
    """Real captured tool output (curl, startup logs), saved by the capture step; never typed by hand."""
    return open(f"{SCRATCH}/{name}").read().rstrip("\n")


def fence(text, lang="text"):
    return f"```{lang}\n{text}\n```"
