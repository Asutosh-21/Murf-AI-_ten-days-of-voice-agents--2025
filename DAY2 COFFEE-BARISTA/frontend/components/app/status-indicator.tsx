'use client';

import { motion } from 'motion/react';

interface StatusIndicatorProps {
  isVisible: boolean;
}

export function StatusIndicator({ isVisible }: StatusIndicatorProps) {
  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50"
    >
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-amber-200 text-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="text-4xl mb-4"
        >
          ☕
        </motion.div>
        
        <h3 className="text-lg font-bold text-amber-800 mb-2">Brewing Your Order</h3>
        <p className="text-gray-600">Maya is preparing your perfect coffee...</p>
        
        <div className="flex justify-center mt-4 space-x-1">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-2 h-2 bg-amber-600 rounded-full"
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.2
              }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}