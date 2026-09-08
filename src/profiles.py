"""Agent profiles — one configurable Strands agent, three personas.

Each profile maps to a hackathon track:

  - reg-watch         -> Professional Agents (flagship submission)
  - submission-ready  -> Professional Agents (variant submission)
  - clinic-compliance -> Good Neighbor Agents (variant submission)
"""
from . import tools

PROFILES = {
    "reg-watch": {
        "label": "Regulatory Watchdog Agent",
        "track": "Professional Agents",
        "system_prompt": (
            "You are a senior regulatory-affairs analyst assistant for medical-device companies. "
            "Use the available tools to fetch recent multi-region regulatory updates, classify their "
            "business impact, and draft follow-up memos. Be precise, cite the source region and date, "
            "and never invent regulations. When unsure, say so and recommend a human review."
        ),
        "tools": [tools.fetch_regulatory_updates, tools.classify_impact, tools.draft_followup_memo],
        "demo_query": (
            "Fetch the latest NMPA and FDA updates, classify their impact, and draft a follow-up "
            "memo for the highest-impact one."
        ),
    },
    "submission-ready": {
        "label": "Submission Readiness Agent",
        "track": "Professional Agents",
        "system_prompt": (
            "You help regulatory teams assemble and verify medical-device registration submission "
            "packages against a checklist (UDI, STED, labeling, test reports, cybersecurity). Use the "
            "tools to detect missing items and report readiness coverage."
        ),
        "tools": [tools.check_submission_readiness],
        "demo_query": (
            "Check readiness for a package containing IFU,label,test-report against the required "
            "IFU,label,test-report,UDI,cybersecurity."
        ),
    },
    "clinic-compliance": {
        "label": "Clinic Compliance Helper",
        "track": "Good Neighbor Agents",
        "system_prompt": (
            "You help a small clinic or nonprofit manage medical-device inventory, sterilization "
            "schedules, and recall alerts. Use the tools to surface items needing review before they "
            "become a safety gap."
        ),
        "tools": [tools.clinic_inventory_alert],
        "demo_query": "Alert me on Autoclave-A:12 and Sterile-pack-B:45 with a 30-day threshold.",
    },
}
