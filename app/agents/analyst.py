from app.llm import get_llm_response
from app.state import AppState

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


def analyst_agent(state: AppState) -> AppState:
    for subtask in state.subtasks:
        if subtask in state.insights:
            continue

        sources = state.raw_sources.get(subtask, [])
        if not sources:
            state.insights[subtask] = [{"error": "No sources available"}]
            continue

        source_text = ""
        for s in sources:
            content = s.get("content", "")
            if content:
                source_text += f"\n--- Source: {s.get('url', 'unknown')} ---\n{content[:3000]}\n"

        user_prompt = (
            f"Subtasks: {subtask}\n\n"
            f"Source Material:\n{source_text[:15000]}\n\n"
            "Extract structured insights (key facts, figures, quotes, takeaways) with source attributions."
        )
        response = get_llm_response(ANALYST_SYSTEM_PROMPT, user_prompt)

        if response and not response.startswith("Error"):
            state.insights[subtask] = [{"analysis": response}]
        else:
            state.insights[subtask] = [{"error": response or "Analysis failed"}]

    return state
