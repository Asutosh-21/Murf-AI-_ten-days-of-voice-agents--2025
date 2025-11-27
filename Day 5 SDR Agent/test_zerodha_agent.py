#!/usr/bin/env python3
"""
Test script for Zerodha SDR Agent
This script helps verify that all components are working correctly.
"""

import json
import os

def test_faq_data():
    """Test if FAQ data is properly loaded"""
    print("Testing FAQ Data...")
    
    try:
        with open("backend/data/company_faq.json", "r") as f:
            faq_data = json.load(f)
        
        print(f"[OK] Company: {faq_data['company']}")
        print(f"[OK] Product: {faq_data['product']}")
        print(f"[OK] FAQ Entries: {len(faq_data['faqs'])}")
        
        # Test specific FAQ entries
        expected_questions = [
            "What does Zerodha do?",
            "Do you have a free plan?",
            "Who is this for?",
            "What are your brokerage fees?"
        ]
        
        actual_questions = [faq['question'] for faq in faq_data['faqs']]
        
        for question in expected_questions:
            if question in actual_questions:
                print(f"[OK] FAQ Question: {question}")
            else:
                print(f"[ERROR] Missing FAQ: {question}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error loading FAQ data: {e}")
        return False

def test_directory_structure():
    """Test if all required directories exist"""
    print("\nTesting Directory Structure...")
    
    required_dirs = [
        "backend/data",
        "backend/leads",
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

def test_agent_file():
    """Test if agent.py has the required components"""
    print("\nTesting Agent File...")
    
    try:
        with open("backend/src/agent.py", "r") as f:
            agent_content = f.read()
        
        required_components = [
            "ZerodhaSDRAssistant",
            "search_zerodha_faq",
            "capture_lead_field",
            "detect_end_call_intent",
            "generate_final_summary",
            "company_faq.json"
        ]
        
        all_good = True
        for component in required_components:
            if component in agent_content:
                print(f"[OK] Component found: {component}")
            else:
                print(f"[ERROR] Missing component: {component}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"[ERROR] Error reading agent.py: {e}")
        return False

def show_test_scenarios():
    """Show the test scenarios for manual testing"""
    print("\nManual Testing Scenarios:")
    print("=" * 50)
    
    scenarios = [
        {
            "title": "1. Greeting & Product Test",
            "inputs": [
                "Hi, what does Zerodha do?",
                "Can you explain Zerodha in simple words?",
                "Who is Zerodha for?"
            ]
        },
        {
            "title": "2. Pricing Test", 
            "inputs": [
                "Do you have a free plan?",
                "What are your brokerage charges?",
                "How much do I pay per order?"
            ]
        },
        {
            "title": "3. Use Case Discovery",
            "inputs": [
                "I want to invest in mutual funds",
                "I trade intraday",
                "I am a beginner and want to start investing"
            ]
        },
        {
            "title": "4. Lead Capture",
            "inputs": [
                "My name is Aditya",
                "My email is aditya.sharma@example.com",
                "I am a beginner in trading",
                "I want to start investing next month"
            ]
        },
        {
            "title": "5. Off-FAQ Testing (Should say 'not in FAQ')",
            "inputs": [
                "Does Zerodha offer cryptocurrency trading?",
                "Do you provide stock tips?",
                "Does Zerodha guarantee returns?"
            ]
        },
        {
            "title": "6. End Call Triggers",
            "inputs": [
                "That's all",
                "Okay, you can wrap up",
                "Thanks, I'm done",
                "That's it for now"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['title']}:")
        for input_text in scenario['inputs']:
            print(f"  Say: \"{input_text}\"")

def main():
    print("Zerodha SDR Agent Test Suite")
    print("=" * 50)
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    if test_directory_structure():
        tests_passed += 1
    
    if test_faq_data():
        tests_passed += 1
        
    if test_agent_file():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("SUCCESS: All tests passed! Agent is ready for testing.")
        show_test_scenarios()
        
        print("\nNext Steps:")
        print("1. Start LiveKit server: .\\livekit-server.exe --dev")
        print("2. Start backend: cd backend && uv run python src/agent.py dev")
        print("3. Start frontend: cd frontend && pnpm dev")
        print("4. Open http://localhost:3000 and test with the scenarios above")
        
    else:
        print("ERROR: Some tests failed. Please fix the issues before proceeding.")

if __name__ == "__main__":
    main()