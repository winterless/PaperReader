# Implicit Intelligence (arXiv:2602.20424) — 单篇深度阅读评论

**来源论文**: `papers/agent/2026_implicit_intelligence_evaluating_agents_on_what_users_dont_say.md`

---

## 1) 结论：核心贡献（3 个）

1. **Implicit Intelligence 评估框架**：提出显式指令遵循之外的评估维度——agent 能否识别、推理并满足用户期望但未明说的需求。四类：Implicit Reasoning（上下文推断未陈述目标）、Catastrophic Risk（避免不可逆操作）、Privacy & Security（尊重敏感边界）、Accessibility（适配可发现的无障碍需求）。

2. **Agent-as-a-World (AaW)**：用人类可读的 YAML 定义交互世界，由 LLM 作为 World Model 模拟环境；无需额外基础设施，World Model 为确定性执行器（行为由 YAML 的 returns 字段完全指定），避免主观解释。支持可扩展的场景创建与评估。

3. **基准与实证发现**：205 个场景（基于 iOS Shortcuts 303 动作），16 个模型评估。最佳模型 GPT-5.2-pro 仅 48.3% 场景通过率；三大失败模式：环境探索不足、功能配置不完整、状态保持不当（临时/永久变更混淆）。模型迭代非单调（如 GPT-5 > GPT-5.1/5.2），DeepSeek-R1 弱于 V3p1。

---

## 2) 依据：逐条证据

- **贡献 1（四类定义）**  
  [source: `inbox/md_converted/2602.20424.md` -> ## 3.1 EvaluationCategories]  
  "We organize implicit requirements into four categories... ImplicitReasoning... CatastrophicRisk... PrivacyandSecurity... Accessibility"

- **贡献 1（与显式智能对比）**  
  [source: `inbox/md_converted/2602.20424.md` -> ## 3 The Implicit Intelligence Framework]  
  "We define implicit intelligence as an agent's capacity to identify, reason about, and satisfy requirements that users expect but never explicitly state. This contrasts with explicit intelligence, the ability to follow well-specified instructions"

- **贡献 2（AaW 范式）**  
  [source: `inbox/md_converted/2602.20424.md` -> ## 4 Agent-as-a-World]  
  "We introduce Agent-as-a-World (AaW)... environments are specified declaratively in human-readable YAML files and delegates simulation to a capable language model... The World Model's role is strictly constrained: it does not generate arbitrary environmental feedback... It is a deterministic executor of pre-specified action semantics"

- **贡献 2（World Model 一致性）**  
  [source: `inbox/md_converted/2602.20424.md` -> ## 7.2 WorldModelSelection]  
  "Claude Opus 4.5 achieved the highest consistency (98.6%) and was selected as the fixed World Model"

- **贡献 3（48.3% 与失败模式）**  
  [source: `inbox/md_converted/2602.20424.md` -> ## 7.1 MainResults]  
  "Even the best-performing model, GPT-5.2-pro, achieves only 48.3% SPR... Three patterns emerge: (1) insufficient environmental exploration; (2) incomplete feature configuration; (3) inadequate state preservation"

- **贡献 3（非单调与 R1 弱于 V3）**  
  [source: `inbox/md_converted/2602.20424.md` -> Table 2, ## 7.1]  
  "GPT-5 outperforms both its predecessor (GPT-4.1) and immediate successors (GPT-5.1, GPT-5.2)... DeepSeek's reasoning-focused R1 underperforms their general-purpose V3p1 on this benchmark (22.4% vs 27.3% SPR)"

- **贡献 3（数据集规模）**  
  [source: `inbox/md_converted/2602.20424.md` -> ## 5.5 DatasetStatistics, Table 1]  
  "205 scenarios... ImplicitReasoning 70 (34%), CatastrophicRisk 56 (27%), Privacy&Security 46 (23%), Accessibility 33 (16%)"

---

## 3) 下一步阅读建议

| 顺序 | 论文 | 理由 |
|------|------|------|
| **1** | **SimuRA** (Deng et al. 2025, arXiv:2507.23773) | 同为 LLM 作为环境模拟器的范式，用于规划与用户-agent 交互。可对比 AaW 的 YAML 声明式与 SimuRA 的架构差异，理解「World Model 作为确定性执行器」的设计取舍。 |
| **2** | **Implicit reasoning in large language models: A comprehensive survey** (Li et al. 2025a, arXiv:2509.02350) | 本文 Related Work 引用的隐式推理综述。先读可建立隐式推理与显式推理的边界，再读 Implicit Intelligence 能更好理解其评估缺口（现有 benchmark 未系统测试 agent 场景下的隐式需求推断）。 |

---

## 4) 最易误解的 2 个点

1. **「World Model 用 Claude Opus 4.5 会偏袒 Claude」**：论文明确说明 World Model 是确定性规则执行器，行为由 YAML 的 returns 字段完全指定，无解释空间、无 rubric 访问权。正确与错误动作序列得到相同的中性模拟；98.6% 一致性表明机械行为。选择 Claude 仅基于一致性指标，其 benchmark 表现是事后测量的。

2. **「Implicit Intelligence 与通用推理能力正相关」**：实证显示模型迭代非单调（GPT-5 > GPT-5.1/5.2），且推理导向的 DeepSeek-R1 弱于通用 V3p1。论文结论：隐式推理可能更依赖训练侧重而非单纯能力缩放；extended thinking 对多数模型无一致增益，甚至部分下降。

---

## 5) 可复现实验切入点

**在 Implicit Intelligence 基准上复现单类子集**：选取 Accessibility 或 Catastrophic Risk 子集（33 或 56 个场景），使用开源 AaW 框架（若作者发布）或按论文 Section 4 的 YAML 规范自建最小场景，用开源 agent（如 DeepSeek-R1、Llama4）作为 Primary Agent，固定 World Model（可用 Claude API 或本地可复现替代），验证 SPR 与 NSS 是否与论文 Table 2 量级一致。可重点复现「环境探索不足」失败模式——对比 agent 是否在修改设置前调用 get_calendar_events()、get_file_metadata() 等观察动作。

---

*生成时间: 2025-03-10*
