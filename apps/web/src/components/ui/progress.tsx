import * as React from "react";

import { cn } from "../../lib/utils";

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number;
}

export function Progress({ value = 0, className, ...props }: ProgressProps) {
  const safeValue = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("nf-progress", className)} {...props}>
      <div className="nf-progress-bar" style={{ width: `${safeValue}%` }} />
    </div>
  );
}
