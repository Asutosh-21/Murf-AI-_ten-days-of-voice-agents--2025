#!/usr/bin/env python3
"""
Call logging system for telephony fraud agent
"""

import json
import os
from datetime import datetime
from typing import List, Dict

CALL_LOG_FILE = "call_logs.json"

def log_call(call_data: Dict):
    """Log a telephony call"""
    try:
        # Load existing logs
        if os.path.exists(CALL_LOG_FILE):
            with open(CALL_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Add timestamp if not present
        if 'timestamp' not in call_data:
            call_data['timestamp'] = datetime.now().isoformat()
        
        # Add call to logs
        logs.append(call_data)
        
        # Save logs
        with open(CALL_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"Call logged: {call_data.get('customer_name', 'Unknown')} - {call_data.get('outcome', 'No outcome')}")
        
    except Exception as e:
        print(f"Error logging call: {e}")

def get_call_logs() -> List[Dict]:
    """Get all call logs"""
    try:
        if os.path.exists(CALL_LOG_FILE):
            with open(CALL_LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error reading call logs: {e}")
        return []

def show_call_logs():
    """Display call logs"""
    logs = get_call_logs()
    
    if not logs:
        print("No call logs found.")
        return
    
    print(f"\n[NOVATRUST BANK] Telephony Call Logs ({len(logs)} calls)")
    print("=" * 60)
    
    for i, log in enumerate(logs, 1):
        timestamp = log.get('timestamp', 'Unknown time')
        customer = log.get('customer_name', 'Unknown customer')
        outcome = log.get('outcome', 'No outcome')
        case_id = log.get('case_id', 'Unknown')
        call_duration = log.get('duration', 'Unknown')
        
        print(f"\nCall {i}:")
        print(f"  Time: {timestamp}")
        print(f"  Customer: {customer}")
        print(f"  Case ID: {case_id}")
        print(f"  Outcome: {outcome}")
        print(f"  Duration: {call_duration}")
        
        if 'verification_status' in log:
            print(f"  Verification: {log['verification_status']}")
        
        if 'transaction_decision' in log:
            print(f"  Decision: {log['transaction_decision']}")

def clear_call_logs():
    """Clear all call logs"""
    try:
        if os.path.exists(CALL_LOG_FILE):
            os.remove(CALL_LOG_FILE)
        print("Call logs cleared successfully.")
    except Exception as e:
        print(f"Error clearing call logs: {e}")

def get_call_stats():
    """Get call statistics"""
    logs = get_call_logs()
    
    if not logs:
        return {"total_calls": 0}
    
    stats = {
        "total_calls": len(logs),
        "verified_calls": 0,
        "failed_verification": 0,
        "safe_transactions": 0,
        "fraud_transactions": 0,
        "incomplete_calls": 0
    }
    
    for log in logs:
        if log.get('verification_status') == 'success':
            stats['verified_calls'] += 1
        elif log.get('verification_status') == 'failed':
            stats['failed_verification'] += 1
        
        if log.get('transaction_decision') == 'safe':
            stats['safe_transactions'] += 1
        elif log.get('transaction_decision') == 'fraud':
            stats['fraud_transactions'] += 1
        elif log.get('outcome') == 'incomplete':
            stats['incomplete_calls'] += 1
    
    return stats

def show_call_stats():
    """Display call statistics"""
    stats = get_call_stats()
    
    print("\n[NOVATRUST BANK] Call Statistics")
    print("=" * 40)
    print(f"Total Calls: {stats['total_calls']}")
    print(f"Verified Calls: {stats['verified_calls']}")
    print(f"Failed Verification: {stats['failed_verification']}")
    print(f"Safe Transactions: {stats['safe_transactions']}")
    print(f"Fraud Transactions: {stats['fraud_transactions']}")
    print(f"Incomplete Calls: {stats['incomplete_calls']}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "show":
            show_call_logs()
        elif sys.argv[1] == "stats":
            show_call_stats()
        elif sys.argv[1] == "clear":
            clear_call_logs()
        else:
            print("Usage: python call_logs.py [show|stats|clear]")
    else:
        show_call_logs()