'use client';

import { useState } from 'react';
import { RoomAudioRenderer, StartAudio } from '@livekit/components-react';
import type { AppConfig } from '@/app-config';
import { SessionProvider } from '@/components/app/session-provider';
import { ViewController } from '@/components/app/view-controller';
import { Toaster } from '@/components/livekit/toaster';
import { CoffeeMenu } from '@/components/app/coffee-menu';
import { OrderDisplay } from '@/components/app/order-display';
import { ReceiptsPanel } from '@/components/app/receipts-panel';
import { StatusIndicator } from '@/components/app/status-indicator';
import { LiveTranscription } from '@/components/app/live-transcription';
import { ProcessingIndicator } from '@/components/app/processing-indicator';
import { ExplanationPanel } from '@/components/app/explanation-panel';

interface AppProps {
  appConfig: AppConfig;
}

export function App({ appConfig }: AppProps) {
  const [showMenu, setShowMenu] = useState(true);
  const [showOrders, setShowOrders] = useState(false);
  const [showReceipts, setShowReceipts] = useState(false);
  const [showStatus, setShowStatus] = useState(false);
  const [showTranscription, setShowTranscription] = useState(true);
  const [showProcessing, setShowProcessing] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <SessionProvider appConfig={appConfig}>
      {/* Coffee shop background */}
      <div className="fixed inset-0 bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 -z-10" />
      
      {/* Main content */}
      <main className="relative grid h-svh grid-cols-1 place-content-center">
        <ViewController />
      </main>

      {/* Side panels */}
      <CoffeeMenu isVisible={showMenu} />
      <OrderDisplay isVisible={showOrders} />
      <ReceiptsPanel isVisible={showReceipts} onClose={() => setShowReceipts(false)} />
      <StatusIndicator isVisible={showStatus} />
      <LiveTranscription isVisible={showTranscription} />
      <ProcessingIndicator isVisible={showProcessing} />
      <ExplanationPanel isVisible={showExplanation} onClose={() => setShowExplanation(false)} />

      {/* Control buttons */}
      <div className="fixed bottom-4 left-4 flex flex-col space-y-2">
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="bg-amber-600 hover:bg-amber-700 text-white p-3 rounded-full shadow-lg transition-colors"
          title="Toggle Menu"
        >
          📋
        </button>
        <button
          onClick={() => setShowOrders(!showOrders)}
          className="bg-amber-600 hover:bg-amber-700 text-white p-3 rounded-full shadow-lg transition-colors"
          title="Toggle Current Orders"
        >
          ☕
        </button>
        <button
          onClick={() => setShowReceipts(true)}
          className="bg-amber-600 hover:bg-amber-700 text-white p-3 rounded-full shadow-lg transition-colors"
          title="View Receipts"
        >
          📄
        </button>
        <button
          onClick={() => setShowProcessing(!showProcessing)}
          className="bg-amber-600 hover:bg-amber-700 text-white p-3 rounded-full shadow-lg transition-colors"
          title="Toggle Processing Info"
        >
          🔄
        </button>
        <button
          onClick={() => setShowExplanation(true)}
          className="bg-amber-600 hover:bg-amber-700 text-white p-3 rounded-full shadow-lg transition-colors"
          title="Why Chat Takes Time?"
        >
          ❓
        </button>
      </div>

      <StartAudio label="Start Audio" />
      <RoomAudioRenderer />
      <Toaster />
    </SessionProvider>
  );
}
