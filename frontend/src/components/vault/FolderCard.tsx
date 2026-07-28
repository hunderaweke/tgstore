import { FolderIcon } from '@phosphor-icons/react'
import { Card } from '../ui/Card'

export interface FolderCardProps {
  name: string
  itemCount: number
  onClick?: () => void
}

export function FolderCard({ name, itemCount, onClick }: FolderCardProps) {
  return (
    <Card
      onClick={onClick}
      className="flex cursor-pointer items-center gap-3 transition-colors hover:bg-muted/10"
    >
      <FolderIcon className="h-8 w-8 shrink-0 text-forest" weight="duotone" />
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-ink">{name}</p>
        <p className="text-xs text-muted">{itemCount} items</p>
      </div>
    </Card>
  )
}
