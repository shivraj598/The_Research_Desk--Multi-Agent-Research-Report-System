export type MessageRole = "user" | "assistant"
export type ResearchMode = "quick" | "deep"

export interface Message {
  id: string
  role: MessageRole
  content: string
  timestamp: Date
  subtasks?: string[]
  fact_checks?: { check?: string; error?: string }[]
  error?: string | null
  mode?: ResearchMode
}
