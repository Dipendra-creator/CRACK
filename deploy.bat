@echo off
REM Quick Deployment Script for Leakosint Telegram Bot (Windows)
REM This script helps you deploy the bot to various platforms

echo ================================================================
echo      Leakosint Telegram Bot - Quick Deployment Script
echo ================================================================
echo.

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo .env file created. Please edit it with your tokens:
    echo    - TELEGRAM_BOT_TOKEN
    echo    - LEAKOSINT_API_TOKEN
    echo.
    pause
)

echo Environment variables will be loaded from .env
echo.

REM Deployment options menu
echo Choose deployment method:
echo.
echo 1^) Docker Compose (Local/VPS)
echo 2^) Docker Run (Local/VPS)
echo 3^) Python (Local)
echo 4^) Render.com (Cloud - FREE)
echo 5^) Railway.app (Cloud - FREE credit)
echo 6^) Fly.io (Cloud - FREE tier)
echo 7^) View Deployment Guide
echo 8^) Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto docker_compose
if "%choice%"=="2" goto docker_run
if "%choice%"=="3" goto python
if "%choice%"=="4" goto render
if "%choice%"=="5" goto railway
if "%choice%"=="6" goto flyio
if "%choice%"=="7" goto guide
if "%choice%"=="8" goto exit
goto invalid

:docker_compose
echo.
echo Deploying with Docker Compose...
echo.
docker-compose up -d --build
echo.
echo Bot deployed!
echo.
echo View logs:
echo    docker-compose logs -f
echo.
echo Stop bot:
echo    docker-compose down
goto end

:docker_run
echo.
echo Deploying with Docker Run...
echo.
echo Building image...
docker build -t leakosint_telegram_bot:latest .
echo.
echo Starting container...
docker run -d --name leakosint_bot --restart unless-stopped --env-file .env leakosint_telegram_bot:latest
echo.
echo Bot deployed!
echo.
echo View logs:
echo    docker logs -f leakosint_bot
echo.
echo Stop bot:
echo    docker stop leakosint_bot
echo    docker rm leakosint_bot
goto end

:python
echo.
echo Running with Python...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting bot...
python main.py
goto end

:render
echo.
echo Deploying to Render.com...
echo.
echo Follow these steps:
echo.
echo 1. Go to https://render.com
echo 2. Sign up with GitHub
echo 3. Click 'New +' - 'Web Service'
echo 4. Select your repository
echo 5. Configure:
echo    - Name: leakosint-telegram-bot
echo    - Environment: Docker
echo    - Branch: main
echo 6. Add environment variables from your .env file
echo 7. Click 'Create Web Service'
echo.
echo Your bot will be live in 2-3 minutes!
echo.
pause
goto end

:railway
echo.
echo Deploying to Railway.app...
echo.
echo Follow these steps:
echo.
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Click 'New Project' - 'Deploy from GitHub repo'
echo 4. Select your repository
echo 5. Go to 'Variables' tab and add environment variables from .env
echo 6. Railway auto-deploys!
echo.
echo Your bot will be live in 2-3 minutes!
echo.
pause
goto end

:flyio
echo.
echo Deploying to Fly.io...
echo.
echo Please install Fly CLI first:
echo https://fly.io/docs/hands-on/install-flyctl/
echo.
echo Then run:
echo    flyctl auth login
echo    flyctl launch --no-deploy
echo    flyctl secrets set TELEGRAM_BOT_TOKEN=your_token
echo    flyctl secrets set LEAKOSINT_API_TOKEN=your_token
echo    flyctl deploy
echo.
pause
goto end

:guide
echo.
type DEPLOYMENT_GUIDE.md
echo.
pause
goto end

:exit
echo.
echo Goodbye!
exit /b 0

:invalid
echo.
echo Invalid choice!
pause
exit /b 1

:end
echo.
echo ================================================================
echo                 Deployment Complete!
echo ================================================================
echo.
echo Test your bot by sending /start in Telegram!
echo.
pause
