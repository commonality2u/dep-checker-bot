# Installation Guide

Alright! Let’s get `dep-checker-bot` up and running on your machine. Follow these steps to get started:

## Prerequisites

- 🐍 Python 3.10 or higher installed.
- 💻 Basic knowledge of the command line.
- 📦 `pip` (Python package manager).

## Step 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/javiifu/dep-checker-bot.git
cd dep-checker-bot
```

## Step 2. Create a Virtual Environment (Recommended)

It’s a good idea to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

**Note:** On some systems you might need to use `python3` and `pip3` instead of `python` and `pip`.

## Step 3. Install Dependencies

Now install the dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install all the packages required to run the bot.

## Updating Dependencies

To update dependencies later on, you can run:

```bash
pip install --upgrade -r requirements.txt
```

## Step 4. Verify Installation

Run the following command to make sure everything is working:

```bash
python main.py --help
```

You should see the help menu with the available commands.

## Optional Configuration

If your project requires credentials (for example, GitHub API tokens), create a `.env` file in the root directory or set the necessary environment variables.

## Troubleshooting

- If you get a `ModuleNotFoundError`, make sure your virtual environment is activated and dependencies are installed.
- If you’re using a different Python version, adjust the commands accordingly.
- For any issues, please open an issue on GitHub.

---

You’re all set! 🚀 Let’s get started with using the bot. Check out the [Usage Guide](usage.md) for details on running your first checks.
```