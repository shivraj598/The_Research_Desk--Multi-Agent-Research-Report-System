"use client"

import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import type { Message } from "@/lib/types"
import { BookOpen, ListTree, ShieldCheck, User, Sparkles, Brain, ChevronRight } from "lucide-react"
import ReactMarkdown from "react-markdown"

interface Props {
  message: Message
}

export function ChatMessage({ message }: Props) {
  const isUser = message.role === "user"

  return (
    <div className={`flex gap-2 sm:gap-3 items-start ${isUser ? "flex-row-reverse" : ""}`}>
      <Avatar className={`h-7 w-7 sm:h-8 sm:w-8 shrink-0 mt-0.5 ring-2 ring-background ${
        isUser
          ? "bg-gradient-to-br from-amber-500 to-amber-700"
          : "bg-gradient-to-br from-amber-500/80 to-amber-700/80"
      }`}>
        <AvatarFallback className="text-white text-[10px] sm:text-xs">
          {isUser ? <User className="h-3.5 w-3.5 sm:h-4 sm:w-4" /> : <BookOpen className="h-3.5 w-3.5 sm:h-4 sm:w-4" />}
        </AvatarFallback>
      </Avatar>

      <div className={`flex flex-col gap-1 max-w-[85%] sm:max-w-[80%] ${isUser ? "items-end" : ""}`}>
        <div className={`flex items-center gap-1.5 sm:gap-2 text-[11px] sm:text-xs text-muted-foreground/80 ${isUser ? "flex-row-reverse" : ""}`}>
          <span className="font-medium">{isUser ? "You" : "Research Desk"}</span>
          {!isUser && message.mode && (
            <Badge variant="secondary" className={`text-[9px] sm:text-[10px] h-4 sm:h-5 px-1.5 gap-1 font-normal ${
              message.mode === "deep"
                ? "bg-violet-500/10 text-violet-600 dark:text-violet-400 border-violet-500/20"
                : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20"
            }`}>
              {message.mode === "deep" ? (
                <><Brain className="h-2.5 w-2.5" /><span className="hidden sm:inline">Deep</span></>
              ) : (
                <><Sparkles className="h-2.5 w-2.5" /><span className="hidden sm:inline">Quick</span></>
              )}
            </Badge>
          )}
        </div>

        {isUser ? (
          <Card className="rounded-2xl rounded-tr-sm bg-gradient-to-br from-amber-600 to-amber-700 text-white px-3.5 sm:px-4 py-2 sm:py-2.5 border-0 shadow-lg shadow-amber-600/20">
            <p className="text-sm leading-relaxed">{message.content}</p>
          </Card>
        ) : message.content ? (
          <Card className="rounded-2xl rounded-tl-sm px-4 sm:px-5 py-3 sm:py-4 border-border/50 shadow-sm bg-card/50 backdrop-blur-sm">
            {message.subtasks && message.subtasks.length > 0 && (
              <details className="mb-3 group">
                <summary className="flex items-center gap-1.5 text-[11px] sm:text-xs text-muted-foreground cursor-pointer hover:text-foreground transition-colors list-none [&::-webkit-details-marker]:hidden">
                  <ChevronRight className="h-3 w-3 transition-transform group-open:rotate-90" />
                  <ListTree className="h-3 w-3 sm:h-3.5 sm:w-3.5 text-amber-500" />
                  {message.subtasks.length} research subtask{message.subtasks.length > 1 ? "s" : ""}
                </summary>
                <ul className="mt-2 space-y-1 pl-5">
                  {message.subtasks.map((t, i) => (
                    <li key={i} className="text-[11px] sm:text-xs text-muted-foreground list-disc">{t}</li>
                  ))}
                </ul>
              </details>
            )}

            <div className="prose prose-sm max-w-none dark:prose-invert prose-headings:font-semibold prose-headings:tracking-tight prose-h2:text-base prose-h3:text-sm prose-p:text-sm prose-p:leading-relaxed prose-a:text-amber-600 dark:prose-a:text-amber-400 prose-a:no-underline hover:prose-a:underline prose-code:text-[12px] prose-pre:bg-secondary/50 prose-pre:border prose-pre:border-border/50">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>

            {message.fact_checks && message.fact_checks.length > 0 && (
              <>
                <Separator className="my-3 bg-border/30" />
                <details className="group">
                  <summary className="flex items-center gap-1.5 text-[11px] sm:text-xs text-muted-foreground cursor-pointer hover:text-foreground transition-colors list-none [&::-webkit-details-marker]:hidden">
                    <ChevronRight className="h-3 w-3 transition-transform group-open:rotate-90" />
                    <ShieldCheck className="h-3 w-3 sm:h-3.5 sm:w-3.5 text-emerald-500" />
                    Fact check results
                  </summary>
                  <div className="mt-2 text-[11px] sm:text-xs text-muted-foreground space-y-1">
                    {message.fact_checks.map((fc, i) => (
                      <p key={i} className="text-[11px] sm:text-xs">{fc.check || fc.error}</p>
                    ))}
                  </div>
                </details>
              </>
            )}

            {message.error && (
              <div className="mt-2 flex items-center gap-1.5 text-[11px] sm:text-xs text-destructive bg-destructive/5 rounded-lg px-2.5 py-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-destructive shrink-0" />
                {message.error}
              </div>
            )}
          </Card>
        ) : null}
      </div>
    </div>
  )
}
