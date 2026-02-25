# Prompt Template 02 - Domain Routing and Bootstrap

Use with: `@inbox/md_converted/<paper>.md` and optionally `@papers/`

```text
任务边界（必须遵守）：
- 只做论文归档路由与领域新增判定。
- 不做领域综述和多论文方法对比。
- 若需要综述/对比，请改用 `03_folder_synthesis_compare.md`。

请判断这篇论文的领域归属，并决定是否需要在papers下新增领域目录或添加到相应的目录。
如果当前 papers 目录下无对应领域，请执行“自归纳建域”。

输出结构（固定）：
1) 归属结论
   - 首选领域：
   - 次选领域：
   - 置信度（0-100）：

2) 证据
   - 至少 3 条证据，必须标注 [source: 文件路径 -> 章节名]

3) 领域决策
   - 决策：沿用已有领域 / 新增领域
   - 若新增：给出领域目录名（snake_case）+ 一句话边界定义（包含什么，不包含什么）

4) 推荐落库动作
   - 建议目标路径：papers/<domain>/<year>_<paper_original_name>.md
   - 对应 PDF 路径：papers/<domain>/<year>_<paper_original_name>.pdf
   - 建议 topic_tags（3-5 个）
   - 建议执行命令（同步归档 md + pdf）：
     mkdir -p papers/<domain> && \
     mv <source_md_path> papers/<domain>/<year>_<paper_original_name>.md && \
     mv <source_pdf_path> papers/<domain>/<year>_<paper_original_name>.pdf

5) 落库后标准化动作（一并给出）
   - Frontmatter（最小）：`paper_id`, `topic_tags`, `source_url`
   - 知识树刷新命令：python scripts/render_knowledge_tree.py
   - 5 行笔记追加模板（写入 `## My Notes`）

判定规则：
- 若 papers 中已有领域可以覆盖论文核心问题，则优先复用，不轻易扩域。
- 若论文核心问题与现有领域都明显不匹配，才建议新增领域。
- 若证据不足，必须明确输出“无法确定”。
- 文件命名必须使用：`年份_论文原名`。
- 需要归档，归档必须同时迁移 `.md` 和对应 `.pdf` 到同一领域目录。
- 本 prompt 输出需覆盖“判定到落库后的完整动作清单”，不遗漏 Frontmatter/渲染/My Notes。

自归纳建域模式（当 papers 为空或样本不足）：
- 仅基于待判定论文内容，先给出“临时领域名”和“边界定义”。
- 说明这是临时归档，后续出现 3+ 同类论文再确认是否固化为正式领域。
```
