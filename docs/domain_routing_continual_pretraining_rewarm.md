# Domain Routing: Continual Pre-Training of Large Language Models: How to (re)warm your model?

**Input:** `inbox/md_converted/continual_pretraining_rewarm_your_model__2308.04014v2.md`

---

## 1) 归属结论

- **首选领域：** adaptive_pretraining
- **次选领域：** training_infra（仅涉及 LR schedule 等训练超参，非核心）
- **置信度：** 92

---

## 2) 证据

1. [source: `inbox/md_converted/continual_pretraining_rewarm_your_model__2308.04014v2.md` -> Abstract] "enable the continual pre-training of these models, i.e. updating pre-trained models with new data instead of re-training them from scratch" — 核心问题为 continual pre-training，与 adaptive_pretraining 的「继续预训练以适应新数据」完全一致。

2. [source: 同上 -> Sec 1 Introduction] "We refer to this as 'continual pre-training' and the goal is to minimize the loss on new data while maintaining low loss on previous data" — 与 2020_dont_stop_pretraining 的 domain-adaptive pretraining 目标一致（适应新域/新数据同时保留旧能力）。

3. [source: 同上 -> Sec 3 Related Work] "In language, continual pre-training was studied under the name of domain adaptation pre-training (Ke et al., 2023a; Scialom et al., 2022; Gururangan et al., 2021)" — 论文自归类为 domain adaptation pre-training 的延续，Gururangan 即 dont_stop_pretraining 作者。

---

## 3) 领域决策

- **决策：** 沿用已有领域
- **领域目录：** `adaptive_pretraining`（已存在）
- **边界说明：** 包含 domain-adaptive / task-adaptive / continual pre-training；不包含 instruction tuning、RLHF 等 alignment 方法。

---

## 4) 推荐落库动作

- **建议目标路径：** `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md`
- **对应 PDF 路径：** `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.pdf`
- **对应评论路径：** `papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model_comment.md`
- **建议 topic_tags：** `[adaptive_pretraining, continual_pretraining, learning_rate_schedule, warmup, domain_adaptation]`
- **建议执行命令：**
```bash
mkdir -p papers/adaptive_pretraining && \
mv inbox/md_converted/continual_pretraining_rewarm_your_model__2308.04014v2.md papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.md && \
mv inbox/pdf_raw/top20_requested/continual_pretraining_rewarm_your_model__2308.04014v2.pdf papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model.pdf && \
(test -f inbox/md_converted/continual_pretraining_rewarm_your_model__2308.04014v2_comment.md && mv inbox/md_converted/continual_pretraining_rewarm_your_model__2308.04014v2_comment.md papers/adaptive_pretraining/2023_continual_pretraining_rewarm_your_model_comment.md || true)
```

---

## 5) 落库后标准化动作

- **Frontmatter（最小）：** `paper_id`, `topic_tags`, `source_url`
- **知识树刷新命令：** `python scripts/render_knowledge_tree.py`
- **5 行笔记追加模板：** 写入 `## My Notes`
