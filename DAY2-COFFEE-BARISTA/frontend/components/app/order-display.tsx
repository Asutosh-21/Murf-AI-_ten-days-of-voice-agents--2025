'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { CoffeeMug } from './coffee-mug';

interface Order {
  drinkType: string;
  size: string;
  milk: string;
  extras: string[];
  name: string;
  timestamp: string;
  order_id: string;
}

interface OrderDisplayProps {
  isVisible: boolean;
}

export function OrderDisplay({ isVisible }: OrderDisplayProps) {
  const [orders, setOrders] = useState<Order[]>([]);
  const [currentOrderIndex, setCurrentOrderIndex] = useState(0);

  useEffect(() => {
    if (isVisible) {
      // Fetch latest orders from API
      fetch('/api/orders')
        .then(res => res.json())
        .then(data => {
          if (data.orders && data.orders.length > 0) {
            setOrders(data.orders.slice(0, 3)); // Show only latest 3 orders
          }
        })
        .catch(error => {
          console.error('Error fetching orders:', error);
        });
    }
  }, [isVisible]);

  // Auto-refresh orders every 5 seconds when visible
  useEffect(() => {
    if (!isVisible) return;
    
    const interval = setInterval(() => {
      fetch('/api/orders')
        .then(res => res.json())
        .then(data => {
          if (data.orders && data.orders.length > 0) {
            setOrders(data.orders.slice(0, 3));
          }
        })
        .catch(error => console.error('Error refreshing orders:', error));
    }, 5000);

    return () => clearInterval(interval);
  }, [isVisible]);

  const currentOrder = orders[currentOrderIndex];

  if (!isVisible || !currentOrder) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.8 }}
        className="fixed top-4 right-4 bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-2xl border border-amber-200 max-w-sm"
      >
        <div className="text-center">
          <h3 className="text-lg font-bold text-amber-800 mb-4">Current Order</h3>
          
          <div className="mb-4">
            <CoffeeMug 
              size={currentOrder.size as 'small' | 'medium' | 'large'}
              drinkType={currentOrder.drinkType}
              hasWhippedCream={currentOrder.extras.some(extra => extra.toLowerCase().includes('whipped'))}
            />
          </div>

          <div className="space-y-2 text-sm text-gray-700">
            <div><span className="font-semibold">Name:</span> {currentOrder.name}</div>
            <div><span className="font-semibold">Drink:</span> {currentOrder.drinkType}</div>
            <div><span className="font-semibold">Size:</span> {currentOrder.size}</div>
            <div><span className="font-semibold">Milk:</span> {currentOrder.milk}</div>
            {currentOrder.extras.length > 0 && (
              <div><span className="font-semibold">Extras:</span> {currentOrder.extras.join(', ')}</div>
            )}
          </div>

          <div className="mt-4 text-xs text-gray-500">
            Order ID: {currentOrder.order_id}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}