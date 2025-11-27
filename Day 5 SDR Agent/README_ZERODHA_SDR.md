# Zerodha SDR Agent - Day 5 Implementation

## Overview
This is a complete implementation of a Sales Development Representative (SDR) voice agent for Zerodha, India's largest stock brokerage platform.

## Features Implemented

### ✅ Core SDR Functionality
- **Warm Greeting**: Agent greets visitors professionally
- **Needs Discovery**: Asks what brought them and what they're working on
- **FAQ-Based Responses**: Answers questions using only Zerodha FAQ content
- **Lead Capture**: Naturally collects prospect information during conversation
- **Call Summary**: Generates summary and saves lead data when call ends

### ✅ Advanced Features
- **Mock Meeting Scheduler**: Books demo calls with available time slots
- **CRM Analysis**: Generates qualification scores and structured notes
- **Pain Point Detection**: Identifies customer frustrations and needs
- **Decision Maker Assessment**: Categorizes prospects as decision makers/influencers
- **Urgency Analysis**: Evaluates timeline and priority level
- **Fit Scoring**: Calculates 0-100 qualification score based on conversation

### ✅ Company Information (Zerodha)
- Complete FAQ database with 7 key questions/answers
- Pricing information (free equity delivery, ₹20 intraday/F&O)
- Product details (trading, mutual funds, account opening)
- Target audience information

### ✅ Lead Capture Fields
- Name
- Company (optional for retail)
- Email
- Role/Experience Level (beginner/trader/investor)
- Use Case (trading, investing, F&O, mutual funds)
- Team Size (for business accounts)
- Timeline (when they want to start)

### ✅ Smart Features
- **FAQ Search**: Keyword-based matching for user questions
- **Hallucination Prevention**: Says "not in FAQ" for unknown topics
- **End Call Detection**: Recognizes phrases like "that's all", "I'm done"
- **JSON Lead Storage**: Saves leads with timestamp and session info
- **Conversation Notes**: Tracks important conversation points
- **Calendar Integration**: Mock calendar with 5 available demo slots
- **Automatic CRM Notes**: Generates structured notes for sales team

## File Structure
```
backend/
├── data/
│   ├── company_faq.json          # Zerodha FAQ database
│   └── mock_calendar.json        # Available meeting slots
├── leads/                        # Generated lead files
├── crm_notes/                    # CRM analysis files
├── src/
│   └── agent.py                  # Main SDR agent implementation
└── .env.local                    # API credentials

frontend/
└── .env.local                    # LiveKit credentials
```

## Testing Scenarios

### 1. Greeting & Product Questions
- "Hi, what does Zerodha do?"
- "Who is Zerodha for?"
- "Can you explain Zerodha in simple words?"

**Expected**: Agent responds with exact FAQ content

### 2. Pricing Questions
- "Do you have a free plan?"
- "What are your brokerage charges?"
- "How much do I pay per order?"

**Expected**: Agent provides accurate pricing from FAQ

### 3. Use Case Discovery
- "I want to invest in mutual funds"
- "I trade intraday"
- "I am a beginner and want to start investing"

**Expected**: Agent captures use case and asks relevant follow-ups

### 4. Lead Information Capture
- "My name is Aditya"
- "My email is aditya.sharma@example.com"
- "I am a beginner in trading"
- "I want to start investing next month"

**Expected**: Agent acknowledges and stores each piece of information

### 5. CRM Analysis Triggers
- "I'm frustrated with my current broker" (pain point)
- "What are your costs?" (budget discussion)
- "I make the decisions here" (decision maker)
- "I need this urgently" (high urgency)

**Expected**: Agent captures insights for CRM analysis

### 6. Hallucination Prevention
- "Does Zerodha offer cryptocurrency trading?"
- "Do you provide stock tips?"
- "Does Zerodha guarantee returns?"

**Expected**: Agent says "This information is not in my FAQ, so I can't confirm that"

