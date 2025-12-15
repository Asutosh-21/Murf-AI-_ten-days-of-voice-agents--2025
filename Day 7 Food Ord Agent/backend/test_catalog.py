#!/usr/bin/env python3
"""
Simple test script to verify the catalog loading and basic functionality
"""
import json
import os

def test_catalog():
    catalog_path = os.path.join('src', 'catalog.json')
    
    try:
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        print("[OK] Catalog loaded successfully!")
        print(f"Total items: {len(catalog['items'])}")
        categories = set(item['category'] for item in catalog['items'])
        print(f"Categories: {len(categories)} ({', '.join(sorted(categories))})")
        print(f"Recipes: {len(catalog.get('recipes', {}))}")
        
        # Show some sample items
        print("\nSample items:")
        for i, item in enumerate(catalog['items'][:5]):
            print(f"  {i+1}. {item['name']} - ${item['price']:.2f} ({item['brand']})")
        
        # Show recipes
        print("\nAvailable recipes:")
        recipes = catalog.get('recipes', {})
        if recipes:
            for recipe in list(recipes.keys())[:5]:
                print(f"  - {recipe}")
        else:
            print("  No recipes found")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] Error loading catalog: {e}")
        return False

if __name__ == "__main__":
    test_catalog()