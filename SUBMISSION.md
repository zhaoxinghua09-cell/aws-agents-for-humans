# Submission Package — MedReg Agent (AWS Agents for Humans)

> Maps directly to the DevPost "What to Submit" requirements. Deadline:
> **Sep 15, 2026 @ 7:00am GMT+7 = Beijing 09-15 08:00**.

## 1. Text description (REQUIRED)

**What it does**
MedReg Agent is a Strands-powered professional agent that automates the
repetitive, high-judgment monitoring work of medical-device regulatory teams.
It fetches multi-region regulatory updates (NMPA / FDA / EU MDR / PMDA),
classifies each update's business impact, and drafts a follow-up memo — in one
command. Two companion personas cover submission-readiness checking and clinic
inventory/compliance alerting from the same codebase.

**Who it is for**
Regulatory-affairs professionals and small medical-device exporters who must
track 4+ jurisdictions but lack a dedicated intelligence function. The
Good-Neighbor persona serves small clinics and nonprofits.

**Why it matters**
A single missed regulatory change (e.g., a tighter endotoxin threshold, a new
UDI rule) can stall a product for months. Manual monitoring is slow and
error-prone. MedReg makes it a one-command, auditable agent — turning
background drudgery into actionable memos.

## 2. Public code repo (REQUIRED)
- Repo URL: **https://github.com/zhaoxinghua09-cell/aws-agents-for-humans** ✅ (pushed 09-08)
- Must show **MIT** (or Apache) license in the About section — ✅ verified `license: MIT`.
- Must include **README** — ✅ `README.md` present with run instructions.

## 3. Architecture Diagram (REQUIRED)
- File: `architecture_diagram.svg` (submission-ready, light-theme).

## 4. Demo video ≤ 5 min (REQUIRED)
Pitch must cover: (1) problem, (2) target user, (3) why it matters.
Suggested script:
1. **0:00–0:40** Problem + user: "Regulatory teams track 4+ jurisdictions by hand…"
2. **0:40–1:30** Live run: `python src/agent.py --profile reg-watch --demo` → show memos.
3. **1:30–2:30** Show a second persona (`submission-ready` / `clinic-compliance`).
4. **2:30–3:30** Architecture walk-through (the SVG).
5. **3:30–4:30** Why it matters + how Strands + Bedrock/AgentCore strengthen it.
6. **4:30–5:00** Close: one command, auditable output, real impact.

## 5. AWS Builder ID (REQUIRED)
- ✅ Created 2026-09-08. (Guide: `AWS_SETUP.md`.)

## 6. Optional (strengthens score)
- Live demo link (deploy on Bedrock AgentCore).
- Builder Center article titled "Agents for Humans" documenting the build.

## Pre-submit checklist
- [ ] DevPost account created + hackathon joined
- [ ] AWS Builder ID created
- [ ] Repo public, MIT license shown in About, README present
- [ ] `architecture_diagram.svg` attached
- [ ] Demo video (≤5 min) recorded + uploaded
- [ ] Description (problem/user/why) pasted
- [ ] (Optional) Bedrock AgentCore live demo deployed
- [ ] (Optional) Builder Center article published
