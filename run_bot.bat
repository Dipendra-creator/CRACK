@echo off
echo ================================================================
echo      Running Leakosint Bot from Docker Hub
echo ================================================================
echo.

REM Stop and remove existing container if running
echo Stopping existing container (if any)...
docker stop leakosint_bot 2>nul
docker rm leakosint_bot 2>nul

echo.
echo Pulling latest image from Docker Hub...
docker pull dipusharma1122/leakosint_telegram_bot:latest

echo.
echo Starting bot container...
docker run -d ^
  --name leakosint_bot ^
  --restart unless-stopped ^
  --env-file .env ^
  dipusharma1122/leakosint_telegram_bot:latest

echo.
echo ================================================================
echo      Bot is now running!
echo ================================================================
echo.
echo View logs:
echo    docker logs -f leakosint_bot
echo.
echo Stop bot:
echo    docker stop leakosint_bot
echo.
echo Check status:
echo    docker ps
echo.

pause
