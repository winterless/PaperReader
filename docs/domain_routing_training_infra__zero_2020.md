# 领域路由结果：ZeRO (2020)

**待判定论文**：`inbox/md_converted/2020_zero.md`（ZeRO: Memory Optimizations Toward Training Trillion Parameter Models）

---

## 1) 归属结论

- **首选领域**：training_infra（训练系统与基础设施）
- **次选领域**：foundation（与大规模预训练相关，但论文核心是系统优化而非模型/算法）
- **置信度**：92

## 2) 证据

- 论文标题与摘要明确聚焦“内存优化”“训练效率”“data/model parallelism”“显存与通信”，属于训练系统问题。  
  [source: `inbox/md_converted/2020_zero.md` -> `## Abstract`]

- 全文将内存消耗拆为“模型状态”与“残余状态”，并提出 ZeRO-DP / ZeRO-R 两套系统级优化，与 foundation（架构/缩放律）或 alignment 明显不同。  
  [source: `inbox/md_converted/2020_zero.md` -> `## 4 ZeRO : Insights and Overview`]  
  [source: `inbox/md_converted/2020_zero.md` -> `## 3 Where Did All the Memory Go?`]

- 实现与评估章节强调“无需改模型”“可与 Megatron 等 MP 组合”“400 GPU、15 PFLOPS”，均为系统/工程维度。  
  [source: `inbox/md_converted/2020_zero.md` -> `## 10 Implementation and Evaluation`]  
  [source: `inbox/md_converted/2020_zero.md` -> `## 10.1 Implementation and Methodology`]

## 3) 领域决策

- **决策**：新增领域
- **领域目录名**：`training_infra`
- **边界定义**：大模型训练系统与基础设施（显存优化、数据/模型/流水线并行、通信与调度等）；**包含**：ZeRO、DeepSpeed、Megatron 类工作、集群级训练效率。**不包含**：模型架构创新（foundation）、对齐与 RLHF（alignment）、领域自适应预训练（adaptive_pretraining）、智能体与工具调用（agent）。

## 4) 推荐落库动作

- **建议目标路径**：`papers/training_infra/2020_zero.md`
- **对应 PDF 路径**：`papers/training_infra/2020_zero.pdf`
- **对应评论路径**：`papers/training_infra/2020_zero_comment.md`（源：`inbox/md_converted/training_infra__zero_2020_comment.md`）
- **建议 topic_tags**：`training_infra`, `zero_redundancy_optimizer`, `memory_optimization`, `data_parallelism`, `distributed_training`
- **建议执行命令**（PDF 实际在 `inbox/pdf_raw/seed_papers/2020_zero.pdf`）：

```bash
mkdir -p papers/training_infra && \
mv inbox/md_converted/2020_zero.md papers/training_infra/2020_zero.md && \
mv inbox/pdf_raw/seed_papers/2020_zero.pdf papers/training_infra/2020_zero.pdf && \
(test -f inbox/md_converted/training_infra__zero_2020_comment.md && mv inbox/md_converted/training_infra__zero_2020_comment.md papers/training_infra/2020_zero_comment.md || true)
```

## 5) 落库后标准化动作

- **Frontmatter（最小）**：在 `papers/training_infra/2020_zero.md` 顶部确保：
  - `paper_id`: `2020_zero`
  - `topic_tags`: `[training_infra, zero_redundancy_optimizer, memory_optimization, data_parallelism, distributed_training]`
  - `source_url`: `https://arxiv.org/abs/1910.02054`
- **知识树刷新**：`python scripts/render_knowledge_tree.py`
- **My Notes 模板**（在文末追加 `## My Notes` 若不存在，并保留以下 5 行模板）：
  - 核心问题：
  - 方法要点：
  - 与已有工作的关系：
  - 可复现/可沿用点：
  - 待查/后续：
