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

1. `[用户]` 把 PDF 放到 `inbox/pdf_raw/`
2. `[用户/Cursor]` 用外部工具（MinerU/Marker/Docling）转成 Markdown 到 `inbox/md_converted/`
3. `[用户]` 快速抽检：标题层级、关键公式、结论段是否可读
4. `[用户]` 合格稿移动到 `papers/<domain>/<paper_id>.md`
5. `[用户+Cursor]` 在 Cursor 里提问并产出 5 行笔记（用户提问，Cursor总结）
6. `[用户+Cursor]` 把 5 行笔记直接追加到该论文文件末尾的 `## My Notes`（只在 `papers/` 层做，不在 `inbox/` 写）

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
