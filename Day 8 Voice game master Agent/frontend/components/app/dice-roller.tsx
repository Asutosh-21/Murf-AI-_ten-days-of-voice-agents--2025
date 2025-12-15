'use client';

import { useState } from 'react';
import { useChat } from '@livekit/components-react';

export function DiceRoller() {
  const { send } = useChat();
  const [isVisible, setIsVisible] = useState(false);
  const [lastRoll, setLastRoll] = useState<{roll: number, modifier: number, total: number, outcome: string} | null>(null);

  const rollDice = async (sides: number = 20, modifier: number = 0) => {
    const roll = Math.floor(Math.random() * sides) + 1;
    const total = roll + modifier;
    let outcome = 'Failure';
    if (total >= 15) outcome = 'Success';
    else if (total >= 10) outcome = 'Partial Success';
    
    setLastRoll({ roll, modifier, total, outcome });
    await send(`Roll ${sides}-sided die with ${modifier} modifier`);
  };

  return (
    <div className="fixed bottom-20 right-4 z-50">
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="bg-secondary text-secondary-foreground px-3 py-2 rounded-lg text-sm font-mono"
      >
        🎲 Dice
      </button>
      
      {isVisible && (
        <div className="mb-2 bg-background border border-input rounded-lg p-4 w-48">
          <h3 className="font-bold mb-3 text-sm">Roll Dice</h3>
          
          {lastRoll && (
            <div className="mb-3 p-2 bg-secondary rounded text-xs">
              <div>Roll: {lastRoll.roll} + {lastRoll.modifier} = {lastRoll.total}</div>
              <div className={`font-bold ${
                lastRoll.outcome === 'Success' ? 'text-green-500' :
                lastRoll.outcome === 'Partial Success' ? 'text-yellow-500' : 'text-red-500'
              }`}>
                {lastRoll.outcome}
              </div>
            </div>
          )}
          
          <div className="space-y-2">
            <button
              onClick={() => rollDice(20, 0)}
              className="w-full bg-primary text-primary-foreground px-3 py-2 rounded text-sm"
            >
              d20
            </button>
            <button
              onClick={() => rollDice(12, 0)}
              className="w-full bg-secondary hover:bg-secondary/80 px-3 py-2 rounded text-sm"
            >
              d12
            </button>
            <button
              onClick={() => rollDice(6, 0)}
              className="w-full bg-secondary hover:bg-secondary/80 px-3 py-2 rounded text-sm"
            >
              d6
            </button>
          </div>
        </div>
      )}
    </div>
  );
}