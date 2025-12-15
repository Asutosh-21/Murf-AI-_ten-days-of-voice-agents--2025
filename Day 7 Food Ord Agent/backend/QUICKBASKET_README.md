# QuickBasket - Food & Grocery Ordering Voice Agent

## Overview

QuickBasket is an intelligent voice agent that helps customers order food and groceries through natural conversation. Built for Day 7 of the AI Voice Agents Challenge, it demonstrates advanced cart management, recipe understanding, and order processing capabilities.

## Features

### 🛒 **Smart Shopping Assistant**
- Natural voice interaction for ordering food and groceries
- Intelligent search across 22+ catalog items in 7 categories
- Real-time cart management with quantity tracking
- Order confirmation and JSON file storage

### 🍳 **Recipe Intelligence**
- Understands ingredient requests like "I need ingredients for pasta"
- Automatically adds multiple related items for common dishes
- Pre-configured recipes for popular meals:
  - Peanut butter sandwich
  - Pasta/Spaghetti
  - Salad
  - Breakfast items
  - Burgers and more

### 📦 **Comprehensive Catalog**
- **Categories**: Groceries, Snacks, Prepared Food, Beverages, Dairy & Eggs, Meat & Seafood, Fresh Produce
- **Realistic Data**: Brands, prices, sizes, stock quantities, tags
- **Rich Metadata**: Descriptions, nutritional tags (vegan, gluten-free), product attributes

### 🛍️ **Advanced Cart Management**
- Add/remove items with quantity control
- View cart contents with pricing
- Update quantities for existing items
- Clear confirmation of all cart changes

## Available Voice Commands

### Search & Browse
- "What do you have for snacks?"
- "Search for bread"
- "Show me dairy products"

### Adding Items
- "Add 2 loaves of bread to my cart"
- "I need some milk"
- "Add peanut butter"

### Recipe Requests
- "I need ingredients for pasta"
- "Get me what I need for a peanut butter sandwich"
- "Add ingredients for making a salad"

### Cart Management
- "What's in my cart?"
- "Remove the bread"
- "Update milk quantity to 2"

### Order Completion
- "I'm done shopping"
- "Place my order"
- "That's all for today"

## Technical Implementation

### Core Components

1. **Catalog System** (`catalog.json`)
   - 22 realistic products across 7 categories
   - Complete e-commerce data structure
   - Recipe mappings for intelligent bundling

2. **Cart Management**
   - In-memory cart state during conversation
   - Quantity tracking and price calculations
   - Real-time updates with voice confirmation

3. **Order Processing**
   - Automatic order ID generation
   - JSON file storage in `orders/` directory
   - Complete order history with timestamps

### Function Tools

- `search_catalog()` - Find items by name, category, or tags
- `add_to_cart()` - Add individual items with quantities
- `add_recipe_ingredients()` - Smart ingredient bundling
- `view_cart()` - Display current cart contents
- `remove_from_cart()` - Remove or reduce item quantities
- `place_order()` - Finalize and save order

## File Structure

```
backend/src/
├── agent.py              # Main QuickBasket agent implementation
├── catalog.json          # Product catalog with 22 items
├── orders/               # Directory for saved orders
└── test_catalog.py       # Catalog validation script
```

## Sample Catalog Items

- **Groceries**: Whole wheat bread, peanut butter, pasta, marinara sauce
- **Dairy**: Organic milk, cage-free eggs, unsalted butter, parmesan cheese
- **Prepared Food**: Margherita pizza, pepperoni pizza, turkey club sandwich
- **Snacks**: Potato chips, chocolate chip cookies
- **Beverages**: Coca-Cola, spring water
- **Meat**: Chicken breast, ground beef
- **Produce**: Bananas, red apples, lettuce, roma tomatoes

## Order JSON Format

```json
{
  "order_id": "QB20241207143022",
  "customer_name": "Customer",
  "timestamp": "2024-12-07T14:30:22.123456",
  "items": [
    {
      "id": "bread_001",
      "name": "Whole Wheat Bread",
      "brand": "Nature's Own",
      "price": 3.49,
      "quantity": 2,
      "subtotal": 6.98
    }
  ],
  "total": 6.98,
  "status": "placed"
}
```

## Testing

Run the catalog validation:
```bash
python test_catalog.py
```

## Usage Example

**User**: "Hi, I need ingredients for pasta for two people"

**QuickBasket**: "I've added ingredients for pasta for two to your cart: Spaghetti Pasta, Marinara Sauce, Parmesan Cheese. Your total is $11.47. Would you like to add anything else?"

**User**: "What's in my cart?"

**QuickBasket**: "Your cart:
1x Spaghetti Pasta - $1.99
1x Marinara Sauce - $2.49
1x Parmesan Cheese - $6.99

Total: $11.47"

**User**: "That's all, place my order"

**QuickBasket**: "Order placed successfully! Order ID: QB20241207143022. Total: $11.47. Your order has been saved and will be processed shortly."

## Key Achievements

✅ **MVP Complete**: Full food & grocery ordering with cart → order JSON  
✅ **Smart Recipe Understanding**: Automatic ingredient bundling  
✅ **Realistic E-commerce Data**: 22 items with complete product information  
✅ **Natural Voice Interface**: Conversational ordering experience  
✅ **Persistent Order Storage**: JSON file system for order history  

QuickBasket demonstrates the power of voice AI for e-commerce applications, combining natural language understanding with practical shopping functionality.