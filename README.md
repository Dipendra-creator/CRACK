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
🤖 **Generic Data Handling** - Displays ALL data from API, regardless of structure changes

## Bot Commands

- `/start` - Show welcome menu with interactive buttons
- `/help` - Display complete help guide
- `/stats` - View bot statistics and API status
- `/examples` - See search query examples
- `/about` - Learn about the bot and its purpose
- `/privacy` - Privacy and security information

## Contents

- [`main.py`](main.py) - Bot entrypoint with generic data formatter
- [`requirements.txt`](requirements.txt) - Python dependencies
- [`Dockerfile`](Dockerfile) - Docker container configuration
- [`docker-compose.yml`](docker-compose.yml) - Docker Compose setup
- [`.env.example`](.env.example) - Environment variables template
- [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Complete deployment instructions

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

Or use Docker Compose:

```bash
docker-compose up -d
```

## Deployment (24/7 Operation)

⚠️ **Important:** GitHub Actions alone will NOT keep your bot running!

The GitHub Actions workflow (`.github/workflows/deploy.yml`) only **builds and pushes** the Docker image to Docker Hub. To actually run the bot 24/7, you need to deploy it to a hosting platform.

### Quick Deployment Options:

1. **Render.com** (Recommended - FREE) - 5 minutes setup
2. **Railway.app** (FREE $5 credit) - Auto-deploy
3. **Fly.io** (FREE tier) - 3 shared VMs
4. **Your VPS** (Full control) - Best for production
5. **Docker Hub + Server** (Pull and run) - Use existing infrastructure

📖 **Full deployment instructions:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### GitHub Actions

The workflow automatically:
- ✅ Builds Docker image on every push to `main`
- ✅ Pushes to Docker Hub as `dipusharma1122/leakosint_telegram_bot:latest`
- ✅ Supports multi-platform (amd64, arm64)

**Required GitHub Secrets:**
- `DOCKERHUB_USERNAME` - Your Docker Hub username
- `DOCKERHUB_TOKEN` - Your Docker Hub access token

## Creating & pushing the repo

```bash
git init
git add .
git commit -m "Initial commit — sanitize secrets and add CI"
git branch -M main
git remote add origin https://github.com/<your-username>/leakosint_telegram_bot.git
git push -u origin main
```

## Security & Notes

- Never commit real secrets. Use [`.env.example`](.env.example) locally and GitHub Secrets for CI.
- This project sends requests to an external Leakosint API. Verify licensing and legal compliance before use.
- The bot includes comprehensive privacy features and temporary caching only.
- All API data is displayed generically - no hardcoded field expectations.

## Usage Examples

Once the bot is running, you can search for:

- **Email addresses**: `user@example.com`
- **Usernames**: `john_doe`
- **Phone numbers**: `+1234567890` or `918433220261`
- **Names**: `John Smith`

The bot will search across multiple databases and return paginated results with navigation buttons.

### Sample Output

```
📊 Search Results

NumOfDatabase: 2
NumOfResults: 5
free_requests_left: 50
price: 0
search time: 0.0155468

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 HiTeckGroop.in

ℹ️ Info: At the beginning of 2025, a huge leak...

📈 Results: 3

━━━ Record #1 ━━━
• Address: W/O Rakesh Kumar,77rampurgabhana...
• DocNumber: 672811474313
• FatherName: Omwati
• FullName: Rakesh Kumar
• Phone: 918433220261
• Phone2: 918171994779
• Phone3: 917060249537
• Region: AIRTEL UPW;Airtel UP West;JIO UPW
```

## Documentation

- 📖 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - How to deploy the bot 24/7
- 📊 [BOT_UPDATE_SUMMARY.md](BOT_UPDATE_SUMMARY.md) - Generic data handling explanation
- 🔄 [DATA_FLOW_DIAGRAM.md](DATA_FLOW_DIAGRAM.md) - How the bot processes API responses
- ✅ [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures and verification

## Support

For questions or issues, use the `/help` command in the bot or check the interactive help menu via `/start`.

## License

Use responsibly and in compliance with applicable laws and regulations.