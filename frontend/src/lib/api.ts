const API_BASE = "/api"

export interface ResearchRequest {
  topic: string
}

export interface ResearchResponse {
  report: string
  subtasks: string[]
  fact_checks: { check?: string; error?: string }[]
  error: string | null
  run_id: string
}

export async function startResearch(topic: string): Promise<ResearchResponse> {
  const res = await fetch(`${API_BASE}/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  })
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || "Research request failed")
  }
  return res.json()
}
