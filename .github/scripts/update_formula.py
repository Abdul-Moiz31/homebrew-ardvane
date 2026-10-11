#!/usr/bin/env python3
"""Point Formula/ardvane.rb at the latest Ardvane release - only if it is newer and provably built by Ardvane's own
release workflow on main. Prints the new version, or nothing when there is nothing to do.

Trust: every Ardvane release carries a source archive (ardvane-<version>.tar.gz) with a GitHub build-provenance
attestation. It is accepted only if that attestation was signed by Abdul-Moiz31/ardvane/.github/workflows/release.yml
running on refs/heads/main on a GitHub-hosted runner (`gh attestation verify`). A release or tag made any other way -
for example with a stolen token - has no such signature and is refused, as is any version older than the current one.

Standard library + the GitHub CLI (GH_TOKEN with read access).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

REPO = "Abdul-Moiz31/ardvane"
SIGNER = f"{REPO}/.github/workflows/release.yml"
FORMULA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Formula", "ardvane.rb")
VERSION_RE = re.compile(r"\d+\.\d+\.\d+")


def get(url):
    headers = {"User-Agent": "homebrew-ardvane", "Accept": "application/vnd.github+json"}
    if os.environ.get("GH_TOKEN"):     # avoids the low rate limit for anonymous API calls on shared runners
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=300)


def as_tuple(ver):
    return tuple(int(x) for x in ver.split("."))


def formula_version(text):
    m = re.search(r'^\s*url "[^"]*?(' + VERSION_RE.pattern + r')[^"]*"', text, re.M)
    if not m:
        sys.exit("no version in the formula's url")
    return m.group(1)


def verify(path):
    """Fail unless the file was built and signed by Ardvane's release workflow on main."""
    r = subprocess.run(["gh", "attestation", "verify", path, "--repo", REPO, "--signer-workflow", SIGNER,
                        "--source-ref", "refs/heads/main", "--deny-self-hosted-runners"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("refusing this release: its source archive is not signed by Ardvane's release workflow on main\n"
                 + (r.stderr or r.stdout).strip())


def main():
    with get(f"https://api.github.com/repos/{REPO}/releases/latest") as r:
        release = json.load(r)
    tag = release.get("tag_name", "")
    if not re.fullmatch(r"v" + VERSION_RE.pattern, tag):
        sys.exit(f"unexpected release tag: {tag!r}")
    ver = tag[1:]
    with open(FORMULA, encoding="utf-8") as f:
        text = f.read()
    current = formula_version(text)
    if as_tuple(ver) == as_tuple(current):
        return 0
    if as_tuple(ver) < as_tuple(current):
        sys.exit(f"refusing to go back from {current} to {ver}")
    name = f"ardvane-{ver}.tar.gz"
    url = f"https://github.com/{REPO}/releases/download/{tag}/{name}"
    if not any(a.get("name") == name and a.get("browser_download_url") == url for a in release.get("assets", [])):
        print(f"{tag} has no signed source archive ({name}) yet - nothing to do", file=sys.stderr)
        return 0
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, name)
        with get(url) as r, open(path, "wb") as out:
            shutil.copyfileobj(r, out)
        verify(path)
        with open(path, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
    text = re.sub(r'^(\s*)url "[^"]+"', rf'\1url "{url}"', text, count=1, flags=re.M)
    text = re.sub(r'^(\s*)sha256 "[0-9a-f]{64}"', rf'\1sha256 "{sha}"', text, count=1, flags=re.M)
    with open(FORMULA, "w", encoding="utf-8") as f:
        f.write(text)
    print(ver)
    return 0


if __name__ == "__main__":
    sys.exit(main())
