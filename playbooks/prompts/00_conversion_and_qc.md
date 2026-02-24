# Prompt Template 00 - Conversion and QC

Use with: `@inbox/pdf_raw/` or `@inbox/pdf_raw/<file>.pdf`

```text
任务边界（必须遵守）：
- 只做 PDF->Markdown 转换和基础质量抽检。
- 不做领域归档决策（不判断放哪个目录）。
- 若需要归档，请改用 `02_domain_routing_and_bootstrap.md`。

请完成以下动作：
1) 将指定 PDF 转换到 `inbox/md_converted/`
2) 对转换结果做快速抽检（至少覆盖以下项）：
   - 标题层级是否完整（H1/H2/H3 是否可读）
   - 关键公式是否可读
   - 结论段是否可读

输出结构（固定）：
1) 转换结果
   - 成功文件列表
   - 失败文件列表（含错误原因）

2) 质检结论
   - 每篇文件给出：通过/待修复
   - 待修复项（简要列出）

3) 下一步动作
   - 可入库文件建议（仅列文件名）
   - 不可入库文件建议（需要重转或手工修复）
```
