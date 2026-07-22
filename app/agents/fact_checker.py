from app.llm import get_llm_response


FACT_CHECKER_SYSTEM_PROMPT = """You are a Fact-Checker. Your job is to verify every claim in the draft report against the original sourced content.

For each claim in the report, determine one of:
- ✅ SUPPORTED: The claim is clearly supported by the sources
- ⚠️ UNSUPPORTED: The claim is not found in or cannot be verified by the sources
- ❌ CONTRADICTED: The claim contradicts the source material

For each UNSUPPORTED or CONTRADICTED claim, provide:
1. The exact claim from the report
2. Why it is unsupported/contradicted
3. The correct information (if available in sources)
4. A suggested correction or annotation"""


def fact_checker_agent(state: dict) -> dict:
    draft_report = state.get("draft_report", "")
    if not draft_report:
        state["error"] = "No draft report to fact-check"
        return state

    raw_sources_text = ""
    for subtask, sources in state.get("raw_sources", {}).items():
        raw_sources_text += f"\n--- {subtask} ---\n"
        for s in sources:
            content = s.get("content", "")
            if content:
                raw_sources_text += f"Source ({s.get('url', 'unknown')}): {content[:2000]}\n"

    user_prompt = (
        f"Original Sources:\n{raw_sources_text[:25000]}\n\n"
        f"Draft Report to Fact-Check:\n{draft_report[:15000]}\n\n"
        "Check every claim in the report against the sources. List all UNSUPPORTED and CONTRADICTED claims with explanations and suggested corrections."
    )
    response = get_llm_response(FACT_CHECKER_SYSTEM_PROMPT, user_prompt, max_tokens=4096)

    if response and not response.startswith("Error"):
        state["fact_check_results"] = [{"check": response}]
    else:
        state["fact_check_results"] = [{"error": response or "Fact-checking failed"}]

    return state
