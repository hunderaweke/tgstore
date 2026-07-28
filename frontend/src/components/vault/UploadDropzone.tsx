import React, { useCallback, useState } from 'react'
import { UploadSimpleIcon } from '@phosphor-icons/react'
import { cn } from '../../lib/cn'

interface UploadDropzoneProps {
  onFiles: (files: FileList) => void
  className?: string
}

export function UploadDropzone({ onFiles, className }: UploadDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLLabelElement>) => {
      e.preventDefault()
      setIsDragging(false)
      if (e.dataTransfer.files.length) onFiles(e.dataTransfer.files)
    },
    [onFiles],
  )

  return (
    <label
      onDragOver={(e) => {
        e.preventDefault()
        setIsDragging(true)
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      className={cn(
        'flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed px-6 py-12 text-center transition-colors',
        isDragging ? 'border-stamp bg-stamp/5' : 'border-muted/40 hover:border-muted/70',
        className,
      )}
    >
      <UploadSimpleIcon className="h-8 w-8 text-stamp" weight="duotone" />
      <p className="font-serif text-base text-ink">Drop files to store them</p>
      <p className="text-sm text-muted">or click to browse from your device</p>
      <input
        type="file"
        multiple
        className="sr-only"
        onChange={(e) => e.target.files && onFiles(e.target.files)}
      />
    </label>
  )
}
