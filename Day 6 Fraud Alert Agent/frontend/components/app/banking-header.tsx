import React from 'react';

export function BankingHeader() {
  return (
    <header className="bg-card/95 border-border/50 border-b shadow-sm backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="from-primary to-accent rounded-lg bg-gradient-to-br p-2">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-primary-foreground"
              >
                <path d="M12 2L2 7V10H22V7L12 2Z" fill="currentColor" />
                <path
                  d="M4 11V20H6V11H4ZM9 11V20H11V11H9ZM13 11V20H15V11H13ZM18 11V20H20V11H18Z"
                  fill="currentColor"
                />
                <path d="M2 21H22V22H2V21Z" fill="currentColor" />
              </svg>
            </div>
            <div>
              <h1 className="text-foreground text-lg font-bold">NovaTrust Bank</h1>
              <p className="text-muted-foreground text-xs">Fraud Detection Center</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-muted-foreground hidden items-center space-x-2 text-sm sm:flex">
              <div className="flex items-center space-x-1">
                <div className="h-2 w-2 animate-pulse rounded-full bg-green-500"></div>
                <span>Live Agent</span>
              </div>
            </div>

            <div className="bg-accent/10 flex items-center space-x-1 rounded-full px-3 py-1">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="text-accent">
                <path
                  d="M12 1L15.09 8.26L22 9L17 14.74L18.18 22.02L12 18.77L5.82 22.02L7 14.74L2 9L8.91 8.26L12 1Z"
                  fill="currentColor"
                />
              </svg>
              <span className="text-accent text-xs font-medium">Secure</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
