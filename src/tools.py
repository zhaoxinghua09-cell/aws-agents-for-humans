"""Custom tools for the MedReg Agent (Strands Agents SDK).

Each tool is a plain Python function decorated with ``@tool`` so Strands can
discover its schema automatically. Tools are deterministic and run offline
(no LLM required), which makes the agent's output auditable — exactly what
regulatory work demands.
"""
from __future__ import annotations

import json
from pathlib import Path

from strands.tools import tool

DATA_PATH = Path(__file__).parent / "data" / "sample_updates.json"

_HIGH = {"endotoxin", "validation", "cybersecurity", "510k", "udi",
         "recertification", "sterilization", "reprocess"}
_MED = {"template", "labeling", "accreditation", "digital signature", "class"}


def _load_updates() -> list[dict]:
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))["updates"]
    except Exception:
        return []


@tool
def fetch_regulatory_updates(regions: str = "all", since_days: int = 30) -> dict:
    """Fetch recent medical-device regulatory updates.

    Args:
        regions: Comma-separated regions to filter, e.g. "NMPA,FDA". Use "all" for everything.
        since_days: Return only updates newer than this many days (ignored for the bundled demo corpus).

    Returns:
        dict: {"count": int, "updates": list} of normalized update records.
    """
    updates = _load_updates()
    if regions and regions.lower() != "all":
        wanted = {r.strip().lower() for r in regions.split(",")}
        updates = [u for u in updates if any(w in u["region"].lower() for w in wanted)]
    return {"count": len(updates), "updates": updates}


@tool
def classify_impact(update_id: str) -> dict:
    """Classify the business impact of a regulatory update by id.

    Args:
        update_id: The id of the update, e.g. "NMPA-2026-0881".

    Returns:
        dict: {"impact": "high|medium|low", "rationale": str, "suggested_action": str}
    """
    updates = _load_updates()
    u = next((x for x in updates if x["id"] == update_id), None)
    if not u:
        return {"impact": "unknown", "rationale": f"No update with id {update_id}",
                "suggested_action": "verify id"}
    blob = (u["title"] + " " + u["summary"] + " " + " ".join(u.get("tags", []))).lower()
    if any(k in blob for k in _HIGH):
        impact, action = "high", "Schedule cross-functional review; update SOP/validation plan within 30 days."
    elif any(k in blob for k in _MED):
        impact, action = "medium", "Assign to regulatory owner; track in submission calendar."
    else:
        impact, action = "low", "File for awareness; no immediate action."
    return {"impact": impact, "rationale": f"Matched keywords in {u['region']} update.",
            "suggested_action": action}


@tool
def draft_followup_memo(update_id: str) -> dict:
    """Draft a follow-up memo for a regulatory update.

    Args:
        update_id: The id of the update, e.g. "FDA-2026-3340".

    Returns:
        dict: {"subject": str, "body": str} ready-to-send memo.
    """
    updates = _load_updates()
    u = next((x for x in updates if x["id"] == update_id), None)
    if not u:
        return {"subject": "Not found", "body": ""}
    impact = classify_impact(update_id)
    subject = f"[RegWatch] {u['region']} — {u['title']}"
    body = (
        f"Source: {u['region']} ({u['date']})\n"
        f"Link: {u.get('url', '')}\n\n"
        f"Summary:\n{u['summary']}\n\n"
        f"Impact: {impact['impact'].upper()}\n"
        f"Recommended action: {impact['suggested_action']}\n\n"
        f"Owner: ___   Due: ___\n"
    )
    return {"subject": subject, "body": body}


@tool
def check_submission_readiness(package_items: str, required_items: str) -> dict:
    """Check a submission package for missing required items.

    Args:
        package_items: Comma-separated items already in the package, e.g. "IFU,label,test-report".
        required_items: Comma-separated required checklist items, e.g. "IFU,label,test-report,UDI,cybersecurity".

    Returns:
        dict: {"missing": list, "ready": bool, "coverage": float}
    """
    have = {i.strip().lower() for i in package_items.split(",") if i.strip()}
    need = [i.strip() for i in required_items.split(",") if i.strip()]
    missing = [i for i in need if i.lower() not in have]
    coverage = round((len(need) - len(missing)) / len(need), 2) if need else 1.0
    return {"missing": missing, "ready": len(missing) == 0, "coverage": coverage}


@tool
def clinic_inventory_alert(items: str, threshold_days: int = 30) -> dict:
    """Flag clinic inventory / sterilization items needing attention.

    Args:
        items: Comma-separated "name:days_until_review" pairs, e.g. "Autoclave-A:12,Sterile-pack-B:45".
        threshold_days: Flag items with fewer than this many days until review.

    Returns:
        dict: {"alerts": list, "count": int}
    """
    alerts = []
    for pair in items.split(","):
        if ":" not in pair:
            continue
        name, _, days = pair.partition(":")
        try:
            d = int(days.strip())
        except ValueError:
            continue
        if d <= threshold_days:
            alerts.append({"item": name.strip(), "days_left": d,
                           "action": "Schedule review / reorder"})
    return {"alerts": alerts, "count": len(alerts)}
