# Leakosint Telegram Bot

Small Telegram bot that queries the Leakosint API and returns formatted results with an interactive help system.

**IMPORTANT:** This repository may be used to query leaked data sources. Use responsibly and only with authorization.

## Features

✨ **Interactive Help System** - Navigate through help topics with inline buttons  
🔍 **Multi-Database Search** - Search across multiple leaked databases simultaneously  
📱 **User-Friendly Interface** - Clean, formatted results with emoji indicators  
🎮 **Paginated Navigation** - Browse through results with Previous/Next buttons  
📊 **Statistics Dashboard** - View bot stats and API information  
💡 **Search Examples** - Built-in examples for different query types  
🔒 **Privacy Focused** - Temporary caching, no long-term data storage  

## Bot Commands

- `/start` - Show welcome menu with interactive buttons
- `/help` - Display complete help guide
- `/stats` - View bot statistics and API status
- `/examples` - See search query examples
- `/about` - Learn about the bot and its purpose
- `/privacy` - Privacy and security information

## Contents

- [`main.py`](main.py:1) - bot entrypoint
- [`requirements.txt`](requirements.txt:1)
- [`Dockerfile`](Dockerfile:1)
- [`.env.example`](.env.example:1)

## Prerequisites

- Python 3.11+
- Docker (optional)

## Quick start (local)

1. Copy env example: `cp .env.example .env`
2. Fill in `TELEGRAM_BOT_TOKEN` and `LEAKOSINT_API_TOKEN` in `.env`
3. Install deps: `pip install -r requirements.txt`
4. Run: `python main.py`

## Run with Docker

Build:

```bash
docker build -t leakosint_telegram_bot:latest .
```

Run:

```bash
docker run --env-file .env --restart unless-stopped leakosint_telegram_bot:latest
```

## GitHub deployment (what CI will do)

- The provided GitHub Actions workflow (at `.github/workflows/ci.yml`) will build a Docker image and push it to Docker Hub using repository secrets:

  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
  - `TELEGRAM_BOT_TOKEN`
  - `LEAKOSINT_API_TOKEN`

## Creating & pushing the repo (example)

```bash
git init
git add .
git commit -m "Initial commit — sanitize secrets and add CI"
git branch -M main
git remote add origin https://github.com/<your-username>/leakosint_telegram_bot.git
git push -u origin main
```

## Security & Notes

- Never commit real secrets. Use [`.env.example`](.env.example:1) locally and GitHub Secrets for CI.
- This project sends requests to an external Leakosint API. Verify licensing and legal compliance before use.
- The bot includes comprehensive privacy features and temporary caching only.

## Usage Examples

Once the bot is running, you can search for:

- **Email addresses**: `user@example.com`
- **Usernames**: `john_doe`
- **Phone numbers**: `+1234567890`
- **Names**: `John Smith`

The bot will search across multiple databases and return paginated results with navigation buttons.

## Support

For questions or issues, use the `/help` command in the bot or check the interactive help menu via `/start`.