'use client';

import { useState, useEffect } from 'react';
import { motion } from 'motion/react';

interface ProcessingIndicatorProps {
  isVisible: boolean;
}

export function ProcessingIndicator({ isVisible }: ProcessingIndicatorProps) {
  const [stage, setStage] = useState(0);
  
  const stages = [
    { icon: '🎤', text: 'Listening to your voice...', color: 'text-blue-600' },
    { icon: '📝', text: 'Converting speech to text...', color: 'text-green-600' },
    { icon: '🧠', text: 'Maya is thinking...', color: 'text-purple-600' },
    { icon: '🗣️', text: 'Generating response...', color: 'text-orange-600' },
    { icon: '💬', text: 'Adding to chat...', color: 'text-amber-600' }
  ];

  useEffect(() => {
    if (!isVisible) {
      setStage(0);
      return;
    }

    const interval = setInterval(() => {
      setStage(prev => (prev + 1) % stages.length);
    }, 1500);

    return () => clearInterval(interval);
  }, [isVisible, stages.length]);

  if (!isVisible) return null;

  const currentStage = stages[stage];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="fixed bottom-32 left-1/2 transform -translate-x-1/2 z-40"
    >
      <div className="bg-white/95 backdrop-blur-sm rounded-full px-6 py-3 shadow-lg border border-amber-200 flex items-center space-x-3">
        <motion.div
          key={stage}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="text-2xl"
        >
          {currentStage.icon}
        </motion.div>
        
        <motion.span
          key={stage}
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          className={`text-sm font-medium ${currentStage.color}`}
        >
          {currentStage.text}
        </motion.span>
        
        <div className="flex space-x-1">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-1.5 h-1.5 bg-amber-400 rounded-full"
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 0.8,
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