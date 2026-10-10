#!/usr/bin/env python3
"""Point Formula/ardvane.rb at the latest Ardvane release (url + sha256). Prints the new tag, or nothing if current.

Standard library only. Reads GitHub's public API, downloads the release's source archive and hashes it.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request

REPO = "Abdul-Moiz31/ardvane"
FORMULA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Formula", "ardvane.rb")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "homebrew-ardvane", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    tag = json.loads(fetch(f"https://api.github.com/repos/{REPO}/releases/latest"))["tag_name"]
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        sys.exit(f"unexpected release tag: {tag!r}")
    url = f"https://github.com/{REPO}/archive/refs/tags/{tag}.tar.gz"
    with open(FORMULA, encoding="utf-8") as f:
        text = f.read()
    if f'url "{url}"' in text:
        return 0
    sha = hashlib.sha256(fetch(url)).hexdigest()
    text = re.sub(r'url "[^"]+"', f'url "{url}"', text, count=1)
    text = re.sub(r'sha256 "[0-9a-f]{64}"', f'sha256 "{sha}"', text, count=1)
    with open(FORMULA, "w", encoding="utf-8") as f:
        f.write(text)
    print(tag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
