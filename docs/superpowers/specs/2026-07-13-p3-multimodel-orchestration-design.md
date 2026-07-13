# P3 做实多模型 Agent 编排 Design

**Goal:** 让不同 agent role（writer/critic/humanizer/extraction）可指向不同真实 provider，provider_calls 记录真实 token/latency/cost（回读 API usage 替换写死 ROLE_CALL_METRICS），前端配置改动真落库，router 按 max_cost/能力做真实路由 —— 使"多模型 Agent 编排"从单模型 + 写死指标变成真实可配置编排。

**背景（两份审计确认）**
- REAL：model_profile/assignment 数据结构与 seed、resolve_model_profile 的选择+fallback+structured 校验、后端 configuration 端点（set_model_profile_enabled/update_agent_model_assignment 真落 store）、`_chat`/`_openai_json_completion` 真实 HTTP。
- STUB/缺口：
  1. 所有 role/profile 共用一个 env provider（`NOVELIST_LLM_PROVIDER` 默认 anthropic，两 profile provider_name 相同）；`OpenAICompatibleWritingAdapter` 是空壳 `pass`。无"writer 用 A 家、critic 用 B 家"。
  2. provider_calls 的 token/cost/latency 全来自写死 `ROLE_CALL_METRICS`（phase_two_store.py:74-78），`_chat` 丢弃真实 `usage`。
  3. 前端 ConfigurationPage 的 toggle/update 只改本地 React state（phase-two-provider.tsx:53-62 调 `...InState` reducer），不打后端，刷新即丢。
  4. router 只做 enabled + structured 校验 + 线性 fallback，未用 assignment 的 max_cost/能力做路由决策。
- 附带：critic issue summary 仍硬编码"主角境界描写与已批准设定冲突"（provider_executor.py:220）——本 tranche 顺手清。

**决策（已确认）**
1. 四件全做：多 provider 差异化 + 真实指标 + 前端落库 + cost 路由。
2. 排期：本 tranche 只碰 model_profile/router/provider_calls/前端配置，**完全不碰 deep_analysis**（后台多书隔离任务 task_62457d44 范围）。

---

## Task 1: profile 携带独立 provider 凭证引用 + adapter 差异化

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`（model_profile seed :1227-1248；provider account seed）
- Modify `apps/ai-worker/worker/provider_executor.py`（`_chat` 按 profile 读 env；`_build_provider_adapter`）
- Test `apps/ai-worker/tests/test_provider_executor.py`（追加）

**做法**
- model_profile 增加可选字段 `base_url_env` / `api_key_env`（默认 `NOVELIST_LLM_BASE_URL`/`NOVELIST_LLM_API_KEY`，可指向不同 env 如 `NOVELIST_CRITIC_LLM_BASE_URL`）。seed 保持默认（向后兼容），但结构支持不同 role 指不同 provider。
- `AnthropicWritingAdapter._chat` 改为读 `model_profile.get("base_url_env", "NOVELIST_LLM_BASE_URL")` 对应的 env，而非硬编码 `NOVELIST_LLM_BASE_URL`。无 key 时确定性 fallback 不变。
- `OpenAICompatibleWritingAdapter` 保持继承（endpoint/鉴权已由 profile env 驱动，差异体现在 profile 配置而非子类）。

**验收**
- profile 配 `base_url_env="NOVELIST_CRITIC_LLM_BASE_URL"` → `_chat` 读该 env。
- 默认 profile 行为不变（现有测试绿）。

## Task 2: 真实 provider_calls 指标（回读 usage/latency）

**Files**
- Modify `apps/ai-worker/worker/provider_executor.py`（`_chat` 返回 usage+latency；三 adapter 方法回传；pipeline 更新 provider_calls）
- Modify `apps/core-service/app/core/phase_two_store.py`（`_build_provider_call` 接受真实 metrics 覆盖 ROLE_CALL_METRICS）
- Test `apps/ai-worker/tests/test_provider_executor.py`（追加）

**做法**
- `_chat` 改返回 `dict`：`{"text": str, "prompt_tokens": int, "completion_tokens": int, "latency_ms": int}`（真调时从 `payload["usage"]` + 计时；无 key fallback 时给确定性估算值如按 user 长度）。draft/review/humanize 方法回传这些。
- `execute_writing_provider_pipeline`：收集三段真实 token/latency，更新对应 `provider_calls` 项的 `prompt_tokens/completion_tokens/latency_ms`，`cost_estimate` 由真实 token × 单价（profile 可带 `cost_per_1k` 或用默认单价常量）算，`cost_estimate_status="measured"`。
- `_build_provider_call`：ROLE_CALL_METRICS 保留为无真实数据时的兜底，但接受可选 `measured_metrics` 覆盖。

**验收**
- mock `_chat` 返回带 usage → provider_calls 的 token/latency 是真实值、cost_estimate_status="measured"。
- 无 key → 确定性兜底值，不崩。

## Task 3: 前端配置真落库

**Files**
- Modify `apps/web/src/lib/api-client.ts`（加 configuration 端点方法）
- Modify `apps/web/src/state/phase-two-provider.tsx`（toggle/update 改 POST 后端）
- Modify `apps/web/src/pages.tsx`（ConfigurationPage 用 resolveApiBaseUrl，有 API 时走后端）
- Test `apps/web/src/test/api-client.test.ts`（追加）

**做法**
- api-client 加 `setModelProfileEnabled(id, enabled)` / `updateAgentAssignment(assignmentId, modelProfileId)` / `updateQualityGateProfile(...)`，POST 到 configuration.py 端点。
- phase-two-provider 的 toggleModelProfile 等：apiClient 存在时 POST 后端并用返回的 configuration_snapshot 刷新 state；无 API 时保持现有本地 reducer（demo 兼容）。
- ConfigurationPage 用 resolveApiBaseUrl 判定。

**验收**
- 配 API base → toggle profile POST 后端、用返回快照刷新。
- 无 API → 本地 reducer 行为不变（现有测试绿）。

## Task 4: router 纳入 cost/能力 + 清 critic 硬编码

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`（`resolve_model_profile` :3960 加 max_cost 过滤）
- Modify `apps/ai-worker/worker/provider_executor.py`（:220 critic issue summary 去硬编码）
- Test `apps/core-service/tests/test_phase_two_api.py`、`apps/ai-worker/tests/test_provider_executor.py`

