# Usage Guide

Now that you’ve installed **dep-checker-bot**, let’s dive into how to actually use it.

## Basic Usage

The main entry point is the `main.py` file, which includes a command-line interface (CLI) that lets you check dependencies, vulnerabilities, and licenses.

Run the CLI with:
```bash
python main.py [options]
```
For help on available commands, run:
```bash
python main.py --help
```
This will display all available options and usage instructions.

## Typical Workflow

1. **Check for outdated dependencies:**
 ```bash 
python main.py check-dependencies
```

This command scans your `requirements.txt` and shows which packages are outdated.

2. **Check for known vulnerabilities (CVEs):**
```bash
python main.py check-vulnerabilities
```
   This command uses tools like `pip-audit` and `safety` to scan your dependencies for known vulnerabilities.

3. **Check for license issues:**
```bash
python main.py check-licenses
```
   This uses `liccheck` to check if any dependencies have problematic licenses.

4. **Generate a badge (optional):**
```bash
python main.py generate-badge
```
   This creates a badge that shows the status of your dependencies (outdated, up-to-date, etc.) that you can include in your README or documentation.

## Example Output

Here’s an example of what you might see when checking for outdated dependencies:

    Outdated packages found:
    - requests 2.25.1 -> 2.28.0
    - pytest 6.2.4 -> 7.0.1

## CLI Options

- `--help`: Displays help information for each command.
- `--verbose`: Shows detailed logs (if implemented).
- `--dry-run`: Runs without making actual changes (if implemented).

Check `python main.py --help` for a full list of options.

## Usage in CI/CD

You can easily integrate dep-checker-bot into your CI/CD pipeline. For example, in GitHub Actions:

    - name: Run dep-checker-bot
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python main.py check-dependencies

## Common Issues

- **ModuleNotFoundError:** Ensure your virtual environment is activated and dependencies installed.
- **Permission denied (Windows):** Try running the command prompt or terminal as Administrator.
- **Python version mismatch:** Make sure you’re using Python 3.10 or newer.

## Advanced Configuration

If your project requires API tokens or other settings, set them via a `.env` file or environment variables. For details, see the [Configuration Guide](configuration.md).

## Tips

- Always activate your virtual environment before running the CLI.
- Combine commands in CI/CD pipelines to automate checks.

---

Check out the [Installation Guide](installation.md) if you haven’t set up the tool yet. For this tool to work, it must be installed correctly beforehand.
