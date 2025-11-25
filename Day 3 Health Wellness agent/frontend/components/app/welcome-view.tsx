import { Button } from '@/components/livekit/button';
import { WellnessDashboard } from '@/components/app/wellness-dashboard';

function WelcomeImage() {
  return (
    <div className="mb-6 flex items-center justify-center">
      <div className="relative">
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 opacity-20 blur-xl"></div>
        <div className="relative rounded-full bg-gradient-to-br from-green-500 to-emerald-600 p-6">
          <svg
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="text-white"
          >
            <path
              d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7.5V9M15 11.5C15.8 11.5 16.5 12.2 16.5 13S15.8 14.5 15 14.5 13.5 13.8 13.5 13 14.2 11.5 15 11.5M5 12C5.8 12 6.5 12.7 6.5 13.5S5.8 15 5 15 3.5 14.3 3.5 13.5 4.2 12 5 12M12 7.5C12.8 7.5 13.5 8.2 13.5 9S12.8 10.5 12 10.5 10.5 9.8 10.5 9 11.2 7.5 12 7.5M12 12C13.1 12 14 12.9 14 14V22H10V14C10 12.9 10.9 12 12 12Z"
              fill="currentColor"
            />
          </svg>
        </div>
      </div>
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
  return (
    <div ref={ref} className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <section className="flex flex-col items-center justify-center text-center mb-12">
        <WelcomeImage />

        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Daily Wellness Companion
        </h1>
        <p className="text-gray-600 dark:text-gray-300 max-w-prose text-lg leading-relaxed mb-4">
          Your supportive AI companion for daily check-ins
        </p>
        <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-6">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Mood & Energy Check</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>Daily Goals</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <span>Wellness Tips</span>
          </div>
        </div>

        <Button 
          variant="primary" 
          size="lg" 
          onClick={onStartCall} 
          className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          🌿 {startButtonText}
        </Button>
        </section>
        
        {/* Wellness Dashboard */}
        <div className="max-w-2xl mx-auto mb-8">
          <WellnessDashboard />
        </div>
      </div>

      <div className="text-center py-8">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          🌱 Start your wellness journey with personalized daily check-ins and supportive guidance.
        </p>
      </div>
    </div>
  );
};
