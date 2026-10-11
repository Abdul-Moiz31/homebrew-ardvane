# Homebrew tap for Ardvane

[Ardvane](https://github.com/Abdul-Moiz31/ardvane) protects developers from malware that spreads through code: it scans
your computer, blocks infected clones and pushes, fixes what's safe to fix, and checks every day. Everything runs on
your own computer.

```bash
brew install abdul-moiz31/ardvane/ardvane
ardvane
```

Update with `brew upgrade ardvane`. The formula follows Ardvane's releases automatically: a workflow checks for a new
release every few hours and accepts it only if its source archive is signed by Ardvane's own release workflow on
`main` (GitHub build provenance) and the version goes up. It then installs exactly that formula on a real Mac, checks
that it runs and reports the right version, and only then updates the formula. A release made any other way, for
example with a stolen token, is refused.

Not on a Mac? `pipx install ardvane` works on macOS, Linux and Windows.
