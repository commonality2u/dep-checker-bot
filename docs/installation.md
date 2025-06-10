# Installation Guide

Alright! Let’s get `dep-checker-bot` up and running on your machine. Follow these steps to get started:

## Prerequisites

- 🐍 Python 3.10 or higher installed.
- 💻 Basic knowledge of the command line.
- 📦 `pip` (Python package manager).

## Step 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/dep-checker-bot.git
cd dep-checker-bot
```
*(Replace `yourusername` with your actual GitHub username.)*

## Step 2. Create a Virtual Environment (Recommended)

It’s a good idea to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

## Step 3. Install Dependencies

Now install the dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install all the packages required to run the bot.

## Step 4. Verify Installation

Run the following command to make sure everything is working:

```bash
python main.py --help
```

You should see the help menu with the available commands.

## Troubleshooting

- If you get a `ModuleNotFoundError`, make sure your virtual environment is activated and dependencies are installed.
- If you’re using a different Python version, adjust the commands accordingly.
- For any issues, please open an issue on GitHub.

---

You’re all set! 🚀 Let’s get started with using the bot. Check out the [Usage Guide](usage.md) for details on running your first checks.
```