### 6. Meeting Booking
- "I'd like to book a demo"
- "Can we schedule a meeting?"
- "Show me available times"
- "I'll take slot 1"

**Expected**: Agent shows available slots, books chosen time, confirms booking

### 7. Call Ending
- "That's all"
- "Okay, you can wrap up"
- "Thanks, I'm done"

**Expected**: Agent provides summary with fit score and saves lead + CRM analysis to JSON files

## How to Run

1. **Start LiveKit Server**:
   ```bash
   .\livekit-server.exe --dev
   ```

2. **Start Backend Agent**:
   ```bash
   cd backend
   uv run python src/agent.py dev
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   pnpm dev
   ```

4. **Open Browser**: http://localhost:3000

## Lead Data Output

When a call ends, the agent saves two JSON files:

### Lead File (`backend/leads/`)
```json
{
  "name": "Aditya",
  "company": null,
  "email": "aditya.sharma@example.com",
  "role": "beginner",
  "use_case": "investing",
  "team_size": null,
  "timeline": "next month",
  "meeting_booked": {
    "date": "2024-11-28",
    "time": "10:00 AM",
    "duration": "30 minutes"
  },
  "pain_points": ["Mentioned expensive", "Mentioned frustrated"],
  "budget_mentioned": true,
  "decision_maker_type": "decision_maker",
  "urgency_level": "medium",
  "fit_score": 85,
  "timestamp": "2024-11-27T14:30:45.123456",
  "session_id": "room_abc123",
  "company_contacted": "Zerodha"
}
```

### CRM Analysis File (`backend/crm_notes/`)
```json
{
  "lead_summary": "Aditya - beginner interested in investing",
  "key_points": ["Mentioned expensive", "Mentioned frustrated"],
  "budget_discussed": true,
  "decision_authority": "decision_maker",
  "urgency": "medium",
  "timeline_refined": "next month",
  "fit_score": 85,
  "next_steps": "Follow up via email and demo call scheduled"
}
```

## Key Agent Functions

### Core Functions
- `search_zerodha_faq()`: Searches FAQ using keyword matching
- `capture_lead_field()`: Stores individual lead information
- `detect_end_call_intent()`: Recognizes when user wants to end call
- `generate_final_summary()`: Creates summary and saves lead data
- `add_conversation_note()`: Tracks conversation context

### Advanced Functions
- `show_available_meeting_slots()`: Displays available demo times
- `book_meeting_slot()`: Books chosen meeting slot
- `analyze_conversation_for_crm()`: Extracts CRM insights and calculates fit score

## Success Criteria Met

### Core Features
✅ Agent behaves as Zerodha SDR  
✅ Answers FAQ questions accurately  
✅ Collects and stores lead information  
✅ Generates end-of-call summary  
✅ Prevents hallucination for unknown topics  
✅ Natural conversation flow  

### Advanced Features
✅ Mock meeting scheduler with 5 available slots  
✅ CRM-style call notes and qualification scoring  
✅ Pain point detection and analysis  
✅ Decision maker type identification  
✅ Urgency level assessment  
✅ Fit score calculation (0-100)  
✅ Structured CRM notes for sales team  

## Fit Score Calculation

The agent calculates a qualification score (0-100) based on:
- **Base Score**: 50 points
- **Email Provided**: +15 points
- **Name Provided**: +10 points
- **Use Case Identified**: +15 points
- **Budget Discussion**: +10 points
- **Decision Maker**: +20 points (Influencer: +10)
- **High Urgency**: +15 points (Medium: +10)
- **Meeting Booked**: +15 points

## Additional Advanced Features Available

1. **Persona Detection**: Adapt pitch based on user type
2. **Follow-up Emails**: Generate email drafts
3. **Return Visitor**: Recognize repeat visitors
4. **Real Calendar**: Connect to Google Calendar
5. **CRM Integration**: Connect to actual CRM system

The agent now includes **Mock Meeting Scheduler** and **CRM Analysis** - ready for advanced Day 5 demonstration!