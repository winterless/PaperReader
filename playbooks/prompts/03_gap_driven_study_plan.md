# Prompt Template 03 - Gap-Driven Study Plan

Use with: `@papers/` and optionally specific files.

```text
我的目标是补齐“大模型并行训练（TP/PP）+ 对齐（DPO/RLHF）”知识缺口。
请你作为论文导师，仅基于当前知识库内容，给我 14 天学习计划。

输出结构：
1) 结论：我当前最关键的 3 个知识短板
2) 依据：每个短板给出对应证据 [source: 文件路径 -> 章节名]
3) 下一步阅读建议：14 天计划（每天 1-2 篇，附学习目标与验收问题）

约束：
- 不要编造仓库外结论
- 若某部分证据不足，明确标注“当前仓库缺失”
```
