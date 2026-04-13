# Domain Routing: Step 3.5 Flash (2026)

## 1) 归属结论

- 首选领域：`training_infra`
- 次选领域：`agent`
- 置信度（0-100）：`88`

## 2) 证据

- 论文摘要把核心目标定义为在 `frontier-level agentic intelligence` 和 `computational efficiency` 之间做统一优化，并直接给出 `196B total / 11B active`、`3:1 Sliding Window/Full Attention` 和 `MTP-3` 这些系统设计点，说明主线不是单一 agent benchmark，而是“面向 agent 负载的模型系统设计”。 [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `Abstract`]

- 引言和架构部分明确把 `inference latency`、`wall-clock time for task completion`、长上下文 prefilling、多轮 interactive decoding 当作设计约束，并围绕 attention、sparse MoE、MTP 做协同设计，这更接近训练/推理基础设施论文的关注点。 [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `1. Introduction`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `2. Architecture`]

- `3.2 TrainingFramework` 与 `3.3 High-ThroughputLightweightMonitoring` 大量篇幅讨论 `Steptron`、`Megatron-LM`、`PP/VPP/EP/ZeRO-1`、通信优化、`Muon ZeRO-1 Resharding`、以及 4096 GPU 规模下的异步 telemetry 监控，这些都是典型的 `training_infra` 领域问题。 [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `3.2. TrainingFramework`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `3.3. High-ThroughputLightweightMonitoring`]

- 论文还系统分析了 `Muon` 数值敏感性、expert collapse、localized activation blow-up 等大规模 MoE 训练失稳模式，并给出监控与干预手段。这进一步表明其核心问题是“大模型训练稳定性与系统可扩展性”。 [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `4.1. TrainingStability`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `4.1.1. NumericalSensitivityofMuon`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `4.1.2. ExpertCollapseBeyondRoutingCollapse`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `4.1.3. LocalizedActivationBlow-upinMoELayers`]

- 次选领域是 `agent`，因为后训练与评测明显覆盖 `MIS-PO`、tool use、search/report generation、`Terminal-Bench 2.0`、`BrowseComp`、`GAIA`、`τ2-Bench` 等 agent 任务；但这些更像该系统设计服务的 downstream workload，而不是全文唯一主轴。 [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `5.2.1. MIS-FilteredPolicyOptimization(MIS-PO)`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `5.2.2. RewardSystem`] [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `6.2. Post-trainingEvaluations`]

## 3) 领域决策

- 决策：沿用已有领域
- 不新增领域；现有 `papers/training_infra` 已能覆盖“大模型训练系统、并行扩展、MoE 稳定性、训练到推理协同优化”这一核心边界。

## 4) 推荐落库动作

- 建议目标路径：`papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md`
- 对应 PDF 路径：`papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.pdf`
- 对应评论路径（若有）：`papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters_comment.md`
- 建议 topic_tags：`training_infra`, `moe_systems`, `distributed_training`, `rl_post_training`, `agentic_llms`
- 建议执行命令（已完成）：

```bash
mkdir -p papers/training_infra && \
mv inbox/md_converted/2602.10604.md papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md && \
mv inbox/pdf_raw/seed_papers/2602.10604.pdf papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.pdf && \
(test -f inbox/md_converted/2602.10604_comment.md && mv inbox/md_converted/2602.10604_comment.md papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters_comment.md || true)
```

## 5) 落库后标准化动作

- Frontmatter（最小）：
  - `paper_id`: `2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters`
  - `topic_tags`: `[training_infra, moe_systems, distributed_training, rl_post_training, agentic_llms]`
  - `source_url`: `https://arxiv.org/abs/2602.10604`
- 知识树刷新命令：`python scripts/render_knowledge_tree.py`
- 5 行笔记追加模板（写入 `## My Notes`）：

```markdown
- 核心问题：
- 方法要点：
- 与已有工作的关系：
- 可复现/可沿用点：
- 待查/后续：
```
