import logging
import json
import os
from datetime import datetime

from dotenv import load_dotenv
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


class CoffeeBaristaAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Maya, a friendly and enthusiastic barista at Brew & Bean Coffee Shop. You love helping customers create the perfect coffee order.
            
            Your job is to take complete coffee orders by asking questions to fill out this order information:
            - drinkType: (espresso, latte, cappuccino, americano, mocha, frappuccino, etc.)
            - size: (small, medium, large)
            - milk: (whole, skim, oat, almond, soy, coconut, or none)
            - extras: (whipped cream, extra shot, decaf, sugar, vanilla syrup, caramel syrup, etc.)
            - name: (customer's name for the order)
            
            Ask friendly questions one at a time to gather missing information. Once you have all details, confirm the order and save it.
            Keep responses conversational and enthusiastic about coffee. No complex formatting or symbols.""",
        )

    @function_tool
    async def save_coffee_order(self, context: RunContext, drink_type: str, size: str, milk: str, extras: str, name: str):
        """Save a complete coffee order to a JSON file.
        
        Args:
            drink_type: Type of coffee drink (latte, cappuccino, etc.)
            size: Size of the drink (small, medium, large)
            milk: Type of milk (whole, oat, almond, etc. or 'none')
            extras: Comma-separated list of extras (whipped cream, extra shot, etc.)
            name: Customer's name for the order
        """
        
        try:
            # Parse extras into a list
            extras_list = [extra.strip() for extra in extras.split(',') if extra.strip()] if extras else []
            
            order = {
                "drinkType": drink_type,
                "size": size,
                "milk": milk,
                "extras": extras_list,
                "name": name,
                "timestamp": datetime.now().isoformat(),
                "order_id": f"order_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            # Get current working directory and create absolute path
            current_dir = os.getcwd()
            orders_dir = os.path.join(current_dir, "orders")
            
            # Create orders directory if it doesn't exist
            if not os.path.exists(orders_dir):
                os.makedirs(orders_dir)
                logger.info(f"Created orders directory: {orders_dir}")
            
            # Save order to JSON file
            filename = os.path.join(orders_dir, f"{order['order_id']}.json")
            with open(filename, 'w') as f:
                json.dump(order, f, indent=2)
            
            # Generate HTML visualization
            try:
                from beverage_visualizer import generate_beverage_html
                html_content = generate_beverage_html(order)
                html_filename = os.path.join(orders_dir, f"{order['order_id']}.html")
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"Visualization created: {html_filename}")
            except Exception as viz_error:
                logger.error(f"Error creating visualization: {viz_error}")
                # Continue without visualization
            
            logger.info(f"Order saved successfully: {filename}")
            
            return f"Perfect! Your order has been saved. Order ID: {order['order_id']}. Your {size} {drink_type} will be ready shortly, {name}! I've also created a visual receipt for you."
            
        except Exception as e:
            logger.error(f"Error saving order: {e}")
            return f"I apologize, but I'm having trouble saving your order right now. Please try again in a moment."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=CoffeeBaristaAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))