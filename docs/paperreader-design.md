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

## 5) Cursor 使用 SOP（核心）

### A. 单篇精读（推荐默认）

- `[用户]` 用 `@papers/<domain>/<paper>.md`
- `[用户]` 问一个明确目标：如“解释方法核心创新与局限”
- `[Cursor]` 返回“结论-依据-下一步阅读建议”

### B. 小范围对比（2-3 篇）

- `[用户]` 一次只 `@` 2-3 篇相关论文
- `[用户]` 指定对比维度（创新点/代价/适用场景）
- `[Cursor]` 输出结构化对比并标注证据来源

### C. 目录扫描（避免上下文爆炸）

- `[用户]` 不直接让模型“读完整个大目录”
- `[用户]` 先要求：从目录里挑最相关 3 篇，再做深入分析
- `[Cursor]` 先给候选文件，再做二轮深读回答

---

## 6) 固定提问模板（直接复用）

`[用户]` 直接粘贴模板；`[Cursor]` 严格按模板结构回答。

```text
@papers/<domain>/<paper>.md
只基于该文件回答，找不到依据就明确说无法验证。
请输出：
1) 3条核心结论
2) 每条对应证据（文件名+章节）
3) 下一篇建议阅读及理由
```

---

## 7) 输出标准（你和模型共同遵守）

- `[Cursor]` 结论：简短、可执行
- `[Cursor]` 依据：必须标注来源（文件 + 章节）
- `[Cursor]` 下一步阅读建议：1-3 篇，给顺序理由
- `[用户]` 复核：无证据条目不采纳，必要时追问来源

---

## 8) 节奏建议（防止系统空转）

- `[用户]` 每天：1 篇论文
- `[用户+Cursor]` 每天：产出 5 行笔记并追加到论文末尾 `## My Notes`
- `[用户+Cursor]` 每周：1 次小专题对比（2-3 篇）
- `[用户]` 连续两周稳定执行后，再考虑自动化，不提前扩展复杂功能

5 行笔记模板（极简）：

- 核心结论：
- 关键证据（章节）：
- 我的理解（人话版）：
- 仍有疑问：
- 下一篇要读：

---

## 9) 何时升级系统

满足以下任一条件再升级：

- `papers/` 超过 30 篇且标签维护明显吃力
- 经常需要跨主题检索但手动筛选成本高
- 你已经稳定执行日/周学习节奏

升级项已放在 `TODO.md`，先记录，不提前实现。

---

## 10) 知识树生成 SOP（轻量版）

1. `[用户]` 在每次新增或移动论文到 `papers/` 后执行：
   - `python scripts/render_knowledge_tree.py`
2. `[Cursor]` 从 `papers/**/*.md` 读取信息：
   - 目录名（领域主归属，唯一真源）
   - `topic_tags`（辅助标签；规范化后用于补齐目录）
   - `prerequisites`（前置关系，可选）
3. `[Cursor]` 生成两个输出文件：
   - `docs/knowledge-tree.md`（当前树 + Mermaid 图）
   - `docs/tree-growth-log.csv`（增长快照）
4. `[用户]` 若 `papers/` 为空，看到 `0 papers` 属于正常现象。
5. `[用户]` 为避免别名问题，领域变更应通过“移动文件到目标目录”完成。
