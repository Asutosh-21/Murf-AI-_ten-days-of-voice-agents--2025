'use client';

import { motion } from 'motion/react';
import { CoffeeMug } from './coffee-mug';

interface MenuItem {
  name: string;
  description: string;
  price: string;
  drinkType: string;
}

const menuItems: MenuItem[] = [
  {
    name: 'Espresso',
    description: 'Rich and bold coffee shot',
    price: '$2.50',
    drinkType: 'espresso'
  },
  {
    name: 'Latte',
    description: 'Smooth espresso with steamed milk',
    price: '$4.50',
    drinkType: 'latte'
  },
  {
    name: 'Cappuccino',
    description: 'Espresso with foamed milk',
    price: '$4.00',
    drinkType: 'cappuccino'
  },
  {
    name: 'Americano',
    description: 'Espresso with hot water',
    price: '$3.50',
    drinkType: 'americano'
  },
  {
    name: 'Mocha',
    description: 'Chocolate and espresso blend',
    price: '$5.00',
    drinkType: 'mocha'
  }
];

interface CoffeeMenuProps {
  isVisible: boolean;
}

export function CoffeeMenu({ isVisible }: CoffeeMenuProps) {
  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, x: -100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="fixed top-4 left-4 bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-2xl border border-amber-200 max-w-xs"
    >
      <h3 className="text-xl font-bold text-amber-800 mb-4 text-center">☕ Menu</h3>
      
      <div className="space-y-4">
        {menuItems.map((item, index) => (
          <motion.div
            key={item.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center space-x-3 p-3 rounded-lg hover:bg-amber-50 transition-colors"
          >
            <div className="flex-shrink-0">
              <CoffeeMug size="small" drinkType={item.drinkType} animated={false} />
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex justify-between items-start">
                <h4 className="font-semibold text-gray-800 text-sm">{item.name}</h4>
                <span className="text-amber-600 font-bold text-sm">{item.price}</span>
              </div>
              <p className="text-xs text-gray-600 mt-1">{item.description}</p>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-amber-200">
        <p className="text-xs text-gray-500 text-center">
          🗣️ Just tell Maya what you'd like!
        </p>
      </div>
    </motion.div>
  );
}