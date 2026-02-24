# PaperReader 统一设计（通读版）

目标：用最小维护成本，持续读懂大模型论文；不自建 RAG 后端，直接使用 Cursor 作为检索与问答入口。

---

## 1) 设计原则（先定边界）

- 只做内容系统，不做复杂工程系统。
- 所有知识管理基于 Markdown，不直接依赖 PDF 检索。
- 回答必须可溯源（文件 + 章节）；无证据就明确说无法验证。
- 每次提问尽量小范围（1-3 篇），优先保证准确性。
- 步骤责任统一标记：`[用户]`、`[Cursor]`、`[用户+Cursor]`。

---

## 2) 最小目录（只保留必要结构）

```text
papers/
  foundation/
  training_infra/
  alignment/
inbox/
  pdf_raw/
  md_converted/
playbooks/
  prompts/
docs/
  paperreader-design.md
.cursorrules
TODO.md
```

说明：
- `papers/`：正式论文库（只放可读 `.md`）
- `inbox/`：转换中转区
- `playbooks/prompts/`：提问模板
- `.cursorrules`：回答质量规则

---

## 3) 入库流程（每天可执行）

1. `[用户]` 放入原始 PDF 到 `inbox/pdf_raw/`
2. `[用户]` 使用 `00_conversion_and_qc.md` 一次完成“PDF->Markdown 转换 + 质检 + 可入库文件确认”
3. `[用户]` 使用 `01_single_paper_deep_read.md` 发起精读
4. `[Cursor]` 输出结构化回答（结论、依据、下一步阅读）
5. `[用户]` 使用 `02_domain_routing_and_bootstrap.md` 一次性完成“领域判定 + 目标路径确定 + 文件移动 + Frontmatter补全 + 知识树渲染 + My Notes落盘”（必要时新建领域目录；命名规则：`年份_论文原名`）

---

## 4) 每篇论文最小元数据（Frontmatter）

先只维护 3 个字段，降低摩擦：

```yaml
---
paper_id: xxx_yyyy_short_name
topic_tags: [training_infra]
source_url: https://arxiv.org/abs/xxxx.xxxxx
---
```

可选增强（有余力再加）：`prerequisites`, `related`, `capability_tags`。

领域统一规则（防别名）：

- 领域主归属只由目录决定：`papers/<domain>/<paper>.md`。
- `topic_tags` 作为检索辅助标签，不作为知识树主干分组依据。
- 若目录名与 `topic_tags` 含义冲突，以目录名为准。
- 渲染器会把 `topic_tags` 规范化为 `snake_case`，并在 `papers/` 下自动补齐同名目录（允许为空）。

---

## 5) 执行入口（全部以 playbooks 为准）

为避免重复维护，SOP、模板和输出约束统一在 `playbooks/prompts/` 中维护。

- `00_conversion_and_qc.md`：转换 + 质检 + 可入库确认
- `01_single_paper_deep_read.md`：单篇精读
- `02_domain_routing_and_bootstrap.md`：领域判定 + 落库闭环
- `03_folder_synthesis_compare.md`：小范围综述与对比

日常只需要记住两条：

- `[用户]` 复制对应 prompt 执行，不在本设计文档中重复写流程细节
- `[Cursor]` 按 prompt 结构返回结果，并附证据来源
