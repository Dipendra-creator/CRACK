# 🚀 Deploy Your Bot to Render.com - Step by Step

## Your Docker Image is Ready!
✅ Image: `dipusharma1122/leakosint_telegram_bot:latest`
✅ Available on Docker Hub

Now let's deploy it to run 24/7 on Render.com (FREE)

---

## Step-by-Step Instructions

### Step 1: Sign Up / Login to Render.com

1. Go to **https://render.com**
2. Click **"Get Started"** or **"Sign In"**
3. **Sign up with GitHub** (recommended) or use email

### Step 2: Create a New Web Service

1. Once logged in, click the **"New +"** button (top right)
2. Select **"Web Service"** from the dropdown

### Step 3: Choose Deployment Method

You'll see options to deploy. Choose:

**"Deploy an existing image from a registry"**

### Step 4: Configure Your Service

Fill in the following:

**Image URL:**
```
dipusharma1122/leakosint_telegram_bot:latest
```

**Service Details:**
- **Name:** `leakosint-telegram-bot` (or any name you prefer)
- **Region:** Choose closest to you (e.g., Singapore, Frankfurt, Oregon)
- **Instance Type:** Select **"Free"** (or upgrade to paid for 24/7)

### Step 5: Add Environment Variables

Click **"Advanced"** to expand options, then scroll to **"Environment Variables"**

Add these 3 variables:

1. **Variable 1:**
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: `[Your bot token from BotFather]`

2. **Variable 2:**
   - Key: `LEAKOSINT_API_TOKEN`
   - Value: `[Your Leakosint API token]`

3. **Variable 3:**
   - Key: `LEAKOSINT_API_URL`
   - Value: `https://leakosintapi.com/`

**Where to find your tokens:**
- Open your `.env` file in the project
- Copy the values (without quotes)

### Step 6: Deploy!

1. Scroll down and click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Watch the logs - you should see:
   ```
   INFO - Starting Leakosint Telegram Bot...
   INFO - Bot is running and waiting for messages...
   ```

### Step 7: Test Your Bot

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Bot should respond immediately! ✅

---

## Important Notes

### Free Tier Limitations:
- ⚠️ Bot **sleeps after 15 minutes** of inactivity
- ⚠️ Takes **~30 seconds to wake up** on first message after sleep
- ✅ Upgrade to **$7/month** for 24/7 uptime (no sleep)

### Viewing Logs:
1. Go to your Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time bot activity

### Updating Your Bot:
When you push code to GitHub:
1. GitHub Actions builds new image
2. Go to Render dashboard
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Or enable **auto-deploy** in settings

---

## Troubleshooting

### Bot not responding?
1. Check Render logs for errors
2. Verify environment variables are correct
3. Make sure bot token is valid (test with BotFather)

### "Service Unavailable" error?
- Free tier is sleeping
- Send a message and wait 30 seconds
- Or upgrade to paid plan

### Logs show "API Error"?
- Check `LEAKOSINT_API_TOKEN` is correct
- Verify `LEAKOSINT_API_URL` is set

---

## Alternative: Auto-Deploy from GitHub

If you want automatic deployments:

1. In Render, click **"New +"** → **"Web Service"**
2. Select **"Build and deploy from a Git repository"**
3. Connect your GitHub account
4. Select your repository
5. Configure:
   - **Environment:** Docker
   - **Dockerfile Path:** `./Dockerfile`
   - Add environment variables (same as above)
6. Enable **"Auto-Deploy"** in settings

Now every push to `main` branch will auto-deploy! 🎉

---

## Your Environment Variables

Copy these from your `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_token_here
LEAKOSINT_API_TOKEN=your_token_here
LEAKOSINT_API_URL=https://leakosintapi.com/
```

---

## Success Checklist

- [ ] Signed up on Render.com
- [ ] Created Web Service
- [ ] Used Docker image: `dipusharma1122/leakosint_telegram_bot:latest`
- [ ] Added all 3 environment variables
- [ ] Deployed successfully
- [ ] Checked logs (no errors)
- [ ] Tested bot with `/start` command
- [ ] Bot responds ✅

---

## Need Help?

**Check Render Logs:**
1. Dashboard → Your Service → Logs tab
2. Look for errors in red
3. Verify bot started successfully

**Common Issues:**
- Missing environment variables → Add them in Render dashboard
- Wrong token → Update in environment variables
- Bot sleeping → Wait 30 seconds or upgrade to paid

---

**Your bot will be live in 2-3 minutes after deployment!** 🚀

**Free tier:** Bot sleeps after 15min inactivity
**Paid tier ($7/mo):** Bot runs 24/7 without sleeping
