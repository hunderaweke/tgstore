import React from 'react'
import { cn } from '../../lib/cn'

type Tone = 'neutral' | 'stamp' | 'forest' | 'danger'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: Tone
}

const toneStyles: Record<Tone, string> = {
  neutral: 'bg-muted/15 text-ink',
  stamp: 'bg-stamp/15 text-stamp',
  forest: 'bg-forest/15 text-forest',
  danger: 'bg-red-700/10 text-red-700',
}

export function Badge({ tone = 'neutral', className, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
        toneStyles[tone],
        className,
      )}
      {...props}
    />
  )
}
