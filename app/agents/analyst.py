from app.llm import get_llm_response


ANALYST_SYSTEM_PROMPT = """You are a Research Analyst. Your job is to read raw source content and extract structured insights.

For each subtask, analyze the provided source material and extract:
1. Key facts and data points (with source URLs)
2. Important quotes (with attribution)
3. Statistics and figures
4. Key takeaways

Output the insights as structured bullet points grouped by subtask. Always cite the source URL for each claim.

CRITICAL RULES:
- Only extract information present in the provided sources
- Do not add external knowledge
- Always attribute claims to their source URL"""


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
