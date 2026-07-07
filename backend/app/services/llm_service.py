import json

import httpx

from app.config import settings

SYSTEM_PROMPT = """You are an ops assistant. Given a problem description, identify:
1. module_candidates: list of {module_name, confidence} matching known modules
2. version_candidates: list of {version, confidence} from the text
3. deploy_mode_hints: detected deployment mode (standalone/ha/cluster/hierarchical) or null
4. root_cause_candidates: list of {description, keywords, confidence}

Available modules: {modules}
Available versions: {versions}

Return JSON only.
"""


async def analyze_problem(description: str, modules: list[str], versions: list[str]) -> dict:
    if not settings.LLM_API_KEY:
        return _fallback_keyword_match(description, modules, versions)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{settings.LLM_API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {settings.LLM_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": settings.LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT.format(modules=modules, versions=versions)},
                        {"role": "user", "content": description},
                    ],
                    "temperature": 0.1,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
    except Exception:
        return _fallback_keyword_match(description, modules, versions)


def _fallback_keyword_match(description: str, modules: list[str], versions: list[str]) -> dict:
    desc_lower = description.lower()
    module_candidates = [{"module": m, "confidence": 0.5} for m in modules if m.lower() in desc_lower]
    version_candidates = [{"version": v, "confidence": 0.5} for v in versions if v in description]
    return {
        "module_candidates": module_candidates,
        "version_candidates": version_candidates,
        "deploy_mode_hints": None,
        "root_cause_candidates": [],
    }
