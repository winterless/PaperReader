# PaperReader (Cursor-Native)

一个基于 Cursor 的论文学习知识库：不自建 RAG 后端，只做高质量 Markdown 语料、规则约束和提问工作流。

## 先看这个

- `docs/paperreader-design.md`：统一通读版（唯一设计文档）
- `TODO.md`：后续优化清单（先不实现）

## 最小目录

- `.cursorrules`：全局导师规则（溯源/拒答/输出格式）
- `docs/paperreader-design.md`：统一架构与流程
- `papers/`：论文 Markdown 库
- `inbox/`：PDF 原稿与转换中间区
- `playbooks/prompts/`：可复用 Prompt 模板

## 开始使用

1. 把 PDF 放进 `inbox/pdf_raw/`，转换成 Markdown 到 `inbox/md_converted/`
2. 把合格 Markdown 移入 `papers/<domain>/`
3. 在 Cursor 中用 `@papers/...` 或 `@papers/<domain>/` 提问
4. 参考 `playbooks/prompts/` 的模板进行精读、综述和学习路径规划
