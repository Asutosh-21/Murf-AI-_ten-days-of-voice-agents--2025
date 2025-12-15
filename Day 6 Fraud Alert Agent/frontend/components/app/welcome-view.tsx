import { Button } from '@/components/livekit/button';

function BankingLogo() {
  return (
    <div className="relative mb-6">
      <div className="from-primary to-accent rounded-full bg-gradient-to-br p-6 shadow-lg">
        <svg
          width="48"
          height="48"
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
      <div className="bg-accent absolute -top-1 -right-1 rounded-full p-1">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          className="text-accent-foreground"
        >
          <path
            d="M12 1L15.09 8.26L22 9L17 14.74L18.18 22.02L12 18.77L5.82 22.02L7 14.74L2 9L8.91 8.26L12 1Z"
            fill="currentColor"
          />
        </svg>
      </div>
    </div>
  );
}

function SecurityFeatures() {
  return (
    <div className="mt-8 mb-6 grid max-w-md grid-cols-3 gap-4">
      <div className="text-center">
        <div className="bg-card mb-2 rounded-lg p-3 shadow-sm">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            className="text-primary mx-auto"
          >
            <path
              d="M12 1L21 5V11C21 16.55 17.16 21.74 12 23C6.84 21.74 3 16.55 3 11V5L12 1Z"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
            />
            <path d="M9 12L11 14L15 10" stroke="currentColor" strokeWidth="2" fill="none" />
          </svg>
        </div>
        <p className="text-muted-foreground text-xs font-medium">Secure</p>
      </div>
      <div className="text-center">
        <div className="bg-card mb-2 rounded-lg p-3 shadow-sm">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            className="text-primary mx-auto"
          >
            <path
              d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 4L13.5 7H7V9H13.5L15 12L21 9Z"
              fill="currentColor"
            />
            <path d="M7 24H9V14H7V24ZM15 24H17V14H15V24Z" fill="currentColor" />
          </svg>
        </div>
        <p className="text-muted-foreground text-xs font-medium">AI Powered</p>
      </div>
      <div className="text-center">
        <div className="bg-card mb-2 rounded-lg p-3 shadow-sm">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            className="text-primary mx-auto"
          >
            <path
              d="M12 14C15.31 14 18 11.31 18 8S15.31 2 12 2 6 4.69 6 8 8.69 14 12 14Z"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
            />
            <path
              d="M3 22V18C3 15.79 4.79 14 7 14H17C19.21 14 21 15.79 21 18V22"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
            />
          </svg>
        </div>
        <p className="text-muted-foreground text-xs font-medium">24/7 Support</p>
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
    <div
      ref={ref}
      className="from-background via-background to-secondary/20 min-h-screen bg-gradient-to-br"
    >
      <section className="flex min-h-screen flex-col items-center justify-center px-6 py-12 text-center">
        <BankingLogo />

        <div className="bg-card/80 border-border/50 w-full max-w-lg rounded-2xl border p-8 shadow-xl backdrop-blur-sm">
          <h1 className="from-primary to-accent mb-3 bg-gradient-to-r bg-clip-text text-3xl font-bold text-transparent">
            NovaTrust Bank
          </h1>
          <h2 className="text-foreground mb-4 text-xl font-semibold">Fraud Detection Agent</h2>
          <p className="text-muted-foreground mb-6 leading-relaxed">
            Advanced AI-powered voice agent for real-time fraud detection, customer verification,
            and secure transaction processing.
          </p>

          <SecurityFeatures />

          <Button
            variant="primary"
            size="lg"
            onClick={onStartCall}
            className="from-primary to-accent hover:from-primary/90 hover:to-accent/90 w-full bg-gradient-to-r py-3 text-lg font-semibold shadow-lg transition-all duration-200"
          >
            {startButtonText}
          </Button>

          <div className="border-border/30 mt-6 border-t pt-4">
            <p className="text-muted-foreground mb-2 text-xs font-medium">
              🔒 Bank-grade security • 🎯 Real-time fraud detection • 🗣️ Natural voice interaction
            </p>
          </div>
        </div>
      </section>

      <div className="fixed right-0 bottom-4 left-0 flex justify-center px-4">
        <div className="bg-card/90 border-border/50 rounded-lg border px-4 py-2 shadow-md backdrop-blur-sm">
          <p className="text-muted-foreground text-center text-xs font-medium">
            Test Customers: John Smith • Sarah Wilson • Michael Brown • Emily Davis • David Martinez
          </p>
        </div>
      </div>
    </div>
  );
};
