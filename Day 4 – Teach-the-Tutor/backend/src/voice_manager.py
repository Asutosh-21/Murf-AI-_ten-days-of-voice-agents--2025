"""Voice Manager for different learning modes"""

from livekit.plugins import murf
from livekit.agents import tokenize


class VoiceManager:
    """Manages different voices for different learning modes"""
    
    @staticmethod
    def get_tts_for_mode(mode: str):
        """Get appropriate TTS voice for the learning mode"""
        voice_config = {
            "learn": "en-US-matthew",      # Friendly teacher voice
            "quiz": "en-US-alicia",       # Encouraging questioner voice  
            "teach_back": "en-US-ken",    # Supportive evaluator voice
            "greeting": "en-US-matthew"   # Default greeting voice
        }
        
        voice = voice_config.get(mode, "en-US-matthew")
        
        return murf.TTS(
            voice=voice,
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )