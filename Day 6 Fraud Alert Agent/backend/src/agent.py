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

class FraudAlertAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a fraud detection representative for NovaTrust Bank. 

Start every conversation by saying: "Hello, this is NovaTrust Bank Fraud Department. We detected suspicious activity on your account. May I have your name to look up your case?"

Follow this process:
1. Get customer name and use load_fraud_case function
2. Ask the security question from their case  
3. Use verify_customer function with their answer
4. If verified, use get_transaction_details function and read the details
5. Ask "Did you make this transaction? Please answer yes or no"
6. Use mark_transaction_safe or mark_transaction_fraudulent based on their answer
7. Confirm what action was taken

Always use the function tools. Keep responses brief and professional.""",
        )
        self.current_case = None
        self.verification_passed = False

    @function_tool
    async def load_fraud_case(self, context: RunContext, customer_name: str):
        """Load fraud case for customer"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fraud_database.json")
            with open(db_path, 'r') as f:
                cases = json.load(f)
            
            for case in cases:
                if case['userName'].lower() == customer_name.lower():
                    self.current_case = case
                    return f"Found case for {customer_name}. {case['securityQuestion']}"
            
            return f"No case found for {customer_name}"
        except Exception as e:
            logger.error(f"Database error: {e}")
            return "Database error"
    
    @function_tool
    async def verify_customer(self, context: RunContext, answer: str):
        """Verify customer identity"""
        if not self.current_case:
            return "No case loaded"
        
        if answer.lower().strip() == self.current_case['securityAnswer'].lower().strip():
            self.verification_passed = True
            return "Verification successful"
        else:
            return "Verification failed"
    
    @function_tool
    async def get_transaction_details(self, context: RunContext):
        """Get transaction details"""
        if not self.current_case or not self.verification_passed:
            return "Verification required"
        
        case = self.current_case
        return f"Suspicious transaction: {case['transactionName']} for {case['transactionAmount']} on card ending {case['cardEnding']} from {case['location']} on {case['transactionTime']}"
    
    @function_tool
    async def mark_transaction_safe(self, context: RunContext):
        """Mark transaction as safe"""
        if not self.current_case or not self.verification_passed:
            return "Verification required"
        
        self.current_case['case'] = 'confirmed_safe'
        self.current_case['outcome'] = f"Customer confirmed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self._update_database()
        return "Transaction marked as safe. No action needed."
    
    @function_tool
    async def mark_transaction_fraudulent(self, context: RunContext):
        """Mark transaction as fraud"""
        if not self.current_case or not self.verification_passed:
            return "Verification required"
        
        self.current_case['case'] = 'confirmed_fraud'
        self.current_case['outcome'] = f"Customer denied on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self._update_database()
        return f"Card ending {self.current_case['cardEnding']} blocked. Dispute initiated."
    
    def _update_database(self):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fraud_database.json")
            with open(db_path, 'r') as f:
                cases = json.load(f)
            
            for i, case in enumerate(cases):
                if case['securityIdentifier'] == self.current_case['securityIdentifier']:
                    cases[i] = self.current_case
                    break
            
            with open(db_path, 'w') as f:
                json.dump(cases, f, indent=2)
        except Exception as e:
            logger.error(f"Update error: {e}")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=google.LLM(),
        tts=murf.TTS(voice="en-US-matthew", style="Conversation"),
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
        agent=FraudAlertAssistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))