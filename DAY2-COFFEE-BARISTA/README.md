# Day 2 - Coffee Shop Barista Agent ☕

## Overview
Maya is a friendly barista at Brew & Bean Coffee Shop who helps customers place complete coffee orders through voice interaction.

## Features Implemented

### ✅ Primary Goal (Required)
- **Barista Persona**: Maya, enthusiastic coffee shop barista
- **Order State Management**: Tracks complete order information:
  ```json
  {
    "drinkType": "latte",
    "size": "large", 
    "milk": "oat",
    "extras": ["whipped cream", "vanilla syrup"],
    "name": "Alice"
  }
  ```
- **Intelligent Questioning**: Asks clarifying questions until all fields are complete
- **JSON Order Storage**: Saves completed orders to `orders/` directory

### ✅ Advanced Challenge (Optional)
- **HTML Beverage Visualization**: Generates visual coffee cup representations
- **Dynamic Styling**: Cup size changes based on order size
- **Visual Extras**: Shows whipped cream and other modifications
- **Order Receipt**: Beautiful HTML receipt with order details

## Project Structure

```
DAY2-COFFEE-BARISTA/
├── backend/
│   ├── src/
│   │   └── agent.py          # Coffee Barista Agent
│   ├── beverage_visualizer.py # HTML generation system
│   ├── view_orders.py        # Order management utility
│   ├── .env.local           # Environment variables
│   ├── pyproject.toml       # Dependencies
│   └── uv.lock             # Lock file
├── frontend/                # React frontend (copied from original)
├── livekit-server.exe      # Local LiveKit server
└── README.md               # This file
```

## How to Run

### 1. Start LiveKit Server
```powershell
cd "E:\ten-days-of-voice-agents-2025-main\DAY2-COFFEE-BARISTA"
.\livekit-server.exe --dev
```

### 2. Start Coffee Barista Agent
```powershell
cd "E:\ten-days-of-voice-agents-2025-main\DAY2-COFFEE-BARISTA\backend"
uv run python src/agent.py dev
```

### 3. Start Frontend
```powershell
cd "E:\ten-days-of-voice-agents-2025-main\DAY2-COFFEE-BARISTA\frontend"
pnpm install
pnpm dev
```

### 4. Open Browser
Navigate to `http://localhost:3000` and start talking to Maya!

## Example Conversation

**Maya**: "Hi! Welcome to Brew & Bean Coffee! I'm Maya, your barista. What can I get started for you today?"

**Customer**: "I'd like a coffee please"

**Maya**: "Great choice! What type of coffee drink would you like? We have lattes, cappuccinos, americanos, mochas, and more!"

**Customer**: "A latte sounds good"

**Maya**: "Perfect! What size would you like - small, medium, or large?"

**Customer**: "Large please"

**Maya**: "Excellent! What type of milk would you prefer? We have whole, skim, oat, almond, soy, or coconut milk."

**Customer**: "Oat milk"

**Maya**: "Great choice! Would you like any extras like whipped cream, extra shots, syrups, or anything else?"

**Customer**: "Whipped cream and vanilla syrup"

**Maya**: "Sounds delicious! And what name should I put on the order?"

**Customer**: "Alice"

**Maya**: "Perfect! Your order has been saved. Order ID: order_20240115_103000. Your large latte will be ready shortly, Alice! I've also created a visual receipt for you."

## Order Management

View saved orders:
```powershell
cd backend
python view_orders.py
```

This will show:
- List of all orders
- Order details
- Option to open HTML visualizations in browser

## Visual Features

The HTML visualization includes:
- **Dynamic cup sizes** (small/medium/large)
- **Drink-specific colors** (espresso dark, latte light brown, etc.)
- **Whipped cream visualization** (white fluffy top)
- **Animated steam** (floating clouds)
- **Professional receipt layout** with all order details
- **Brew & Bean Coffee branding**

## Files Created

- `backend/src/agent.py` - Coffee Barista Agent with order management
- `backend/beverage_visualizer.py` - HTML visualization generator
- `backend/view_orders.py` - Order viewing utility
- `backend/orders/` - Directory for saved orders (auto-created)

## Technical Implementation

- **Function Tool**: `save_coffee_order()` handles order completion
- **State Management**: Order state tracked through conversation
- **File Organization**: Orders saved with timestamps and unique IDs
- **HTML Generation**: Dynamic styling based on order contents
- **Error Handling**: Graceful handling of missing information

This implementation fulfills both the required primary goal and the optional advanced challenge, creating a complete coffee ordering experience with visual feedback!

## Original Project Preserved

The original AI VOICE AGENT project remains unchanged in its directory. This Day 2 project is completely separate and self-contained.