import {
  ArchiveIcon,
  ClockCounterClockwiseIcon,
  GearIcon,
  HouseIcon,
  TrashIcon,
} from '@phosphor-icons/react'
import { cn } from '../../lib/cn'

const NAV_ITEMS = [
  { key: 'home', label: 'Home', icon: HouseIcon },
  { key: 'recent', label: 'Recent', icon: ClockCounterClockwiseIcon },
  { key: 'archive', label: 'Archive', icon: ArchiveIcon },
  { key: 'trash', label: 'Trash', icon: TrashIcon },
  { key: 'settings', label: 'Settings', icon: GearIcon },
] as const

export type SidebarKey = (typeof NAV_ITEMS)[number]['key']

interface SidebarProps {
  active: SidebarKey
  onSelect: (key: SidebarKey) => void
}

export function Sidebar({ active, onSelect }: SidebarProps) {
  return (
    <nav className="flex w-56 shrink-0 flex-col gap-1 border-r border-muted/20 bg-paper p-3">
      <p className="px-3 pb-3 font-serif text-lg text-ink">tgstore</p>
      {NAV_ITEMS.map(({ key, label, icon: Icon }) => {
        const isActive = key === active
        return (
          <button
            key={key}
            onClick={() => onSelect(key)}
            className={cn(
              'flex items-center gap-2.5 rounded-lg px-3 py-2 text-left text-sm transition-colors',
              isActive ? 'bg-stamp/15 text-stamp font-medium' : 'text-ink hover:bg-surface',
            )}
          >
            <Icon className="h-5 w-5" weight="duotone" />
            {label}
          </button>
        )
      })}
    </nav>
  )
}
