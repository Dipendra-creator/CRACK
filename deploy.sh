#!/bin/bash

# Quick Deployment Script for Leakosint Telegram Bot
# This script helps you deploy the bot to various platforms

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Leakosint Telegram Bot - Quick Deployment Script          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your tokens:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - LEAKOSINT_API_TOKEN"
    echo ""
    read -p "Press Enter after you've updated .env file..."
fi

# Source .env
export $(cat .env | grep -v '^#' | xargs)

# Check if tokens are set
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$LEAKOSINT_API_TOKEN" ]; then
    echo "❌ Error: Tokens not set in .env file!"
    echo "Please edit .env and add your tokens."
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

# Deployment options menu
echo "Choose deployment method:"
echo ""
echo "1) 🐳 Docker Compose (Local/VPS)"
echo "2) 🐋 Docker Run (Local/VPS)"
echo "3) 🐍 Python (Local)"
echo "4) ☁️  Render.com (Cloud - FREE)"
echo "5) 🚂 Railway.app (Cloud - FREE credit)"
echo "6) ✈️  Fly.io (Cloud - FREE tier)"
echo "7) 📚 View Deployment Guide"
echo "8) ❌ Exit"
echo ""
read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo ""
        echo "🐳 Deploying with Docker Compose..."
        echo ""
        
        # Check if docker-compose is installed
        if ! command -v docker-compose &> /dev/null; then
            echo "❌ docker-compose not found!"
            echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
            exit 1
        fi
        
        echo "Building and starting container..."
        docker-compose up -d --build
        
        echo ""
        echo "✅ Bot deployed!"
        echo ""
        echo "📊 View logs:"
        echo "   docker-compose logs -f"
        echo ""
        echo "🛑 Stop bot:"
        echo "   docker-compose down"
        ;;
        
    2)
        echo ""
        echo "🐋 Deploying with Docker Run..."
        echo ""
        
        # Check if docker is installed
        if ! command -v docker &> /dev/null; then
            echo "❌ docker not found!"
            echo "Please install Docker: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        echo "Building image..."
        docker build -t leakosint_telegram_bot:latest .
        
        echo "Starting container..."
        docker run -d \
            --name leakosint_bot \
            --restart unless-stopped \
            -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
            -e LEAKOSINT_API_TOKEN="$LEAKOSINT_API_TOKEN" \
            -e LEAKOSINT_API_URL="$LEAKOSINT_API_URL" \
            leakosint_telegram_bot:latest
        
        echo ""
        echo "✅ Bot deployed!"
        echo ""
        echo "📊 View logs:"
        echo "   docker logs -f leakosint_bot"
        echo ""
        echo "🛑 Stop bot:"
        echo "   docker stop leakosint_bot"
        echo "   docker rm leakosint_bot"
        ;;
        
    3)
        echo ""
        echo "🐍 Running with Python..."
        echo ""
        
        # Check if python is installed
        if ! command -v python3 &> /dev/null; then
            echo "❌ python3 not found!"
            echo "Please install Python 3.11+: https://www.python.org/downloads/"
            exit 1
        fi
        
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        echo ""
        echo "Starting bot..."
        python3 main.py
        ;;
        
    4)
        echo ""
        echo "☁️  Deploying to Render.com..."
        echo ""
        echo "📖 Follow these steps:"
        echo ""
        echo "1. Go to https://render.com"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Select your repository"
        echo "5. Configure:"
        echo "   - Name: leakosint-telegram-bot"
        echo "   - Environment: Docker"
        echo "   - Branch: main"
        echo "6. Add environment variables:"
        echo "   - TELEGRAM_BOT_TOKEN = $TELEGRAM_BOT_TOKEN"
        echo "   - LEAKOSINT_API_TOKEN = $LEAKOSINT_API_TOKEN"
        echo "   - LEAKOSINT_API_URL = $LEAKOSINT_API_URL"
        echo "7. Click 'Create Web Service'"
        echo ""
        echo "✅ Your bot will be live in 2-3 minutes!"
        echo ""
        read -p "Press Enter to continue..."
        ;;
        
    5)
        echo ""
        echo "🚂 Deploying to Railway.app..."
        echo ""
        echo "📖 Follow these steps:"
        echo ""
        echo "1. Go to https://railway.app"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Select your repository"
        echo "5. Go to 'Variables' tab and add:"
        echo "   - TELEGRAM_BOT_TOKEN = $TELEGRAM_BOT_TOKEN"
        echo "   - LEAKOSINT_API_TOKEN = $LEAKOSINT_API_TOKEN"
        echo "   - LEAKOSINT_API_URL = $LEAKOSINT_API_URL"
        echo "6. Railway auto-deploys!"
        echo ""
        echo "✅ Your bot will be live in 2-3 minutes!"
        echo ""
        read -p "Press Enter to continue..."
        ;;
        
    6)
        echo ""
        echo "✈️  Deploying to Fly.io..."
        echo ""
        
        # Check if flyctl is installed
        if ! command -v flyctl &> /dev/null; then
            echo "Installing Fly CLI..."
            curl -L https://fly.io/install.sh | sh
            echo ""
            echo "⚠️  Please restart your terminal and run this script again."
            exit 0
        fi
        
        echo "Logging in to Fly.io..."
        flyctl auth login
        
        echo ""
        echo "Launching app..."
        flyctl launch --no-deploy
        
        echo ""
        echo "Setting secrets..."
        flyctl secrets set TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
        flyctl secrets set LEAKOSINT_API_TOKEN="$LEAKOSINT_API_TOKEN"
        flyctl secrets set LEAKOSINT_API_URL="$LEAKOSINT_API_URL"
        
        echo ""
        echo "Deploying..."
        flyctl deploy
        
        echo ""
        echo "✅ Bot deployed to Fly.io!"
        echo ""
        echo "📊 View logs:"
        echo "   flyctl logs"
        echo ""
        echo "📈 Check status:"
        echo "   flyctl status"
        ;;
        
    7)
        echo ""
        echo "📚 Opening Deployment Guide..."
        echo ""
        if [ -f DEPLOYMENT_GUIDE.md ]; then
            cat DEPLOYMENT_GUIDE.md
        else
            echo "❌ DEPLOYMENT_GUIDE.md not found!"
        fi
        echo ""
        read -p "Press Enter to continue..."
        ;;
        
    8)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Deployment Complete! 🎉                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Test your bot by sending /start in Telegram!"
echo ""
