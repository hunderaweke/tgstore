import React from 'react'
import { cn } from '../../lib/cn'

interface EmptyStateProps {
  icon: React.ReactNode
  title: string
  description?: string
  action?: React.ReactNode
  className?: string
}

export function EmptyState({ icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-muted/40 px-6 py-16 text-center',
        className,
      )}
    >
      <div className="text-muted [&>svg]:h-10 [&>svg]:w-10">{icon}</div>
      <h3 className="font-serif text-lg text-ink">{title}</h3>
      {description && <p className="max-w-sm text-sm text-muted">{description}</p>}
      {action}
    </div>
  )
}
