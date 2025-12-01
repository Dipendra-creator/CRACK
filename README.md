# Leakosint Telegram Bot

Small Telegram bot that queries the Leakosint API and returns formatted results.

IMPORTANT: This repository may be used to query leaked data sources. Use responsibly and only with authorization.

Contents

- [`main.py`](main.py:1) - bot entrypoint
- [`requirements.txt`](requirements.txt:1)
- [`Dockerfile`](Dockerfile:1)
- [`.env.example`](.env.example:1)

Prerequisites

- Python 3.11+
- Docker (optional)

Quick start (local)

1. Copy env example: cp .env.example .env
2. Fill in `TELEGRAM_BOT_TOKEN` and `LEAKOSINT_API_TOKEN` in `.env`
3. Install deps: pip install -r requirements.txt
4. Run: python main.py

Run with Docker

Build:

docker build -t leakosint-telegram-bot:latest .

Run:

docker run --env-file .env --restart unless-stopped leakosint-telegram-bot:latest

GitHub deployment (what CI will do)

- The provided GitHub Actions workflow (to be added at `.github/workflows/ci.yml`) will build a Docker image and push it to Docker Hub using repository secrets:

  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
  - `TELEGRAM_BOT_TOKEN`
  - `LEAKOSINT_API_TOKEN`

Creating & pushing the repo (example)

git init
git add .
git commit -m "Initial commit — sanitize secrets and add CI"
git branch -M main
git remote add origin https://github.com/<your-username>/leakosint-telegram-bot.git
git push -u origin main

Security & Notes

- Never commit real secrets. Use [`.env.example`](.env.example:1) locally and GitHub Secrets for CI.
- This project sends requests to an external Leakosint API. Verify licensing and legal compliance before use.

Support

If you want, I can (a) create the GitHub repo and push these files, and (b) add the GitHub Actions workflow to build and push to Docker Hub — tell me which GitHub username/org and Docker Hub repo to use.