# LiveKit Telephony Setup for NovaTrust Bank Fraud Agent

## Overview

This guide enables real phone call integration with the fraud agent using LiveKit Telephony.

## Quick Start

### 1. Start Telephony Agent
```bash
start_telephony.bat
```

### 2. Configure Phone Integration

#### Option A: LiveKit Cloud (Recommended)
1. **Sign up for LiveKit Cloud:** https://cloud.livekit.io
2. **Get a phone number:**
   - Go to SIP/Telephony section
   - Purchase a phone number
   - Configure SIP trunk

#### Option B: Local SIP Trunk
1. **Configure SIP provider** (Twilio, Plivo, etc.)
2. **Set up SIP trunk** to route to LiveKit
3. **Update environment variables**

## Configuration

### Environment Variables (.env.local)
```bash
# Existing LiveKit config
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Telephony-specific (optional)
SIP_TRUNK_URL=sip.your-provider.com
SIP_USERNAME=your_sip_username
SIP_PASSWORD=your_sip_password
```

## Features

### Enhanced Fraud Agent
- **Phone-optimized responses** for natural conversation
- **Enhanced logging** for call tracking
- **BVCTelephony noise cancellation** for clear audio
- **Automatic database updates** after each call

### Call Flow
1. **Incoming call** routed to fraud agent
2. **Agent introduction:** "Hello, this is NovaTrust Bank Fraud Department..."
3. **Customer verification** using security questions
4. **Transaction review** with clear details
5. **Decision processing** (safe/fraud)
6. **Database update** with call outcome
7. **Professional call closure**

### Call Logging
- **Complete call records** in `call_logs.json`
- **Call statistics** and metrics
- **Verification tracking**
- **Transaction decisions**

## Testing

### 1. Web Interface Test (First)
```bash
# Test with web interface first
http://localhost:3000
```

### 2. Phone Call Test
- **Call the configured number**
- **Follow fraud verification flow**
- **Check database updates**

### 3. View Call Logs
```bash
cd backend
python call_logs.py show    # View all calls
python call_logs.py stats   # Call statistics
```

## Telephony Commands

### Start Telephony Agent
```bash
cd backend
uv run python src/telephony_agent.py dev
```

### View Configuration
```bash
python telephony_config.py
```

### Monitor Calls
```bash
python call_logs.py show
```

### Database After Calls
```bash
python show_database.py
```

## Phone Integration Options

### LiveKit Cloud
- **Easiest setup** with managed infrastructure
- **Built-in phone numbers** available
- **Automatic SIP routing**
- **Usage-based pricing**

### Custom SIP Provider
- **Twilio:** Configure SIP trunk to LiveKit
- **Plivo:** Set up inbound/outbound routing
- **Custom:** Any SIP-compatible provider

### Local Testing
- **SIP clients:** Use softphones for testing
- **WebRTC:** Test through web interface first
- **Simulation:** Mock phone calls via web

## Expected Results

### Successful Phone Call
1. **Phone rings** → Agent answers
2. **Professional greeting** from NovaTrust Bank
3. **Customer verification** process
4. **Transaction details** read clearly
5. **Customer decision** processed
6. **Database updated** automatically
7. **Call logged** with outcome

### Call Logs Example
```json
{
  "timestamp": "2024-12-15T10:30:00",
  "customer_name": "John Smith",
  "case_id": "12345",
  "verification_status": "success",
  "transaction_decision": "safe",
  "outcome": "confirmed_safe",
  "duration": "2m 15s"
}
```

## Troubleshooting

### Agent Not Answering
- Check LiveKit server connection
- Verify SIP trunk configuration
- Test web interface first

### Audio Quality Issues
- Ensure BVCTelephony is enabled
- Check network connectivity
- Verify SIP codec settings

### Database Not Updating
- Check file permissions
- Verify JSON format
- Monitor agent logs

## Security Notes

- **Demo system only** - uses fake data
- **No real banking information** processed
- **Secure SIP encryption** recommended
- **Call logging** for audit purposes

## Next Steps

1. **Test web interface** thoroughly
2. **Configure phone integration**
3. **Make test calls** with sample customers
4. **Monitor call logs** and database updates
5. **Scale for production** if needed

The telephony fraud agent provides a complete phone-based fraud detection system! 📞🏦✅