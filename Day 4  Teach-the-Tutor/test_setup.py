#!/usr/bin/env python3
"""
Quick setup verification script for Day 4/5 Voice Agent project
"""

import sys
import subprocess
import os

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"[FAIL] Python {version.major}.{version.minor}.{version.micro} - Need 3.9+")
        return False

def check_command(cmd, name):
    """Check if a command exists"""
    try:
        result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] {name} - OK")
            return True
    except FileNotFoundError:
        pass
    print(f"[FAIL] {name} - Not found")
    return False

def check_file(filepath, name):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {name} - OK")
        return True
    else:
        print(f"[FAIL] {name} - Not found")
        return False

def main():
    print("Checking Day 4/5 Voice Agent Prerequisites...\n")
    
    checks = []
    
    # Check Python
    checks.append(check_python())
    
    # Check package managers
    checks.append(check_command("uv", "UV Package Manager"))
    checks.append(check_command("node", "Node.js"))
    checks.append(check_command("pnpm", "PNPM"))
    
    # Check LiveKit server
    checks.append(check_file("livekit-server.exe", "LiveKit Server"))
    
    # Check project structure
    checks.append(check_file("backend/pyproject.toml", "Backend Config"))
    checks.append(check_file("frontend/package.json", "Frontend Config"))
    
    print(f"\nResults: {sum(checks)}/{len(checks)} checks passed")
    
    if all(checks):
        print("All prerequisites are ready! You can start Day 5 development.")
    else:
        print("Some prerequisites are missing. Please install them before proceeding.")

if __name__ == "__main__":
    main()