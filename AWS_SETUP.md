# AWS Setup Guide — Agents for Humans Hackathon

> 你目前 AWS 账户 + Builder ID 都没有。以下步骤按**阻塞优先级**排序：
> **最优先 = 建 Builder ID（5 分钟，提交必填）+ 本机 Ollama 跑通代码**。
> 只有「部署到 Bedrock AgentCore 拿技术分」才需要完整 AWS 账户。

---

## ⚠️ 资格提醒（先读）
- 官网排除名单含 **Hong Kong（香港）**、新加坡、马来西亚、泰国、越南、阿联酋等，
  **中国大陆不在排除列表 → 你以「中国大陆居民」身份参赛合规**。
- 注册 DevPost / 填表时地区务必选 **China (Mainland)**，**别选 Hong Kong**。

---

## Step 1 — 创建 AWS Builder ID（强制 · 提交必填）
约 5 分钟，免费，只需邮箱。
1. 打开 https://aws.amazon.com/builder-id/
2. 点 **Create an AWS Builder ID** / **Get started**
3. 输入常用邮箱（用你注册 Builder ID 所用的邮箱；本仓库不记录任何具体邮箱）
4. 收验证邮件 → 点链接 → 设密码 → 完成
5. **记下这个 Builder ID（提交表单时要填）**

> Builder ID 是 AWS Builder Center 的身份，和下面的 AWS 控制台账户是两回事。
> 本项目里它只作为提交必填字段出现。

## Step 2 — 创建 AWS 账户（仅当你要部署 Bedrock AgentCore 拿技术分）
纯本地开发/Ollama 跑通**不需要** AWS 账户，可暂缓。
1. 打开 https://aws.amazon.com/ → **Create an AWS Account**
2. root 邮箱（可与 Builder ID 同邮箱）→ 手机验证 → 填**支付方式**（信用卡，用于实名+扣费；
   本活动有 $50 credits + 免费层，建议设**预算告警**）
3. 选 **Basic** 支持计划（免费）
4. 登录后到 **IAM** → 建一个 **IAM 用户（Programmatic access）** 拿 Access Key
   —— **绝不用 root key 做本地配置**
5. 开 **Bedrock**：进入 Amazon Bedrock 控制台 → 选区域（如 `us-east-1`）→
   **Model access** → 申请 Claude / Amazon Nova 模型访问（审批通常即时~几分钟）

## Step 3 — 申请 $50 AWS credits（Resources 标签页）
1. 登录 DevPost → 进入 https://agentsforhumans.devpost.com → 已 Join
2. 点 **Resources** 标签 → 填 $50 credits 申请表（需 DevPost 账号 + 已 join）

## Step 4 — 本地配置（部署 AgentCore 时才需要）
```bash
# 用 IAM 用户 key（不是 root）
aws configure   # Access Key / Secret / region=us-east-1
# 然后按 README 用 AWS_REGION 环境变量跑 Bedrock 模式
```

---

## 关键路径（Critical Path）
| 优先级 | 动作 | 谁做 | 耗时 |
|---|---|---|---|
| 🔴 P0 | 建 AWS Builder ID | 你 | 5 min |
| 🔴 P0 | 本机 Ollama 跑通 `reg-watch` demo | 我+你 | 30 min |
| 🟠 P1 | 录 ≤5min 演示视频 | 你 | 1 h |
| 🟠 P1 | 画架构图 + 写描述（已就绪） | 我 | done |
| 🟡 P2 | 建 AWS 账户 + Bedrock 访问（冲技术分） | 你 | 30 min |
| 🟡 P2 | 部署 Bedrock AgentCore 实时 demo（选交但加分） | 我+你 | 1 h |
| 🟡 P2 | 发 Builder Center 文章（加分） | 你 | 1 h |

**结论**：今天最该做的就一件——**开浏览器建 Builder ID**，同时我把代码在你本机 Ollama 上跑通验证。
