'use client';

import { useState, useEffect } from 'react';

interface WellnessEntry {
  timestamp: string;
  mood: string;
  energy: string;
  objectives: string[];
  summary: string;
}

export function WellnessDashboard() {
  const [entries, setEntries] = useState<WellnessEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from an API
    // For now, we'll simulate the data
    const mockEntries: WellnessEntry[] = [
      {
        timestamp: new Date().toISOString(),
        mood: "energetic",
        energy: "high",
        objectives: ["Complete wellness check-in", "Take a walk", "Drink more water"],
        summary: "Focus on small, achievable goals today"
      }
    ];
    
    setTimeout(() => {
      setEntries(mockEntries);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        🌿 Recent Wellness Check-ins
      </h3>
      
      {entries.length === 0 ? (
        <p className="text-gray-500 dark:text-gray-400 text-center py-8">
          No wellness entries yet. Start your first check-in!
        </p>
      ) : (
        <div className="space-y-4">
          {entries.map((entry, index) => (
            <div key={index} className="border-l-4 border-green-500 pl-4 py-2">
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-2">
                <span>{new Date(entry.timestamp).toLocaleDateString()}</span>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-xs">
                    {entry.mood}
                  </span>
                  <span className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-xs">
                    {entry.energy} energy
                  </span>
                </div>
              </div>
              
              <div className="mb-2">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Goals:</p>
                <ul className="text-sm text-gray-600 dark:text-gray-400 list-disc list-inside">
                  {entry.objectives.map((objective, i) => (
                    <li key={i}>{objective}</li>
                  ))}
                </ul>
              </div>
              
              {entry.summary && (
                <p className="text-sm text-gray-600 dark:text-gray-400 italic">
                  💡 {entry.summary}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}