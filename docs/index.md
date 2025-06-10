# Welcome to dep-checker-bot Documentation

Hey there! 👋 Welcome to the official documentation for **dep-checker-bot** — a handy tool to keep your Python project’s dependencies in check.

## What’s dep-checker-bot?

`dep-checker-bot` is a Python script that helps you stay on top of your dependencies. It scans your `requirements.txt` (or `pyproject.toml`), checks if any packages are outdated, and even flags known vulnerabilities (CVEs) and license issues. It’s a straightforward way to make sure your project stays secure and up to date.

## Why should I use it?

- 🔍 Checks for outdated dependencies in your project.
- 🛡️ Warns you about known security vulnerabilities (using `pip-audit` and `safety`).
- 📑 Flags potential license problems (using `liccheck`).
- 🤖 Automatically generates badges and pull requests.
- 🛠️ Built with a modular architecture, so it’s easy to maintain and extend.

## What’s in this documentation?

- [Installation](installation.md): How to get everything set up.
- [Usage](usage.md): How to actually use the tool.
- [Configuration](configuration.md): Tweak things to fit your workflow.
- [Contributing](contributing.md): Wanna help out? Start here!

## Quickstart

Make sure you’re using Python 3.10 (or newer). Then install the dependencies:

```bash
pip install -r requirements.txt
```

And you’re ready to roll.
## Questions?

If you run into any issues or have questions, open an issue on GitHub or start a discussion. We’re happy to help.

Thank you and enjoy!!