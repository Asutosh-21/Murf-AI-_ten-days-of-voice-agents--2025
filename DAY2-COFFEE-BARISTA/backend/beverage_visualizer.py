import json
import os
from typing import Dict, List

def generate_beverage_html(order: Dict) -> str:
    """Generate HTML visualization of a coffee order."""
    
    # Cup size mapping
    cup_sizes = {
        "small": {"height": "120px", "width": "80px"},
        "medium": {"height": "150px", "width": "100px"},
        "large": {"height": "180px", "width": "120px"}
    }
    
    # Drink color mapping
    drink_colors = {
        "espresso": "#3C2415",
        "americano": "#4A2C17",
        "latte": "#D2B48C",
        "cappuccino": "#DEB887",
        "mocha": "#8B4513",
        "frappuccino": "#F5DEB3"
    }
    
    size = order.get("size", "medium").lower()
    drink_type = order.get("drinkType", "latte").lower()
    extras = order.get("extras", [])
    name = order.get("name", "Customer")
    milk = order.get("milk", "whole")
    
    cup_style = cup_sizes.get(size, cup_sizes["medium"])
    drink_color = drink_colors.get(drink_type, "#D2B48C")
    
    # Check for whipped cream
    has_whipped_cream = any("whipped" in extra.lower() for extra in extras)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Coffee Order - {name}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #8B4513, #D2691E);
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .order-container {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 400px;
            }}
            .coffee-cup {{
                position: relative;
                margin: 20px auto;
                width: {cup_style["width"]};
                height: {cup_style["height"]};
                background: linear-gradient(to bottom, {drink_color} 0%, {drink_color} 85%, #F5F5DC 85%);
                border: 3px solid #8B4513;
                border-radius: 0 0 20px 20px;
                box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
            }}
            .cup-handle {{
                position: absolute;
                right: -25px;
                top: 30%;
                width: 20px;
                height: 40px;
                border: 3px solid #8B4513;
                border-left: none;
                border-radius: 0 10px 10px 0;
            }}
            .whipped-cream {{
                position: absolute;
                top: -15px;
                left: 50%;
                transform: translateX(-50%);
                width: 80%;
                height: 30px;
                background: #FFFAF0;
                border-radius: 50%;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            .steam {{
                position: absolute;
                top: -40px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 20px;
                color: #DDD;
                animation: steam 2s infinite;
            }}
            @keyframes steam {{
                0%, 100% {{ opacity: 0.7; transform: translateX(-50%) translateY(0); }}
                50% {{ opacity: 0.3; transform: translateX(-50%) translateY(-10px); }}
            }}
            .order-details {{
                margin-top: 30px;
                text-align: left;
                background: #F8F8F8;
                padding: 20px;
                border-radius: 10px;
            }}
            .order-title {{
                font-size: 24px;
                color: #8B4513;
                margin-bottom: 20px;
                text-align: center;
            }}
            .detail-item {{
                margin: 10px 0;
                font-size: 16px;
                color: #333;
            }}
            .detail-label {{
                font-weight: bold;
                color: #8B4513;
            }}
        </style>
    </head>
    <body>
        <div class="order-container">
            <h1 class="order-title">☕ Brew & Bean Coffee</h1>
            
            <div class="coffee-cup">
                <div class="cup-handle"></div>
                {"<div class='whipped-cream'></div>" if has_whipped_cream else ""}
                <div class="steam">☁️ ☁️ ☁️</div>
            </div>
            
            <div class="order-details">
                <h2 style="text-align: center; color: #8B4513;">Order for {name}</h2>
                
                <div class="detail-item">
                    <span class="detail-label">Drink:</span> {drink_type.title()}
                </div>
                
                <div class="detail-item">
                    <span class="detail-label">Size:</span> {size.title()}
                </div>
                
                <div class="detail-item">
                    <span class="detail-label">Milk:</span> {milk.title()}
                </div>
                
                {"<div class='detail-item'><span class='detail-label'>Extras:</span> " + ", ".join(extras) + "</div>" if extras else ""}
                
                <div class="detail-item">
                    <span class="detail-label">Order ID:</span> {order.get('order_id', 'N/A')}
                </div>
                
                <div class="detail-item">
                    <span class="detail-label">Time:</span> {order.get('timestamp', 'N/A')[:19].replace('T', ' ')}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html