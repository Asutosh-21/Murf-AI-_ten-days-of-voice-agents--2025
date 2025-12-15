# Day 5 SDR Agent - Railway Deployment Guide

## Quick Deploy to Railway (5 minutes)

### Step 1: Create requirements.txt from pyproject.toml

```bash
cd "Day 5 SDR Agent/backend"
pip install uv
uv pip compile pyproject.toml -o requirements.txt
```

Or create manually:

```txt
livekit-agents[assemblyai,deepgram,google,silero,turn-detector]~=1.2
livekit-murf>=0.1.0
livekit-plugins-noise-cancellation~=0.2
python-dotenv
```

### Step 2: Create Railway Config

Create `railway.toml` in backend folder:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python src/agent.py start"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
```

### Step 3: Deploy Backend to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo → Choose "Day 5 SDR Agent/backend" folder
5. Add Environment Variables:
   - `LIVEKIT_URL` (from LiveKit Cloud)
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`
   - `MURF_API_KEY`
   - `GOOGLE_API_KEY`
   - `DEEPGRAM_API_KEY`
6. Click Deploy

### Step 4: Deploy Frontend to Vercel

```bash
cd "Day 5 SDR Agent/frontend"

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Follow prompts:
- Set up and deploy: Yes
- Which scope: Your account
- Link to existing project: No
- Project name: sdr-agent
- Directory: ./
- Override settings: No

Add environment variables in Vercel dashboard:
- `NEXT_PUBLIC_LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

### Step 5: Get Your Live URL

Railway will give you: `https://your-backend.railway.app`
Vercel will give you: `https://sdr-agent.vercel.app`

Update frontend `.env.local` with Railway backend URL if needed.

## Resume Line:

"Deployed SDR voice agent on Railway (Python backend) and Vercel (Next.js frontend) with automated CI/CD and environment-based configuration"
