import { Badge } from "./ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { type ResearchResponse } from "@/lib/api"
import { FileText, ListTree, ShieldCheck } from "lucide-react"
import ReactMarkdown from "react-markdown"

interface ReportViewProps {
  result: ResearchResponse
}

export function ReportView({ result }: ReportViewProps) {
  return (
    <div className="space-y-6">
      {result.subtasks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <ListTree className="h-4 w-4" />
              Research Subtasks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-1">
              {result.subtasks.map((task, i) => (
                <li key={i} className="text-sm text-muted-foreground">
                  {i + 1}. {task}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {result.fact_checks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <ShieldCheck className="h-4 w-4" />
              Fact Check Results
            </CardTitle>
          </CardHeader>
          <CardContent>
            {result.fact_checks.map((fc, i) => (
              <div key={i} className="text-sm text-muted-foreground whitespace-pre-wrap">
                {fc.check || fc.error}
                {i < result.fact_checks.length - 1 && <hr className="my-2" />}
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {result.error && (
        <Card className="border-red-200">
          <CardContent className="pt-6">
            <p className="text-sm text-red-600">Error: {result.error}</p>
          </CardContent>
        </Card>
      )}

      {(result.report || result.error) && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <FileText className="h-4 w-4" />
              Research Report
            </CardTitle>
          </CardHeader>
          <CardContent>
            {result.report ? (
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <ReactMarkdown>{result.report}</ReactMarkdown>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No report generated.</p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
