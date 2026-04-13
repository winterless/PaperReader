# Deep Read: Continual Pre-Training of Large Language Models: How to (re)warm your model?

**Source:** `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` (archived)

---

## 1) 结论

1. **线性 warm-up 非必要**：在 continual pre-training 场景下，渐进式 warm-up 对最终 perplexity 无显著影响；直接从 max LR 开始会产生短暂的「混沌期」（stability gap），但无长期后果。
2. **Max LR 调节上下游权衡**：增大 max LR 提升下游（SlimPajama）表现但加剧上游（Pile）遗忘；减小 max LR 则相反。Re-warm + decay 在足够长训练后优于 constant LR。
3. **使用最新 checkpoint**：从更早的 pre-training checkpoint 开始 continual pre-training 并不能更快适应下游；应使用最新 checkpoint。

---

## 2) 依据

| 结论 | 证据 |
|------|------|
| Warm-up 长度无显著影响 | [source: `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md` -> Sec 4.1] "The results... show that the amount of data used for warming up the learning rate does not significantly influence the perplexity on the downstream task (learning) or the upstream task (forgetting)." Takeaway 1: "The length of the warmup phase does not appear to have a significant effect on the Pile and SlimPajama validation losses." Fig 1 显示 0%, 0.5%, 1%, 2% warm-up 曲线几乎重合。 |
| 0% warm-up 有混沌期但无长期影响 | [source: 同上 -> Sec 4.1] "the model trained without any progressive warmup experiences an initial 'chaotic phase' causing a spike in the loss in its first few iterations... this phenomenon is also referred to as stability gap (Lange et al., 2023; Caccia et al., 2022)" |
| Max LR 调节上下游权衡 | [source: 同上 -> Sec 4.2] "larger maximum learning rates improve performance on downstream data, while they hurt performance on upstream data. Conversely, a smaller maximum learning rate improves performance on upstream data, while limiting adaptation to downstream data." Fig 2, 3, 4。Takeaway 2: "Rewarming then decaying the learning rate appears necessary to learn well on the downstream task." |
| 最新 checkpoint 最优 | [source: 同上 -> Sec 4.5] "selecting earlier checkpoints for later fine-tuning does not lead to improvement in downstream performance. Therefore, selecting the latest checkpoint is the best option." Fig 7。Takeaway 4: "Using an earlier checkpoint when pretraining on the Pile does not lead to learning faster on SlimPajama." |
| Continual pre-training 优于 from-scratch | [source: 同上 -> Sec 4.3] "all the fine-tuned models with a warm-up outperform the model trained from scratch." Fig 2, 3。 |
| Re-warming 本身导致 loss 上升 | [source: 同上 -> Sec 4.4] "re-warming the learning rate while continuing to pre-train on the Pile has a similar effect as re-warming on SlimPajama data... the distribution shift between Pile and SlimPajama is not solely to blame... the optimization dynamics also plays a role." Fig 5, 6。Takeaway 3。 |

---

## 3) 下一步阅读建议

1. **Ke et al. (2023) "Continual pre-training of language models" (ICLR)**  
   本文多处引用，研究 constant LR vs progressive decrease 等策略，与 warm-up 研究互补。先读可建立 continual pre-training 的整体图景。

2. **Gururangan et al. (2020) "Don't stop pretraining"** [source: `papers/adaptive_pretraining/2020_dont_stop_pretraining.md`]  
   域适应预训练的开创工作，讨论何时继续预训练、如何混合数据。本文的 Pile→SlimPajama 设定与之相关，可对比「同域扩展」与「跨域适应」的差异。

---

## 4) 最易误解的点

1. **「必须用 warm-up 才能稳定训练」**  
   本文表明：0% warm-up 虽在初期有 loss spike（stability gap），但最终 perplexity 与 0.5%/1%/2% warm-up 无显著差异。结论是「线性 warm-up 在此设定下无用」，而非「warm-up 有害」。

2. **「更早的 checkpoint 更易适应新数据」**  
   直觉上可能认为未完全收敛的 checkpoint 更有「可塑性」。本文实验显示：从 iter 10k/27k 开始的 continual pre-training 在 SlimPajama 上表现不如从 iter 143k（最新）开始，说明 pre-training 并未导致明显 loss of plasticity。

---

## 5) 可复现实验切入点

**复现 Fig 1（warm-up 长度实验）**  
- 模型：Pythia 410M（Pile 预训练）  
- 上游：Pile（300B tokens）；下游：SlimPajama（297B tokens）  
- 变量：warm-up 长度 0%, 0.5%, 1%, 2%（基于 297B tokens 计算）  
- 固定：MaxLR=3e-4，MinLR=0.1·MaxLR，cosine decay  
- 评估：在 50B tokens 处测量 Pile 与 SlimPajama 的 validation perplexity  
- 预期：四条曲线在 50B 处基本重合，0% warm-up 在最初几 B tokens 有更高 loss spike。

---

*Generated per playbook 01_single_paper_deep_read*
