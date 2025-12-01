# Deployment Guide - Leakosint Telegram Bot

## Problem
The bot only works when running locally because it needs to be **continuously running** to receive and respond to Telegram messages. GitHub Actions only builds the Docker image but doesn't keep the bot running.

## Solutions

---

## ✅ **Option 1: Deploy to Render.com (Recommended - FREE)**

Render.com offers free hosting for Docker containers. The bot will run 24/7 (with some limitations on free tier).

### Steps:

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Sign up at [Render.com](https://render.com)**
   - Use your GitHub account to sign up

3. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `leakosint_telegram_bot` repository

4. **Configure the Service**
   - **Name**: `leakosint-telegram-bot`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`

5. **Add Environment Variables**
   Click "Advanced" and add:
   - `TELEGRAM_BOT_TOKEN` = `your_bot_token`
   - `LEAKOSINT_API_TOKEN` = `your_api_token`
   - `LEAKOSINT_API_URL` = `https://leakosintapi.com/`

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - Bot will start automatically! 🎉

### Free Tier Limitations:
- ⚠️ Bot sleeps after 15 minutes of inactivity
- ⚠️ Takes ~30 seconds to wake up on first message
- ✅ Upgrade to $7/month for 24/7 uptime

---

## ✅ **Option 2: Deploy to Railway.app (FREE with limitations)**

Railway offers $5 free credit per month.

### Steps:

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variables**
   - Go to "Variables" tab
   - Add:
     - `TELEGRAM_BOT_TOKEN`
     - `LEAKOSINT_API_TOKEN`
     - `LEAKOSINT_API_URL`

4. **Deploy**
   - Railway auto-detects Dockerfile
   - Deployment starts automatically
   - Bot runs 24/7 until credit runs out

### Cost:
- Free $5/month credit
- ~$5-10/month after free credit

---

## ✅ **Option 3: Deploy to Your Own VPS (Best for 24/7)**

If you have a VPS (DigitalOcean, AWS, Linode, etc.), this is the best option.

### Steps:

1. **SSH into your VPS**
   ```bash
   ssh user@your-vps-ip
   ```

2. **Install Docker** (if not installed)
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Clone your repository**
   ```bash
   git clone https://github.com/yourusername/leakosint_telegram_bot.git
   cd leakosint_telegram_bot
   ```

4. **Create .env file**
   ```bash
   nano .env
   ```
   Add:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   LEAKOSINT_API_TOKEN=your_token_here
   LEAKOSINT_API_URL=https://leakosintapi.com/
   ```

5. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

6. **Check logs**
   ```bash
   docker-compose logs -f
   ```

7. **Bot is now running 24/7!** ✅

### To update:
```bash
git pull
docker-compose down
docker-compose up -d --build
```

---

## ✅ **Option 4: Deploy to Fly.io (FREE)**

Fly.io offers free tier with 3 shared VMs.

### Steps:

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Linux/Mac
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Create fly.toml** (already created in repo)

4. **Deploy**
   ```bash
   fly launch
   ```
   - Choose app name
   - Select region
   - Don't deploy database

5. **Set secrets**
   ```bash
   fly secrets set TELEGRAM_BOT_TOKEN=your_token
   fly secrets set LEAKOSINT_API_TOKEN=your_token
   fly secrets set LEAKOSINT_API_URL=https://leakosintapi.com/
   ```

6. **Deploy**
   ```bash
   fly deploy
   ```

7. **Check status**
   ```bash
   fly status
   fly logs
   ```

---

## ✅ **Option 5: Use Docker Hub + Pull on Server**

If you already have a server, you can pull the image from Docker Hub.

### Steps:

1. **GitHub Actions already pushes to Docker Hub** ✅

2. **On your server, pull and run**
   ```bash
   docker pull dipusharma1122/leakosint_telegram_bot:latest
   
   docker run -d \
     --name leakosint_bot \
     --restart unless-stopped \
     -e TELEGRAM_BOT_TOKEN=your_token \
     -e LEAKOSINT_API_TOKEN=your_token \
     -e LEAKOSINT_API_URL=https://leakosintapi.com/ \
     dipusharma1122/leakosint_telegram_bot:latest
   ```

3. **Check logs**
   ```bash
   docker logs -f leakosint_bot
   ```

---

## 🚫 **Why GitHub Actions Alone Doesn't Work**

GitHub Actions is a **CI/CD pipeline**, not a hosting platform:
- ❌ Jobs run for a limited time (max 6 hours)
- ❌ Jobs stop after completion
- ❌ Not designed for long-running services
- ✅ Good for building and pushing images
- ✅ Good for running tests

**Your current workflow** builds the image but doesn't run it anywhere!

---

## 📊 **Comparison**

| Platform | Cost | Uptime | Setup Difficulty | Best For |
|----------|------|--------|------------------|----------|
| **Render.com** | Free (with sleep) | 99% (paid) | ⭐ Easy | Quick start |
| **Railway.app** | $5 free credit | 99.9% | ⭐ Easy | Small projects |
| **Fly.io** | Free tier | 99.9% | ⭐⭐ Medium | Production |
| **VPS** | $5-20/month | 99.9% | ⭐⭐⭐ Hard | Full control |
| **Docker Hub + Server** | Server cost | 99.9% | ⭐⭐ Medium | Existing infra |

---

## 🎯 **Recommended Solution**

For your use case, I recommend **Render.com**:
1. ✅ Free to start
2. ✅ Easy setup (5 minutes)
3. ✅ Auto-deploys on git push
4. ✅ Built-in logging and monitoring
5. ✅ Can upgrade to paid for 24/7

---

## 📝 **Quick Start with Render.com**

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your repo
5. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `LEAKOSINT_API_TOKEN`
   - `LEAKOSINT_API_URL`
6. Click "Create Web Service"
7. **Done!** Bot is live in 2-3 minutes 🚀

---

## 🔧 **Troubleshooting**

### Bot not responding?
```bash
# Check logs on Render
# Go to your service → Logs tab

# Check logs on VPS
docker logs -f leakosint_bot

# Check logs on Railway
# Go to your service → Deployments → View Logs
```

### Environment variables not working?
- Make sure they're set in the platform (not just .env)
- Restart the service after adding variables
- Check for typos in variable names

### Docker image not updating?
```bash
# Force rebuild
docker-compose down
docker-compose pull
docker-compose up -d --force-recreate
```

---

## 🎉 **Success Checklist**

- [ ] Code pushed to GitHub
- [ ] Docker image builds successfully
- [ ] Deployment platform chosen
- [ ] Environment variables set
- [ ] Bot deployed and running
- [ ] Bot responds to /start command
- [ ] Bot can perform searches
- [ ] Logs show no errors

---

## 📞 **Need Help?**

If you're stuck, check:
1. Platform logs for errors
2. Environment variables are correct
3. Bot token is valid
4. API token is valid
5. Network connectivity

---

**Choose your deployment method and follow the steps above. The bot will be running 24/7!** 🚀
