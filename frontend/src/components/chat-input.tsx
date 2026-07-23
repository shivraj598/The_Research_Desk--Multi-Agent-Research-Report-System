"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import type { ResearchMode } from "@/lib/types"
import { Square, Sparkles, Brain, ArrowUp } from "lucide-react"

interface Props {
  onSend: (topic: string, mode: ResearchMode) => void
  onStop: () => void
  loading: boolean
}

export function ChatInput({ onSend, onStop, loading }: Props) {
  const [topic, setTopic] = useState("")
  const [mode, setMode] = useState<ResearchMode>("quick")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (!loading && textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [loading])

  const handleSubmit = () => {
    if (!topic.trim() || loading) return
    onSend(topic.trim(), mode)
    setTopic("")
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-border/40 bg-gradient-to-t from-background via-background/95 to-transparent backdrop-blur-sm">
      <div className="max-w-3xl mx-auto px-3 sm:px-4 py-2.5 sm:py-4">
        <div className="relative rounded-xl sm:rounded-2xl border border-border/60 bg-card/80 backdrop-blur-sm shadow-lg shadow-black/5 transition-all duration-200 focus-within:shadow-xl focus-within:shadow-primary/5 focus-within:border-primary/40 focus-within:bg-card">
          <div className="flex items-end gap-1.5 p-1.5 sm:p-2">
            <Textarea
              ref={textareaRef}
              placeholder="What would you like to research?"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              rows={1}
              className="min-h-[44px] max-h-[160px] resize-none border-0 bg-transparent px-2.5 sm:px-3 py-2.5 sm:py-3 text-sm shadow-none placeholder:text-muted-foreground/50 focus-visible:ring-0 leading-relaxed"
            />

            <div className="flex items-center gap-1 shrink-0 pb-0.5 sm:pb-1">
              <Select value={mode} onValueChange={(v) => setMode(v as ResearchMode)}>
                <SelectTrigger className="h-8 sm:h-9 min-w-[36px] sm:min-w-[140px] rounded-lg border-border/40 bg-secondary/40 px-1.5 sm:px-3 shadow-none hover:bg-secondary/60 transition-colors text-xs font-medium">
                  <SelectValue>
                    {mode === "quick" ? (
                      <span className="flex items-center gap-1 sm:gap-1.5">
                        <Sparkles className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                        <span className="hidden sm:inline">Quick Search</span>
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 sm:gap-1.5">
                        <Brain className="h-3.5 w-3.5 text-violet-500 shrink-0" />
                        <span className="hidden sm:inline">Deep Research</span>
                      </span>
                    )}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent align="end" className="min-w-[160px]">
                  <SelectItem value="quick">
                    <span className="flex items-center gap-2 text-sm">
                      <Sparkles className="h-3.5 w-3.5 text-amber-500" />
                      Quick Search
                    </span>
                  </SelectItem>
                  <SelectItem value="deep">
                    <span className="flex items-center gap-2 text-sm">
                      <Brain className="h-3.5 w-3.5 text-violet-500" />
                      Deep Research
                    </span>
                  </SelectItem>
                </SelectContent>
              </Select>

              {loading ? (
                <Button
                  onClick={onStop}
                  size="icon"
                  variant="destructive"
                  className="h-8 w-8 sm:h-9 sm:w-9 rounded-lg shrink-0"
                >
                  <Square className="h-3.5 w-3.5 sm:h-4 sm:w-4 fill-current" />
                </Button>
              ) : (
                <Button
                  onClick={handleSubmit}
                  size="icon"
                  disabled={!topic.trim()}
                  className="h-8 w-8 sm:h-9 sm:w-9 rounded-lg shrink-0 bg-gradient-to-br from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white shadow-md shadow-amber-600/20 disabled:opacity-40 disabled:shadow-none transition-all duration-200"
                >
                  <ArrowUp className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                </Button>
              )}
            </div>
          </div>
        </div>
        <p className="mt-1.5 sm:mt-2 text-[10px] sm:text-[11px] text-muted-foreground/50 text-center hidden sm:block">
          Research Desk uses AI. Verify important facts from reliable sources.
        </p>
      </div>
    </div>
  )
}
