# QuickBasket Advanced Features

## 🚀 **New Features Added**

### 1. **Mock Order Tracking Over Time**
- **Order Statuses**: received → confirmed → being_prepared → out_for_delivery → delivered
- **Auto-progression**: Orders advance every 2 minutes automatically
- **Manual Control**: Use `python src/status_updater.py` to manually update statuses

**Voice Commands:**
- "Where is my order?"
- "Track my order"
- "What's the status of order QB20241207143022?"

### 2. **Order History & Previous Orders**
- **Persistent Storage**: All orders saved in `orders/order_history.json`
- **Unique IDs**: Each order has timestamp-based ID
- **Complete History**: Items, totals, timestamps, statuses

**Voice Commands:**
- "What did I order last time?"
- "Show me my order history"
- "Have I ordered apples before?"

### 3. **Multiple Concurrent Orders**
- **Order Types**: grocery, restaurant, pharmacy, etc.
- **Distinct Tracking**: Each order tracked separately
- **Smart Queries**: Agent asks for clarification when needed

**Voice Commands:**
- "Track my grocery order"
- "What's my latest restaurant order?"
- "Place a pharmacy order"

### 4. **Smart Reorder & Recommendations**
- **Reorder**: Rebuild cart from previous orders
- **Recommendations**: Based on frequently ordered items
- **Usage Analytics**: Track ordering patterns

**Voice Commands:**
- "Reorder what I got last time"
- "Get me my usual groceries"
- "What do you recommend?"

### 5. **Budget & Constraints-Aware Ordering**
- **Budget Limits**: Set spending limits for shopping sessions
- **Dietary Constraints**: Filter by vegan, gluten-free, etc.
- **Smart Filtering**: Only show items that meet constraints
- **Real-time Warnings**: Alert when constraints are violated

**Voice Commands:**
- "Keep it under $50"
- "Only show vegan items"
- "Set dietary constraints to gluten-free"
- "Check if my cart meets my budget"

## 🛠 **New Function Tools**

1. `track_order(order_id)` - Track order status
2. `order_history(limit)` - View recent orders
3. `reorder_last()` - Reorder from last order
4. `get_recommendations()` - Get personalized recommendations
5. `search_order_history(item_name)` - Search if item was ordered before
6. `set_budget(budget)` - Set budget constraint
7. `set_dietary_constraints(tags)` - Set dietary requirements
8. `search_within_constraints(query)` - Search items matching constraints
9. `check_cart_constraints()` - Validate cart against constraints

## 📁 **File Structure**

```
backend/src/
├── agent.py              # Enhanced QuickBasket agent
├── order_manager.py      # Order tracking & history management
├── status_updater.py     # Manual status update tool
├── test_constraints.py   # Constraint testing tool
├── catalog.json          # Product catalog
└── orders/
    └── order_history.json # All orders with tracking
```

## 🎯 **Usage Examples**

### Order Tracking
**User**: "Where is my order?"
**QuickBasket**: "Order QB20241207143022: Your order is out for delivery!"

### Order History
**User**: "What did I order last time?"
**QuickBasket**: "Your recent orders:
Order QB20241207143022: 2x Whole Wheat Bread, 1x Creamy Peanut Butter - $11.47 (delivered)"

### Smart Reorder
**User**: "Reorder what I got last time"
**QuickBasket**: "Reordered from your last order: 2x Whole Wheat Bread, 1x Creamy Peanut Butter. Check your cart!"

### Recommendations
**User**: "What do you recommend?"
**QuickBasket**: "Based on your order history, you might like: Whole Wheat Bread (you've ordered 5 times), Creamy Peanut Butter (you've ordered 3 times)"

### Budget & Constraints
**User**: "Keep it under $20 and only vegan items"
**QuickBasket**: "Budget set to $20.00. Dietary constraints set: vegan. I'll only suggest items that match these requirements."

**User**: "Search for fruit"
**QuickBasket**: "Found 2 items (matching your constraints): Bananas - $1.29, Red Apples - $2.99"

## 🔧 **Manual Testing**

Run the status updater:
```bash
cd backend/src
python status_updater.py
```

This allows you to:
- View all recent orders
- Auto-advance all order statuses
- Manually set specific order statuses

## 📊 **Order JSON Format**

```json
{
  "order_id": "QB20241207143022",
  "customer_name": "Customer",
  "order_type": "grocery",
  "timestamp": "2024-12-07T14:30:22.123456",
  "status": "out_for_delivery",
  "status_updated": "2024-12-07T14:35:22.123456",
  "items": [...],
  "total": 11.47
}
```

## ✅ **All Features Complete**

- ✅ Mock order tracking with time-based progression
- ✅ Complete order history with persistent storage
- ✅ Multiple concurrent orders with type classification
- ✅ Smart reordering from previous orders
- ✅ Personalized recommendations based on history
- ✅ Advanced search through order history
- ✅ Manual status management tools
- ✅ Budget-aware ordering with spending limits
- ✅ Dietary constraint filtering (vegan, gluten-free)
- ✅ Real-time constraint violation warnings
- ✅ Smart search within constraints

QuickBasket now provides a complete e-commerce ordering experience with intelligent tracking, history management, personalized recommendations, and constraint-aware shopping!