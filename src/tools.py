"""Custom tools for the MedReg Agent (Strands Agents SDK).

Each tool is a plain Python function decorated with ``@tool`` so Strands can
discover its schema automatically. Tools are deterministic and run offline
(no LLM required), which makes the agent's output auditable — exactly what
regulatory work demands.
"""
from __future__ import annotations

import datetime as _dt
import json
import urllib.error
import urllib.request
from pathlib import Path

from strands.tools import tool

DATA_PATH = Path(__file__).parent / "data" / "sample_updates.json"

_OPENFDA = "https://api.fda.gov/device/recall.json"

_HIGH = {"endotoxin", "validation", "cybersecurity", "510k", "udi",
         "recertification", "sterilization", "reprocess", "sterility",
         "contamination", "high-priority"}
_MED = {"template", "labeling", "accreditation", "digital signature", "class"}

# Live-fetched records are registered here so downstream tools
# (classify_impact / draft_followup_memo) can resolve their ids.
_CACHE: dict[str, dict] = {}

# Diagnostic: reason the last live openFDA fetch failed ("" when healthy).
LAST_LIVE_ERROR = ""


def _load_updates() -> list[dict]:
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))["updates"]
    except Exception:
        return []


def _fetch_fda_live(since_days: int = 30, limit: int = 5) -> list[dict]:
    """Fetch real medical-device recalls from the openFDA public API.

    No API key required. openFDA answers HTTP 404 when ZERO records match the
    window (recall posting lags behind real events), so empty recent windows
    are handled by widening up to 90 days. Returns [] on real failures so the
    bundled demo corpus can serve as an offline fallback.
    """
    global LAST_LIVE_ERROR
    LAST_LIVE_ERROR = ""
    window = max(int(since_days), 1)
    today = _dt.date.today()
    payload = None
    for _ in range(3):
        begin = (today - _dt.timedelta(days=window)).isoformat()
        end = today.isoformat()
        url = (
            f"{_OPENFDA}?search=event_date_initiated:%5B{begin}+TO+{end}%5D"
            f"&sort=event_date_initiated:desc&limit={limit}"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "medreg-agent/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                payload = json.loads(resp.read())
            break
        except urllib.error.HTTPError as e:
            if e.code == 404 and window < 90:
                LAST_LIVE_ERROR = f"no recalls posted in last {window}d; widening window"
                window = min(window * 4, 90)
                continue
            LAST_LIVE_ERROR = f"HTTP {e.code} (window={window}d)"
            return []
        except Exception as e:
            LAST_LIVE_ERROR = f"{type(e).__name__}: {e}"
            return []
    if payload is None:
        return []
    LAST_LIVE_ERROR = ""  # live fetch succeeded; do not leak stale widening notes
    out: list[dict] = []
    for r in payload.get("results", []):
        cls = r.get("classification") or ""
        rec_id = r.get("product_res_number") or f"FDA-{r.get('res_event_number', 'unknown')}"
        parts = [
            f"Status: {r.get('recall_status', 'n/a')}.",
            f"Reason: {r.get('reason_for_recall', 'n/a')}",
            f"Recalling firm: {r.get('recalling_firm', 'n/a')}.",
        ]
        if r.get("code_info"):
            parts.append(f"Codes: {str(r['code_info'])[:120]}")
        detail_url = ""
        if r.get("cfres_id"):
            detail_url = ("https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/"
                          f"cfres/detail.cfm?ID={r['cfres_id']}")
        out.append({
            "id": rec_id,
            "region": "FDA",
            "date": r.get("event_date_initiated", ""),
            "title": f"{cls + ' ' if cls else ''}recall: "
                     f"{str(r.get('product_description', ''))[:90]}".strip(),
            "summary": " ".join(parts),
            "url": detail_url,
            "tags": ["recall"] + (["high-priority"] if cls == "Class I" else []),
            "source": "openFDA (live)",
        })
    return out


@tool
def fetch_regulatory_updates(regions: str = "all", since_days: int = 30) -> dict:
    """Fetch recent medical-device regulatory updates.

    FDA records are fetched LIVE from the openFDA public API (real device
    recalls, no API key needed). Other regions come from a bundled demo
    corpus, which also serves as the offline fallback when the network is
    unavailable — so the demo always runs.

    Args:
        regions: Comma-separated regions to filter, e.g. "NMPA,FDA". Use "all" for everything.
        since_days: Return only FDA recalls initiated within this many days.

    Returns:
        dict: {"count": int, "updates": list} of normalized update records.
    """
    try:
        since_days = int(since_days)
    except (TypeError, ValueError):
        since_days = 30
    wanted = None
    if regions and regions.lower() != "all":
        wanted = {r.strip().lower() for r in regions.split(",")}
    updates: list[dict] = []
    if wanted is None or "fda" in wanted:
        for rec in _fetch_fda_live(since_days):
            _CACHE[rec["id"]] = rec
            updates.append(rec)
    live_fda = bool(updates)  # non-empty means the live openFDA fetch succeeded
    for u in _load_updates():
        if u["id"] in _CACHE:
            continue
        if live_fda and "fda" in u["region"].lower():
            continue  # live openFDA data supersedes the bundled FDA sample
        updates.append(u)
    if wanted is not None:
        updates = [u for u in updates if any(w in u["region"].lower() for w in wanted)]
    result = {"count": len(updates), "updates": updates}
    if LAST_LIVE_ERROR:
        result["live_source_error"] = (
            "openFDA unreachable, serving bundled demo corpus — " + LAST_LIVE_ERROR
        )
    return result


@tool
def classify_impact(update_id: str) -> dict:
    """Classify the business impact of a regulatory update by id.

    Args:
        update_id: The id of the update, e.g. "NMPA-2026-0881".

    Returns:
        dict: {"impact": "high|medium|low", "rationale": str, "suggested_action": str}
    """
    updates = _load_updates()
    u = _CACHE.get(update_id) or next((x for x in updates if x["id"] == update_id), None)
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
    u = _CACHE.get(update_id) or next((x for x in updates if x["id"] == update_id), None)
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
