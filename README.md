# MedReg Agent — Strands-powered Professional Agent for Medical-Device Regulatory Teams

> Submission for the **AWS Agents for Humans Hackathon** (Professional Agents track).
> Built with the **Strands Agents SDK** (required technology).

A single configurable Strands agent with three personas (one codebase → multiple submissions if desired):

| Profile | Persona | Track | What it does |
|---|---|---|---|
| `reg-watch` (flagship) | Regulatory Watchdog | Professional Agents | Monitors multi-region regulatory updates (NMPA/FDA/MDR/PMDA), classifies business impact, drafts follow-up memos |
| `submission-ready` | Submission Readiness | Professional Agents | Checks registration packages against a checklist (UDI/STED/labeling/cybersecurity), reports readiness |
| `clinic-compliance` | Clinic Compliance Helper | Good Neighbor Agents | Flags clinic inventory / sterilization / recall items needing review |

**Tools are deterministic and run offline** (no LLM required), so the agent's output is auditable — exactly what regulatory work demands.

## Why it matters
Regulatory-affairs teams drown in manual monitoring across 4+ jurisdictions. A single missed update (e.g., a tighter endotoxin threshold for implanted orthopedic devices) can stall a product for months. MedReg turns that repetitive, high-judgment work into a one-command agent.

## Quick start
```bash
pip install -r requirements.txt

# Local dev with Ollama (zero AWS cost) — point at your local model
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=qwen3.5:latest
python src/agent.py --profile reg-watch --demo

# Production on AWS Bedrock (for submission / AgentCore deployment)
export AWS_REGION=us-east-1
export BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
python src/agent.py --profile reg-watch --demo
```

## Architecture
See `architecture_diagram.svg`.

## License
MIT — see `LICENSE`.
