@echo off
REM Set GitHub repo owner and secrets for leakosint-telegram-bot
REM Replace YOUR_GH_USERNAME with your GitHub username and replace placeholder tokens before running.

echo dckr_pat_10pA6bPrAh3A2DpYiNcLBkB78b4 | gh secret set DOCKERHUB_TOKEN --repo YOUR_GH_USERNAME/leakosint-telegram-bot
echo your-telegram-token | gh secret set TELEGRAM_BOT_TOKEN --repo YOUR_GH_USERNAME/leakosint-telegram-bot
echo your-leakosint-token | gh secret set LEAKOSINT_API_TOKEN --repo YOUR_GH_USERNAME/leakosint-telegram-bot
echo your-dockerhub-username | gh secret set DOCKERHUB_USERNAME --repo YOUR_GH_USERNAME/leakosint-telegram-bot

REM Optional: create repo via gh and push (if not already done)
REM gh repo create YOUR_GH_USERNAME/leakosint-telegram-bot --public --source=. --remote=origin --push