#!/usr/bin/env python3
"""Simple test for fraud agent"""

import os
import json

def test_basic():
    print("Testing basic setup...")
    
    # Check database
    db_path = "fraud_database.json"
    if os.path.exists(db_path):
        with open(db_path, 'r') as f:
            cases = json.load(f)
        print(f"Database: {len(cases)} cases loaded")
    else:
        print("ERROR: Database not found")
        return False
    
    # Check env file
    env_path = ".env.local"
    if os.path.exists(env_path):
        print("Environment file: Found")
    else:
        print("ERROR: .env.local not found")
        return False
    
    # Test case lookup
    test_name = "John Smith"
    found = any(case['userName'].lower() == test_name.lower() for case in cases)
    print(f"Test case '{test_name}': {'Found' if found else 'Not found'}")
    
    return True

if __name__ == "__main__":
    if test_basic():
        print("Basic test passed!")
    else:
        print("Basic test failed!")