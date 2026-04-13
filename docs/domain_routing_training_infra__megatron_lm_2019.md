# Domain Routing: Megatron-LM (2019)

## 1) 归属结论

- **首选领域：** training_infra
- **次选领域：** foundation
- **置信度（0-100）：** 92

## 2) 证据

- 论文标题与摘要明确聚焦“training very large transformer models”与“intra-layer model parallel approach”，属于训练系统与并行基础设施。  
  [source: `inbox/md_converted/training_infra__megatron_lm_2019.md` -> `Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism`]  
  [source: `inbox/md_converted/training_infra__megatron_lm_2019.md` -> `Abstract`]

- 贡献点强调“model parallel approach”“PyTorch”“memory”“512 GPUs”“scaling efficiency”，与现有 `papers/training_infra/2020_zero.md` 同属“如何高效/可扩展地训练大模型”的系统问题。  
  [source: `inbox/md_converted/training_infra__megatron_lm_2019.md` -> `1. Introduction`]  
  [source: `inbox/md_converted/training_infra__megatron_lm_2019.md` -> `2.3. Data and Model Parallelism in Deep Learning`]

- 正文详细描述“model parallelism”“all-reduce”“hybrid model and data parallelism”，与 ZeRO 等训练基础设施工作形成同一领域谱系。  
  [source: `inbox/md_converted/training_infra__megatron_lm_2019.md` -> `3. Model Parallel Transformers`]  
  [source: `inbox/md_converted/training_infra__megatron_lm_2019.md` -> `B.1. Hybrid Model and Data Parallelism`]

## 3) 领域决策

- **决策：** 沿用已有领域
- 不新增领域；`training_infra` 已存在且可覆盖“大模型训练并行与内存/扩展”这一核心问题。

## 4) 推荐落库动作

- **建议目标路径：** `papers/training_infra/2019_megatron_lm.md`
- **对应 PDF 路径：** `papers/training_infra/2019_megatron_lm.pdf`
- **对应评论路径（若有）：** `papers/training_infra/2019_megatron_lm_comment.md`（源：`inbox/md_converted/training_infra__megatron_lm_2019_comment.md`）
- **建议 topic_tags：** `training_infra`, `model_parallelism`, `distributed_training`, `transformer`, `megatron`
- **建议执行命令：**
```bash
mkdir -p papers/training_infra && \
mv inbox/md_converted/training_infra__megatron_lm_2019.md papers/training_infra/2019_megatron_lm.md && \
(test -f inbox/pdf_raw/seed_papers/training_infra__megatron_lm_2019.pdf && mv inbox/pdf_raw/seed_papers/training_infra__megatron_lm_2019.pdf papers/training_infra/2019_megatron_lm.pdf || true) && \
(test -f inbox/md_converted/training_infra__megatron_lm_2019_comment.md && mv inbox/md_converted/training_infra__megatron_lm_2019_comment.md papers/training_infra/2019_megatron_lm_comment.md || true)
```

## 5) 落库后标准化动作

- **Frontmatter（最小）：**
  - `paper_id`: `2019_megatron_lm`
  - `topic_tags`: `[training_infra, model_parallelism, distributed_training, transformer, megatron]`
  - `source_url`: `https://arxiv.org/abs/1909.08053`
- **知识树刷新命令：** `python scripts/render_knowledge_tree.py`
- **5 行笔记追加模板（写入 `## My Notes`）：** 见下方执行结果。
