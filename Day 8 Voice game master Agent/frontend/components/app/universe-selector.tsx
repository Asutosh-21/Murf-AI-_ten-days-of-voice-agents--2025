'use client';

import { useState } from 'react';
import { useChat } from '@livekit/components-react';

const UNIVERSES = [
  { id: 'fantasy', name: 'Classic Fantasy', desc: 'Dragons, magic, medieval adventure' },
  { id: 'cyberpunk', name: 'Cyberpunk City', desc: 'Neon streets, corporate conspiracies' },
  { id: 'space', name: 'Space Opera', desc: 'Galactic adventures, alien worlds' }
];

export function UniverseSelector() {
  const { send } = useChat();
  const [isVisible, setIsVisible] = useState(false);
  const [currentUniverse, setCurrentUniverse] = useState('fantasy');

  const switchUniverse = async (universeId: string) => {
    await send(`Switch to ${universeId} universe`);
    setCurrentUniverse(universeId);
    setIsVisible(false);
  };

  const currentUniverseName = UNIVERSES.find(u => u.id === currentUniverse)?.name || 'Fantasy';

  return (
    <div className="fixed top-4 left-4 z-50">
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="bg-secondary text-secondary-foreground px-3 py-2 rounded-lg text-sm font-mono"
      >
        🌍 {currentUniverseName}
      </button>
      
      {isVisible && (
        <div className="mt-2 bg-background border border-input rounded-lg p-4 w-72">
          <h3 className="font-bold mb-3 text-sm">Choose Universe</h3>
          <div className="space-y-2">
            {UNIVERSES.map((universe) => (
              <button
                key={universe.id}
                onClick={() => switchUniverse(universe.id)}
                className={`w-full text-left p-3 rounded-lg border transition-colors ${
                  currentUniverse === universe.id
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-secondary hover:bg-secondary/80 border-input'
                }`}
              >
                <div className="font-semibold text-sm">{universe.name}</div>
                <div className="text-xs opacity-70">{universe.desc}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}