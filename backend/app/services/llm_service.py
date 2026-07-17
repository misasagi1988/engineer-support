import json
import logging
import re

import httpx

logger = logging.getLogger(__name__)

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

CASE_GENERATION_PROMPT = """You are converting a resolved ops ticket into a knowledge base case.
Given the following information, produce a well-structured case draft.

Module: {module}
Problem description: {description}
Identified root cause: {root_cause}
Solution applied: {solution}

Return JSON with these fields:
- title: concise case title (e.g. "XX module reports YY error in ZZ deployment mode")
- root_cause: clear root cause analysis
- solution: step-by-step solution
- troubleshooting_path: array of {{step: string, description: string}} capturing the key diagnostic steps
- tags: array of relevant keyword tags (3-8 items)

Return JSON only.
"""


def _extract_json(text: str) -> dict | None:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Try direct parse first
    text_stripped = text.strip()
    try:
        return json.loads(text_stripped)
    except json.JSONDecodeError:
        pass
    # Try to extract from ```json ... ``` block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text_stripped, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    # Try to find any top-level JSON object
    match = re.search(r"\{.*\}", text_stripped, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


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
            parsed = _extract_json(content)
            if parsed is None:
                return _fallback_keyword_match(description, modules, versions)
            return parsed
    except Exception:
        logger.exception("LLM analyze_problem failed, using fallback")
        return _fallback_keyword_match(description, modules, versions)


async def generate_case_from_ticket(
    description: str,
    root_cause: str,
    solution: str,
    module_name: str = "",
) -> dict:
    """Call LLM to generate a knowledge base case draft from a resolved ticket."""
    fallback = {
        "title": f"Case from ticket: {description[:50]}",
        "root_cause": root_cause,
        "solution": solution,
        "troubleshooting_path": [],
        "tags": [],
    }
    if not settings.LLM_API_KEY:
        return fallback
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{settings.LLM_API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {settings.LLM_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": settings.LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": CASE_GENERATION_PROMPT.format(
                            module=module_name,
                            description=description,
                            root_cause=root_cause,
                            solution=solution,
                        )},
                        {"role": "user", "content": "Generate the case draft."},
                    ],
                    "temperature": 0.3,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            parsed = _extract_json(content)
            if parsed is None:
                return fallback
            # Ensure all expected keys exist
            parsed.setdefault("title", fallback["title"])
            parsed.setdefault("root_cause", root_cause)
            parsed.setdefault("solution", solution)
            parsed.setdefault("troubleshooting_path", [])
            parsed.setdefault("tags", [])
            return parsed
    except Exception:
        logger.exception("LLM generate_case_from_ticket failed, using fallback")
        return fallback


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
