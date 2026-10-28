"""Shared check that shipped text carries nothing identifying.

Generic patterns only: email addresses and private-network IPv4 addresses.
Terms specific to one machine go in `.private-terms` at the repo root, one per
line; that file is gitignored so the terms themselves are never published.
"""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = {
    "email address": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "private IPv4": re.compile(
        r"\b(?:10|127|192\.168|172\.(?:1[6-9]|2\d|3[01])|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))"
        r"(?:\.\d{1,3}){1,3}\b"),
}


def local_terms():
    path = os.path.join(REPO, ".private-terms")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [t.strip() for t in fh if t.strip() and not t.startswith("#")]


def problems(text):
    found = [f"{name}: {m.group(0)}" for name, rx in PATTERNS.items() for m in rx.finditer(text)]
    found += [f"private term: {t}" for t in local_terms() if t.lower() in text.lower()]
    return found
