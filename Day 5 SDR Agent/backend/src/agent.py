import logging
import json
import os
from datetime import datetime
from typing import Dict, Any

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

# Load Zerodha company data
with open("data/company_faq.json", "r") as f:
    COMPANY_DATA = json.load(f)

# Load mock calendar data
with open("data/mock_calendar.json", "r") as f:
    CALENDAR_DATA = json.load(f)

# Global lead storage for the session
LEAD_DATA = {
    "name": None,
    "company": None,
    "email": None,
    "role": None,
    "use_case": None,
    "team_size": None,
    "timeline": None,
    "conversation_notes": [],
    "meeting_booked": None,
    "pain_points": [],
    "budget_mentioned": False,
    "decision_maker_type": "unknown",
    "urgency_level": "unknown"
}


class ZerodhaSDRAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=f"""You are an SDR (Sales Development Representative) for {COMPANY_DATA['company']}.

Your job:
1. Greet every visitor warmly: "Hi! I'm your Zerodha assistant. What brings you here today?"
2. After answering 2-3 questions, PROACTIVELY ask: "I'd love to learn more about you. Could you share your name and what type of trading/investing interests you?"
3. Answer user questions STRICTLY using the FAQ content provided - do NOT add anything that is not in the FAQ
4. If asked about something not in the FAQ, say "This information is not in my FAQ, so I can't confirm that"
5. AUTOMATICALLY collect lead details by asking:
   - "What's your name?" (if not provided)
   - "What's your email so I can send you resources?" (after good conversation)
   - "Are you a beginner, experienced trader, or investor?"
   - "What interests you most - stocks, mutual funds, or F&O trading?"
   - "When are you looking to start?"
6. After collecting basic info, AUTOMATICALLY offer: "Would you like me to schedule a quick 30-minute demo to show you our platform? I have some great slots available."
7. When offering demo, use show_available_meeting_slots() and book_meeting_slot()
8. Throughout conversation, note pain points, budget mentions, and decision-making authority
9. Be proactive: "Based on what you've told me, I think Zerodha would be perfect for you. Let me book you a demo!"
10. When conversation naturally ends, provide summary with fit score and save data

Be enthusiastic, helpful, and always guide toward booking a demo!""",
        )

    @function_tool
    async def search_zerodha_faq(self, context: RunContext, query: str):
        """Search Zerodha FAQ for relevant information. Only return exact FAQ content.
        
        Args:
            query: The user's question or topic to search for
        """
        query_lower = query.lower()
        
        # Enhanced keyword mapping for comprehensive matching
        keyword_mapping = {
            # Basic company info
            "what does zerodha do": ["what does zerodha do"],
            "about zerodha": ["what does zerodha do"],
            "zerodha business": ["what does zerodha do"],
            
            # Pricing and fees
            "free": ["do you have a free plan", "what are your brokerage fees"],
            "cost": ["what are your brokerage fees"],
            "price": ["what are your brokerage fees"],
            "brokerage": ["what are your brokerage fees"],
            "charges": ["what are your brokerage fees", "what are amc charges", "what are the fund transfer charges"],
            "fees": ["what are your brokerage fees"],
            "expensive": ["what are your brokerage fees"],
            "cheap": ["what are your brokerage fees"],
            
            # Account opening
            "account": ["how do i open an account", "what documents are required"],
            "open account": ["how do i open an account"],
            "signup": ["how do i open an account"],
            "register": ["how do i open an account"],
            "documents": ["what documents are required"],
            "kyc": ["how do i open an account"],
            
            # Trading platforms
            "kite": ["what is kite", "what trading platforms do you offer"],
            "app": ["do you have a mobile app", "what is kite"],
            "mobile": ["do you have a mobile app"],
            "platform": ["what trading platforms do you offer"],
            "software": ["what trading platforms do you offer"],
            
            # Mutual funds
            "mutual fund": ["do you offer mutual funds", "what is coin", "what are the charges for mutual funds"],
            "sip": ["do you offer mutual funds", "what is coin"],
            "coin": ["what is coin"],
            
            # Safety and security
            "safe": ["is zerodha safe"],
            "security": ["is zerodha safe"],
            "secure": ["is zerodha safe"],
            "trust": ["is zerodha safe"],
            "reliable": ["is zerodha safe"],
            
            # Trading types
            "intraday": ["what are the intraday timings", "can i convert intraday to delivery"],
            "delivery": ["can i convert intraday to delivery"],
            "options": ["can i trade options and futures", "what is sensibull"],
            "futures": ["can i trade options and futures"],
            "f&o": ["can i trade options and futures"],
            "commodity": ["do you offer commodity trading"],
            "currency": ["can i trade currencies"],
            
            # Support
            "support": ["do you have customer support"],
            "help": ["do you have customer support"],
            "contact": ["do you have customer support"],
            "phone": ["do you have customer support"],
            
            # Minimum investment
            "minimum": ["what is the minimum amount to start trading"],
            "start": ["what is the minimum amount to start trading"],
            "begin": ["what is the minimum amount to start trading"],
            
            # Research and tips
            "tips": ["do you provide research and tips"],
            "research": ["do you provide research and tips"],
            "advice": ["do you provide research and tips"],
            "recommendation": ["do you provide research and tips"],
            
            # IPO
            "ipo": ["can i invest in ipos"],
            
            # Algo trading
            "algo": ["do you offer algo trading", "what is streak"],
            "algorithm": ["do you offer algo trading", "what is streak"],
            "streak": ["what is streak"],
            
            # Margin
            "margin": ["what is your margin policy"],
            "leverage": ["what is your margin policy"],
            
            # Time related
            "time": ["how long does account opening take", "what are the intraday timings"],
            "timing": ["what are the intraday timings"],
            "hours": ["what are the intraday timings"],
            
            # Payment methods
            "upi": ["do you support upi payments"],
            "payment": ["do you support upi payments", "what are the fund transfer charges"],
            "transfer": ["what are the fund transfer charges"],
            
            # Tax
            "tax": ["what are the tax implications"],
            
            # Portfolio
            "portfolio": ["do you offer portfolio management", "what is console"],
            "console": ["what is console"],
            
            # Education
            "learn": ["what is varsity"],
            "education": ["what is varsity"],
            "varsity": ["what is varsity"]
        }
        
        # First try exact question matching
        for faq in COMPANY_DATA['faqs']:
            if query_lower in faq['question'].lower() or faq['question'].lower() in query_lower:
                return faq['answer']
        
        # Then try keyword-based matching
        matched_faqs = []
        for keyword, questions in keyword_mapping.items():
            if keyword in query_lower:
                for faq in COMPANY_DATA['faqs']:
                    for question in questions:
                        if question in faq['question'].lower():
                            matched_faqs.append(faq)
        
        # Return first match or search by individual words
        if matched_faqs:
            return matched_faqs[0]['answer']
        
        # Search in company details and other sections
        if 'founder' in query_lower or 'who started' in query_lower or 'who founded' in query_lower:
            return f"Zerodha was founded in 2010 by {COMPANY_DATA['company_details']['founders']} in {COMPANY_DATA['company_details']['headquarters']}."
        
        if 'how big' in query_lower or 'size' in query_lower or 'customers' in query_lower:
            return f"Zerodha has {COMPANY_DATA['company_details']['customers']} customers and handles {COMPANY_DATA['company_details']['daily_trades']} trades daily."
        
        if 'how it works' in query_lower or 'process' in query_lower:
            return COMPANY_DATA['how_it_works']['trading_process']
        
        if 'why zerodha' in query_lower or 'why choose' in query_lower:
            return COMPANY_DATA['why_zerodha']['cost_advantage'] + ' ' + COMPANY_DATA['why_zerodha']['technology_first']
        
        # Last resort: search by individual words in query
        query_words = query_lower.split()
        for faq in COMPANY_DATA['faqs']:
            faq_text = (faq['question'] + ' ' + faq['answer']).lower()
            if any(word in faq_text for word in query_words if len(word) > 3):
                return faq['answer']
        
        return "This information is not in my FAQ, so I can't confirm that. Let me connect you with our team for detailed information."
    
    @function_tool
    async def capture_lead_field(self, context: RunContext, field_type: str, value: str):
        """Capture specific lead information during conversation.
        
        Args:
            field_type: Type of information (name, email, role, use_case, timeline, company, team_size)
            value: The actual value provided by the user
        """
        global LEAD_DATA
        
        if field_type in LEAD_DATA:
            LEAD_DATA[field_type] = value
            LEAD_DATA['conversation_notes'].append(f"Captured {field_type}: {value}")
            logger.info(f"Captured lead field: {field_type} = {value}")
            return f"Perfect! I've noted that your {field_type} is {value}."
        else:
            return "I'll make a note of that information."
    
    @function_tool
    async def detect_end_call_intent(self, context: RunContext, user_message: str):
        """Detect if user wants to end the call and trigger summary.
        
        Args:
            user_message: The user's message to analyze
        """
        end_phrases = [
            "that's all", "i'm done", "thanks", "thank you", 
            "okay you can wrap up", "that's it for now", "wrap up",
            "i think that's everything", "nothing else", "that covers it"
        ]
        
        message_lower = user_message.lower()
        
        for phrase in end_phrases:
            if phrase in message_lower:
                return await self.generate_final_summary(context)
        
        return None
    
    @function_tool
    async def generate_final_summary(self, context: RunContext):
        """Generate final lead summary with CRM analysis and save to JSON file."""
        global LEAD_DATA
        
        # Analyze conversation for CRM insights
        conversation_text = " ".join(LEAD_DATA.get('conversation_notes', []))
        await self.analyze_conversation_for_crm(context, conversation_text)
        
        # Add session metadata
        LEAD_DATA['timestamp'] = datetime.now().isoformat()
        LEAD_DATA['session_id'] = context.room.name
        LEAD_DATA['company_contacted'] = COMPANY_DATA['company']
        
        # Create CRM notes
        crm_notes = {
            "lead_summary": f"{LEAD_DATA.get('name', 'Unknown')} - {LEAD_DATA.get('role', 'Unknown role')} interested in {LEAD_DATA.get('use_case', 'general services')}",
            "key_points": LEAD_DATA.get('pain_points', []),
            "budget_discussed": LEAD_DATA.get('budget_mentioned', False),
            "decision_authority": LEAD_DATA.get('decision_maker_type', 'unknown'),
            "urgency": LEAD_DATA.get('urgency_level', 'unknown'),
            "timeline_refined": LEAD_DATA.get('timeline', 'not specified'),
            "fit_score": LEAD_DATA.get('fit_score', 50),
            "next_steps": "Follow up via email" + (" and demo call scheduled" if LEAD_DATA.get('meeting_booked') else "")
        }
        
        LEAD_DATA['crm_analysis'] = crm_notes
        
        # Create directories
        os.makedirs('leads', exist_ok=True)
        os.makedirs('crm_notes', exist_ok=True)
        
        # Save lead file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        lead_filename = f"leads/zerodha_lead_{timestamp}.json"
        crm_filename = f"crm_notes/crm_analysis_{timestamp}.json"
        
        with open(lead_filename, 'w') as f:
            json.dump(LEAD_DATA, f, indent=2)
        
        with open(crm_filename, 'w') as f:
            json.dump(crm_notes, f, indent=2)
        
        # Generate verbal summary
        name = LEAD_DATA.get('name', 'our visitor')
        role = LEAD_DATA.get('role', 'not specified')
        use_case = LEAD_DATA.get('use_case', 'general interest')
        timeline = LEAD_DATA.get('timeline', 'not specified')
        fit_score = LEAD_DATA.get('fit_score', 50)
        meeting_info = ""
        
        if LEAD_DATA.get('meeting_booked'):
            meeting = LEAD_DATA['meeting_booked']
            meeting_info = f" We've also scheduled a demo for {meeting['date']} at {meeting['time']}."
        
        summary = f"""Thank you for your time today! Let me quickly summarize:
        
I spoke with {name}, who is interested in {use_case}. 
Their experience level is {role} and they're looking to start {timeline}.
Based on our conversation, I've given this lead a fit score of {fit_score}/100.{meeting_info}
        
I've saved all your details and our CRM analysis. Someone from our team will follow up with you soon. 
Thank you for considering Zerodha for your investment and trading needs!"""
        
        logger.info(f"Lead and CRM analysis saved to {lead_filename} and {crm_filename}")
        logger.info(f"Lead data: {LEAD_DATA}")
        
        return summary
    
    @function_tool
    async def show_available_meeting_slots(self, context: RunContext):
        """Show available meeting slots when user wants to book a demo or meeting."""
        available_slots = [slot for slot in CALENDAR_DATA['available_slots'] 
                          if slot['id'] not in [meeting['slot_id'] for meeting in CALENDAR_DATA['booked_meetings']]]
        
        if not available_slots:
            return "I don't have any available slots right now. Let me check with our team and get back to you."
        
        slots_text = "I have these available slots for a Zerodha demo:\n"
        for i, slot in enumerate(available_slots[:3], 1):
            slots_text += f"{i}. {slot['date']} at {slot['time']} ({slot['duration']})\n"
        
        slots_text += "Which slot works best for you? Just say the number or tell me the date and time."
        return slots_text
    
    @function_tool
    async def book_meeting_slot(self, context: RunContext, slot_choice: str):
        """Book a specific meeting slot based on user choice.
        
        Args:
            slot_choice: User's choice (number, date, or time preference)
        """
        global LEAD_DATA, CALENDAR_DATA
        
        available_slots = [slot for slot in CALENDAR_DATA['available_slots'] 
                          if slot['id'] not in [meeting['slot_id'] for meeting in CALENDAR_DATA['booked_meetings']]]
        
        selected_slot = None
        choice_lower = slot_choice.lower()
        
        # Try to match by number
        if choice_lower in ['1', 'first', 'one']:
            selected_slot = available_slots[0] if available_slots else None
        elif choice_lower in ['2', 'second', 'two']:
            selected_slot = available_slots[1] if len(available_slots) > 1 else None
        elif choice_lower in ['3', 'third', 'three']:
            selected_slot = available_slots[2] if len(available_slots) > 2 else None
        else:
            # Try to match by date or time
            for slot in available_slots:
                if slot['date'] in choice_lower or slot['time'].lower() in choice_lower:
                    selected_slot = slot
                    break
        
        if not selected_slot:
            return "I couldn't find that slot. Could you please choose from the available options I mentioned?"
        
        # Book the meeting
        meeting_details = {
            "slot_id": selected_slot['id'],
            "date": selected_slot['date'],
            "time": selected_slot['time'],
            "duration": selected_slot['duration'],
            "lead_name": LEAD_DATA.get('name', 'Unknown'),
            "lead_email": LEAD_DATA.get('email', 'Not provided'),
            "booked_at": datetime.now().isoformat()
        }
        
        CALENDAR_DATA['booked_meetings'].append(meeting_details)
        LEAD_DATA['meeting_booked'] = meeting_details
        
        # Save updated calendar
        with open("data/mock_calendar.json", "w") as f:
            json.dump(CALENDAR_DATA, f, indent=2)
        
        return f"Perfect! I've booked your Zerodha demo for {selected_slot['date']} at {selected_slot['time']}. You'll receive a confirmation email shortly. Looking forward to showing you our platform!"
    
    @function_tool
    async def analyze_conversation_for_crm(self, context: RunContext, conversation_text: str):
        """Analyze conversation to extract CRM insights and qualification score.
        
        Args:
            conversation_text: The full conversation transcript
        """
        global LEAD_DATA
        
        text_lower = conversation_text.lower()
        
        # Extract pain points
        pain_indicators = ['problem', 'issue', 'difficult', 'expensive', 'slow', 'frustrated', 'need', 'looking for']
        pain_points = []
        for indicator in pain_indicators:
            if indicator in text_lower:
                pain_points.append(f"Mentioned {indicator}")
        
        # Check budget mentions
        budget_keywords = ['budget', 'cost', 'price', 'expensive', 'cheap', 'afford', 'money', 'fees']
        budget_mentioned = any(keyword in text_lower for keyword in budget_keywords)
        
        # Determine decision maker type
        decision_keywords = ['i decide', 'my decision', 'i choose', 'founder', 'ceo', 'owner']
        influencer_keywords = ['team decision', 'discuss with', 'check with', 'manager', 'boss']
        
        if any(keyword in text_lower for keyword in decision_keywords):
            decision_maker_type = "decision_maker"
        elif any(keyword in text_lower for keyword in influencer_keywords):
            decision_maker_type = "influencer"
        else:
            decision_maker_type = "unknown"
        
        # Assess urgency
        urgent_keywords = ['urgent', 'asap', 'immediately', 'right now', 'this week']
        soon_keywords = ['soon', 'next month', 'few weeks', 'planning']
        
        if any(keyword in text_lower for keyword in urgent_keywords):
            urgency_level = "high"
        elif any(keyword in text_lower for keyword in soon_keywords):
            urgency_level = "medium"
        else:
            urgency_level = "low"
        
        # Calculate fit score (0-100)
        fit_score = 50  # Base score
        
        if LEAD_DATA.get('email'): fit_score += 15
        if LEAD_DATA.get('name'): fit_score += 10
        if LEAD_DATA.get('use_case'): fit_score += 15
        if budget_mentioned: fit_score += 10
        if decision_maker_type == "decision_maker": fit_score += 20
        elif decision_maker_type == "influencer": fit_score += 10
        if urgency_level == "high": fit_score += 15
        elif urgency_level == "medium": fit_score += 10
        if LEAD_DATA.get('meeting_booked'): fit_score += 15
        
        # Update lead data
        LEAD_DATA.update({
            'pain_points': pain_points,
            'budget_mentioned': budget_mentioned,
            'decision_maker_type': decision_maker_type,
            'urgency_level': urgency_level,
            'fit_score': min(fit_score, 100)
        })
        
        return f"CRM analysis complete. Fit score: {fit_score}/100"
    
    @function_tool
    async def proactive_demo_offer(self, context: RunContext):
        """Proactively offer demo booking after collecting basic lead info."""
        global LEAD_DATA
        
        # Check if we have enough info to offer demo
        has_name = LEAD_DATA.get('name') is not None
        has_interest = LEAD_DATA.get('use_case') is not None
        
        if has_name and has_interest and not LEAD_DATA.get('meeting_booked'):
            return await self.show_available_meeting_slots(context)
        
        return "Let me learn a bit more about you first, then I can show you our platform!"
    
    @function_tool
    async def proactive_lead_collection(self, context: RunContext, missing_field: str):
        """Proactively ask for missing lead information.
        
        Args:
            missing_field: The field that needs to be collected (name, email, use_case, timeline)
        """
        prompts = {
            'name': "I'd love to personalize our conversation! What's your name?",
            'email': "Could you share your email? I'll send you some helpful resources about trading and investing.",
            'use_case': "What interests you most - stock trading, mutual fund investing, or F&O trading?",
            'timeline': "When are you looking to start your investment journey?",
            'role': "Are you new to investing, or do you have some trading experience?"
        }
        
        return prompts.get(missing_field, "Could you tell me more about your investment goals?")
    
    @function_tool
    async def add_conversation_note(self, context: RunContext, note: str):
        """Add a note about the conversation for lead context.
        
        Args:
            note: Important information or context from the conversation
        """
        global LEAD_DATA
        LEAD_DATA['conversation_notes'].append(f"{datetime.now().strftime('%H:%M:%S')}: {note}")
        return "Noted."


def prewarm(proc: JobProcess):
    """Preload models and company data for faster agent startup."""
    proc.userdata["vad"] = silero.VAD.load()
    
    # Preload company FAQ data
    proc.userdata["company_data"] = COMPANY_DATA
    logger.info(f"Preloaded {COMPANY_DATA['company']} FAQ with {len(COMPANY_DATA['faqs'])} entries")


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

    # Start the session with Zerodha SDR agent
    await session.start(
        agent=ZerodhaSDRAssistant(),
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
