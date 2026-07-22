from app.llm import get_llm_response
from app.state import AppState

WRITER_SYSTEM_PROMPT = """You are a professional Report Writer. Your job is to compile structured research insights into a cohesive, well-formatted report.

The report should include:
1. Title
2. Executive Summary (2-3 paragraphs)
3. Main sections with headings (one per subtask)
4. Conclusion
5. Sources/References section

Format the report in Markdown with proper headings, bullet points, and emphasis where appropriate.

CRITICAL RULES:
- Write in a professional, objective tone
- Use the provided insights as your sole source of information
- Cite sources inline where possible
- The report should be comprehensive but readable
- Do not fabricate information not present in the insights"""


def writer_agent(state: AppState) -> AppState:
    insights_text = ""
    for subtask in state.subtasks:
        items = state.insights.get(subtask, [])
        if not items:
            continue
        insights_text += f"\n\n## Subtask: {subtask}\n"
        for item in items:
            if "analysis" in item:
                insights_text += item["analysis"] + "\n"
            elif "error" in item:
                insights_text += f"[No insights available: {item['error']}]\n"

    user_prompt = (
        f"Report Topic: {state.topic}\n\n"
        f"Structured Insights:\n{insights_text[:20000]}\n\n"
        "Compile these insights into a professional, well-formatted report following the guidelines."
    )
    response = get_llm_response(WRITER_SYSTEM_PROMPT, user_prompt, max_tokens=8192)

    if response and not response.startswith("Error"):
        state.draft_report = response
    else:
        state.error = f"Writer failed: {response}"

    return state
