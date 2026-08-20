import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center border px-2.5 py-1 text-[0.68rem] font-bold uppercase tracking-[0.12em] transition-colors",
        {
          "border-primary/40 bg-primary/10 text-primary": variant === "default",
          "border-border bg-muted text-muted-foreground": variant === "secondary",
          "border-border text-foreground": variant === "outline",
        },
        className
      )}
      {...props}
    />
  )
}

export { Badge }
