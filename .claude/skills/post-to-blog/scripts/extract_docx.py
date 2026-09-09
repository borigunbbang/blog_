#!/usr/bin/env python3
"""
Extract paragraphs and tables from a .docx file's word/document.xml,
without needing pandoc or python-docx (neither is reliably available
in every environment this skill runs in).

Usage:
    python3 extract_docx.py "path/to/file.docx"

Prints JSON to stdout:
    {
      "paragraphs": ["line 1", "line 2", ...],   # reading order, tables excluded
      "tables": [
        [["cell", "cell"], ["cell", "cell"]],    # table 1, row-major
        ...
      ]
    }

Notes for whoever reads/extends this:
- A naive regex like `<w:t[^>]*>` also matches `<w:tab .../>`, `<w:tabs>` etc.
  because "tab" starts with "t". That swallows huge chunks of raw XML into
  the "text" and silently corrupts the extraction. Anchor on `<w:t(?:\\s[^>]*)?>`
  instead (requires the character right after "w:t" to be '>' or whitespace).
- Paragraphs that belong to a table are extracted separately (see `tables`)
  so the caller can decide to render them as a markdown table rather than
  flattening them into prose.
"""
import re
import sys
import json
import zipfile

TEXT_RE = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)


def cell_text(cell_xml: str) -> str:
    return "".join(TEXT_RE.findall(cell_xml)).replace("\xa0", " ")


def extract(path: str):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")

    # Pull out tables first and replace them with a placeholder so the
    # paragraph pass doesn't also emit each cell as a loose paragraph.
    tables = []
    table_blocks = list(re.finditer(r"<w:tbl>.*?</w:tbl>", xml, re.S))
    for m in table_blocks:
        rows = re.findall(r"<w:tr[ >].*?</w:tr>", m.group(0), re.S)
        table = []
        for r in rows:
            cells = re.findall(r"<w:tc[ >].*?</w:tc>", r, re.S)
            table.append([cell_text(c) for c in cells])
        tables.append(table)

    # Remove table blocks before extracting body paragraphs.
    body_xml = re.sub(r"<w:tbl>.*?</w:tbl>", "", xml, flags=re.S)

    paragraphs = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", body_xml, re.S):
        line = "".join(TEXT_RE.findall(p)).replace("\xa0", " ")
        paragraphs.append(line)

    return {"paragraphs": paragraphs, "tables": tables}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: extract_docx.py <file.docx>", file=sys.stderr)
        sys.exit(1)
    result = extract(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
