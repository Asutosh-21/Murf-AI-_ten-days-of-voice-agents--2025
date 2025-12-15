# Day 8 - Advanced D&D Voice Game Master

A comprehensive voice-powered D&D-style Game Master with full RPG mechanics, multiple universes, and stateful world management using Murf Falcon TTS and LiveKit.

## 🎯 Core Features

✅ **Game Master Persona**: Multiple universe settings with appropriate tones
✅ **Interactive Storytelling**: GM describes scenes and prompts player actions
✅ **JSON World State**: Tracks player stats, inventory, NPCs, locations, and events
✅ **Character Sheet**: HP, attributes (STR/INT/LUCK), inventory, and status
✅ **Dice Mechanics**: Automated skill checks with success/failure outcomes
✅ **Multiple Universes**: Fantasy, Cyberpunk, and Space Opera settings
✅ **Save/Load Game**: Export and import game states
✅ **Voice Interface**: Complete voice interaction with visual feedback

## 🌍 Available Universes

- **Classic Fantasy**: Dragons, magic, medieval adventures
- **Cyberpunk City**: Neon streets, corporate conspiracies, hackers
- **Space Opera**: Galactic adventures, alien worlds, cosmic mysteries

## 🎲 Advanced Mechanics

- **Dice Rolling**: d20 system with modifiers and outcome tiers
- **Attribute System**: Strength, Intelligence, Luck affect outcomes
- **Inventory Management**: Track items, weapons, and consumables
- **Health System**: HP tracking with status effects
- **World Persistence**: JSON state maintains continuity across sessions

## Quick Start

1. **Install Dependencies**:
   ```bash
   # Backend
   cd backend && uv sync
   
   # Frontend  
   cd frontend && pnpm install
   ```

2. **Configure Environment**:
   - Backend: Copy `.env.example` to `.env.local` and add your API keys
   - Frontend: Copy `.env.example` to `.env.local` and add LiveKit credentials

3. **Run the Application**:
   ```bash
   # Option 1: Use the convenience script
   chmod +x start_app.sh
   ./start_app.sh
   
   # Option 2: Run services individually
   # Terminal 1: livekit-server --dev
   # Terminal 2: cd backend && uv run python src/agent.py dev  
   # Terminal 3: cd frontend && pnpm dev
   ```

4. **Play**: Open http://localhost:3000 and start your adventure!

## 🎮 How to Play

1. **Choose Universe**: Click the universe selector (top-left) to pick your setting
2. **Check Character**: Click "Show Character" (top-right) to view your stats
3. **Speak Actions**: Respond to the GM's "What do you do?" prompts
4. **Use Tools**: 
   - Say "check my inventory" to see your items
   - Say "roll dice" for skill checks
   - Use the dice roller for manual rolls
5. **Save Progress**: Click the save button to export your game
6. **Load Game**: Click load to import a saved game file
7. **Restart**: Click restart for a fresh adventure

## How It Works

The Game Master:
- Sets a fantasy universe with dramatic tone
- Describes vivid scenes in 2-3 sentences
- Always ends with action prompts
- Remembers your choices and story continuity
- Builds toward mini-arcs (treasure hunts, escaping danger, etc.)

## 🎮 Game Master Features

- **Multi-Universe Support**: Switch between Fantasy, Cyberpunk, and Space settings
- **Stateful World**: JSON-based world state tracking all game elements
- **Smart Dice System**: Automatic skill checks based on player attributes
- **Dynamic NPCs**: Persistent characters with attitudes and knowledge
- **Quest System**: Track active and completed objectives
- **Location Mapping**: Interconnected world with explorable areas

## 🖥️ UI Components

- **Character Sheet**: Toggle panel showing HP, stats, inventory, location
- **Universe Selector**: Switch between different game settings
- **Dice Roller**: Manual dice rolling with visual results
- **Save/Load**: Export game state to JSON file or load saved games
- **Voice Controls**: Full voice interaction with transcript view
- **Game Controls**: Restart, save, load, and standard session controls

## 🎭 Example Adventure Flow

### Fantasy Universe
1. **GM**: "You arrive at the fog-shrouded village of Ravenshollow. The locals whisper of strange lights in the ancient forest. What do you do?"
2. **Player**: "I'll investigate the forest."
3. **GM**: "Roll for perception... Success! You notice glowing runes on ancient trees. A shadowy figure watches from the darkness. What do you do?"

### Cyberpunk Universe  
1. **GM**: "Your neural implant crackles as you jack into Neo-Tokyo's data streams. Corporate security algorithms hunt for your digital signature. What do you do?"
2. **Player**: "I'll try to hack the mainframe."
3. **GM**: "Roll for intelligence... Partial success! You breach the outer firewall but trigger an alarm. Security drones are incoming. What do you do?"

### Space Opera Universe
1. **GM**: "Your starship's sensors detect an ancient alien artifact drifting in the nebula. Strange energy readings spike across your instruments. What do you do?"
2. **Player**: "I'll scan the artifact."
3. **GM**: "Roll for luck... Failure! The scan activates the artifact, and your ship is caught in a tractor beam. Alien voices echo through your comms. What do you do?"

## 🛠️ Technical Implementation

### Backend Features
- **JSON World State**: Complete game state management
- **Function Tools**: 7 specialized tools for game mechanics
  - `roll_dice()`: Skill checks and random events
  - `check_inventory()`: Player status and inventory
  - `update_world_state()`: Dynamic world updates
  - `switch_universe()`: Change game settings
  - `save_game()`: Export game state
  - `get_available_universes()`: List available settings
- **Multi-Universe System**: 3 complete universe configurations
- **Attribute-Based Outcomes**: Player stats influence success rates

### Frontend Features
- **Character Sheet Component**: Real-time player stats display
- **Universe Selector**: Easy universe switching interface
- **Dice Roller**: Visual dice rolling with outcome display
- **Save/Load System**: File-based game state persistence
- **Enhanced Control Bar**: Game-specific controls

### Core Technologies
- **TTS**: Murf Falcon for ultra-fast voice synthesis
- **STT**: Deepgram Nova-3 for accurate speech recognition
- **LLM**: Google Gemini 2.5 Flash with function calling
- **Framework**: LiveKit Agents with React frontend

## 🎯 Advanced Goals Completed

✅ **JSON World State**: Complete character, location, and event tracking
✅ **Player Character Sheet**: HP, attributes, inventory, and status
✅ **Dice Mechanics**: d20 system with success tiers
✅ **Multiple Universes**: 3 complete universe settings
✅ **Save & Resume**: Full game state export/import

Built for the Murf AI Voice Agents Challenge - Day 8!