import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ChatEntryProps extends React.HTMLAttributes<HTMLLIElement> {
  /** The locale to use for the timestamp. */
  locale: string;
  /** The timestamp of the message. */
  timestamp: number;
  /** The message to display. */
  message: string;
  /** The origin of the message. */
  messageOrigin: 'local' | 'remote';
  /** The sender's name. */
  name?: string;
  /** Whether the message has been edited. */
  hasBeenEdited?: boolean;
}

export const ChatEntry = ({
  name,
  locale,
  timestamp,
  message,
  messageOrigin,
  hasBeenEdited = false,
  className,
  ...props
}: ChatEntryProps) => {
  const time = new Date(timestamp);
  const title = time.toLocaleTimeString(locale, { timeStyle: 'full' });

  return (
    <li
      title={title}
      data-lk-message-origin={messageOrigin}
      className={cn('group flex w-full flex-col gap-0.5', className)}
      {...props}
    >
      <header
        className={cn(
          'text-amber-700 flex items-center gap-2 text-sm font-medium',
          messageOrigin === 'local' ? 'flex-row-reverse' : 'text-left'
        )}
      >
        {name && <strong className="text-amber-800">{name}</strong>}
        <span className="font-mono text-xs text-amber-600 opacity-70 transition-opacity ease-linear group-hover:opacity-100">
          {hasBeenEdited && '*'}
          {time.toLocaleTimeString(locale, { timeStyle: 'short' })}
        </span>
      </header>
      <span
        className={cn(
          'max-w-4/5 rounded-[20px] p-3 text-sm',
          messageOrigin === 'local' 
            ? 'bg-amber-600 text-white ml-auto shadow-md' 
            : 'bg-white text-gray-800 mr-auto shadow-md border border-amber-200'
        )}
      >
        {message}
      </span>
    </li>
  );
};
