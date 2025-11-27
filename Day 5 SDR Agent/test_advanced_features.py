#!/usr/bin/env python3
"""
Test script for Advanced Features - Meeting Scheduler & CRM Analysis
"""

import json
import os

def test_calendar_data():
    """Test if calendar data is properly loaded"""
    print("Testing Calendar Data...")
    
    try:
        with open("backend/data/mock_calendar.json", "r") as f:
            calendar_data = json.load(f)
        
        print(f"[OK] Available slots: {len(calendar_data['available_slots'])}")
        print(f"[OK] Booked meetings: {len(calendar_data['booked_meetings'])}")
        
        # Show sample slots
        for i, slot in enumerate(calendar_data['available_slots'][:3], 1):
            print(f"[OK] Slot {i}: {slot['date']} at {slot['time']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error loading calendar data: {e}")
        return False

def test_directories():
    """Test if all required directories exist"""
    print("\nTesting Directory Structure...")
    
    required_dirs = [
        "backend/data",
        "backend/leads", 
        "backend/crm_notes",
        "backend/src"
    ]
    
    all_good = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"[OK] Directory exists: {directory}")
        else:
            print(f"[ERROR] Missing directory: {directory}")
            all_good = False
    
    return all_good

def test_agent_advanced_features():
    """Test if agent.py has the advanced features"""
    print("\nTesting Advanced Agent Features...")
    
    try:
        with open("backend/src/agent.py", "r") as f:
            agent_content = f.read()
        
        advanced_features = [
            "show_available_meeting_slots",
            "book_meeting_slot", 
            "analyze_conversation_for_crm",
            "fit_score",
            "pain_points",
            "decision_maker_type",
            "urgency_level",
            "crm_analysis"
        ]
        
        all_good = True
        for feature in advanced_features:
            if feature in agent_content:
                print(f"[OK] Feature found: {feature}")
            else:
                print(f"[ERROR] Missing feature: {feature}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"[ERROR] Error reading agent.py: {e}")
        return False

def show_advanced_test_scenarios():
    """Show test scenarios for advanced features"""
    print("\nAdvanced Feature Testing Scenarios:")
    print("=" * 50)
    
    scenarios = [
        {
            "title": "Meeting Scheduler Test",
            "inputs": [
                "I'd like to book a demo",
                "Can we schedule a meeting?", 
                "I want to book a call",
                "Show me available times",
                "I'll take slot 1" or "I'll take the first one",
                "Book me for tomorrow at 2 PM"
            ]
        },
        {
            "title": "CRM Analysis - Pain Points",
            "inputs": [
                "I'm frustrated with my current broker",
                "The fees are too expensive", 
                "I have problems with slow execution",
                "I need a better platform",
                "Looking for cheaper options"
            ]
        },
        {
            "title": "CRM Analysis - Budget Discussion", 
            "inputs": [
                "What are your costs?",
                "Is it expensive?",
                "I'm on a tight budget",
                "Can I afford this?",
                "What are the fees?"
            ]
        },
        {
            "title": "CRM Analysis - Decision Making",
            "inputs": [
                "I make the decisions here",  # decision maker
                "I need to check with my team",  # influencer
                "I'm the founder",  # decision maker
                "My manager decides"  # influencer
            ]
        },
        {
            "title": "CRM Analysis - Urgency",
            "inputs": [
                "I need this urgently",  # high urgency
                "I want to start next month",  # medium urgency
                "Just exploring options",  # low urgency
                "Need it ASAP"  # high urgency
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['title']}:")
        for input_text in scenario['inputs']:
            print(f"  Say: \"{input_text}\"")

def show_expected_outputs():
    """Show what outputs to expect"""
    print("\nExpected Outputs:")
    print("=" * 30)
    
    print("\n1. Meeting Booking:")
    print("   - Agent shows 3 available slots")
    print("   - User picks a slot")
    print("   - Agent confirms booking")
    print("   - Meeting saved to mock_calendar.json")
    
    print("\n2. CRM Analysis (at call end):")
    print("   - Lead file in leads/ directory")
    print("   - CRM analysis file in crm_notes/ directory")
    print("   - Fit score (0-100) calculated")
    print("   - Pain points extracted")
    print("   - Decision maker type identified")
    print("   - Urgency level assessed")

def main():
    print("Advanced Features Test Suite")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_directories():
        tests_passed += 1
    
    if test_calendar_data():
        tests_passed += 1
        
    if test_agent_advanced_features():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("SUCCESS: All advanced features ready!")
        show_advanced_test_scenarios()
        show_expected_outputs()
        
        print("\nTo Test Advanced Features:")
        print("1. Start the agent (same as before)")
        print("2. Try the scenarios above")
        print("3. Check generated files in leads/ and crm_notes/")
        
    else:
        print("ERROR: Some advanced features missing.")

if __name__ == "__main__":
    main()