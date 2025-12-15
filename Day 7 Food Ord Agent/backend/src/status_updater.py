#!/usr/bin/env python3
"""
Manual status updater for testing order progression
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from order_manager import OrderManager

def main():
    om = OrderManager()
    
    if not om.orders:
        print("No orders found.")
        return
    
    print("Recent orders:")
    for i, order in enumerate(om.get_recent_orders(5)):
        print(f"{i+1}. Order {order['order_id']} - Status: {order['status']}")
    
    print("\nOptions:")
    print("1. Auto-advance all order statuses")
    print("2. Manually update specific order")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        om.advance_order_statuses()
        print("All order statuses updated!")
    elif choice == "2":
        order_id = input("Enter order ID: ").strip()
        statuses = ["received", "confirmed", "being_prepared", "out_for_delivery", "delivered"]
        print("Available statuses:", ", ".join(statuses))
        new_status = input("Enter new status: ").strip()
        
        if new_status in statuses:
            if om.update_order_status(order_id, new_status):
                print(f"Order {order_id} updated to {new_status}")
            else:
                print("Order not found")
        else:
            print("Invalid status")

if __name__ == "__main__":
    main()