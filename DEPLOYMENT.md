# 🚀 Deployment Guide — AI Code Reviewer (Reflex Cloud)

Follow these steps carefully **in order**. Skipping or reordering steps will cause the app backend to fail silently.

---

## Prerequisites

- You have a [Reflex Cloud](https://reflex.dev/) account and are **logged in**.
- You have already run `reflex init` and the app works locally.
- You have your **OpenAI** and/or **Anthropic** API keys ready.

---

## STEP 1 — Add API Keys to Reflex Cloud Dashboard

> ⚠️ Do this **before** deploying. Secrets added after deployment require a redeploy to take effect.

1. Go to 👉 [https://build.reflex.dev/project-settings](https://build.reflex.dev/project-settings)
2. Log in with the **same account** used for deployment.
3. Click **"Secrets"** in the left sidebar.
4. Click **"Add new variable"** and add each secret:

   | Variable Name       | Value           |
   |---------------------|-----------------|
   | `GROQ_API_KEY`      | `gsk_...your key` |

5. Click **"Save secret"** after each one.

> 💡 Do **NOT** use the `--secrets` flag in the terminal if you've added secrets via the dashboard — they will conflict.

---

## STEP 2 — First Deployment

From the **project root** (`Code_Review/`), run:

```bash
reflex deploy
```

- Wait for the deployment to complete (this may take a few minutes).
- At the end, you will receive your **app URL** in the format:

  ```
  https://your-username-appname.reflex.run
  ```

- **Copy this URL** — you'll need it in the next step.

---

## STEP 3 — Update `rxconfig.py`

Open `rxconfig.py` at the project root and update it to include your `api_url`:

```python
import reflex as rx
import os

if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

config = rx.Config(
    app_name="Code_Review",
    api_url="https://your-username-appname.reflex.run",  # ← Replace with your actual URL
)
```

Replace `https://your-username-appname.reflex.run` with the **exact URL** you received in Step 2.

**Save the file.**

> 🔒 The app URL is **permanent** — it will not change between deployments, so you only need to set this once.

---

## STEP 4 — Redeploy (Critical!)

Run the deploy command **one more time**:

```bash
reflex deploy
```

> ⚠️ **This step is mandatory.** The first deployment sets up the infrastructure; the second deployment connects the frontend to the backend using the `api_url` you just configured. Without this step, the UI will load but the backend will not respond.

---

## ✅ Verification Checklist

After Step 4 completes, verify the following:

- [ ] App loads at your URL without errors
- [ ] Code analysis (AI review) triggers and returns results
- [ ] History page shows past reviews
- [ ] No "Backend not connected" or network errors in the browser console

---

## 🛠️ Troubleshooting

| Issue | Fix |
|-------|-----|
| Backend doesn't respond | Confirm `api_url` in `rxconfig.py` exactly matches your deployed URL (no trailing slash) |
| Secrets not available at runtime | Ensure secrets were added via dashboard **before** deploying, then redeploy |
| Deployment hangs | Check your internet connection; re-run `reflex deploy` |
| App URL not found | Wait 1–2 minutes after deployment; DNS propagation can cause a short delay |

---

## 📁 File Reference

| File | Purpose |
|------|---------|
| `rxconfig.py` | App configuration — must include `api_url` after first deploy |
| `.env` | Local environment variables (never commit to Git!) |
| `.env.example` | Template for required environment variables |

---

*Last updated: April 2026*
