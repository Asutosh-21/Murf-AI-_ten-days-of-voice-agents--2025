import React from 'react';

interface SessionStatusProps {
  isConnected: boolean;
  customerName?: string;
  caseStatus?: string;
}

export function SessionStatus({ isConnected, customerName, caseStatus }: SessionStatusProps) {
  if (!isConnected) return null;

  return (
    <div className="bg-card/95 border-border/50 fixed top-20 right-4 max-w-sm rounded-lg border p-4 shadow-lg backdrop-blur-sm">
      <div className="mb-2 flex items-center space-x-2">
        <div className="h-3 w-3 animate-pulse rounded-full bg-green-500"></div>
        <span className="text-foreground text-sm font-semibold">Session Active</span>
      </div>

      {customerName && (
        <div className="text-muted-foreground mb-1 text-sm">
          <span className="font-medium">Customer:</span> {customerName}
        </div>
      )}

      {caseStatus && (
        <div className="text-muted-foreground text-sm">
          <span className="font-medium">Status:</span>
          <span
            className={`ml-1 rounded-full px-2 py-0.5 text-xs font-medium ${
              caseStatus === 'verified'
                ? 'bg-green-100 text-green-800'
                : caseStatus === 'pending'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
            }`}
          >
            {caseStatus}
          </span>
        </div>
      )}

      <div className="border-border/30 mt-3 border-t pt-2">
        <div className="text-muted-foreground flex items-center justify-between text-xs">
          <span>🔒 Encrypted Connection</span>
          <span>🎯 AI Fraud Detection</span>
        </div>
      </div>
    </div>
  );
}
