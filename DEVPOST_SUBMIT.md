# DevPost 提交页 · 逐字段粘贴包（MedReg Agent）

> 每个字段直接复制粘贴。英文为评委可见文案；中文只是给你的标注。
> 提交入口：https://agentsforhumans.devpost.com → Your Submissions → Edit
> 死线：**北京 2026-09-15 08:00**。

---

## 1. Project Name（项目名）
```
MedReg Agent
```

## 2. Tagline / Elevator Pitch（一句话，≤200 字符）
```
A Strands-powered AI agent that monitors NMPA/FDA/MDR/PMDA regulatory updates, classifies their impact, and drafts follow-up memos — turning weeks of manual compliance watching into one command.
```

## 3. Inspiration（受什么启发写的）
```
Medical-device regulatory teams must track four or more jurisdictions (NMPA, FDA, EU MDR, PMDA) at once. A single missed change — a tighter endotoxin threshold, a new UDI requirement — can stall a product launch for months. Small manufacturers and clinics have no dedicated intelligence function; monitoring is done by hand, in spreadsheets, after work hours. We built the agent we wished existed: one command, auditable output, every region covered.
```

## 4. What it does（它做什么 —— 必交项①核心）
```
MedReg Agent is a professional agent built on the Strands Agents SDK that automates the repetitive, high-judgment work of medical-device regulatory monitoring:

1. Regulatory Watchdog (reg-watch) — fetches the latest regulatory updates across NMPA / FDA / EU MDR / PMDA, classifies each update's business impact (HIGH / MEDIUM / LOW) using region-aware keyword rules, and drafts a follow-up memo for the highest-impact item with recommended actions, owner, and due date.

2. Submission Readiness (submission-ready) — checks a device submission package against a required checklist (IFU, label, test report, UDI, cybersecurity), reports coverage percentage, and lists exactly what is missing and how to fix it.

3. Clinic Compliance (clinic-compliance) — alerts clinics on equipment inventory approaching sterilization/revalidation thresholds, so small clinics without a compliance officer stay safe.

All three personas share one Strands codebase and switch via a single --profile flag. The agent autonomously chains tool calls (fetch → classify → draft) and produces auditable, structured output.
```

## 5. How we built it（怎么构建的）
```
- Strands Agents SDK (v1.54.0) for the agent loop, tool decoration (@tool), and model abstraction.
- Pluggable model backends via Strands: Amazon Bedrock (Claude) for production, and a local OllamaModel for zero-cost development and offline demos — the same code runs on both.
- Pure-Python deterministic tools: fetch_regulatory_updates, classify_impact, draft_followup_memo, check_submission_readiness, clinic_inventory_alert — every tool returns structured JSON so the agent's decisions are auditable.
- Profile system: one codebase, three personas, selected at runtime (--profile reg-watch | submission-ready | clinic-compliance).
- MIT-licensed public repo with architecture diagram and a runnable demo: python src/agent.py --profile reg-watch --demo
```

## 6. Challenges we ran into / Accomplishments（可选加分字段）
```
Challenge: keeping the agent's judgment auditable — we solved it by making every tool deterministic and returning structured JSON, so a human reviewer can trace exactly why an update was classified HIGH.
Accomplishment: one codebase serving three distinct professional personas, and a model-agnostic design that runs on Amazon Bedrock in production and fully offline on local Ollama for demo and privacy-sensitive clinics.
```

## 7. Built With（技术标签，DevPost 复选/输入）
```
Strands Agents SDK
Amazon Bedrock
Python
Ollama
AI Agent
Healthcare
Regulatory Compliance
```

## 8. GitHub Repository URL（仓库）
```
https://github.com/zhaoxinghua09-cell/aws-agents-for-humans
```
> 提交前检查仓库 About 一栏：DevPost 要求 License 显示 MIT 或 Apache。到仓库页 → About 右上齿轮 → License 勾选 MIT → Save。若 GitHub 尚未自动识别，手动勾一次。

## 9. Demo Video（≤5 分钟，必交项④）
- 上传 YouTube/Vimeo 后把链接填进 DevPost「Demo video」字段。
- 分镜脚本见 `SUBMISSION.md` 第 4 节（0:00 问题+用户 → 0:40 实跑 reg-watch → 1:30 第二画像 → 2:30 架构图 → 3:30 Strands/Bedrock 说明 → 4:30 收尾）。
- 实跑命令（录屏用）：
```
cd D:\Workbuddy\2026-09-08-19-59-19\aws-agents-for-humans
set OLLAMA_MODEL=qwen3.5:4b
python src\agent.py --profile reg-watch --demo
python src\agent.py --profile submission-ready --demo
python src\agent.py --profile clinic-compliance --demo
```

## 10. Architecture Diagram（必交项③）
- 上传文件：`architecture_diagram.svg`（仓库根目录已含）。

## 11. AWS Builder ID（必交项⑤）
- ✅ 已建（09-08）。DevPost 表单如需填写，用你建 Builder ID 的邮箱。

## 提交前 30 秒终检
- [ ] 视频 ≤5:00、能公开访问（unlisted 也行）
- [ ] 仓库 About 显示 MIT License
- [ ] 地区填 **China (Mainland)**（勿选 Hong Kong！）
- [ ] Team 一栏单人（或删掉多余成员）
- [ ] 全部 REQUIRED 字段无空
