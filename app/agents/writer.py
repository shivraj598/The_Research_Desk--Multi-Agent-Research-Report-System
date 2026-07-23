from datetime import date

from app.llm import get_llm_response

TODAY = date.today().isoformat()

WRITER_SYSTEM_PROMPT = f"""Today is {TODAY}. You are a professional Report Writer.

Your job is to compile structured research insights into a cohesive, well-formatted report.

The report should include:
1. Title
2. Executive Summary (2-3 paragraphs)
3. Main sections with headings (one per subtask)
4. Conclusion
5. Sources/References section

Format the report in Markdown with proper headings, bullet points, and emphasis where appropriate.

CRITICAL RULES:
- Your training data may be outdated. Use ONLY the provided insights below.
- Do NOT add any facts, figures, or claims from your own knowledge.
- If the insights lack information on a subtask, state that clearly.
- Cite source URLs inline where possible.
- Write in a professional, objective tone."""


def writer_agent(state: dict) -> dict:
    insights_text = ""
    for subtask in state.get("subtasks", []):
        items = state.get("insights", {}).get(subtask, [])
        if not items:
            continue
        insights_text += f"\n\n## Subtask: {subtask}\n"
        for item in items:
            if "analysis" in item:
                insights_text += item["analysis"] + "\n"
            elif "error" in item:
                insights_text += f"[No insights available: {item['error']}]\n"

    user_prompt = (
        f"Report Topic: {state.get('topic', '')}\n\n"
        f"Structured Insights (dated {TODAY}):\n{insights_text[:20000]}\n\n"
        "Compile these insights into a professional report. Do NOT use any outside knowledge."
    )
    response = get_llm_response(WRITER_SYSTEM_PROMPT, user_prompt, max_tokens=8192)

    if response and not response.startswith("Error"):
        state["draft_report"] = response
    else:
        state["error"] = f"Writer failed: {response}"

    return state
