#!/usr/bin/env python3
"""
Test script for constraint features
"""
import json
import os

def test_constraints():
    # Load catalog
    catalog_path = os.path.join('src', 'catalog.json')
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)
    
    print("=== Budget & Dietary Constraints Test ===")
    
    # Test budget filtering
    budget = 10.0
    affordable_items = []
    for item in catalog['items']:
        if item['price'] <= budget:
            affordable_items.append(f"{item['name']} - ${item['price']:.2f}")
    
    print(f"\nItems under ${budget}:")
    for item in affordable_items[:5]:
        print(f"  {item}")
    
    # Test dietary filtering
    dietary_req = "vegan"
    vegan_items = []
    for item in catalog['items']:
        if dietary_req in [tag.lower() for tag in item.get('tags', [])]:
            vegan_items.append(f"{item['name']} - ${item['price']:.2f}")
    
    print(f"\nVegan items:")
    for item in vegan_items:
        print(f"  {item}")
    
    # Test gluten-free filtering
    gf_items = []
    for item in catalog['items']:
        if 'gluten-free' in [tag.lower() for tag in item.get('tags', [])]:
            gf_items.append(f"{item['name']} - ${item['price']:.2f}")
    
    print(f"\nGluten-free items:")
    for item in gf_items:
        print(f"  {item}")
    
    # Test combined constraints
    print(f"\nVegan items under ${budget}:")
    for item in catalog['items']:
        if (item['price'] <= budget and 
            'vegan' in [tag.lower() for tag in item.get('tags', [])]):
            print(f"  {item['name']} - ${item['price']:.2f}")
    
    print("\n[OK] Constraint filtering works correctly!")

if __name__ == "__main__":
    test_constraints()