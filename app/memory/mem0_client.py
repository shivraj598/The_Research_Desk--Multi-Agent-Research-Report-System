import os
from typing import Optional

from mem0 import Memory

_memory: Optional[Memory] = None


def get_memory() -> Memory:
    global _memory
    if _memory is None:
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY not set in environment")
        _memory = Memory(api_key=api_key)
    return _memory


def store_context(session_id: str, role: str, content: str) -> None:
    mem = get_memory()
    mem.add(content, user_id=session_id, metadata={"role": role})


def get_context(session_id: str, query: str) -> str:
    mem = get_memory()
    results = mem.search(query, user_id=session_id)
    if not results:
        return ""
    return "\n".join(r.get("text", "") for r in results)