**做法**
- resolve_model_profile：在 fallback 链遍历时，若 assignment 有 `max_cost` 且候选 profile 预估单次成本超限则跳过（用 profile 的 cost_per_1k × 预期 token 估算，或 profile 带 `est_cost` 字段）；保留现有 enabled/structured 过滤。
- critic issue summary（provider_executor.py:220）：改为用真实 critic review 文本（consistency_issues 里的 summary）而非硬编码"主角境界描写..."。

**验收**
- assignment max_cost 极低 → 跳过高成本 profile 走 fallback。
- critic issue summary 反映真实 review，非写死斗破苍穹。

---

## Global Constraints
- 不硬编码任何真实 API 密钥（只存 env 引用名）。
- 无 key 时确定性 fallback，绝不崩。
- HTTP API shape 不变（新增字段向后兼容）；现有 demo（model_profile/assignment/writing seed）测试仍绿。
- **完全不碰 deep_analysis / apply_task_execution_result 的 extraction 落表段 / 多书隔离**（后台任务 task_62457d44 范围）。
- worker 经 load_phase_two_store() 调 core，不新增跨服务 HTTP。
- 每任务 ≤2 迭代 / ~15 分钟。命令用 rtk；core-service 测试用其 .venv；worker 用 rtk python3（无 dramatiq 依赖测试）。跑前后清构建污染。

## Verification
```
cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py -q
cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```
浏览器手验：配置中心 toggle profile → 刷新后仍生效（落库）；配不同 role 的 base_url env → 生成时不同段走不同 provider；provider_calls 指标反映真实 token（配 key 时）。

## Done bar
- 不同 role 可配不同 provider（profile env 引用驱动）。
- provider_calls token/latency/cost 真实（配 key 回读 usage），cost_estimate_status="measured"。
- 前端配置改动 POST 后端、刷新不丢。
- router 纳入 max_cost 路由；critic issue 去硬编码。
- 全量测试绿；现有 demo 测试仍绿；未碰 deep_analysis/多书隔离。

## 排期说明
本 tranche 与后台多书隔离任务 task_62457d44 零冲突（不碰 deep_analysis）。深抽取（pattern/rhythm/expression）留待多书任务合并后单独做，因其落表进 deep_analysis 区域。
