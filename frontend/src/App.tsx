import { useState } from "react"
import { ResearchForm } from "./components/ResearchForm"
import { ReportView } from "./components/ReportView"
import { type ResearchResponse } from "./lib/api"
import { BookOpen } from "lucide-react"

export default function App() {
  const [result, setResult] = useState<ResearchResponse | null>(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20">
      <header className="border-b border-border">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-3">
          <BookOpen className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-semibold tracking-tight">The Research Desk</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">Multi-Agent Research & Report System</h2>
          <p className="text-muted-foreground">
            Enter a topic and let our AI research team do the rest.
          </p>
        </div>

        <ResearchForm onResult={setResult} onLoading={setLoading} />

        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="flex flex-col items-center gap-3">
              <div className="flex gap-1">
                <span className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
              <p className="text-sm text-muted-foreground">
                Orchestrating agents, researching, analyzing, writing, fact-checking...
              </p>
            </div>
          </div>
        )}

        {result && <ReportView result={result} />}
      </main>
    </div>
  )
}
