import logging
from typing import Optional

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
from voice_manager import VoiceManager

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class TeachTheTutorAssistant(Agent):
    def __init__(self) -> None:
        self.current_mode = "greeting"  # greeting, learn, quiz, teach_back
        self.current_topic = None
        self._agent_session = None
        
        super().__init__(
            instructions="""You are an Active Recall Coach that helps users learn ANY topic through three modes:

MODES:
1. LEARN - Explain any topic clearly (Matthew voice - friendly teacher)
2. QUIZ - Ask questions about any topic (Alicia voice - encouraging questioner) 
3. TEACH_BACK - Let user explain any topic back (Ken voice - supportive evaluator)

You can teach ANY subject: programming, science, history, math, languages, etc.

GREETING MODE: Greet warmly and ask which learning mode and topic they prefer.

LEARN MODE: Explain the requested topic clearly with examples. Ask if they want to switch modes or learn another topic.

QUIZ MODE: Create relevant questions about the topic and provide constructive feedback on answers.

TEACH_BACK MODE: Ask user to explain the topic back to you and give qualitative feedback on their explanation.

Always be encouraging and supportive. Users can switch modes and topics anytime. Start with a warm greeting asking what they'd like to learn about.""",
        )



    def set_session(self, session: AgentSession):
        """Set the agent session reference"""
        self._agent_session = session

    async def _switch_voice(self, mode: str):
        """Switch TTS voice based on mode"""
        try:
            new_tts = VoiceManager.get_tts_for_mode(mode)
            if self._agent_session:
                self._agent_session.tts = new_tts
                logger.info(f"Switched to {mode} voice")
        except Exception as e:
            logger.error(f"Failed to switch voice: {e}")

    @function_tool
    async def switch_to_learn_mode(self, context: RunContext, topic: str = ""):
        """Switch to learn mode to have any topic explained to you.
        
        Args:
            topic: Any topic you want to learn about (programming, science, history, math, etc.)
        """
        self.current_mode = "learn"
        await self._switch_voice("learn")
        
        if topic:
            self.current_topic = topic
            return f"Switching to LEARN mode for {topic}. Let me explain this topic clearly with examples and make it easy to understand."
        else:
            return f"Switched to LEARN mode! What topic would you like me to explain? I can teach you about anything - programming, science, history, math, languages, or any other subject you're curious about."

    @function_tool
    async def switch_to_quiz_mode(self, context: RunContext, topic: str = ""):
        """Switch to quiz mode to be asked questions about any topic.
        
        Args:
            topic: Any topic you want to be quizzed on (programming, science, history, math, etc.)
        """
        self.current_mode = "quiz"
        await self._switch_voice("quiz")
        
        if topic:
            self.current_topic = topic
            return f"Switching to QUIZ mode for {topic}. I'll ask you questions to test your understanding. Ready for your first question about {topic}?"
        else:
            return f"Switched to QUIZ mode! What topic would you like to be quizzed on? I can create questions about any subject you want to test your knowledge on."

    @function_tool
    async def switch_to_teach_back_mode(self, context: RunContext, topic: str = ""):
        """Switch to teach-back mode where you explain any topic back to me.
        
        Args:
            topic: Any topic you want to teach back (programming, science, history, math, etc.)
        """
        self.current_mode = "teach_back"
        await self._switch_voice("teach_back")
        
        if topic:
            self.current_topic = topic
            return f"Switching to TEACH-BACK mode for {topic}. Now you become the teacher! Explain {topic} to me as if I'm learning it for the first time. I'll give you feedback on your explanation."
        else:
            return f"Switched to TEACH-BACK mode! What topic would you like to teach me about? Pick any subject you want to explain and I'll listen and give you constructive feedback."

    @function_tool
    async def select_topic(self, context: RunContext, topic: str):
        """Select a specific topic to work with in the current mode.
        
        Args:
            topic: Any topic to select (programming, science, history, math, etc.)
        """
        self.current_topic = topic
        
        if self.current_mode == "learn":
            return f"Great! Let me explain {topic} clearly with examples and make it easy to understand."
        elif self.current_mode == "quiz":
            return f"Perfect! I'll create questions about {topic} to test your understanding. Ready?"
        elif self.current_mode == "teach_back":
            return f"Excellent! Now you teach me about {topic} - explain it as if I'm learning for the first time!"
        else:
            return f"Selected {topic}. Which mode would you like: learn, quiz, or teach-back?"


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Create session with Matthew voice as default (learn mode)
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-matthew",  # Default to Matthew for greeting/learn mode
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session
    agent = TeachTheTutorAssistant()
    agent.set_session(session)
    await session.start(
        agent=agent,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))