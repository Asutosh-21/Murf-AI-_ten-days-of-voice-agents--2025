# Day 6 - NovaTrust Bank Fraud Alert Agent

## Overview

A voice-powered fraud detection agent for NovaTrust Bank that verifies suspicious transactions through secure customer interaction.

## Quick Start

### Web Interface (Basic)
1. **Start the agent:**
   ```bash
   start_default_gemini.bat
   ```
2. **Open browser:** `http://localhost:3000`
3. **Click "Start call"** and allow microphone

### Telephony (Advanced)
1. **Start telephony agent:**
   ```bash
   start_telephony.bat
   ```
2. **Configure phone integration** (see TELEPHONY_SETUP.md)
3. **Make real phone calls** to the fraud agent

## Features

### Core Features
- **Professional fraud investigation workflow**
- **Secure customer verification** using security questions
- **Real-time database updates** for case outcomes
- **15 test fraud cases** with diverse scenarios
- **Voice-first interaction** with LiveKit integration

### Telephony Features (NEW)
- **Real phone call integration** via LiveKit Telephony
- **SIP trunk support** for phone providers
- **Enhanced call logging** and metrics
- **Phone-optimized responses** for natural conversation
- **BVCTelephony noise cancellation** for clear audio

## Test Customers

| Customer | Security Question | Answer | Transaction |
|----------|------------------|--------|-------------|
| John Smith | Mother's maiden name? | Johnson | ABC Industry - $1,247.99 |
| Sarah Wilson | First pet's name? | Buddy | Luxury Watches - $3,899.00 |
| Michael Brown | Birth city? | Chicago | Digital Services - $599.99 |
| Emily Davis | Favorite color? | Blue | Tech Gadgets - $2,156.50 |
| David Martinez | First car model? | Honda | Global Trading - $4,750.00 |

*Plus 10 additional test cases with various currencies and locations*

## Voice Test Scenarios

### Legitimate Transaction Test
1. Say: "John Smith"
2. Agent asks: "What is your mother's maiden name?"
3. Answer: "Johnson"
4. Agent reads transaction details
5. Say: "Yes" → Transaction marked as safe

### Fraudulent Transaction Test
1. Say: "Sarah Wilson"  
2. Agent asks: "What was the name of your first pet?"
3. Answer: "Buddy"
4. Agent reads transaction details
5. Say: "No" → Card blocked, dispute initiated

### Failed Verification Test
1. Say: "Michael Brown"
2. Agent asks: "What city were you born in?"
3. Answer: "Wrong answer" → Verification fails

## Database Management

**View all cases:**
```bash
cd backend
python show_database.py
```

**Test setup:**
```bash
cd backend
python test_simple.py
```

## Project Structure

```
Day 6 Fraud Alert Agent/
├── backend/
│   ├── src/
│   │   ├── agent.py              # Web fraud agent
│   │   └── telephony_agent.py    # Phone fraud agent
│   ├── fraud_database.json       # 15 test cases
│   ├── show_database.py          # Database viewer
│   ├── call_logs.py              # Call logging system
│   ├── telephony_config.py       # Phone configuration
│   └── test_simple.py            # Setup test
├── frontend/                     # LiveKit React UI
├── start_default_gemini.bat      # Web agent startup
├── start_telephony.bat           # Phone agent startup
├── VOICE_TEST_GUIDE.md           # Web testing guide
└── TELEPHONY_SETUP.md            # Phone setup guide
```

## How It Works

1. **Agent Introduction:** "Hello, this is NovaTrust Bank Fraud Department..."
2. **Customer Lookup:** Loads fraud case from database
3. **Identity Verification:** Asks security question from case
4. **Transaction Review:** Reads suspicious transaction details
5. **Customer Decision:** Processes yes/no response
6. **Action Taken:** Updates database and confirms outcome

## Technical Details

### Core Technology
- **LLM:** Google Gemini (default model)
- **TTS:** Murf Falcon for voice synthesis
- **STT:** Deepgram for speech recognition
- **Database:** JSON file with 15 fraud cases
- **Framework:** LiveKit Agents with React frontend

### Telephony Integration
- **SIP Support:** LiveKit Telephony with SIP trunks
- **Phone Providers:** Twilio, Plivo, or custom SIP
- **Audio Processing:** BVCTelephony noise cancellation
- **Call Logging:** Complete call records and statistics
- **Real-time Updates:** Database updates during phone calls

## Success Criteria

- ✅ Agent responds immediately with professional greeting
- ✅ Loads customer cases from database correctly
- ✅ Verifies identity with security questions
- ✅ Reads transaction details accurately
- ✅ Processes customer responses appropriately
- ✅ Updates database with investigation outcomes
- ✅ Maintains professional banking tone throughout

## Security Features

- **No sensitive data requested** (no PINs, full card numbers)
- **Identity verification** through security questions only
- **Professional fraud investigation** workflow
- **Secure database updates** with audit trail
- **Demo data only** - all information is fictional

Ready to test your fraud detection skills! 🏦🎤