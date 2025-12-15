# NovaTrust Bank Fraud Agent - Voice Test Guide

## 🚀 Quick Start

1. **Start the agent:**
   ```bash
   start_default_gemini.bat
   ```

2. **Open browser:** `http://localhost:3000`

3. **Click "Start call"** and allow microphone

## 🎯 Test Scenarios

### Test 1: Legitimate Transaction (John Smith)

**Step 1:** Say "Hello" or "My name is John Smith"
**Agent should say:** "Hello, this is NovaTrust Bank Fraud Department. We detected suspicious activity on your account. May I have your name to look up your case?"

**Step 2:** Say "John Smith"
**Agent should say:** "Found case for John Smith. What is your mother's maiden name?"

**Step 3:** Say "Johnson"
**Agent should say:** "Verification successful. Suspicious transaction: ABC Industry for $1,247.99 on card ending 4242 from Shanghai, China on 2024-12-15 14:32:00"

**Step 4:** Agent asks "Did you make this transaction? Please answer yes or no"
**Say:** "Yes"

**Step 5:** Agent should say "Transaction marked as safe. No action needed."

---

### Test 2: Fraudulent Transaction (Sarah Wilson)

**Step 1:** Say "Hello"
**Agent responds:** Fraud department greeting

**Step 2:** Say "Sarah Wilson"
**Agent asks:** "What was the name of your first pet?"

**Step 3:** Say "Buddy"
**Agent reads:** "Suspicious transaction: Luxury Watches Ltd for $3,899.00 on card ending 8765 from Geneva, Switzerland..."

**Step 4:** Say "No" (deny the transaction)
**Agent should say:** "Card ending 8765 blocked. Dispute initiated."

---

### Test 3: Failed Verification (Michael Brown)

**Step 1:** Say "Michael Brown"
**Agent asks:** "What city were you born in?"

**Step 2:** Say "Wrong answer" (correct is "Chicago")
**Agent should say:** "Verification failed"

---

### Test 4: Additional Customers

**Amit Verma:** Answer "blue"
**David Chen:** Answer "liu"  
**Priya Nair:** Answer "dangal"
**John Carter:** Answer "football"
**Emma Williams:** Answer "madrid"

## 🔍 What to Check

### ✅ Audio Input/Output
- [ ] Microphone button visible at bottom
- [ ] Audio visualization shows when speaking
- [ ] Agent voice is clear and audible
- [ ] No audio delays or echoes

### ✅ Agent Responses
- [ ] Agent starts conversation immediately
- [ ] Uses function tools (loads cases, verifies, etc.)
- [ ] Follows fraud investigation workflow
- [ ] Provides appropriate responses for yes/no answers

### ✅ Database Updates
After each test, check database:
```bash
cd backend
python show_database.py
```
- [ ] Case status changes to `confirmed_safe` or `confirmed_fraud`
- [ ] Outcome field shows timestamp and result

### ✅ Error Handling
- [ ] Handles unknown customer names
- [ ] Responds to wrong security answers
- [ ] Continues conversation smoothly

## 🎤 Voice Tips

**Speak clearly:** Use normal conversational tone
**Wait for response:** Let agent finish before speaking
**Use exact answers:** Security answers are case-insensitive but should match
**Simple responses:** "Yes", "No", "John Smith" work best

## 🐛 Troubleshooting

**Agent not responding:**
- Check backend terminal for errors
- Verify microphone permissions in browser
- Try refreshing page and reconnecting

**Wrong responses:**
- Ensure you're using correct customer names
- Check security answers match database
- Speak clearly and wait for agent to finish

**Database not updating:**
- Check backend terminal for database errors
- Verify fraud_database.json exists
- Run `python show_database.py` to check status

## 📊 Expected Results

**Successful Test:** Complete fraud workflow from greeting to final confirmation
**Database Updated:** Case status and outcome recorded
**Audio Quality:** Clear two-way voice communication
**Function Tools:** Agent uses all fraud detection tools properly

## 🎯 Success Criteria

- [ ] Agent greets and introduces NovaTrust Bank
- [ ] Loads customer cases from database
- [ ] Verifies identity with security questions
- [ ] Reads transaction details accurately
- [ ] Processes yes/no responses correctly
- [ ] Updates database with outcomes
- [ ] Provides professional banking responses

The fraud agent should handle all scenarios smoothly with natural voice interaction! 🏦✅