"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { ChatMessage } from "@/components/chat-message"
import { ChatInput } from "@/components/chat-input"
import { ResearchingIndicator } from "@/components/researching-indicator"
import { ThemeToggle } from "@/components/theme-toggle"
import { startResearch, pollResearch } from "@/lib/api"
import type { Message, ResearchMode } from "@/lib/types"
import { BookOpen } from "lucide-react"

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const pollingRef = useRef(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  const handleSend = useCallback(async (topic: string, mode: ResearchMode) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: topic,
      timestamp: new Date(),
      mode,
    }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    pollingRef.current = true

    try {
      const { run_id } = await startResearch(topic, mode)

      while (pollingRef.current) {
        await new Promise((r) => setTimeout(r, 2000))
        if (!pollingRef.current) break
        const result = await pollResearch(run_id)
        if (result.status === "cancelled") {
          setMessages((prev) => [
            ...prev,
            { id: crypto.randomUUID(), role: "assistant", content: "", timestamp: new Date(), error: "Research cancelled", mode },
          ])
          return
        }
        if (result.status === "done" || result.status === "error") {
          setMessages((prev) => [
            ...prev,
            { id: crypto.randomUUID(), role: "assistant", content: result.report || "", timestamp: new Date(), subtasks: result.subtasks, fact_checks: result.fact_checks, error: result.error, mode },
          ])
          return
        }
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "assistant", content: "", timestamp: new Date(), error: err instanceof Error ? err.message : "Failed to get response", mode },
      ])
    } finally {
      setLoading(false)
      pollingRef.current = false
    }
  }, [])

  const handleStop = useCallback(async () => {
    pollingRef.current = false
    setLoading(false)
  }, [])

  return (
    <div className="h-dvh flex flex-col bg-gradient-to-b from-background via-background to-secondary/30">
      <header className="border-b border-border/40 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-5xl mx-auto px-3 sm:px-4 h-14 sm:h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5 sm:gap-3">
            <div className="h-8 w-8 sm:h-9 sm:w-9 rounded-lg sm:rounded-xl bg-gradient-to-br from-amber-500 to-amber-700 shadow-lg shadow-amber-500/20 flex items-center justify-center">
              <BookOpen className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
            </div>
            <div>
              <h1 className="text-sm sm:text-base font-semibold tracking-tight">The Research Desk</h1>
              <p className="text-[10px] sm:text-[11px] text-muted-foreground hidden sm:block">Multi-Agent Research System</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </header>

      <main className="flex-1 overflow-y-auto scroll-smooth">
        <div className="max-w-3xl mx-auto px-3 sm:px-4 py-4 sm:py-8 space-y-4 sm:space-y-6">
          {messages.length === 0 && !loading && (
            <div className="flex flex-col items-center justify-center h-[50vh] sm:h-[60vh] text-center px-4">
              <div className="h-14 w-14 sm:h-20 sm:w-20 rounded-2xl sm:rounded-3xl bg-gradient-to-br from-amber-500/20 to-amber-700/10 flex items-center justify-center mb-4 sm:mb-6 ring-1 ring-amber-500/10">
                <BookOpen className="h-7 w-7 sm:h-10 sm:w-10 text-amber-600 dark:text-amber-400" />
              </div>
              <h2 className="text-xl sm:text-2xl font-semibold tracking-tight mb-2">What would you like to research?</h2>
              <p className="text-sm text-muted-foreground max-w-md">
                Ask anything — Quick Search for fast answers, Deep Research for comprehensive reports with web sources.
              </p>
            </div>
          )}

          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}

          {loading && <ResearchingIndicator />}

          <div ref={bottomRef} />
        </div>
      </main>

      <ChatInput onSend={handleSend} onStop={handleStop} loading={loading} />
    </div>
  )
}
