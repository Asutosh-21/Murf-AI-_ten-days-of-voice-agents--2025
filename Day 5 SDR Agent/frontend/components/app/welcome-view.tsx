'use client';

import { Button } from '@/components/livekit/button';
import { useState } from 'react';

function ZerodhaLogo() {
  return (
    <div className="mb-6">
      <svg width="200" height="60" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="60" rx="8" fill="#387ED1"/>
        <text x="100" y="38" fontFamily="Arial, sans-serif" fontSize="24" fontWeight="bold" textAnchor="middle" fill="white">Zerodha</text>
      </svg>
      <p className="text-sm text-gray-600 mt-2">India's Largest Stock Broker</p>
    </div>
  );
}

function FeatureCard({ icon, title, description, onClick }: { icon: string, title: string, description: string, onClick: () => void }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer" onClick={onClick}>
      <div className="text-2xl mb-2">{icon}</div>
      <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  const [showFeatures, setShowFeatures] = useState(false);

  const handleFeatureClick = (feature: string) => {
    console.log(`Feature clicked: ${feature}`);
    onStartCall();
  };

  return (
    <div ref={ref} className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <section className="flex flex-col items-center justify-center text-center px-6 py-12">
        <ZerodhaLogo />

        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          Meet Your Zerodha SDR Assistant
        </h1>
        
        <p className="text-lg text-gray-600 max-w-2xl mb-8">
          Get instant answers about trading, investing, and our platform. 
          Book demos, learn about our services, and start your investment journey.
        </p>

        <div className="flex gap-4 mb-8">
          <Button 
            variant="primary" 
            size="lg" 
            onClick={onStartCall} 
            className="bg-blue-600 hover:bg-blue-700 px-8 py-3 text-lg font-semibold"
          >
            🎤 Start Voice Chat
          </Button>
          
          <Button 
            variant="outline" 
            size="lg" 
            onClick={() => setShowFeatures(!showFeatures)}
            className="border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-3 text-lg"
          >
            📋 View Features
          </Button>
        </div>

        {showFeatures && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mt-8">
            <FeatureCard 
              icon="💬" 
              title="FAQ Assistant" 
              description="Ask about trading, fees, platforms, and account opening"
              onClick={() => handleFeatureClick('faq')}
            />
            <FeatureCard 
              icon="📅" 
              title="Book Demo" 
              description="Schedule a personalized platform demonstration"
              onClick={() => handleFeatureClick('demo')}
            />
            <FeatureCard 
              icon="📊" 
              title="Lead Capture" 
              description="Share your details for personalized assistance"
              onClick={() => handleFeatureClick('lead')}
            />
            <FeatureCard 
              icon="🎯" 
              title="CRM Analysis" 
              description="Get qualification scoring and structured notes"
              onClick={() => handleFeatureClick('crm')}
            />
            <FeatureCard 
              icon="💰" 
              title="Pricing Info" 
              description="Learn about our transparent, low-cost structure"
              onClick={() => handleFeatureClick('pricing')}
            />
            <FeatureCard 
              icon="🚀" 
              title="Get Started" 
              description="Open account and start trading in minutes"
              onClick={() => handleFeatureClick('start')}
            />
          </div>
        )}

        <div className="mt-12 bg-white rounded-lg p-6 shadow-sm max-w-4xl">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">What You Can Do:</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
            <div>
              <h3 className="font-medium text-gray-700 mb-2">Ask Questions:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• "What does Zerodha do?"</li>
                <li>• "What are your brokerage fees?"</li>
                <li>• "How do I open an account?"</li>
                <li>• "Do you offer mutual funds?"</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-700 mb-2">Get Assistance:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Book a personalized demo</li>
                <li>• Share your investment goals</li>
                <li>• Get platform recommendations</li>
                <li>• Schedule follow-up calls</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <div className="fixed bottom-4 left-0 flex w-full items-center justify-center">
        <p className="text-gray-500 text-xs">
          Powered by LiveKit Agents • 
          <a href="https://zerodha.com" target="_blank" className="underline hover:text-blue-600">
            Visit Zerodha.com
          </a>
        </p>
      </div>
    </div>
  );
};
