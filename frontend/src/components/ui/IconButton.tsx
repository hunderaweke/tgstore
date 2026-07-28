import React from 'react'
import { cn } from '../../lib/cn'

type Variant = 'ghost' | 'solid'

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  label: string
}

export function IconButton({
  variant = 'ghost',
  label,
  className,
  children,
  ...props
}: IconButtonProps) {
  return (
    <button
      aria-label={label}
      title={label}
      className={cn(
        'inline-flex h-9 w-9 items-center justify-center rounded-lg transition-colors disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-stamp',
        variant === 'ghost' && 'text-ink hover:bg-surface',
        variant === 'solid' && 'bg-surface text-ink hover:bg-muted/30',
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}
