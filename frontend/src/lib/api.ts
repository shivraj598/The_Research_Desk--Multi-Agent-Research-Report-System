export interface ResearchResponse {
  report: string
  subtasks: string[]
  fact_checks: { check?: string; error?: string }[]
  error: string | null
  run_id: string
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"

export async function startResearch(topic: string): Promise<ResearchResponse> {
  const res = await fetch(`${API_BASE}/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Request failed (${res.status})`)
  }
  return res.json()
}
