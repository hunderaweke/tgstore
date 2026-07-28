import React, { useState } from "react";

interface SpoilerProps {
  children: React.ReactNode;
  className?: string;
}

export function Spoiler({ children, className = "" }: SpoilerProps) {
  const [isRevealed, setIsRevealed] = useState(false);

  return (
    <span
      onClick={() => setIsRevealed((prev) => !prev)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          setIsRevealed((prev) => !prev);
        }
      }}
      role="button"
      tabIndex={0}
      aria-expanded={isRevealed}
      title={isRevealed ? "Click to hide" : "Click to reveal"}
      className={`telegram-spoiler ${isRevealed ? "revealed" : ""} ${className}`}
    >
      <span className="spoiler-content">{children}</span>
    </span>
  );
}
