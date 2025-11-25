#!/usr/bin/env python3
"""
Test script for Day 4 Teach-the-Tutor setup
"""

import json
import os

def test_content_file():
    """Test if content file exists and is valid"""
    content_path = os.path.join("backend", "shared-data", "day4_tutor_content.json")
    
    if not os.path.exists(content_path):
        print("[FAIL] Content file not found")
        return False
    
    try:
        with open(content_path, 'r') as f:
            content = json.load(f)
        
        if not isinstance(content, list):
            print("[FAIL] Content should be a list")
            return False
        
        required_fields = ['id', 'title', 'summary', 'sample_question']
        for item in content:
            for field in required_fields:
                if field not in item:
                    print(f"[FAIL] Missing field '{field}' in content item")
                    return False
        
        print(f"[OK] Content file loaded with {len(content)} concepts")
        return True
        
    except Exception as e:
        print(f"[FAIL] Error loading content: {e}")
        return False

def test_agent_file():
    """Test if agent file exists"""
    agent_path = os.path.join("backend", "src", "agent.py")
    
    if not os.path.exists(agent_path):
        print("[FAIL] Agent file not found")
        return False
    
    try:
        with open(agent_path, 'r') as f:
            content = f.read()
        
        required_elements = [
            'TeachTheTutorAssistant',
            'switch_to_learn_mode',
            'switch_to_quiz_mode', 
            'switch_to_teach_back_mode',
            'function_tool'
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"[FAIL] Missing element '{element}' in agent")
                return False
        
        print("[OK] Agent file contains required elements")
        return True
        
    except Exception as e:
        print(f"[FAIL] Error reading agent file: {e}")
        return False

def test_voice_manager():
    """Test if voice manager exists"""
    voice_path = os.path.join("backend", "src", "voice_manager.py")
    
    if not os.path.exists(voice_path):
        print("[FAIL] Voice manager not found")
        return False
    
    print("[OK] Voice manager file exists")
    return True

def main():
    print("Testing Day 4 Teach-the-Tutor Setup...\n")
    
    tests = [
        test_content_file(),
        test_agent_file(),
        test_voice_manager()
    ]
    
    passed = sum(tests)
    total = len(tests)
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if all(tests):
        print("\nDay 4 setup is ready!")
        print("\nTo start the agent:")
        print("1. cd backend")
        print("2. uv run python src/agent.py")
        print("\nTo start the frontend:")
        print("1. cd frontend") 
        print("2. pnpm dev")
    else:
        print("\nSome components are missing. Please check the setup.")

if __name__ == "__main__":
    main()