# Master Deployment Guide - All 3 Projects

## Quick Deploy Summary

| Project | Platform | Time | Difficulty | Impressiveness |
|---------|----------|------|------------|----------------|
| Day 5 SDR | Railway + Vercel | 10 min | Easy | ⭐⭐⭐⭐ |
| Day 9 E-commerce | Render | 15 min | Easy | ⭐⭐⭐⭐ |
| Day 6 Fraud | AWS EB + Vercel | 20 min | Medium | ⭐⭐⭐⭐⭐ |

---

## 🚀 Fastest Path (1 Hour Total)

### Project 1: Day 5 SDR → Railway (10 min)

```bash
# Backend
cd "Day 5 SDR Agent/backend"
# Go to railway.app → New Project → Deploy from GitHub
# Add environment variables in Railway dashboard

# Frontend
cd ../frontend
npm i -g vercel
vercel
# Add environment variables in Vercel dashboard
```

**Live URLs:**
- Backend: `https://sdr-backend.railway.app`
- Frontend: `https://sdr-agent.vercel.app`

---

### Project 2: Day 9 E-commerce → Render (15 min)

```bash
# Go to render.com → New Blueprint
# Connect GitHub repo
# Render auto-detects services
# Add environment variables
# Click "Apply"
```

**Live URLs:**
- Backend: `https://ecommerce-backend.onrender.com`
- Frontend: `https://ecommerce-frontend.onrender.com`

---

### Project 3: Day 6 Fraud → AWS Elastic Beanstalk (20 min)

```bash
# Install AWS CLI
pip install awscli awsebcli

# Configure AWS
aws configure

# Deploy backend
cd "Day 6 Fraud Alert Agent/backend"
pip freeze > requirements.txt
eb init -p python-3.9 fraud-agent --region us-east-1
eb create fraud-env
eb setenv LIVEKIT_URL=xxx LIVEKIT_API_KEY=xxx LIVEKIT_API_SECRET=xxx MURF_API_KEY=xxx GOOGLE_API_KEY=xxx DEEPGRAM_API_KEY=xxx
eb deploy

# Deploy frontend
cd ../frontend
vercel
```

**Live URLs:**
- Backend: `http://fraud-env.eba-xxxxx.us-east-1.elasticbeanstalk.com`
- Frontend: `https://fraud-agent.vercel.app`

---

## 📝 Environment Variables Needed

### All Projects Need:
```
LIVEKIT_URL=wss://your-livekit-cloud.livekit.cloud
LIVEKIT_API_KEY=APIxxxxxxxxx
LIVEKIT_API_SECRET=secretxxxxxxxxx
MURF_API_KEY=your-murf-key
GOOGLE_API_KEY=your-google-key (for Gemini)
DEEPGRAM_API_KEY=your-deepgram-key
```

### Get LiveKit Cloud Credentials:
1. Go to https://cloud.livekit.io
2. Create account
3. Create project
4. Copy API Key, Secret, and URL

---

## 🎯 Resume Section (Copy-Paste Ready)

```
AI Voice Agent Development | Murf AI Voice Agents Challenge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SDR Lead Generation Agent
• Deployed RAG-powered sales assistant on Railway with FAQ retrieval and lead qualification
• Implemented structured LLM outputs for CRM integration and automated follow-up generation
• Tech: Python, FastAPI, LiveKit, OpenAI/Gemini APIs, Railway, Vercel
• Live: https://sdr-agent.vercel.app

E-commerce Voice Shopping Agent
• Built ACP-compliant voice shopping system with catalog API and order management on Render
• Designed microservices architecture with separate backend/frontend deployment
• Tech: Python, Next.js, RESTful APIs, JSON persistence, Render
• Live: https://ecommerce-frontend.onrender.com

Fraud Detection Voice Agent
• Architected fraud alert system on AWS Elastic Beanstalk with database-driven workflows
• Implemented telephony integration using LiveKit for real-time phone-based verification
• Tech: Python, AWS (EB, CloudWatch), SQLite, LiveKit Telephony, Vercel
• Live: http://fraud-env.elasticbeanstalk.com
```

---

## 🔧 Troubleshooting

### Railway Issues:
```bash
# Check logs
railway logs

# Redeploy
railway up --detach
```

### Render Issues:
```bash
# Check logs in dashboard
# Manual redeploy: Dashboard → Manual Deploy → Deploy latest commit
```

### AWS EB Issues:
```bash
# Check logs
eb logs

# SSH into instance
eb ssh

# Redeploy
eb deploy
```

### Common Fixes:
```bash
# Port issues - Make sure backend uses PORT env variable
PORT = os.getenv("PORT", 8080)

# Build failures - Check requirements.txt has all dependencies
pip freeze > requirements.txt

# Environment variables - Double-check all keys are set correctly
```

---

## 💰 Cost Breakdown

| Platform | Free Tier | Monthly Cost |
|----------|-----------|--------------|
| Railway | 500 hours | $0-5 |
| Render | 750 hours | $0 |
| AWS EB | 750 hours (12 months) | $0-10 |
| Vercel | Unlimited | $0 |
| **Total** | | **$0-15/month** |

---

## 📊 LinkedIn Post Template

```
🚀 Just deployed 3 production AI Voice Agents as part of the Murf AI Voice Agents Challenge!

✅ SDR Agent: RAG-powered lead generation with automated CRM integration
✅ E-commerce Agent: ACP-compliant voice shopping with order management  
✅ Fraud Alert Agent: Banking fraud detection with telephony integration

Tech Stack: Python, LiveKit, OpenAI/Gemini APIs, FastAPI, Next.js
Deployed on: Railway, Render, AWS Elastic Beanstalk, Vercel

Built with the fastest TTS API - Murf Falcon 🎙️

#MurfAIVoiceAgentsChallenge #10DaysofAIVoiceAgents #AI #VoiceAgents #LLM #AWS

[Tag @Murf AI]
[Add demo video/screenshots]
```

---

## ⚡ Next Steps

1. **Deploy all 3 projects** (1 hour)
2. **Test live URLs** (30 min)
3. **Record demo videos** (30 min)
4. **Update resume** (15 min)
5. **Post on LinkedIn** (15 min)
6. **Add to GitHub README** with live links

Total Time: ~2.5 hours for complete portfolio

---

## 🎓 What You'll Learn

- Microservices deployment
- Cloud infrastructure (AWS)
- CI/CD pipelines
- Environment management
- Production debugging
- Serverless architecture
- Container orchestration (if using Docker)

All skills mentioned in the AI Engineer job description! ✅
