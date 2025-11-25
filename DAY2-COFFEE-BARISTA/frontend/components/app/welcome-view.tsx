import { motion } from 'motion/react';
import { Button } from '@/components/livekit/button';
import { CoffeeMug } from './coffee-mug';

function CoffeeShopLogo() {
  return (
    <div className="flex flex-col items-center mb-8">
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 260, damping: 20 }}
        className="mb-4"
      >
        <CoffeeMug size="large" drinkType="latte" animated={true} />
      </motion.div>
      
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-4xl font-bold text-amber-800 mb-2"
      >
        ☕ Brew & Bean
      </motion.h1>
      
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="text-lg text-amber-600 font-medium"
      >
        Coffee Shop
      </motion.p>
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
    <div ref={ref}>
      <section className="flex flex-col items-center justify-center text-center min-h-screen">
        <CoffeeShopLogo />

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="text-center mb-8"
        >
          <p className="text-gray-700 max-w-prose leading-6 font-medium text-lg mb-2">
            Hi! I'm Maya, your friendly barista! 👋
          </p>
          <p className="text-gray-600 max-w-prose leading-6">
            Ready to take your coffee order with voice AI
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.9 }}
        >
          <Button 
            variant="primary" 
            size="lg" 
            onClick={onStartCall} 
            className="mt-6 w-64 font-mono bg-amber-600 hover:bg-amber-700 text-white border-amber-600 hover:border-amber-700"
          >
            {startButtonText}
          </Button>
        </motion.div>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-amber-700/70 max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm"
        >
          🎤 Just speak naturally - I'll help you create the perfect coffee order!
        </motion.p>
      </div>
    </div>
  );
};
