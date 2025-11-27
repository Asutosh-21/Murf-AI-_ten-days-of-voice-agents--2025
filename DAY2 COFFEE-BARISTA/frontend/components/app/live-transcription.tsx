'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { useChatMessages } from '@/hooks/useChatMessages';

interface LiveTranscriptionProps {
  isVisible: boolean;
}

export function LiveTranscription({ isVisible }: LiveTranscriptionProps) {
  const [currentTranscript, setCurrentTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const messages = useChatMessages();

  useEffect(() => {
    // Simulate live transcription (in real implementation, this would connect to STT stream)
    let timeout: NodeJS.Timeout;
    
    if (isListening && currentTranscript) {
      timeout = setTimeout(() => {
        setCurrentTranscript('');
        setIsListening(false);
      }, 3000);
    }

    return () => clearTimeout(timeout);
  }, [currentTranscript, isListening]);

  // Monitor for new messages to show processing states
  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.from?.isLocal) {
      setCurrentTranscript(lastMessage.message);
      setIsListening(true);
    }
  }, [messages]);

  if (!isVisible) return null;

  return (
    <AnimatePresence>
      {(isListening || currentTranscript) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="fixed top-20 left-1/2 transform -translate-x-1/2 z-40 max-w-md"
        >
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-4 shadow-lg border-2 border-amber-300">
            <div className="flex items-center space-x-2 mb-2">
              <div className="flex space-x-1">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className="w-2 h-2 bg-amber-600 rounded-full"
                    animate={{
                      scale: [1, 1.5, 1],
                      opacity: [0.5, 1, 0.5]
                    }}
                    transition={{
                      duration: 1,
                      repeat: Infinity,
                      delay: i * 0.2
                    }}
                  />
                ))}
              </div>
              <span className="text-sm font-medium text-amber-800">
                {isListening ? 'Processing...' : 'Transcribing...'}
              </span>
            </div>
            
            <div className="text-gray-700 text-sm">
              {currentTranscript || 'Listening for your voice...'}
            </div>
            
            <div className="mt-2 text-xs text-amber-600">
              💡 Your message will appear in chat after AI processing
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}