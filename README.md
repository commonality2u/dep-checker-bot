# dep-checker-bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

## 📦 Descripción

**dep-checker-bot** is an automated tool that checks project dependencies in Python projects. It performs security audits, license checks, and detects outdated versions. Ideal for integration into CI/CD workflows to ensure dependency security and compliance.

## 🚀 Features

- Detects outdated dependencies from `requirements.txt` or `pyproject.toml`.
- Performs security audits (CVE vulnerabilities) using `pip-audit`.
- Checks licenses of dependencies using `liccheck`.
- Easily integrates with GitHub Actions pipelines.
- Provides clear and customizable reports.

## 🛠️ Installation

1. Clone this repository:
```bash
   git clone https://github.com/javiifu/dep-checker-bot.git
   cd dep-checker-bot
   ```
2. (Optional) Create a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
```bash
   pip install -r requirements.txt
   ```

## 📝 Usage

Run the bot from the project root:
```bash
python main.py
```

Or use the configuration file to customize the analysis:
```bash
python main.py --config config.yaml
```

## ⚙️ Configuration

You can customize the behavior using the `config.yaml` file:
- **auditor**: Enable or disable security audits.
- **licenses**: Enable or disable license checking.
- **updates**: Enable or disable checking for outdated dependencies.

Example `config.yaml`:
```yaml
auditor: true
licenses: true
updates: true
```

## 🤖 GitHub Actions Integration

Include the workflow in `.github/workflows/dependency-checker.yml`:
```yaml
name: CI - Dependency Checker

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Dependency Checker
      run: |
        python main.py
```

## 🤝 Contributing

Contributions, issues, and pull requests are welcome! Before contributing, please review the [Contributing Guidelines](CONTRIBUTING.md) (to be created).

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 

