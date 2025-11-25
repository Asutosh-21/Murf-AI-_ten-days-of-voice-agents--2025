export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Wellness Companion',
  pageTitle: 'Daily Wellness Voice Companion',
  pageDescription: 'Your supportive AI companion for daily health check-ins and wellness guidance',

  supportsChatInput: false,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/wellness-logo.svg',
  accent: '#10b981',
  logoDark: '/wellness-logo.svg',
  accentDark: '#34d399',
  startButtonText: 'Start Wellness Check-in',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
