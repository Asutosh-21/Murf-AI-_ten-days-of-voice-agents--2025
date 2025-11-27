#!/usr/bin/env python3

import os
import json
from datetime import datetime
from beverage_visualizer import generate_beverage_html

def test_order_creation():
    """Test creating an order to verify the system works"""
    
    # Test order data
    order = {
        "drinkType": "latte",
        "size": "medium", 
        "milk": "oat",
        "extras": ["whipped cream", "vanilla syrup"],
        "name": "Test Customer",
        "timestamp": datetime.now().isoformat(),
        "order_id": f"test_order_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }
    
    # Get current working directory and create absolute path
    current_dir = os.getcwd()
    orders_dir = os.path.join(current_dir, "orders")
    
    print(f"Current directory: {current_dir}")
    print(f"Orders directory: {orders_dir}")
    
    # Create orders directory if it doesn't exist
    if not os.path.exists(orders_dir):
        os.makedirs(orders_dir)
        print(f"Created orders directory: {orders_dir}")
    else:
        print(f"Orders directory already exists: {orders_dir}")
    
    # Save order to JSON file
    filename = os.path.join(orders_dir, f"{order['order_id']}.json")
    with open(filename, 'w') as f:
        json.dump(order, f, indent=2)
    print(f"Order saved: {filename}")
    
    # Generate HTML visualization
    try:
        html_content = generate_beverage_html(order)
        html_filename = os.path.join(orders_dir, f"{order['order_id']}.html")
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Visualization created: {html_filename}")
        print("Test order creation successful!")
        return True
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return False

if __name__ == "__main__":
    test_order_creation()