#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "papers"
DOCS_DIR = ROOT / "docs"
TREE_MD = DOCS_DIR / "knowledge-tree.md"
TREE_HTML = DOCS_DIR / "knowledge-tree.html"
TREE_PNG = DOCS_DIR / "knowledge-tree.png"


def parse_list_value(raw: str) -> list[str]:
    value = raw.strip()
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        if not body:
            return []
        items = [x.strip().strip("'\"") for x in body.split(",")]
        return [x for x in items if x]
    if value:
        return [value.strip("'\"")]
    return []


def normalize_topic_tag(tag: str) -> str:
    value = (tag or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def parse_frontmatter(md_text: str) -> dict[str, str]:
    lines = md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def parse_wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", text or "")


def safe_id(value: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9_]+", "_", value)
    clean = clean.strip("_")
    return clean or "node"


def collect_papers() -> list[dict]:
    papers = []
    for path in sorted(PAPERS_DIR.rglob("*.md")):
        # 评论/笔记文件（*_comment.md）不算作论文节点
        if path.stem.endswith("_comment"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        fm = parse_frontmatter(text)
        paper_id = fm.get("paper_id") or path.stem
        title = fm.get("title") or path.stem
        # Canonical domain source: parent folder name under papers/.
        # This avoids alias drift between folder names and topic_tags.
        topic_tags = [path.parent.name]
        aux_topic_tags = []
        for raw_tag in parse_list_value(fm.get("topic_tags", "")):
            norm = normalize_topic_tag(raw_tag)
            if norm:
                aux_topic_tags.append(norm)
        aux_topic_tags = sorted(set(aux_topic_tags))

        prereq_raw = fm.get("prerequisites", "")
        prereq_list = parse_wikilinks(prereq_raw)
        if not prereq_list:
            prereq_list = parse_list_value(prereq_raw)

        papers.append(
            {
                "paper_id": paper_id,
                "title": title,
                "path": path.relative_to(ROOT).as_posix(),
                "topics": topic_tags,
                "aux_topics": aux_topic_tags,
                "prerequisites": prereq_list,
            }
        )
    return papers


def ensure_topic_directories(papers: list[dict]) -> list[str]:
    created = []
    all_tags = sorted({t for p in papers for t in p.get("aux_topics", [])})
    for tag in all_tags:
        tag_dir = PAPERS_DIR / tag
        if not tag_dir.exists():
            tag_dir.mkdir(parents=True, exist_ok=True)
            created.append(tag)
    return created


def build_mermaid(papers: list[dict]) -> str:
    # LR: 主题在左侧从上往下排布，叶子（论文）节点向右侧展开
    lines = ["graph LR"]
    topic_nodes: set[str] = set()
    paper_nodes: set[str] = set()

    for p in papers:
        p_node = f"P_{safe_id(p['paper_id'])}"
        if p_node not in paper_nodes:
            lines.append(f'  {p_node}["{p["paper_id"]}"]')
            paper_nodes.add(p_node)

        for topic in p["topics"]:
            t_node = f"T_{safe_id(topic)}"
            if t_node not in topic_nodes:
                lines.append(f'  {t_node}["{topic}"]')
                topic_nodes.add(t_node)
            lines.append(f"  {t_node} --> {p_node}")

        for pre in p["prerequisites"]:
            pre_node = f"P_{safe_id(pre)}"
            if pre_node not in paper_nodes:
                lines.append(f'  {pre_node}["{pre}"]')
                paper_nodes.add(pre_node)
            lines.append(f"  {pre_node} --> {p_node}")

    return "\n".join(lines)


def write_tree_markdown(papers: list[dict]) -> None:
    topics = Counter()
    prereq_edges = 0
    for p in papers:
        topics.update(p["topics"])
        prereq_edges += len(p["prerequisites"])

    lines = [
        "# Knowledge Tree",
        "",
        f"Updated at: `{dt.datetime.now().isoformat(timespec='seconds')}`",
        "",
        "## Snapshot",
        "",
        f"- Total papers: **{len(papers)}**",
        f"- Total topics: **{len(topics)}**",
        f"- Prerequisite edges: **{prereq_edges}**",
        "",
        "## Topic Coverage",
        "",
        "| Topic | Paper Count |",
        "|---|---:|",
    ]
    for topic, count in topics.most_common():
        lines.append(f"| {topic} | {count} |")

    lines.extend(
        [
            "",
            "## Tree Graph",
            "",
            "```mermaid",
            build_mermaid(papers),
            "```",
        ]
    )

    TREE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tree_html(papers: list[dict]) -> None:
    topics = Counter()
    prereq_edges = 0
    for p in papers:
        topics.update(p["topics"])
        prereq_edges += len(p["prerequisites"])

    mermaid_graph = build_mermaid(papers)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Knowledge Tree</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f1117;
      --fg: #e6e8ee;
      --card: #171a23;
      --muted: #9aa3b2;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #f7f9fc;
        --fg: #1e2430;
        --card: #ffffff;
        --muted: #5f6b7d;
      }}
    }}
    body {{
      margin: 0;
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: var(--bg);
      color: var(--fg);
    }}
    .wrap {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }}
    .header {{
      margin-bottom: 16px;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 10px;
      color: var(--muted);
      font-size: 14px;
    }}
    .badge {{
      background: var(--card);
      border-radius: 999px;
      padding: 6px 10px;
    }}
    .panel {{
      background: var(--card);
      border-radius: 12px;
      padding: 16px;
      overflow: auto;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <h1>Knowledge Tree</h1>
      <div class="meta">
        <span class="badge">Updated: {dt.datetime.now().isoformat(timespec='seconds')}</span>
        <span class="badge">Papers: {len(papers)}</span>
        <span class="badge">Topics: {len(topics)}</span>
        <span class="badge">Prerequisite edges: {prereq_edges}</span>
      </div>
    </div>
    <div class="panel">
      <pre class="mermaid">
{mermaid_graph}
      </pre>
    </div>
  </div>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    mermaid.initialize({{
      startOnLoad: true,
      theme: "default",
      flowchart: {{ curve: "basis" }},
      securityLevel: "loose"
    }});
  </script>
</body>
</html>
"""
    TREE_HTML.write_text(html, encoding="utf-8")


# PNG export: viewport and scale for resolution; mermaid flowchart spacing for layout
PNG_VIEWPORT_WIDTH = 1400
PNG_VIEWPORT_HEIGHT = 1000
PNG_SCALE = 2  # 2x for sharper output on high-DPI displays


def render_tree_png(papers: list[dict]) -> tuple[bool, str]:
    mermaid_graph = build_mermaid(papers)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_file = tmp_path / "knowledge-tree.mmd"
        pptr_cfg = tmp_path / "puppeteer-config.json"
        mermaid_cfg = tmp_path / "mermaid-config.json"
        input_file.write_text(mermaid_graph + "\n", encoding="utf-8")
        pptr_cfg.write_text(
            '{\n'
            '  "args": ["--no-sandbox", "--disable-setuid-sandbox"]\n'
            '}\n',
            encoding="utf-8",
        )
        # Flowchart layout (LR: 主题左列从上往下，论文右列): 节点与层级间距
        mermaid_cfg.write_text(
            '{\n'
            '  "flowchart": {\n'
            '    "nodeSpacing": 60,\n'
            '    "rankSpacing": 120,\n'
            '    "diagramPadding": 30\n'
            '  }\n'
            '}\n',
            encoding="utf-8",
        )

        mmdc = shutil.which("mmdc")
        if mmdc:
            cmd = [
                mmdc,
                "-i",
                str(input_file),
                "-o",
                str(TREE_PNG),
                "-p",
                str(pptr_cfg),
                "-c",
                str(mermaid_cfg),
                "-w",
                str(PNG_VIEWPORT_WIDTH),
                "-H",
                str(PNG_VIEWPORT_HEIGHT),
                "-s",
                str(PNG_SCALE),
                "-b",
                "transparent",
            ]
        else:
            npx = shutil.which("npx")
            if not npx:
                return (
                    False,
                    "skip_png: missing `mmdc` and `npx` (install Node.js or @mermaid-js/mermaid-cli)",
                )
            cmd = [
                npx,
                "-y",
                "@mermaid-js/mermaid-cli",
                "-i",
                str(input_file),
                "-o",
                str(TREE_PNG),
                "-p",
                str(pptr_cfg),
                "-c",
                str(mermaid_cfg),
                "-w",
                str(PNG_VIEWPORT_WIDTH),
                "-H",
                str(PNG_VIEWPORT_HEIGHT),
                "-s",
                str(PNG_SCALE),
                "-b",
                "transparent",
            ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            stdout = (exc.stdout or "").strip()
            details = stderr or stdout or "unknown error"
            return False, f"skip_png: {details}"

        if TREE_PNG.exists():
            return True, f"rendered: {TREE_PNG}"

        stdout = (result.stdout or "").strip()
        return False, f"skip_png: png not produced ({stdout or 'no output'})"


def main() -> None:
    papers = collect_papers()
    created_topic_dirs = ensure_topic_directories(papers)
    topics = {t for p in papers for t in p["topics"]}
    prereq_edges = sum(len(p["prerequisites"]) for p in papers)

    write_tree_markdown(papers)
    write_tree_html(papers)
    png_ok, png_msg = render_tree_png(papers)

    print(f"rendered: {TREE_MD}")
    print(f"rendered: {TREE_HTML}")
    print(png_msg)
    print(f"papers={len(papers)} topics={len(topics)} prereq_edges={prereq_edges}")
    print(f"topic_dirs_created={len(created_topic_dirs)}")
    if not png_ok:
        print("hint: npm i -g @mermaid-js/mermaid-cli")
    if created_topic_dirs:
        print("created_dirs: " + ", ".join(created_topic_dirs))


if __name__ == "__main__":
    main()
