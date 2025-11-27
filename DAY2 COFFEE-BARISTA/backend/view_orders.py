#!/usr/bin/env python3
"""
Coffee Shop Order Viewer
View and manage saved coffee orders
"""

import json
import os
import webbrowser
from datetime import datetime

def list_orders():
    """List all saved orders."""
    orders_dir = "orders"
    if not os.path.exists(orders_dir):
        print("No orders directory found!")
        return []
    
    json_files = [f for f in os.listdir(orders_dir) if f.endswith('.json')]
    
    if not json_files:
        print("No orders found!")
        return []
    
    orders = []
    print("\n📋 Coffee Orders:")
    print("-" * 50)
    
    for i, filename in enumerate(sorted(json_files), 1):
        filepath = os.path.join(orders_dir, filename)
        with open(filepath, 'r') as f:
            order = json.load(f)
        
        orders.append((filepath, order))
        
        timestamp = order.get('timestamp', 'Unknown')
        if 'T' in timestamp:
            timestamp = timestamp[:19].replace('T', ' ')
        
        print(f"{i}. {order['name']} - {order['drinkType'].title()} ({order['size']})")
        print(f"   Order ID: {order['order_id']}")
        print(f"   Time: {timestamp}")
        print()
    
    return orders

def view_order_details(order_data):
    """Display detailed order information."""
    filepath, order = order_data
    
    print(f"\n☕ Order Details:")
    print("=" * 40)
    print(f"Customer: {order['name']}")
    print(f"Drink: {order['drinkType'].title()}")
    print(f"Size: {order['size'].title()}")
    print(f"Milk: {order['milk'].title()}")
    
    if order['extras']:
        print(f"Extras: {', '.join(order['extras'])}")
    
    print(f"Order ID: {order['order_id']}")
    print(f"Timestamp: {order.get('timestamp', 'Unknown')}")
    
    # Check if HTML visualization exists
    html_file = filepath.replace('.json', '.html')
    if os.path.exists(html_file):
        print(f"\n🎨 Visual receipt available: {html_file}")
        choice = input("Open visual receipt in browser? (y/n): ").lower()
        if choice == 'y':
            webbrowser.open(f"file://{os.path.abspath(html_file)}")

def main():
    """Main menu for order management."""
    while True:
        print("\n☕ Brew & Bean Coffee - Order Management")
        print("1. List all orders")
        print("2. View order details")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            orders = list_orders()
        
        elif choice == '2':
            orders = list_orders()
            if orders:
                try:
                    order_num = int(input(f"\nSelect order (1-{len(orders)}): ")) - 1
                    if 0 <= order_num < len(orders):
                        view_order_details(orders[order_num])
                    else:
                        print("Invalid order number!")
                except ValueError:
                    print("Please enter a valid number!")
        
        elif choice == '3':
            print("Thanks for using Brew & Bean Coffee! ☕")
            break
        
        else:
            print("Invalid choice! Please select 1-3.")

if __name__ == "__main__":
    main()