from datetime import date

from app.llm import get_llm_response

TODAY = date.today().isoformat()

ANALYST_SYSTEM_PROMPT = f"""Today is {TODAY}. You are a Research Analyst.

Read the raw source content below and extract structured insights.

For each source, extract:
1. Key facts and data points (with source URLs)
2. Important quotes (with attribution)
3. Statistics and figures
4. Key takeaways

Output as structured bullet points. Always cite the source URL for each claim.

CRITICAL RULES:
- Extract ONLY information present in the provided sources.
- Do NOT use any of your own knowledge or training data.
- Your training data may be months or years old — rely only on what you see here.
- If a source is not relevant, skip it."""


def analyst_agent(state: dict) -> dict:
    insights = state.get("insights", {})
    raw_sources = state.get("raw_sources", {})

    for subtask in state.get("subtasks", []):
        if subtask in insights:
            continue

        sources = raw_sources.get(subtask, [])
        if not sources:
            insights[subtask] = [{"error": "No sources available"}]
            continue

        source_text = ""
        for s in sources:
            content = s.get("content", "")
            if content:
                source_text += f"\n--- Source: {s.get('url', 'unknown')} ---\n{content[:3000]}\n"

        response = get_llm_response(
            ANALYST_SYSTEM_PROMPT,
            f"Subtasks: {subtask}\n\nSource Material:\n{source_text[:15000]}\n\nExtract structured insights (key facts, figures, quotes, takeaways) with source attributions.",
        )

        if response and not response.startswith("Error"):
            insights[subtask] = [{"analysis": response}]
        else:
            insights[subtask] = [{"error": response or "Analysis failed"}]

    state["insights"] = insights
    return state
