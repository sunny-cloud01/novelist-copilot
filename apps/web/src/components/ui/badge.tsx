import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "../../lib/utils";

const badgeVariants = cva("nf-badge", {
  variants: {
    variant: {
      default: "nf-badge-default",
      success: "nf-badge-success",
      warning: "nf-badge-warning",
      danger: "nf-badge-danger",
      muted: "nf-badge-muted",
    },
  },
  defaultVariants: {
    variant: "default",
  },
});

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant, className }))} {...props} />;
}
