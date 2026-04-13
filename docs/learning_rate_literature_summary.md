# 学习率策略：按训练场景整理

这篇文档只回答一个问题：**在不同训练场景下，学习率策略通常怎么选，为什么这样选，可以参考哪篇论文。**

文中所有事实性判断都尽量落在仓库内已有 Markdown 上，并用 `[source: 路径 -> 章节]` 标注。表格里的“建议”是基于这些论文做的整理，不等于论文原话。

---

## 总表

| 训练场景 | 常见策略 | 参考论文 | 选型原因 |
|---------|---------|---------|-------------|
| 从零预训练 | `short warmup + cosine decay` | `Scaling Laws` / `Chinchilla` / `Megatron-LM` | 是最稳定、最常见的默认方案；真正更重要的是周期是否匹配训练长度，而不是曲线名字本身。 |
| 继续预训练 / 换域续训 | `re-warm + decay`，重点扫 `max LR` | `Rewarm Your Model` | max LR 决定新域适应速度与旧域遗忘程度；warm-up 长度本身往往不是主要矛盾。 |
| 多阶段预训练 / 中训 | 分阶段 schedule：`warmup -> constant` 或 `warmup -> decay`，阶段切换时显式重设 LR | `Step 3.5 Flash` | 不同阶段目标不同，直接沿用上一段末期 LR 容易导致新阶段“学不动”。 |
| 长上下文 / annealing 阶段 | 前段 decay，后段 lower LR 或固定小 LR | `Step 3.5 Flash` | 上下文变长、数据变难后，通常更偏向稳定收敛，而不是继续激进更新。 |
| SFT / 对齐 / RL 后训练 | 更小 LR，常配 `short warmup + cosine decay` | `Step 3.5 Flash` / `DeepSeek-R1` | 后训练更新幅度小，目标是稳住能力分布与行为，而不是重新塑造全部底座能力。 |
| 垂直领域大模型 | 沿用预训练常规配方，再按数据域微调 max LR / warmup | `BloombergGPT` | 这类论文的重点通常在数据与任务，LR 更多是成熟工程配方，适合拿来做锚点。 |

总表里用了短论文名以便阅读；对应的仓库路径与章节引用都放在下文各节里。

---

## 1. 从零预训练

| 选择 | 原因 | 文献依据 |
|------|------|---------|
| 用 `short warmup + cosine decay` 作为默认基线 | 这是仓库里最稳定、最常见的预训练写法 | [source: `papers/training_infra/2019_megatron_lm.md` -> `## 4.2. Training Optimization and Hyperparameters`] GPT-2 使用 `1.5e-4`，`3k` warmup，随后单周期 cosine decay 到 `1e-5`。 |
| 不必过度纠结 schedule 形状本身 | 在满足 warmup、末期 LR 足够低等前提下，schedule 细节通常不是决定性因素 | [source: `papers/foundation/2020_scaling_laws_for_neural_language_models.md` -> Figure 22 相关讨论] 文中比较多种 schedule，结论是 performance 对 schedule 不强敏感，只要学习率不要太小、衰减不要太快。 |
| cosine 周期要和训练长度对齐 | 周期设得过长，会导致中后期 LR 掉不下来，最终训练不充分 | [source: `papers/foundation/2022_chinchilla.md` -> `## B. Optimal cosine cycle length`]；[source: `papers/foundation/2022_chinchilla.md` -> Figure A1 相关叙述] 文中指出当 cosine 周期比目标训练步数高估超过约 25% 时，性能会明显变差。 |
| 模型变大时，max LR 往往要更保守 | 大模型更容易发散 | [source: `papers/foundation/2020_scaling_laws_for_neural_language_models.md` -> 含 “larger models require a smaller learning rate” 的规则叙述段落] |

**适用判断：**

- 训练总步数或总 token 比较清楚。
- 你想先要一个稳妥基线，而不是发明新 schedule。

