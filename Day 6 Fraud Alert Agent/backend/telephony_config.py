#!/usr/bin/env python3
"""
LiveKit Telephony Configuration for NovaTrust Bank Fraud Agent
"""

import os
from dotenv import load_dotenv

load_dotenv(".env.local")

# LiveKit Telephony Configuration
TELEPHONY_CONFIG = {
    # LiveKit Server Configuration
    "livekit_url": os.getenv("LIVEKIT_URL"),
    "livekit_api_key": os.getenv("LIVEKIT_API_KEY"),
    "livekit_api_secret": os.getenv("LIVEKIT_API_SECRET"),
    
    # SIP Configuration (for phone integration)
    "sip_trunk": {
        "name": "novatrust-fraud-trunk",
        "inbound_addresses": ["sip.livekit.io"],
        "outbound_address": "sip.livekit.io",
        "transport": "udp"
    },
    
    # Phone Number Configuration
    "phone_config": {
        "country_code": "+1",
        "area_code": "555",
        "number": "0123",  # Demo number
        "full_number": "+15550123"
    },
    
    # Agent Configuration
    "agent_config": {
        "name": "NovaTrust Fraud Agent",
        "description": "Automated fraud detection and verification system",
        "max_call_duration": 600,  # 10 minutes
        "auto_hangup_timeout": 30,  # 30 seconds of silence
    },
    
    # Fraud Detection Settings
    "fraud_settings": {
        "max_verification_attempts": 3,
        "case_timeout": 300,  # 5 minutes
        "require_verification": True,
        "log_all_calls": True
    }
}

def get_telephony_config():
    """Get telephony configuration"""
    return TELEPHONY_CONFIG

def validate_config():
    """Validate telephony configuration"""
    required_env = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing = [var for var in required_env if not os.getenv(var)]
    
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        return False
    
    print("Telephony configuration validated successfully")
    return True

if __name__ == "__main__":
    if validate_config():
        config = get_telephony_config()
        print("LiveKit Telephony Configuration:")
        print(f"  Server: {config['livekit_url']}")
        print(f"  Phone: {config['phone_config']['full_number']}")
        print(f"  Agent: {config['agent_config']['name']}")
    else:
        print("Configuration validation failed!")