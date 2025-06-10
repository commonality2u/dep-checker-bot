# Configuration Guide

Here you’ll find details on how to configure **dep-checker-bot** to fit your project’s needs.

## Environment Variables

If your project requires API keys, tokens, or other credentials (for example, to integrate with the GitHub API), it’s recommended to use environment variables or a `.env` file.

### Using a `.env` File

Create a `.env` file in the root of your project with the following content:

    GITHUB_TOKEN=your_github_token_here

Replace `your_github_token_here` with your actual GitHub personal access token. This token is used by the bot to authenticate with the GitHub API.

### Setting Environment Variables Directly

Alternatively, you can set environment variables directly in your shell or CI/CD environment:

On macOS/Linux:

    export GITHUB_TOKEN=your_github_token_here

On Windows (PowerShell):

    setx GITHUB_TOKEN \"your_github_token_here\"

## Configuration Options

Depending on your implementation, you might have other settings in the `main.py` file, such as:

- `LOG_LEVEL`: Controls the verbosity of the application’s logging.
- `OUTPUT_DIRECTORY`: The directory where reports or badges are generated.

Example `.env` file:

    GITHUB_TOKEN=your_github_token_here
    LOG_LEVEL=INFO
    OUTPUT_DIRECTORY=reports/

## Using Configuration Files

If you need to support complex configurations, consider adding a configuration file like `config.yaml` or `config.json`. For example:

**config.yaml:**

    github_token: your_github_token_here
    log_level: INFO
    output_directory: reports/

Then, in your code, parse this file using a library like `pyyaml` or `json` to load the settings.

## Notes

- Always keep your `.env` file out of version control by adding it to `.gitignore`.
- Never commit your credentials to version control.
- Validate your token’s permissions (e.g. repo scope) to ensure full functionality.
- Keep your configuration consistent across environments to avoid surprises.

## Troubleshooting

- **Authentication errors:** Check that your token has the necessary scopes and that it’s loaded correctly.
- **Missing environment variables:** Ensure your environment variables are set properly in your shell or CI/CD environment. Sometimes a shell restart is required.
- **Configuration file not found:** Make sure the configuration file is named correctly and located in the root of your project or the specified directory.
- **Invalid YAML/JSON:** Validate your config file format to prevent parsing errors.

---

That’s it! 🚀 For help using the tool, check out the [Usage Guide](usage.md).