**更像工程上的一句话建议：**  
先用 `warmup + cosine`，然后把精力放在 **max LR 是否过大**、**cosine 周期是否和真实训练长度匹配**，而不是先纠结 cosine 和 linear decay 谁更“高级”。

---

## 2. 继续预训练 / 换域续训

| 选择 | 原因 | 文献依据 |
|------|------|---------|
| 用 `re-warm + decay`，不要默认直接 constant LR 跑到底 | 继续预训练时，模型已经在旧分布上收敛过，重新升温通常有助于学新数据 | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> Abstract]；[source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.2. How high to warmup?`] |
| 优先扫 `max LR`，而不是先花很多时间调 warm-up 长度 | 在这篇工作里，warm-up 长度对最终表现影响不大，但 max LR 直接影响新域适应和旧域遗忘 | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.1. How long to warmup?`]；[source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.2. How high to warmup?`] |
| 如果更在意开头稳定性，可以保留短 warm-up | 不做 progressive warm-up 会有初始 loss spike / chaotic phase | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.1. How long to warmup?`] |
| 如果更在意保住旧能力，就把 max LR 收小 | 更大的 max LR 提升下游新数据表现，但会加剧对上游旧数据的遗忘 | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.2. How high to warmup?`] |

**适用判断：**

- 你手里已经有 checkpoint。
- 新数据分布和原来不同。
- 你关心“学新东西”和“别忘太多”之间的平衡。

**更像工程上的一句话建议：**  
续训时，学习率首先是**遗忘–适应旋钮**。先扫 max LR，小范围试 warm-up；不要把主要时间花在 warm-up 从 0.5% 改到 1% 这种细节上。

---

## 3. 多阶段预训练 / 中训 / 长上下文阶段

| 选择 | 原因 | 文献依据 |
|------|------|---------|
| 每一阶段单独定义 LR，而不是默认承接上一阶段末值 | 阶段目标不同，延续上阶段的低 LR 容易让新阶段更新太弱 | [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 4.2.3. Hyper-Parameters`] |
| 前段可以继续 decay，后段常转成更小 LR 或固定 LR | 阶段后期更偏向稳定收敛，而不是继续大幅更新 | [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 4.2.3. Hyper-Parameters`] 文中 pre-training Stage 2 先做 secondary cosine decay，再在 32k 段固定较小 LR。 |
| 中训阶段常见 `warmup -> constant -> decay` | 先重新适应当前阶段，再稳定学习，最后再收尾 | [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 4.2.3. Hyper-Parameters`] 文中 mid-training 先 warmup 到 `2e-5`，Stage 1 保持 constant，Stage 2 再 decay 到 `7.3e-6`。 |

**适用判断：**

- 训练被拆成 pre-train / anneal / long-context / mid-train 多段。
- 数据混合、上下文长度、目标能力在中途发生变化。

**更像工程上的一句话建议：**  
多阶段训练里，最容易犯的错不是 schedule 太简单，而是**没有把阶段切换当成新的优化问题**。

---

## 4. SFT / 对齐 / RL 后训练

