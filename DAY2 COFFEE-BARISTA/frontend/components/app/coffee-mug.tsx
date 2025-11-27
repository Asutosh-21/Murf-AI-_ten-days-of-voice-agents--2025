'use client';

import { motion } from 'motion/react';

interface CoffeeMugProps {
  size?: 'small' | 'medium' | 'large';
  drinkType?: string;
  hasWhippedCream?: boolean;
  animated?: boolean;
}

export function CoffeeMug({ 
  size = 'medium', 
  drinkType = 'latte', 
  hasWhippedCream = false,
  animated = true 
}: CoffeeMugProps) {
  const sizeClasses = {
    small: 'w-16 h-20',
    medium: 'w-20 h-24',
    large: 'w-24 h-28'
  };

  const drinkColors = {
    espresso: '#3C2415',
    americano: '#4A2C17',
    latte: '#D2B48C',
    cappuccino: '#DEB887',
    mocha: '#8B4513',
    frappuccino: '#F5DEB3'
  };

  const drinkColor = drinkColors[drinkType as keyof typeof drinkColors] || '#D2B48C';

  return (
    <div className="relative flex items-center justify-center">
      {/* Steam animation */}
      {animated && (
        <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 flex space-x-1">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="text-gray-400 text-sm"
              animate={{
                y: [-5, -15, -5],
                opacity: [0.7, 0.3, 0.7]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.3
              }}
            >
              ☁️
            </motion.div>
          ))}
        </div>
      )}

      {/* Coffee mug */}
      <div className={`relative ${sizeClasses[size]}`}>
        {/* Mug body */}
        <div 
          className="w-full h-full rounded-b-2xl border-4 border-amber-800 relative overflow-hidden"
          style={{
            background: `linear-gradient(to bottom, ${drinkColor} 0%, ${drinkColor} 85%, #F5F5DC 85%)`
          }}
        >
          {/* Whipped cream */}
          {hasWhippedCream && (
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 w-4/5 h-6 bg-white rounded-full shadow-md" />
          )}
        </div>

        {/* Mug handle */}
        <div className="absolute right-0 top-1/3 w-4 h-8 border-4 border-amber-800 border-l-0 rounded-r-lg transform translate-x-2" />
      </div>
    </div>
  );
}