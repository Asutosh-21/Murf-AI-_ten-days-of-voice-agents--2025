import logging
import json
import random
from typing import Dict, List, Any

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


# Universe configurations
UNIVERSES = {
    "fantasy": {
        "name": "Classic Fantasy",
        "prompt": """You are a Game Master running a fantasy adventure in a world of dragons, magic, and ancient mysteries. Create medieval settings with magical creatures, wizards, and epic quests. Use a dramatic, heroic tone.""",
        "starting_location": "Village of Ravenshollow",
        "starting_scenario": "You arrive at the fog-shrouded village where locals whisper of strange lights in the ancient forest."
    },
    "cyberpunk": {
        "name": "Cyberpunk City", 
        "prompt": """You are a Game Master running a cyberpunk adventure in Neo-Tokyo 2087. Create neon-lit streets, corporate conspiracies, hackers, and augmented reality. Use a gritty, noir tone.""",
        "starting_location": "Neo-Tokyo Underground",
        "starting_scenario": "You jack into the neon-soaked undercity where corporate data flows like digital blood through fiber optic veins."
    },
    "space": {
        "name": "Space Opera",
        "prompt": """You are a Game Master running a space opera adventure across the galaxy. Create alien worlds, space stations, starships, and cosmic mysteries. Use an epic, adventurous tone.""",
        "starting_location": "Frontier Station Alpha",
        "starting_scenario": "Your ship docks at the remote frontier station where distress signals echo from the unexplored nebula beyond."
    }
}

class GameMaster(Agent):
    def __init__(self) -> None:
        self.world_state = self._init_world_state()
        self.current_universe = "fantasy"
        
        super().__init__(
            instructions=self._get_instructions(),
        )
    
    def _init_world_state(self) -> Dict[str, Any]:
        return {
            "player": {
                "name": "Adventurer",
                "hp": 100,
                "status": "Healthy",
                "attributes": {"strength": 12, "intelligence": 14, "luck": 10},
                "inventory": ["basic sword", "leather armor", "health potion"]
            },
            "current_location": "Village of Ravenshollow",
            "locations": {
                "Village of Ravenshollow": {
                    "description": "A fog-shrouded village with nervous locals",
                    "npcs": ["tavern keeper", "village elder"],
                    "paths": ["ancient forest", "mountain pass"]
                }
            },
            "npcs": {
                "tavern keeper": {"attitude": "nervous", "knows": "missing travelers story"},
                "village elder": {"attitude": "wise", "knows": "ancient forest secrets"}
            },
            "events": [],
            "quests": {"active": [], "completed": []}
        }
    
    def _get_instructions(self) -> str:
        universe = UNIVERSES[self.current_universe]
        return f"""{universe['prompt']}
        
        Your role:
        - You are the GM. Describe scenes vividly and ask the player what they do.
        - Use the JSON world state to track player progress, inventory, NPCs, and locations.
        - Always end responses with "What do you do?" or similar action prompts.
        - Keep responses concise but atmospheric - 2-3 sentences, then prompt for action.
        - Use dice rolls for risky actions and describe outcomes based on results.
        
        Rules:
        - No complex formatting, emojis, or asterisks.
        - Make consequences meaningful but keep the adventure moving.
        - Update world state after significant events.
        - Consider player attributes when determining action outcomes."""
    
    @function_tool
    async def roll_dice(self, context: RunContext, sides: int = 20, modifier: int = 0) -> str:
        """Roll dice for skill checks and random events.
        
        Args:
            sides: Number of sides on the die (default 20)
            modifier: Modifier to add to the roll
        """
        roll = random.randint(1, sides)
        total = roll + modifier
        
        if total >= 15:
            outcome = "Success"
        elif total >= 10:
            outcome = "Partial Success"
        else:
            outcome = "Failure"
            
        logger.info(f"Dice roll: {roll} + {modifier} = {total} ({outcome})")
        return f"Roll: {roll} + {modifier} = {total} ({outcome})"
    
    @function_tool
    async def check_inventory(self, context: RunContext) -> str:
        """Check the player's current inventory and status."""
        player = self.world_state["player"]
        inventory_list = ", ".join(player["inventory"])
        return f"HP: {player['hp']}/100 ({player['status']}). Inventory: {inventory_list}. Attributes: STR {player['attributes']['strength']}, INT {player['attributes']['intelligence']}, LUCK {player['attributes']['luck']}."
    
    @function_tool
    async def update_world_state(self, context: RunContext, updates: str) -> str:
        """Update the world state based on player actions.
        
        Args:
            updates: JSON string describing what to update
        """
        try:
            update_data = json.loads(updates)
            
            # Update player stats
            if "player" in update_data:
                for key, value in update_data["player"].items():
                    if key in self.world_state["player"]:
                        self.world_state["player"][key] = value
            
            # Add events
            if "event" in update_data:
                self.world_state["events"].append(update_data["event"])
            
            # Update location
            if "location" in update_data:
                self.world_state["current_location"] = update_data["location"]
            
            # Add new locations
            if "new_location" in update_data:
                loc_name = update_data["new_location"]["name"]
                self.world_state["locations"][loc_name] = update_data["new_location"]
            
            logger.info(f"World state updated: {json.dumps(self.world_state, indent=2)}")
            return "World state updated successfully."
            
        except json.JSONDecodeError:
            return "Failed to parse update data."
    
    @function_tool
    async def switch_universe(self, context: RunContext, universe: str) -> str:
        """Switch to a different universe setting.
        
        Args:
            universe: Universe to switch to (fantasy, cyberpunk, space)
        """
        if universe in UNIVERSES:
            self.current_universe = universe
            self.world_state = self._init_world_state()
            
            # Update world state for new universe
            universe_data = UNIVERSES[universe]
            self.world_state["current_location"] = universe_data["starting_location"]
            
            logger.info(f"Switched to {universe} universe")
            return f"Switched to {UNIVERSES[universe]['name']}! {universe_data['starting_scenario']} What do you do?"
        else:
            return f"Unknown universe. Available: {', '.join(UNIVERSES.keys())}"
    
    @function_tool
    async def save_game(self, context: RunContext) -> str:
        """Save the current game state."""
        save_data = {
            "world_state": self.world_state,
            "universe": self.current_universe
        }
        logger.info(f"Game saved: {json.dumps(save_data, indent=2)}")
        return f"Game saved! Current location: {self.world_state['current_location']}, HP: {self.world_state['player']['hp']}"
    
    @function_tool
    async def get_available_universes(self, context: RunContext) -> str:
        """Get list of available universe settings."""
        universe_list = [f"{key}: {data['name']}" for key, data in UNIVERSES.items()]
        return "Available universes: " + ", ".join(universe_list)




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
        agent=GameMaster(),
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
