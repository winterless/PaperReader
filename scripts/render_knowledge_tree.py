#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "papers"
DOCS_DIR = ROOT / "docs"
TREE_MD = DOCS_DIR / "knowledge-tree.md"
GROWTH_CSV = DOCS_DIR / "tree-growth-log.csv"


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


def append_growth_snapshot(total_papers: int, total_topics: int, prereq_edges: int) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = GROWTH_CSV.exists()
    with GROWTH_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "total_papers", "total_topics", "total_prereq_edges"])
        writer.writerow(
            [
                dt.datetime.now().isoformat(timespec="seconds"),
                total_papers,
                total_topics,
                prereq_edges,
            ]
        )


def load_growth_rows(limit: int = 12) -> list[dict]:
    if not GROWTH_CSV.exists():
        return []
    with GROWTH_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-limit:]


def build_mermaid(papers: list[dict]) -> str:
    lines = ["graph TD"]
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


def write_tree_markdown(papers: list[dict], growth_rows: list[dict]) -> None:
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
            "",
            "## Growth Trend",
            "",
            "| Timestamp | Papers | Topics | Prereq Edges |",
            "|---|---:|---:|---:|",
        ]
    )

    for row in growth_rows:
        lines.append(
            f"| {row.get('timestamp','')} | {row.get('total_papers','')} | "
            f"{row.get('total_topics','')} | {row.get('total_prereq_edges','')} |"
        )

    TREE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    papers = collect_papers()
    created_topic_dirs = ensure_topic_directories(papers)
    topics = {t for p in papers for t in p["topics"]}
    prereq_edges = sum(len(p["prerequisites"]) for p in papers)

    append_growth_snapshot(
        total_papers=len(papers),
        total_topics=len(topics),
        prereq_edges=prereq_edges,
    )
    growth_rows = load_growth_rows()
    write_tree_markdown(papers, growth_rows)

    print(f"rendered: {TREE_MD}")
    print(f"papers={len(papers)} topics={len(topics)} prereq_edges={prereq_edges}")
    print(f"topic_dirs_created={len(created_topic_dirs)}")
    if created_topic_dirs:
        print("created_dirs: " + ", ".join(created_topic_dirs))
    print(f"growth_log: {GROWTH_CSV}")


if __name__ == "__main__":
    main()
