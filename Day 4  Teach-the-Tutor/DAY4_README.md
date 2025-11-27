# Day 4 - Teach-the-Tutor: Active Recall Coach

## Overview
An Active Recall Coach that helps users learn programming concepts through three interactive modes with different Murf Falcon voices.

## Features

### Three Learning Modes
1. **LEARN** - Agent explains concepts (Matthew voice - friendly teacher)
2. **QUIZ** - Agent asks questions (Alicia voice - encouraging questioner)  
3. **TEACH_BACK** - User explains concepts back (Ken voice - supportive evaluator)

### Programming Concepts
- Variables
- Loops  
- Functions
- Conditionals

## Quick Start

### 1. Start Backend
```bash
cd backend
uv run python src/agent.py
```

### 2. Start Frontend
```bash
cd frontend
pnpm dev
```

### 3. Open Browser
Navigate to `http://localhost:3000`

## Usage

1. **Greeting**: Agent asks which mode and concept you prefer
2. **Mode Switching**: Say "switch to learn mode" or "quiz mode" or "teach back mode"
3. **Concept Selection**: Choose from variables, loops, functions, or conditionals
4. **Interactive Learning**: Engage with the agent based on selected mode

## Voice Personalities

- **Matthew** (Learn): Friendly, explanatory teacher
- **Alicia** (Quiz): Encouraging, supportive questioner
- **Ken** (Teach Back): Patient, constructive evaluator

## File Structure

```
backend/
├── src/
│   ├── agent.py              # Main agent with three modes
│   └── voice_manager.py      # Voice switching logic
├── shared-data/
│   └── day4_tutor_content.json  # Learning content
└── .env.local               # API keys

frontend/
├── app/                     # Next.js frontend
└── .env.local              # Frontend config
```

## API Keys Required

- `MURF_API_KEY` - For Murf Falcon TTS voices
- `GOOGLE_API_KEY` - For Gemini LLM
- `DEEPGRAM_API_KEY` - For speech-to-text
- `LIVEKIT_*` - For LiveKit cloud service

## Testing

Run the test script to verify setup:
```bash
python test_day4.py
```

## Day 4 Completion Checklist

✅ Agent greets user and asks for preferred learning mode  
✅ Three modes (learn, quiz, teach_back) fully implemented  
✅ Content-driven responses using JSON file  
✅ Voice switching between Matthew, Alicia, and Ken  
✅ Users can switch modes anytime by voice command  
✅ All modes use the tutor content appropriately