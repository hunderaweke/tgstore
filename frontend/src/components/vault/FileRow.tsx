import {
  FileIcon,
  FilePdfIcon,
  FileImageIcon,
  FileZipIcon,
  DotsThreeVerticalIcon,
} from '@phosphor-icons/react'
import { IconButton } from '../ui/IconButton'

export interface FileRowProps {
  name: string
  size: string
  updatedAt: string
  kind?: 'pdf' | 'image' | 'zip' | 'other'
  onOpenMenu?: () => void
}

const kindIcon = {
  pdf: FilePdfIcon,
  image: FileImageIcon,
  zip: FileZipIcon,
  other: FileIcon,
}

export function FileRow({ name, size, updatedAt, kind = 'other', onOpenMenu }: FileRowProps) {
  const Icon = kindIcon[kind]
  return (
    <div className="group flex items-center gap-3 rounded-lg px-3 py-2.5 hover:bg-surface">
      <Icon className="h-6 w-6 shrink-0 text-stamp" weight="duotone" />
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm text-ink">{name}</p>
        <p className="text-xs text-muted">
          {size} · {updatedAt}
        </p>
      </div>
      <IconButton
        label="File actions"
        onClick={onOpenMenu}
        className="opacity-0 group-hover:opacity-100"
      >
        <DotsThreeVerticalIcon className="h-5 w-5" weight="duotone" />
      </IconButton>
    </div>
  )
}
