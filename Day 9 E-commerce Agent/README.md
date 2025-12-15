# Day 9 E-commerce Voice Agent 🛍️

**AI Voice Agents Challenge** by [murf.ai](https://murf.ai)

A fully functional e-commerce voice agent with smart product search, cart management, and order placement.

## ✨ Features

✅ **107 Products** across 21 categories  
✅ **Smart Search** with fuzzy matching & synonyms  
✅ **Natural Voice** interaction with Murf Falcon TTS  
✅ **Full Cart Management** (add, view, remove)  
✅ **Order Placement** with persistence  
✅ **Order History** retrieval  

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- [LiveKit Server](https://docs.livekit.io/home/self-hosting/local/)

### 1. Start LiveKit Server
```bash
livekit-server --dev
```

### 2. Start Backend Agent
```bash
cd backend
uv run python src/agent.py dev
```

### 3. Start Frontend
```bash
cd frontend
pnpm dev
```

Open http://localhost:3000 and start talking! 🎤

## 🎤 Voice Commands

### Search Products
```
"Find iPhone"
"Search for frying pan"
"Do you have moisturizer?"
```

### Browse Categories
```
"Show me electronics"
"Browse clothing"
"What home products do you have?"
```

### Shopping Cart
```
"Add phone-001 to cart"
"Show my cart"
"Remove phone-001 from cart"
"Checkout"
```

### Order History
```
"Show my recent order"
"What was my last order?"
```

## 📂 Repository Structure

```
Day 9 E-commerce Agent/
├── backend/          # LiveKit Agents backend with Murf Falcon TTS
│   ├── src/
│   │   ├── agent.py       # Voice agent (7 functions)
│   │   ├── commerce.py    # Product catalog & logic
│   │   └── api_server.py  # Optional FastAPI server
│   └── tests/
├── frontend/         # Next.js frontend for voice interaction
├── ESSENTIAL_GUIDE.md           # Quick start & commands
├── VOICE_COMMANDS_CHEATSHEET.md # Command reference
└── start_app.sh      # Convenience startup script
```

## 🛠️ Technical Stack

### Backend
- **LiveKit Agents** - Voice agent framework
- **Murf Falcon TTS** - Ultra-fast text-to-speech
- **Google Gemini 2.5 Flash** - LLM for conversation
- **Deepgram Nova-3** - Speech-to-text
- **Python 3.9+** with FastAPI

### Frontend
- **Next.js 14** - React framework
- **LiveKit React Components** - Real-time voice UI
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Styling

[→ Backend Documentation](./backend/README.md)  
[→ Frontend Documentation](./frontend/README.md)

## ⚙️ Configuration

### Backend Setup

1. Install dependencies:
```bash
cd backend
uv sync
```

2. Configure API keys in `backend/.env.local`:
```bash
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
MURF_API_KEY=your_murf_key
GOOGLE_API_KEY=your_gemini_key
DEEPGRAM_API_KEY=your_deepgram_key
```

3. Download models:
```bash
uv run python src/agent.py download-files
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
pnpm install
```

2. Configure LiveKit in `frontend/.env.local`:
```bash
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
```

## 🎯 Quick Test (2 Minutes)

1. **"Find iPhone"** → See available phones
2. **"Add phone-001 to cart"** → Add to cart
3. **"Show my cart"** → View cart
4. **"Checkout"** → Place order
5. **"Show my last order"** → Confirm order

## 📦 Product Categories (21)

electronics | clothing | home | food | beauty | health | fitness | accessory | gaming | sports | outdoor | automotive | pet | daily | cleaning | stationery | baby | garden | office | travel

**Total: 107 Products**

## 📚 Documentation

- **[ESSENTIAL_GUIDE.md](./ESSENTIAL_GUIDE.md)** - Quick start & voice commands
- **[VOICE_COMMANDS_CHEATSHEET.md](./VOICE_COMMANDS_CHEATSHEET.md)** - Command reference
- **[FIXES_SUMMARY.md](./FIXES_SUMMARY.md)** - Technical improvements
- **[Day 9 Task.md](./Day%209%20Task.md)** - Original task requirements

### External Resources
- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [LiveKit Testing Guide](https://docs.livekit.io/agents/build/testing/)

## 🧪 Testing

```bash
cd backend
uv run pytest
```

## 🔧 What Was Fixed

✅ Enhanced search with fuzzy matching  
✅ Synonym support (moisturizer = moisturizing, cream)  
✅ Multi-word query handling  
✅ Better error messages  
✅ Improved agent instructions  

Previously failed searches now work:
- "nonstick frying pan" ✅
- "moisturizer face cream" ✅

## 💡 Pro Tips

1. **Search first** to get product IDs
2. **Use natural language** - agent understands context
3. **Product IDs** shown in search results (e.g., phone-001)
4. **Check cart** before checkout

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details.

Based on LiveKit templates with Murf Falcon integration.

## 🎉 Status

**Production Ready!** All features tested and working.

---

**Built for the AI Voice Agents Challenge by [murf.ai](https://murf.ai)** 🚀
