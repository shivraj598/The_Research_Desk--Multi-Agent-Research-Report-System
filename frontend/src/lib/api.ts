export interface ResearchResponse {
  report: string
  subtasks: string[]
  fact_checks: { check?: string; error?: string }[]
  error: string | null
  run_id: string
  status: string
}

const API_BASE = "/api"

export async function startResearch(topic: string, mode: string = "quick"): Promise<{ run_id: string }> {
  const res = await fetch(`${API_BASE}/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic, mode }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export async function pollResearch(runId: string): Promise<ResearchResponse> {
  const res = await fetch(`${API_BASE}/research/${runId}`)
  if (!res.ok) return { status: "error", error: "Failed to fetch result", report: "", subtasks: [], fact_checks: [], run_id: runId }
  return res.json()
}

export async function stopResearch(runId: string): Promise<void> {
  await fetch(`${API_BASE}/research/${runId}/stop`, { method: "POST" })
}
