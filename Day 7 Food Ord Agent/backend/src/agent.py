import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Any

from dotenv import load_dotenv
from order_manager import OrderManager
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class QuickBasketAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are QuickBasket, a friendly food and grocery ordering assistant for our store. 
            
            ALWAYS start conversations by greeting users and saying: "Hi! I'm QuickBasket. I can help you order groceries and simple meal ingredients, track your orders, help you reorder from your history, and work within your budget or dietary constraints. What would you like to do today?"
            
            Key behaviors:
            - Ask for clarifications on size, brand, quantity when items have multiple options
            - Always confirm cart changes verbally so users know what's happening
            - When users ask for ingredients for dishes, intelligently add multiple related items
            - Help users track orders, view history, and reorder previous items
            - Respect budget limits and dietary constraints when adding items
            - Warn users when constraints might be violated
            - Keep responses conversational and helpful
            
            You have access to tools for catalog search, cart management, order placement, order tracking, history viewing, smart reordering, and constraint management. Use them actively to help customers.""",
        )
        self.catalog = self._load_catalog()
        self.cart = {}
        self.order_manager = OrderManager()
        self.constraints = {"budget": None, "dietary": []}
        
    def _load_catalog(self) -> Dict[str, Any]:
        try:
            catalog_path = os.path.join(os.path.dirname(__file__), 'catalog.json')
            with open(catalog_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load catalog: {e}")
            return {"items": [], "recipes": {}}

    @function_tool
    async def search_catalog(self, context: RunContext, query: str) -> str:
        """Search for items in the catalog by name, category, or tags.
        
        Args:
            query: Search term (item name, category, or description)
        """
        query_lower = query.lower()
        matches = []
        
        for item in self.catalog.get("items", []):
            if (query_lower in item["name"].lower() or 
                query_lower in item["category"].lower() or
                any(query_lower in tag.lower() for tag in item.get("tags", [])) or
                query_lower in item.get("description", "").lower()):
                matches.append(f"{item['name']} - ${item['price']:.2f} ({item['brand']}, {item['size']})")
        
        if matches:
            return f"Found {len(matches)} items: " + ", ".join(matches[:5])
        return f"No items found matching '{query}'. Try searching for categories like groceries, snacks, or prepared food."
    
    @function_tool
    async def add_to_cart(self, context: RunContext, item_name: str, quantity: int = 1, notes: str = "") -> str:
        """Add an item to the shopping cart.
        
        Args:
            item_name: Name of the item to add
            quantity: Quantity to add (default 1)
            notes: Optional notes (e.g. "whole wheat", "large size")
        """
        item = self._find_item_by_name(item_name)
        if not item:
            return f"Sorry, I couldn't find '{item_name}' in our catalog. Try searching first."
        
        item_name_key = item["name"]
        if item_name_key in self.cart:
            self.cart[item_name_key]["quantity"] += quantity
            if notes:
                self.cart[item_name_key]["notes"] = notes
        else:
            self.cart[item_name_key] = {
                "item": item,
                "quantity": quantity,
                "notes": notes
            }
        
        total_qty = self.cart[item_name_key]["quantity"]
        note_text = f" ({notes})" if notes else ""
        # Check constraints before confirming
        constraint_warning = self._check_constraints_after_add(item, quantity)
        response = f"Added {quantity} {item['name']}{note_text} to your cart. You now have {total_qty} total."
        
        if constraint_warning:
            response += f" {constraint_warning}"
        
        return response
    
    @function_tool
    async def add_recipe_ingredients(self, context: RunContext, dish_name: str) -> str:
        """Add ingredients for a specific dish to the cart.
        
        Args:
            dish_name: Name of the dish (e.g., 'pasta', 'peanut butter sandwich')
        """
        dish_lower = dish_name.lower()
        recipe_items = self.catalog.get("recipes", {}).get(dish_lower, [])
        
        if not recipe_items:
            return f"I don't have a recipe for '{dish_name}'. Try asking me to search for individual ingredients."
        
        added_items = []
        for item_name in recipe_items:
            item = self._find_item_by_name(item_name)
            if item:
                if item_name in self.cart:
                    self.cart[item_name]["quantity"] += 1
                else:
                    self.cart[item_name] = {"item": item, "quantity": 1, "notes": ""}
                added_items.append(item["name"])
        
        if added_items:
            return f"I've added ingredients for {dish_name} to your cart: {', '.join(added_items)}"
        return f"Sorry, I couldn't find the ingredients for {dish_name}."
    
    @function_tool
    async def track_order(self, context: RunContext, order_id: str = None) -> str:
        """Track the status of an order.
        
        Args:
            order_id: Specific order ID to track (optional, defaults to latest)
        """
        # Update statuses first
        self.order_manager.advance_order_statuses()
        
        order = self.order_manager.get_order_status(order_id)
        if not order:
            return "No orders found. Place an order first!"
        
        status_messages = {
            "received": "Your order has been received and is being reviewed.",
            "confirmed": "Your order has been confirmed and is being prepared.",
            "being_prepared": "Your order is currently being prepared.",
            "out_for_delivery": "Your order is out for delivery!",
            "delivered": "Your order has been delivered. Enjoy!"
        }
        
        status_msg = status_messages.get(order["status"], f"Status: {order['status']}")
        return f"Order {order['order_id']}: {status_msg}"
    
    @function_tool
    async def order_history(self, context: RunContext, limit: int = 3) -> str:
        """Show recent order history.
        
        Args:
            limit: Number of recent orders to show
        """
        orders = self.order_manager.get_recent_orders(limit)
        if not orders:
            return "You haven't placed any orders yet."
        
        history = []
        for order in orders:
            items_summary = ", ".join([f"{item['quantity']}x {item['name']}" for item in order['items'][:3]])
            if len(order['items']) > 3:
                items_summary += "..."
            history.append(f"Order {order['order_id']}: {items_summary} - ${order['total']:.2f} ({order['status']})")
        
        return "Your recent orders:\n" + "\n".join(history)
    
    @function_tool
    async def reorder_last(self, context: RunContext) -> str:
        """Reorder items from the last order."""
        orders = self.order_manager.get_recent_orders(1)
        if not orders:
            return "No previous orders found to reorder from."
        
        last_order = orders[0]
        added_items = []
        
        for order_item in last_order['items']:
            item = self._find_item_by_name(order_item['name'])
            if item:
                item_name = item['name']
                qty = order_item['quantity']
                
                if item_name in self.cart:
                    self.cart[item_name]['quantity'] += qty
                else:
                    self.cart[item_name] = {
                        'item': item,
                        'quantity': qty,
                        'notes': order_item.get('notes', '')
                    }
                added_items.append(f"{qty}x {item['name']}")
        
        if added_items:
            return f"Reordered from your last order: {', '.join(added_items)}. Check your cart!"
        return "Couldn't find items from your last order in current catalog."
    
    @function_tool
    async def get_recommendations(self, context: RunContext) -> str:
        """Get recommendations based on order history."""
        frequent_items = self.order_manager.get_frequent_items(5)
        if not frequent_items:
            return "No order history available for recommendations."
        
        recommendations = []
        for item_data in frequent_items:
            item = self._find_item_by_name(item_data['name'])
            if item:
                recommendations.append(f"{item['name']} (you've ordered {item_data['count']} times)")
        
        return "Based on your order history, you might like: " + ", ".join(recommendations)
    
    @function_tool
    async def search_order_history(self, context: RunContext, item_name: str) -> str:
        """Search if an item was ordered before.
        
        Args:
            item_name: Name of item to search for
        """
        found_orders = []
        for order in self.order_manager.orders:
            for item in order['items']:
                if item_name.lower() in item['name'].lower():
                    found_orders.append(f"Order {order['order_id']} on {order['timestamp'][:10]}")
                    break
        
        if found_orders:
            return f"Yes, you've ordered {item_name} in: {', '.join(found_orders[-3:])}"  # Last 3
        return f"No, you haven't ordered {item_name} before."
    
    @function_tool
    async def set_budget(self, context: RunContext, budget: float) -> str:
        """Set a budget constraint for the current shopping session.
        
        Args:
            budget: Maximum budget amount
        """
        self.constraints["budget"] = budget
        current_total = sum(item["item"]["price"] * item["quantity"] for item in self.cart.values())
        
        if current_total > budget:
            return f"Budget set to ${budget:.2f}. Warning: Your current cart total (${current_total:.2f}) exceeds this budget."
        else:
            remaining = budget - current_total
            return f"Budget set to ${budget:.2f}. You have ${remaining:.2f} remaining for this shopping session."
    
    @function_tool
    async def set_dietary_constraints(self, context: RunContext, dietary_tags: str) -> str:
        """Set dietary constraints for filtering items.
        
        Args:
            dietary_tags: Comma-separated dietary requirements (e.g., 'vegan,gluten-free')
        """
        tags = [tag.strip().lower() for tag in dietary_tags.split(',')]
        self.constraints["dietary"] = tags
        
        return f"Dietary constraints set: {', '.join(tags)}. I'll only suggest items that match these requirements."
    
    @function_tool
    async def search_within_constraints(self, context: RunContext, query: str) -> str:
        """Search for items that match current constraints.
        
        Args:
            query: Search term
        """
        query_lower = query.lower()
        matches = []
        
        for item in self.catalog.get("items", []):
            # Basic search match
            if not (query_lower in item["name"].lower() or 
                   query_lower in item["category"].lower() or
                   any(query_lower in tag.lower() for tag in item.get("tags", []))):
                continue
            
            # Check dietary constraints
            if self.constraints["dietary"]:
                item_tags = [tag.lower() for tag in item.get("tags", [])]
                if not any(diet_tag in item_tags for diet_tag in self.constraints["dietary"]):
                    continue
            
            # Check budget constraint
            if self.constraints["budget"]:
                current_total = sum(cart_item["item"]["price"] * cart_item["quantity"] for cart_item in self.cart.values())
                if current_total + item["price"] > self.constraints["budget"]:
                    continue
            
            matches.append(f"{item['name']} - ${item['price']:.2f} ({item['brand']}, {item['size']})")
        
        if matches:
            constraint_info = ""
            if self.constraints["dietary"] or self.constraints["budget"]:
                constraint_info = " (matching your constraints)"
            return f"Found {len(matches)} items{constraint_info}: " + ", ".join(matches[:5])
        
        constraint_msg = ""
        if self.constraints["dietary"]:
            constraint_msg += f" matching {', '.join(self.constraints['dietary'])}"
        if self.constraints["budget"]:
            constraint_msg += f" within budget"
        
        return f"No items found for '{query}'{constraint_msg}. Try a different search or adjust constraints."
    
    @function_tool
    async def check_cart_constraints(self, context: RunContext) -> str:
        """Check if current cart meets all constraints."""
        if not self.cart:
            return "Your cart is empty."
        
        total = sum(item["item"]["price"] * item["quantity"] for item in self.cart.values())
        warnings = []
        
        # Budget check
        if self.constraints["budget"] and total > self.constraints["budget"]:
            over = total - self.constraints["budget"]
            warnings.append(f"Cart total (${total:.2f}) exceeds budget by ${over:.2f}")
        
        # Dietary check
        if self.constraints["dietary"]:
            violating_items = []
            for cart_item in self.cart.values():
                item = cart_item["item"]
                item_tags = [tag.lower() for tag in item.get("tags", [])]
                if not any(diet_tag in item_tags for diet_tag in self.constraints["dietary"]):
                    violating_items.append(item["name"])
            
            if violating_items:
                warnings.append(f"Items not matching dietary constraints: {', '.join(violating_items)}")
        
        if warnings:
            return "Cart constraint warnings: " + "; ".join(warnings)
        
        constraint_info = ""
        if self.constraints["budget"]:
            remaining = self.constraints["budget"] - total
            constraint_info += f" Budget remaining: ${remaining:.2f}."
        if self.constraints["dietary"]:
            constraint_info += f" All items match {', '.join(self.constraints['dietary'])} requirements."
        
        return f"Cart looks good!{constraint_info}"
    
    def _check_constraints_after_add(self, item: Dict, quantity: int) -> str:
        """Check constraints after adding an item and return warning if needed."""
        warnings = []
        
        # Budget check
        if self.constraints["budget"]:
            current_total = sum(cart_item["item"]["price"] * cart_item["quantity"] for cart_item in self.cart.values())
            if current_total > self.constraints["budget"]:
                over = current_total - self.constraints["budget"]
                warnings.append(f"This puts you ${over:.2f} over budget")
        
        # Dietary check
        if self.constraints["dietary"]:
            item_tags = [tag.lower() for tag in item.get("tags", [])]
            if not any(diet_tag in item_tags for diet_tag in self.constraints["dietary"]):
                warnings.append(f"This item doesn't match your {', '.join(self.constraints['dietary'])} requirements")
        
        return " Warning: " + "; ".join(warnings) if warnings else ""
    
    @function_tool
    async def view_cart(self, context: RunContext) -> str:
        """Show the current contents of the shopping cart."""
        if not self.cart:
            return "Your cart is empty. What would you like to add?"
        
        cart_items = []
        total = 0
        
        for cart_item in self.cart.values():
            item = cart_item["item"]
            qty = cart_item["quantity"]
            notes = cart_item.get("notes", "")
            subtotal = item["price"] * qty
            total += subtotal
            note_text = f" ({notes})" if notes else ""
            cart_items.append(f"{qty}x {item['name']}{note_text} - ${subtotal:.2f}")
        
        cart_summary = "\n".join(cart_items)
        return f"Your cart:\n{cart_summary}\n\nTotal: ${total:.2f}"
    
    @function_tool
    async def update_cart_quantity(self, context: RunContext, item_name: str, new_quantity: int) -> str:
        """Update the quantity of an item in the cart.
        
        Args:
            item_name: Name of the item to update
            new_quantity: New quantity (use 0 to remove item)
        """
        item = self._find_item_by_name(item_name)
        if not item or item["name"] not in self.cart:
            return f"'{item_name}' is not in your cart."
        
        item_name_key = item["name"]
        if new_quantity <= 0:
            del self.cart[item_name_key]
            return f"Removed {item['name']} from your cart."
        else:
            old_qty = self.cart[item_name_key]["quantity"]
            self.cart[item_name_key]["quantity"] = new_quantity
            return f"Updated {item['name']} quantity from {old_qty} to {new_quantity}."
    
    @function_tool
    async def remove_from_cart(self, context: RunContext, item_name: str, quantity: int = None) -> str:
        """Remove an item from the cart.
        
        Args:
            item_name: Name of the item to remove
            quantity: Quantity to remove (if None, removes all)
        """
        item = self._find_item_by_name(item_name)
        if not item or item["name"] not in self.cart:
            return f"'{item_name}' is not in your cart."
        
        item_name_key = item["name"]
        current_qty = self.cart[item_name_key]["quantity"]
        
        if quantity is None or quantity >= current_qty:
            del self.cart[item_name_key]
            return f"Removed all {item['name']} from your cart."
        else:
            self.cart[item_name_key]["quantity"] -= quantity
            remaining = self.cart[item_name_key]["quantity"]
            return f"Removed {quantity} {item['name']} from your cart. {remaining} remaining."
    
    @function_tool
    async def place_order(self, context: RunContext, customer_name: str = "Customer", order_type: str = "grocery") -> str:
        """Place the final order and save it to order history.
        
        Args:
            customer_name: Name for the order (optional)
            order_type: Type of order (grocery, restaurant, etc.)
        """
        if not self.cart:
            return "Your cart is empty. Add some items before placing an order."
        
        # Create order using OrderManager
        order_id = self.order_manager.create_order(self.cart, customer_name, order_type)
        
        # Calculate total for response
        total = sum(item["item"]["price"] * item["quantity"] for item in self.cart.values())
        
        # Clear cart
        self.cart = {}
        
        return f"Order placed successfully! Order ID: {order_id}. Total: ${total:.2f}. Your order is now being processed and you can track its status."
    
    def _find_item_by_name(self, name: str):
        """Find an item in the catalog by name (case insensitive)."""
        name_lower = name.lower()
        for item in self.catalog.get("items", []):
            if name_lower in item["name"].lower():
                return item
        return None


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=QuickBasketAssistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
