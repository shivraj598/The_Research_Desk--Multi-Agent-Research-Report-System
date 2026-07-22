"use client"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { type ResearchResponse } from "@/lib/api"
import { FileText, ListTree, ShieldCheck } from "lucide-react"
import ReactMarkdown from "react-markdown"

interface Props {
  result: ResearchResponse
}

export function ReportView({ result }: Props) {
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

      {result.error && (
        <Card className="border-destructive">
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">Error: {result.error}</p>
          </CardContent>
        </Card>
      )}

      <Tabs defaultValue="report" className="w-full">
        <TabsList>
          <TabsTrigger value="report" className="flex items-center gap-1">
            <FileText className="h-4 w-4" /> Report
          </TabsTrigger>
          {result.fact_checks.length > 0 && (
            <TabsTrigger value="factcheck" className="flex items-center gap-1">
              <ShieldCheck className="h-4 w-4" /> Fact Check
            </TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="report" className="mt-4">
          <Card>
            <CardContent className="pt-6">
              <ScrollArea className="h-[600px]">
                {result.report ? (
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <ReactMarkdown>{result.report}</ReactMarkdown>
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No report generated.</p>
                )}
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        {result.fact_checks.length > 0 && (
          <TabsContent value="factcheck" className="mt-4">
            <Card>
              <CardContent className="pt-6">
                {result.fact_checks.map((fc, i) => (
                  <div key={i} className="text-sm whitespace-pre-wrap">
                    {fc.check || fc.error}
                    {i < result.fact_checks.length - 1 && <hr className="my-2" />}
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>
        )}
      </Tabs>
    </div>
  )
}
