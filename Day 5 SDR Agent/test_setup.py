#!/usr/bin/env python3
"""Test script to verify Day 5 SDR Agent setup"""

import os
import json
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[ERROR] {description}: {filepath} - NOT FOUND")
        return False

def check_env_vars(filepath):
    """Check if required environment variables are set in .env.local"""
    if not os.path.exists(filepath):
        print(f"[ERROR] Environment file not found: {filepath}")
        return False
    
    required_vars = [
        'LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET',
        'GOOGLE_API_KEY', 'MURF_API_KEY', 'DEEPGRAM_API_KEY'
    ]
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if f"{var}=" not in content or f"{var}=\n" in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"[ERROR] Missing environment variables in {filepath}: {', '.join(missing_vars)}")
        return False
    else:
        print(f"[OK] All required environment variables set in {filepath}")
        return True

def main():
    print("Checking Day 5 SDR Agent Setup...")
    print("=" * 50)
    
    all_good = True
    
    # Check backend files
    print("\nBackend Files:")
    all_good &= check_file_exists("backend/pyproject.toml", "Backend project file")
    all_good &= check_file_exists("backend/uv.lock", "Backend dependencies")
    all_good &= check_file_exists("backend/.env.local", "Backend environment")
    all_good &= check_file_exists("backend/src/agent.py", "Main agent file")
    all_good &= check_file_exists("backend/company_data.json", "Company data")
    
    # Check frontend files
    print("\nFrontend Files:")
    all_good &= check_file_exists("frontend/package.json", "Frontend project file")
    all_good &= check_file_exists("frontend/pnpm-lock.yaml", "Frontend dependencies")
    all_good &= check_file_exists("frontend/.env.local", "Frontend environment")
    
    # Check LiveKit server
    print("\nLiveKit Server:")
    all_good &= check_file_exists("livekit-server.exe", "LiveKit server executable")
    
    # Check environment variables
    print("\nEnvironment Variables:")
    all_good &= check_env_vars("backend/.env.local")
    all_good &= check_env_vars("frontend/.env.local")
    
    # Check company data
    print("\nCompany Data:")
    try:
        with open("backend/company_data.json", 'r') as f:
            company_data = json.load(f)
        print(f"[OK] Company: {company_data['company']}")
        print(f"[OK] FAQ entries: {len(company_data['faq'])}")
    except Exception as e:
        print(f"[ERROR] Error reading company data: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("SUCCESS: Setup Complete! Ready to run Day 5 SDR Agent")
        print("\nNext steps:")
        print("1. Start LiveKit server: .\\livekit-server.exe --dev")
        print("2. Start backend: cd backend && uv run python src/agent.py dev")
        print("3. Start frontend: cd frontend && pnpm dev")
        print("4. Open http://localhost:3000")
    else:
        print("ERROR: Setup incomplete. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()