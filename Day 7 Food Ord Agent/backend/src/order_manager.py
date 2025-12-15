import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class OrderManager:
    def __init__(self):
        self.orders_file = os.path.join(os.path.dirname(__file__), 'orders', 'order_history.json')
        self.orders = self._load_orders()
        
    def _load_orders(self) -> List[Dict]:
        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_orders(self):
        os.makedirs(os.path.dirname(self.orders_file), exist_ok=True)
        with open(self.orders_file, 'w') as f:
            json.dump(self.orders, f, indent=2)
    
    def create_order(self, cart_items: Dict, customer_name: str = "Customer", order_type: str = "grocery") -> str:
        order_id = f"QB{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        items = []
        total = 0
        for cart_item in cart_items.values():
            item = cart_item["item"]
            qty = cart_item["quantity"]
            subtotal = item["price"] * qty
            total += subtotal
            
            items.append({
                "name": item["name"],
                "brand": item["brand"],
                "price": item["price"],
                "quantity": qty,
                "notes": cart_item.get("notes", ""),
                "subtotal": subtotal
            })
        
        order = {
            "order_id": order_id,
            "customer_name": customer_name,
            "order_type": order_type,
            "timestamp": datetime.now().isoformat(),
            "status": "received",
            "status_updated": datetime.now().isoformat(),
            "items": items,
            "total": total
        }
        
        self.orders.append(order)
        self._save_orders()
        return order_id
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        for order in self.orders:
            if order["order_id"] == order_id:
                order["status"] = new_status
                order["status_updated"] = datetime.now().isoformat()
                self._save_orders()
                return True
        return False
    
    def get_order_status(self, order_id: str = None) -> Optional[Dict]:
        if order_id:
            for order in reversed(self.orders):
                if order["order_id"] == order_id:
                    return order
        else:
            # Return latest order
            return self.orders[-1] if self.orders else None
        return None
    
    def get_recent_orders(self, limit: int = 5) -> List[Dict]:
        return list(reversed(self.orders[-limit:]))
    
    def get_orders_by_type(self, order_type: str) -> List[Dict]:
        return [order for order in self.orders if order.get("order_type") == order_type]
    
    def get_frequent_items(self, limit: int = 5) -> List[Dict]:
        item_counts = {}
        for order in self.orders:
            for item in order["items"]:
                name = item["name"]
                if name in item_counts:
                    item_counts[name]["count"] += item["quantity"]
                else:
                    item_counts[name] = {"name": name, "count": item["quantity"], "last_price": item["price"]}
        
        return sorted(item_counts.values(), key=lambda x: x["count"], reverse=True)[:limit]
    
    def advance_order_statuses(self):
        """Mock status progression based on time"""
        status_flow = ["received", "confirmed", "being_prepared", "out_for_delivery", "delivered"]
        
        for order in self.orders:
            if order["status"] == "delivered":
                continue
                
            status_time = datetime.fromisoformat(order["status_updated"])
            minutes_passed = (datetime.now() - status_time).total_seconds() / 60
            
            current_idx = status_flow.index(order["status"])
            # Advance every 2 minutes for demo
            if minutes_passed >= 2 and current_idx < len(status_flow) - 1:
                order["status"] = status_flow[current_idx + 1]
                order["status_updated"] = datetime.now().isoformat()
        
        self._save_orders()