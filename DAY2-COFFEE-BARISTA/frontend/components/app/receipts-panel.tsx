'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { CoffeeMug } from './coffee-mug';

interface Receipt {
  order_id: string;
  drinkType: string;
  size: string;
  milk: string;
  extras: string[];
  name: string;
  timestamp: string;
  total?: string;
}

interface ReceiptsPanelProps {
  isVisible: boolean;
  onClose: () => void;
}

export function ReceiptsPanel({ isVisible, onClose }: ReceiptsPanelProps) {
  const [receipts, setReceipts] = useState<Receipt[]>([]);

  useEffect(() => {
    if (isVisible) {
      // Fetch real orders from API
      fetch('/api/orders')
        .then(res => res.json())
        .then(data => {
          if (data.orders) {
            const receiptsWithPrices = data.orders.map((order: any) => ({
              ...order,
              total: calculatePrice(order)
            }));
            setReceipts(receiptsWithPrices);
          }
        })
        .catch(error => {
          console.error('Error fetching orders:', error);
          // Fallback to empty array
          setReceipts([]);
        });
    }
  }, [isVisible]);

  const calculatePrice = (order: any) => {
    const basePrices = {
      espresso: 2.50,
      americano: 3.50,
      latte: 4.50,
      cappuccino: 4.00,
      mocha: 5.00,
      frappuccino: 5.50
    };
    
    const sizeMultipliers = {
      small: 0.8,
      medium: 1.0,
      large: 1.3
    };
    
    const basePrice = basePrices[order.drinkType as keyof typeof basePrices] || 4.00;
    const sizeMultiplier = sizeMultipliers[order.size as keyof typeof sizeMultipliers] || 1.0;
    const extrasPrice = (order.extras?.length || 0) * 0.75;
    
    const total = (basePrice * sizeMultiplier) + extrasPrice;
    return `$${total.toFixed(2)}`;
  };

  if (!isVisible) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.8, opacity: 0 }}
          className="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-amber-800">📄 Recent Orders</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ×
            </button>
          </div>

          <div className="space-y-4">
            {receipts.map((receipt, index) => (
              <motion.div
                key={receipt.order_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="border border-amber-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <CoffeeMug 
                      size={receipt.size as 'small' | 'medium' | 'large'}
                      drinkType={receipt.drinkType}
                      hasWhippedCream={receipt.extras.some(extra => extra.toLowerCase().includes('whipped'))}
                      animated={false}
                    />
                  </div>

                  <div className="flex-1">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-800">{receipt.name}'s Order</h3>
                      <span className="text-amber-600 font-bold">{receipt.total}</span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-sm text-gray-600 mb-2">
                      <div><span className="font-medium">Drink:</span> {receipt.drinkType}</div>
                      <div><span className="font-medium">Size:</span> {receipt.size}</div>
                      <div><span className="font-medium">Milk:</span> {receipt.milk}</div>
                      {receipt.extras.length > 0 && (
                        <div className="col-span-2">
                          <span className="font-medium">Extras:</span> {receipt.extras.join(', ')}
                        </div>
                      )}
                    </div>

                    <div className="flex justify-between items-center text-xs text-gray-500">
                      <span>Order ID: {receipt.order_id}</span>
                      <span>{new Date(receipt.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {receipts.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-2">☕</div>
              <p>No orders yet. Start by talking to Maya!</p>
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}