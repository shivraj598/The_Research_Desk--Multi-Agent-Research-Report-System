"use client"

import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Card } from "@/components/ui/card"
import { BookOpen } from "lucide-react"

export function ResearchingIndicator() {
  return (
    <div className="flex gap-2 sm:gap-3 items-start">
      <Avatar className="h-7 w-7 sm:h-8 sm:w-8 shrink-0 mt-0.5 ring-2 ring-background bg-gradient-to-br from-amber-500/80 to-amber-700/80">
        <AvatarFallback className="text-white text-[10px] sm:text-xs">
          <BookOpen className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
        </AvatarFallback>
      </Avatar>

      <Card className="rounded-2xl rounded-tl-sm px-4 sm:px-5 py-3 sm:py-4 border-border/50 shadow-sm bg-card/50 backdrop-blur-sm min-w-[160px] sm:min-w-[200px]">
        <div className="flex items-center gap-3">
          <div className="flex gap-1">
            <span className="h-1.5 w-1.5 sm:h-2 sm:w-2 rounded-full bg-amber-500 animate-bounce [animation-delay:0ms]" />
            <span className="h-1.5 w-1.5 sm:h-2 sm:w-2 rounded-full bg-amber-500 animate-bounce [animation-delay:150ms]" />
            <span className="h-1.5 w-1.5 sm:h-2 sm:w-2 rounded-full bg-amber-500 animate-bounce [animation-delay:300ms]" />
          </div>
          <span className="text-xs sm:text-sm text-muted-foreground font-medium">Researching...</span>
        </div>
      </Card>
    </div>
  )
}
