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

logger = logging.getLogger("telephony_agent")
load_dotenv(".env.local")

class TelephonyFraudAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a fraud detection representative for NovaTrust Bank calling customers about suspicious transactions.

TELEPHONY PROTOCOL:
- This is a PHONE CALL, speak naturally and clearly
- Start: "Hello, this is NovaTrust Bank Fraud Department calling about suspicious activity on your account. May I have your name please?"
- Wait for customer name, then use load_fraud_case function
- Ask security question from their case
- Use verify_customer function with their answer
- If verified, use get_transaction_details and read details clearly
- Ask "Did you make this transaction? Please say yes or no"
- Use mark_transaction_safe or mark_transaction_fraudulent based on answer
- Confirm action and end call professionally

Keep responses conversational for phone calls. Log all actions.""",
        )
        self.current_case = None
        self.verification_passed = False
        self.call_log = []

    def _log_action(self, action: str, details: str = ""):
        """Log telephony actions"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action}: {details}"
        self.call_log.append(log_entry)
        logger.info(f"TELEPHONY - {log_entry}")

    @function_tool
    async def load_fraud_case(self, context: RunContext, customer_name: str):
        """Load fraud case for telephony customer"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fraud_database.json")
            with open(db_path, 'r', encoding='utf-8') as f:
                cases = json.load(f)
            
            for case in cases:
                if case['userName'].lower() == customer_name.lower():
                    self.current_case = case
                    self._log_action("CASE_LOADED", f"Customer: {customer_name}, ID: {case['securityIdentifier']}")
                    return f"Thank you {customer_name}. For security verification, {case['securityQuestion']}"
            
            self._log_action("CASE_NOT_FOUND", f"Customer: {customer_name}")
            return f"I'm sorry, I don't have a case for {customer_name}. Please verify your name."
            
        except Exception as e:
            self._log_action("DATABASE_ERROR", str(e))
            logger.error(f"Telephony database error: {e}")
            return "I'm experiencing technical difficulties. Please call back later."
    
    @function_tool
    async def verify_customer(self, context: RunContext, answer: str):
        """Verify telephony customer identity"""
        if not self.current_case:
            return "Please provide your name first."
        
        if answer.lower().strip() == self.current_case['securityAnswer'].lower().strip():
            self.verification_passed = True
            self._log_action("VERIFICATION_SUCCESS", f"Customer verified: {self.current_case['userName']}")
            return "Thank you, verification successful. Let me review the suspicious transaction."
        else:
            self._log_action("VERIFICATION_FAILED", f"Wrong answer for: {self.current_case['userName']}")
            return "I'm sorry, that doesn't match our records. For security reasons, I cannot proceed with this call. Goodbye."
    
    @function_tool
    async def get_transaction_details(self, context: RunContext):
        """Get transaction details for telephony"""
        if not self.current_case or not self.verification_passed:
            return "Verification required before proceeding."
        
        case = self.current_case
        details = f"We detected a suspicious transaction from {case['transactionName']} for {case['transactionAmount']} on your card ending in {case['cardEnding']}. This occurred in {case['location']} on {case['transactionTime']}."
        
        self._log_action("TRANSACTION_READ", f"Case: {case['securityIdentifier']}")
        return details
    
    @function_tool
    async def mark_transaction_safe(self, context: RunContext):
        """Mark transaction as safe via telephony"""
        if not self.current_case or not self.verification_passed:
            return "Verification required."
        
        self.current_case['case'] = 'confirmed_safe'
        self.current_case['outcome'] = f"Customer confirmed via phone on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self._update_database()
        
        self._log_action("MARKED_SAFE", f"Case: {self.current_case['securityIdentifier']}")
        return "Thank you for confirming. The transaction has been marked as legitimate. No further action is needed. Have a great day!"
    
    @function_tool
    async def mark_transaction_fraudulent(self, context: RunContext):
        """Mark transaction as fraudulent via telephony"""
        if not self.current_case or not self.verification_passed:
            return "Verification required."
        
        self.current_case['case'] = 'confirmed_fraud'
        self.current_case['outcome'] = f"Customer denied via phone on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self._update_database()
        
        self._log_action("MARKED_FRAUD", f"Case: {self.current_case['securityIdentifier']}, Card: {self.current_case['cardEnding']}")
        return f"I understand. I have immediately blocked your card ending in {self.current_case['cardEnding']} and initiated a dispute for the {self.current_case['transactionAmount']} charge. You will receive a new card within 3 to 5 business days. Is there anything else I can help you with today?"
    
    def _update_database(self):
        """Update database with telephony call results"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fraud_database.json")
            with open(db_path, 'r', encoding='utf-8') as f:
                cases = json.load(f)
            
            for i, case in enumerate(cases):
                if case['securityIdentifier'] == self.current_case['securityIdentifier']:
                    cases[i] = self.current_case
                    break
            
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(cases, f, indent=2, ensure_ascii=False)
            
            self._log_action("DATABASE_UPDATED", f"Case: {self.current_case['securityIdentifier']}")
            
        except Exception as e:
            self._log_action("DATABASE_UPDATE_ERROR", str(e))
            logger.error(f"Telephony database update error: {e}")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    # Enhanced logging for telephony
    ctx.log_context_fields = {
        "room": ctx.room.name,
        "telephony": True,
        "fraud_agent": "NovaTrust"
    }
    
    logger.info(f"TELEPHONY - Starting fraud agent for room: {ctx.room.name}")

    # Optimized for telephony calls
    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=google.LLM(),
        tts=murf.TTS(
            voice="en-US-matthew", 
            style="Conversation",
            # Optimized for phone calls
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=1)
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
        logger.info(f"TELEPHONY - Usage summary: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Use BVCTelephony for best telephony performance
    await session.start(
        agent=TelephonyFraudAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVCTelephony(),
        ),
    )

    await ctx.connect()
    logger.info("TELEPHONY - Fraud agent connected and ready for calls")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))