| 选择 | 原因 | 文献依据 |
|------|------|---------|
| 用更小 LR | 后训练更重视稳定对齐，而不是大幅改写底座能力 | [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 5.1. Expert Model Construction and Self-Distillation` 末段 Hyper-Parameters] |
| 常配短 warmup + cosine decay | 是比较稳的后训练默认选项 | [source: 同上 -> `## 5.1. Expert Model Construction and Self-Distillation` 末段 Hyper-Parameters] 文中 SFT 使用 `3% warmup + cosine decay`。 |
| 不要只看 LR，一起看 KL / clip / batch 等 | 后训练中的稳定性往往不是单一由 LR 决定 | [source: `papers/alignment/2025_deepseek_r1.md` -> 含 learning rate / cosine decay scheduler 的后训练相关段落] |

**适用判断：**

- 你在做 SFT、偏好对齐、RL 或蒸馏。
- 目标是稳住输出风格或能力分布，而不是重新预训练。

**更像工程上的一句话建议：**  
后训练调 LR 时，默认方向是**更小、更稳、更配合其他稳定化超参一起看**。

---

## 5. 领域模型与工程锚点

| 文件 | 可借鉴的地方 | 适合什么时候看 |
|------|-------------|---------------|
| `papers/adaptive_pretraining/2023_bloomberggpt.md` | 完整训练超参配方，含 max LR、cosine、warmup、batch size warmup | 做垂直领域预训练，需要一组成熟配方作锚点时 [source: `papers/adaptive_pretraining/2023_bloomberggpt.md` -> 训练超参相关小节] |
| `papers/training_infra/2019_megatron_lm.md` | 经典 GPT 式预训练 LR 写法，适合拿来做 baseline | 想先搭一个朴素、成熟的预训练方案时 [source: `papers/training_infra/2019_megatron_lm.md` -> `## 4.2. Training Optimization and Hyperparameters`] |
| `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` | 多阶段、大规模、长上下文训练中如何分段设 LR | 训练计划比较复杂时 [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 4.2.3. Hyper-Parameters`] |

---

## 快速决策表

| 如果你现在遇到的问题 | 优先改什么 | 参考论文 |
|---------------------|-----------|---------|
| 训练中后期 loss 下不去 | 检查 cosine 周期是否过长，末期 LR 是否降得不够 | [source: `papers/foundation/2022_chinchilla.md` -> `## B. Optimal cosine cycle length`] |
| 一开训就容易 spike / 发散 | 降低 max LR，保留短 warmup | [source: `papers/foundation/2020_scaling_laws_for_neural_language_models.md` -> 含大模型更需小 LR 的段落]；[source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.1. How long to warmup?`] |
| 继续预训练时新域学不动 | 提高 max LR，考虑 re-warm | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.2. How high to warmup?`] |
| 继续预训练时旧能力掉太多 | 降低 max LR，必要时缩短有效高 LR 阶段 | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4.2. How high to warmup?`] |
| 进入新阶段后几乎没更新 | 不要沿用上阶段末期 LR，重新定义该阶段 LR | [source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 4.2.3. Hyper-Parameters`] |
| 不知道先用什么 baseline | 先上 warmup + cosine | [source: `papers/training_infra/2019_megatron_lm.md` -> `## 4.2. Training Optimization and Hyperparameters`] |

---

## 读文献的优先顺序

如果只想花最少时间抓住要点，建议按这个顺序读：

1. `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md`
   原因：最像“把学习率当研究对象”来写，尤其适合续训场景。[source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> `4. Continual Warm-up`]
2. `papers/foundation/2022_chinchilla.md`
   原因：最适合理解“schedule 要和训练长度匹配”。[source: `papers/foundation/2022_chinchilla.md` -> `## B. Optimal cosine cycle length`]
3. `papers/foundation/2020_scaling_laws_for_neural_language_models.md`
   原因：最适合理解“别把 schedule 形状神化”。[source: `papers/foundation/2020_scaling_laws_for_neural_language_models.md` -> Figure 22 相关讨论]
4. `papers/training_infra/2019_megatron_lm.md`
   原因：给你一套经典可执行 baseline。[source: `papers/training_infra/2019_megatron_lm.md` -> `## 4.2. Training Optimization and Hyperparameters`]
5. `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md`
   原因：适合复杂多阶段训练时对照工业配方。[source: `papers/training_infra/2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters.md` -> `## 4.2.3. Hyper-Parameters`]

---

## 边界

- 这篇文档主要整理**策略选择**，不是完整超参手册。
- 各论文的模型、数据、优化器不同，表里的数字不能直接横向照搬。
- 当前仓库正文里没有可靠的 **WSD（Warmup–Stable–Decay）** 术语定义来源。**I cannot verify this from current repository sources.**
