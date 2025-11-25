'use client';

import { motion, AnimatePresence } from 'motion/react';

interface ExplanationPanelProps {
  isVisible: boolean;
  onClose: () => void;
}

export function ExplanationPanel({ isVisible, onClose }: ExplanationPanelProps) {
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
          className="bg-white rounded-2xl p-6 max-w-lg w-full"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-amber-800">🤔 Why Chat Takes Time?</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ×
            </button>
          </div>

          <div className="space-y-4 text-sm text-gray-700">
            <div className="bg-amber-50 p-3 rounded-lg">
              <h3 className="font-semibold text-amber-800 mb-2">Voice AI Processing Pipeline:</h3>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">🎤</span>
                  <span><strong>Step 1:</strong> Your voice is captured (~0.5s)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg">📝</span>
                  <span><strong>Step 2:</strong> Deepgram converts speech to text (~1-2s)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg">🧠</span>
                  <span><strong>Step 3:</strong> Google Gemini processes & responds (~2-4s)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg">🗣️</span>
                  <span><strong>Step 4:</strong> Murf converts text to speech (~1-2s)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg">💬</span>
                  <span><strong>Step 5:</strong> Message appears in chat</span>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 p-3 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">⏱️ Total Time: 4-8 seconds</h3>
              <p>This is normal for voice AI systems. The delay ensures:</p>
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li>Accurate speech recognition</li>
                <li>Thoughtful AI responses</li>
                <li>Natural-sounding voice output</li>
              </ul>
            </div>

            <div className="bg-green-50 p-3 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-2">💡 Pro Tips:</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Speak clearly and pause between sentences</li>
                <li>Watch the audio visualizer to see when Maya is listening</li>
                <li>Use the processing indicator to see what's happening</li>
                <li>Chat messages appear after the full AI pipeline completes</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}