#!/usr/bin/env python3
"""
One-off PDF → Markdown conversion using pdfplumber.
Output: inbox/md_converted/<stem>.md
Usage: python scripts/pdf_to_md.py <path-to-pdf>
"""
import re
import sys
from pathlib import Path

import pdfplumber

def extract_md(pdf_path: Path) -> str:
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                page_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
                for ln in page_lines:
                    # Section-like: numbered (e.g. "1. Introduction") or known headings; skip page headers like "REVISITING..."
                    is_section = (
                        len(ln) < 100
                        and (
                            re.match(r"^[\d.]+\s+[A-Za-z]", ln)
                            or re.match(r"^(Abstract|Introduction|Conclusion|References|Appendix)\s*$", ln, re.I)
                        )
                    )
                    # Skip repeated full-title page headers (often all-caps or title case)
                    is_page_header = re.match(r"^REVISITING GROUP RELATIVE", ln, re.I) or (
                        len(ln) < 80 and re.match(r"^[\d]+\s*$", ln)
                    )
                    if is_section and not is_page_header:
                        lines.append("## " + ln)
                    elif not is_page_header or len(ln) > 20:
                        lines.append(ln)
            if i < len(pdf.pages) - 1:
                lines.append("")
    return "\n".join(lines)


def main():
    pdf_path = Path(sys.argv[1]).resolve()
    if not pdf_path.suffix.lower() == ".pdf" or not pdf_path.exists():
        print("Usage: python pdf_to_md.py <path-to-pdf>", file=sys.stderr)
        sys.exit(1)
    stem = pdf_path.stem
    out_dir = Path(__file__).resolve().parent.parent / "inbox" / "md_converted"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{stem}.md"
    md = extract_md(pdf_path)
    out_path.write_text(md, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
