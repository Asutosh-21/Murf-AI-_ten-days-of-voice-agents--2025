#!/usr/bin/env python3
"""
Enhanced fraud database viewer and manager
"""

import json
import sys
from datetime import datetime

def show_database():
    """Display the fraud database contents"""
    try:
        with open("fraud_database.json", 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        print("[NOVATRUST BANK] Fraud Database Contents")
        print("=" * 60)
        print(f"Total cases: {len(cases)}")
        
        # Summary by status
        status_counts = {}
        for case in cases:
            status = case['case']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\nStatus Summary:")
        for status, count in status_counts.items():
            icon = {
                'pending_review': '[PENDING]',
                'confirmed_safe': '[SAFE]',
                'confirmed_fraud': '[FRAUD]',
                'verification_failed': '[FAILED]'
            }.get(status, '[UNKNOWN]')
            print(f"  {icon} {status}: {count} cases")
        
        print("\nDetailed Cases:")
        print("-" * 60)
        
        for i, case in enumerate(cases, 1):
            status_icon = {
                'pending_review': '[PENDING]',
                'confirmed_safe': '[SAFE]',
                'confirmed_fraud': '[FRAUD]',
                'verification_failed': '[FAILED]'
            }.get(case['case'], '[UNKNOWN]')
            
            print(f"\n{status_icon} Case {i}: {case['userName']}")
            print(f"   Security ID: {case['securityIdentifier']}")
            print(f"   Card: ****{case['cardEnding']}")
            # Handle currency display safely
            amount = case['transactionAmount']
            if '₹' in amount:
                amount = amount.replace('₹', 'INR ')
            elif '€' in amount:
                amount = amount.replace('€', 'EUR ')
            print(f"   Transaction: {case['transactionName']} - {amount}")
            print(f"   Location: {case['location']}")
            print(f"   Time: {case['transactionTime']}")
            print(f"   Category: {case['transactionCategory']}")
            print(f"   Source: {case['transactionSource']}")
            print(f"   Status: {case['case']}")
            print(f"   Security Question: {case['securityQuestion']}")
            print(f"   Expected Answer: {case['securityAnswer']}")
            
            if case['outcome']:
                print(f"   Outcome: {case['outcome']}")
        
        return cases
        
    except FileNotFoundError:
        print("[ERROR] fraud_database.json not found!")
        return []
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON in fraud_database.json!")
        return []
    except UnicodeDecodeError:
        print("[ERROR] Unicode encoding issue in database!")
        return []
    except UnicodeEncodeError:
        print("[ERROR] Unicode display issue - check terminal encoding!")
        return []

def reset_database():
    """Reset all cases to pending_review status"""
    try:
        with open("fraud_database.json", 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Reset all cases
        for case in cases:
            case['case'] = 'pending_review'
            case['outcome'] = ''
        
        with open("fraud_database.json", 'w', encoding='utf-8') as f:
            json.dump(cases, f, indent=2, ensure_ascii=False)
        
        print("[SUCCESS] All cases reset to pending_review status!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to reset database: {e}")
        return False

def show_test_customers():
    """Show quick reference for test customers"""
    print("\n[QUICK REFERENCE] Test Customers")
    print("=" * 50)
    
    test_cases = [
        ("John Smith", "Johnson", "Mother's maiden name"),
        ("Sarah Wilson", "Buddy", "First pet's name"),
        ("Michael Brown", "Chicago", "Birth city"),
        ("Emily Davis", "Blue", "Favorite color"),
        ("David Martinez", "Honda", "First car model"),
        ("Amit Verma", "blue", "Favorite color"),
        ("David Chen", "liu", "Mother's maiden name"),
        ("Priya Nair", "dangal", "Favorite movie"),
        ("John Carter", "football", "Favorite sport"),
        ("Emma Williams", "madrid", "Current city")
    ]
    
    for name, answer, question in test_cases:
        print(f"  {name:<15} -> {answer:<10} ({question})")

def main():
    """Main menu"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            reset_database()
            return
        elif sys.argv[1] == "test":
            show_test_customers()
            return
    
    print("\n[NOVATRUST BANK] Database Manager")
    print("=" * 40)
    print("1. View database")
    print("2. Reset all cases")
    print("3. Show test customers")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                show_database()
            elif choice == '2':
                confirm = input("Reset all cases to pending? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    reset_database()
            elif choice == '3':
                show_test_customers()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Try again.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - just show database
        show_database()
    else:
        # With arguments - run main menu
        main()