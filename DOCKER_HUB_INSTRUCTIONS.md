Docker Hub — repository creation & access token instructions
=============================================================

This document shows step-by-step instructions to create a Docker Hub repository, generate an access token, test login locally, and configure GitHub Actions secrets so the workflow at `.github/workflows/ci.yml` can push images.

1) Create a Docker Hub repository (Web UI)
- Sign in at https://hub.docker.com
- Click "Create Repository" (top-right or Repositories -> Create Repository)
- Repository name: leakosint_telegram_bot
- Visibility: Public (or Private if you prefer)
- Click "Create"

2) Generate a Docker Hub access token (Web UI)
- Click your avatar → Account Settings → Security
- Under "Access Tokens" click "New Access Token"
- Give it a descriptive name (e.g., "github-actions-ci")
- Copy the token value shown (this is the only time you'll see it). Treat it like a password.

3) Test Docker login locally
- Locally, run:
  - `echo "YOUR_DOCKERHUB_TOKEN" | docker login --username YOUR_DOCKERHUB_USERNAME --password-stdin`
- If successful, you can push images manually:
  - `docker tag leakosint_telegram_bot:local YOUR_DOCKERHUB_USERNAME/leakosint_telegram_bot:latest`
  - `docker push YOUR_DOCKERHUB_USERNAME/leakosint_telegram_bot:latest`

4) Configure GitHub repository secrets (so Actions can log in)
- On GitHub → your repo → Settings → Secrets and variables → Actions → New repository secret
- Add:
  - `DOCKERHUB_USERNAME` → your Docker Hub username
  - `DOCKERHUB_TOKEN` → the token from step (2)
- Also add:
  - `TELEGRAM_BOT_TOKEN`
  - `LEAKOSINT_API_TOKEN`

CLI alternative using gh (GitHub CLI)
- Create secrets via CLI:
  - `echo "your-telegram-token" | gh secret set TELEGRAM_BOT_TOKEN --repo YOUR_GH_USERNAME/leakosint_telegram_bot`
  - `echo "your-leakosint-token" | gh secret set LEAKOSINT_API_TOKEN --repo YOUR_GH_USERNAME/leakosint_telegram_bot`
  - `echo "dockerhub-username" | gh secret set DOCKERHUB_USERNAME --repo YOUR_GH_USERNAME/leakosint_telegram_bot`
  - `echo "dockerhub-token" | gh secret set DOCKERHUB_TOKEN --repo YOUR_GH_USERNAME/leakosint_telegram_bot`

5) Notes for GitHub Actions (the provided workflow)
- The workflow uses `docker/login-action` which requires `username` and `password` (token).
- Ensure `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set before relying on CI to push images.
- If secrets are missing, the Actions run will fail at the Docker login step.

6) Manual push flow (if you prefer not to use CI publishing right away)
- Build the image locally:
  - `docker build -t leakosint_telegram_bot:local .`
- Tag & push:
  - `docker tag leakosint_telegram_bot:local YOUR_DOCKERHUB_USERNAME/leakosint_telegram_bot:latest`
  - `echo "YOUR_DOCKERHUB_TOKEN" | docker login --username YOUR_DOCKERHUB_USERNAME --password-stdin`
  - `docker push YOUR_DOCKERHUB_USERNAME/leakosint_telegram_bot:latest`

7) Security & rotation
- Keep tokens secret; do not commit them.
- If a token is exposed, revoke it in Docker Hub → Account Settings → Security → Revoke.
- For CI, prefer repository-scoped secrets and rotate tokens periodically.

End of instructions.