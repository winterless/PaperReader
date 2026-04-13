# Prompt Template 01 - Single Paper Deep Read

Use with: `@papers/<domain>/<paper>.md`

```text
只基于我附加的论文文件回答；找不到依据请明确说无法验证。

请按以下结构输出：
1) 结论：这篇论文最核心的n个贡献（建议不超过3个，每个不超过 2 句话）
2) 依据：逐条给出证据，必须标注 [source: 文件路径 -> 章节名]
3) 下一步阅读建议：给出 2 篇后续论文和阅读顺序理由

附加要求：
- 指出 2 个最容易误解的点
- 给出 1 个可复现实验切入点

输出后落盘（必须执行）：
- 在 `inbox/md_converted/` 下创建与论文同名的评论文件：`<paper_stem>_comment.md`
- `paper_stem` 定义：去掉原论文文件扩展名后的文件名（不含目录）
- 示例：输入论文为 `papers/alignment/2023_dpo.md`，则输出文件为 `inbox/md_converted/2023_dpo_comment.md`
- 文件内容必须包含你刚刚给出的完整三段结构化回答（结论/依据/下一步阅读建议）以及“最易误解点”和“可复现实验切入点”
```
