# Day 8 Voice Game Master - Testing Guide

## 🚀 Quick Start Testing

### 1. Launch the Application
```bash
# Start all services
./start_app.sh

# Or manually:
# Terminal 1: livekit-server --dev
# Terminal 2: cd backend && uv run python src/agent.py dev
# Terminal 3: cd frontend && pnpm dev
```

### 2. Open Browser
- Go to `http://localhost:3000`
- Allow microphone permissions when prompted
- Click "Start Audio" if needed

## 🎯 Core Features Testing

### Basic Voice Interaction
1. **Start Adventure**: The GM will automatically begin with a scenario
2. **Speak Your Action**: Say something like:
   - "I look around"
   - "I talk to the tavern keeper"
   - "I explore the forest"
3. **Listen**: GM responds with story continuation and "What do you do?"

### Expected Flow:
```
GM: "You arrive at the fog-shrouded village of Ravenshollow..."
You: "I'll go to the tavern"
GM: "The tavern door creaks open. The keeper eyes you nervously..."
```

## 🎲 Advanced Features Testing

### 1. Character Sheet Testing
- **Open**: Click "Show Character" (top-right)
- **Test Commands**:
  - Say: "Check my inventory"
  - Say: "What are my stats?"
  - Say: "How much health do I have?"
- **Expected**: Character panel updates with current stats

### 2. Dice Rolling Testing
- **Manual Dice**: Click "🎲 Dice" (bottom-right)
  - Click d20, d12, or d6
  - See visual roll results
- **Voice Commands**:
  - Say: "Roll a d20"
  - Say: "I want to roll for strength"
  - Say: "Roll dice to climb the wall"
- **Expected**: Dice results with Success/Partial/Failure outcomes

### 3. Universe Switching Testing
- **Open**: Click "🌍 Fantasy" (top-left)
- **Switch**: Try each universe:
  - "Switch to cyberpunk universe"
  - "Switch to space universe" 
  - "Switch to fantasy universe"
- **Expected**: New scenario and setting change

### 4. Save/Load Testing
- **Save**: Click save button (💾) in control bar
  - Say: "Save my game"
  - Check console logs for save data
- **Load**: Click load button (📁)
  - Upload a JSON save file
  - Game state should restore

## 🗣️ Voice Commands Cheat Sheet

### Basic Actions
- "I look around"
- "I talk to [character name]"
- "I go to [location]"
- "I search for clues"
- "I attack the monster"
- "I cast a spell"

### Game Mechanics
- "Check my inventory"
- "What are my stats?"
- "Roll a d20"
- "I want to use my sword"
- "How much health do I have?"

### Meta Commands
- "Switch to cyberpunk universe"
- "Save my game"
- "Start a new adventure"
- "What universes are available?"

## 🧪 Specific Test Scenarios

### Scenario 1: Basic Adventure
1. Start in Fantasy universe
2. Say: "I explore the village"
3. Say: "I talk to the villagers"
4. Say: "I investigate the mysterious forest"
5. **Expected**: Coherent story progression with dice rolls

### Scenario 2: Combat & Dice
1. Get into a dangerous situation
2. Say: "I try to fight the creature"
3. **Expected**: Automatic dice roll, outcome affects story
4. Say: "Roll a d20 for luck"
5. **Expected**: Manual dice roll with visual feedback

### Scenario 3: Inventory Management
1. Say: "Check my inventory"
2. Find/pick up items during adventure
3. Say: "I use my health potion"
4. **Expected**: Inventory updates, HP changes

### Scenario 4: Universe Switching
1. Start in Fantasy
2. Switch to Cyberpunk via UI or voice
3. **Expected**: New scenario, different tone
4. Switch to Space Opera
5. **Expected**: Sci-fi setting, space adventure

### Scenario 5: Save/Load Game
1. Play for several turns
2. Save game (button or voice)
3. Restart browser/session
4. Load saved game
5. **Expected**: Game continues from saved point

## 🔧 Troubleshooting

### Voice Not Working
- Check microphone permissions
- Click "Start Audio" button
- Ensure microphone toggle is enabled (blue)

### Agent Not Responding
- Check backend logs: `cd backend && uv run python src/agent.py dev`
- Verify API keys in `.env.local`
- Check LiveKit server is running

### Features Not Working
- Open browser console (F12) for errors
- Check if all components are loaded
- Verify function tools are working in backend logs

## 📊 Expected Behaviors

### GM Responses Should:
- Always end with "What do you do?" or similar
- Be 2-3 sentences max
- Include atmospheric descriptions
- Reference previous actions/decisions
- Use appropriate universe tone

### Dice System Should:
- Roll 1-20 for d20
- Add appropriate modifiers
- Show Success (15+), Partial (10-14), Failure (<10)
- Affect story outcomes

### World State Should:
- Track HP, inventory, location
- Remember NPCs and their attitudes
- Maintain story continuity
- Update based on player actions

## 🎮 Sample Test Session

```
1. GM: "You arrive at Ravenshollow village..."
2. You: "I go to the tavern"
3. GM: "The tavern keeper looks nervous. What do you do?"
4. You: "I ask about the missing travelers"
5. GM: "He whispers about strange lights. Roll for perception..."
6. [Automatic dice roll: 16 - Success]
7. GM: "You notice his hands shaking. He slides you a map..."
8. You: "Check my inventory"
9. Agent: "HP: 100/100 (Healthy). Inventory: basic sword, leather armor..."
10. You: "I examine the map"
11. GM: "The map shows ancient ruins. What do you do?"
```

## ✅ Success Criteria

Your agent is working correctly if:
- ✅ Voice interaction flows naturally
- ✅ GM maintains character and story continuity  
- ✅ Dice rolls affect outcomes appropriately
- ✅ Character sheet updates correctly
- ✅ Universe switching changes tone/setting
- ✅ Save/load preserves game state
- ✅ All UI components respond properly

## 🐛 Common Issues

1. **No voice response**: Check microphone permissions
2. **Robotic responses**: Verify Murf API key
3. **No dice rolls**: Check function tools in logs
4. **UI not updating**: Refresh browser, check console
5. **Save/load broken**: Verify JSON format in console

This comprehensive testing guide covers all features of your advanced D&D Voice Game Master!