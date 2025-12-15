'use client';

import { useState, useEffect } from 'react';
import { useChat } from '@livekit/components-react';

interface PlayerStats {
  name: string;
  hp: number;
  status: string;
  attributes: {
    strength: number;
    intelligence: number;
    luck: number;
  };
  inventory: string[];
  location: string;
}

export function CharacterSheet() {
  const { send } = useChat();
  const [stats, setStats] = useState<PlayerStats>({
    name: 'Adventurer',
    hp: 100,
    status: 'Healthy',
    attributes: { strength: 12, intelligence: 14, luck: 10 },
    inventory: ['basic sword', 'leather armor', 'health potion'],
    location: 'Village of Ravenshollow'
  });
  const [isVisible, setIsVisible] = useState(false);

  const refreshStats = async () => {
    await send('Check my inventory and status');
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="bg-secondary text-secondary-foreground px-3 py-2 rounded-lg text-sm font-mono"
      >
        {isVisible ? 'Hide' : 'Show'} Character
      </button>
      
      {isVisible && (
        <div className="mt-2 bg-background border border-input rounded-lg p-4 w-64 text-sm">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-bold">{stats.name}</h3>
            <button
              onClick={refreshStats}
              className="text-xs bg-secondary px-2 py-1 rounded"
            >
              Refresh
            </button>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP:</span>
              <span className={stats.hp < 30 ? 'text-red-500' : stats.hp < 60 ? 'text-yellow-500' : 'text-green-500'}>
                {stats.hp}/100
              </span>
            </div>
            
            <div className="flex justify-between">
              <span>Status:</span>
              <span>{stats.status}</span>
            </div>
            
            <div className="border-t pt-2">
              <div className="text-xs font-semibold mb-1">Attributes</div>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <div>STR: {stats.attributes.strength}</div>
                <div>INT: {stats.attributes.intelligence}</div>
                <div>LUCK: {stats.attributes.luck}</div>
              </div>
            </div>
            
            <div className="border-t pt-2">
              <div className="text-xs font-semibold mb-1">Location</div>
              <div className="text-xs">{stats.location}</div>
            </div>
            
            <div className="border-t pt-2">
              <div className="text-xs font-semibold mb-1">Inventory</div>
              <div className="text-xs space-y-1">
                {stats.inventory.map((item, i) => (
                  <div key={i}>• {item}</div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}