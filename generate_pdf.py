import os
import re
import subprocess
import html

def markdown_to_html(md_text):
    lines = md_text.splitlines()
    html_lines = []
    in_code_block = False
    code_lang = ""
    code_content = []
    in_table = False
    table_rows = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        res = []
        if in_ul:
            res.append("</ul>")
            in_ul = False
        if in_ol:
            res.append("</ol>")
            in_ol = False
        return res

    def format_inline(text):
        # escape html first
        text = html.escape(text)
        # inline code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # bold italic
        text = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # bold
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
        # italic
        text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
        # links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text

    for line in lines:
        stripped = line.strip()

        # Fenced code block
        if stripped.startswith("```"):
            if not in_code_block:
                html_lines.extend(close_lists())
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_content = []
            else:
                in_code_block = False
                escaped_code = html.escape("\n".join(code_content))
                html_lines.append(f'<pre><code class="language-{code_lang}">{escaped_code}</code></pre>')
                code_content = []
            continue

        if in_code_block:
            code_content.append(line)
            continue

        # Table row
        if stripped.startswith("|") and stripped.endswith("|"):
            html_lines.extend(close_lists())
            # check if it's separator row
            if re.match(r'^\|(\s*:?-+:?\s*\|)+$', stripped):
                continue
            cols = [col.strip() for col in stripped[1:-1].split("|")]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cols)
            continue
        else:
            if in_table:
                in_table = False
                # generate table html
                table_html = ['<table>']
                if table_rows:
                    table_html.append('<thead><tr>')
                    for header in table_rows[0]:
                        table_html.append(f'<th>{format_inline(header)}</th>')
                    table_html.append('</tr></thead>')
                    if len(table_rows) > 1:
                        table_html.append('<tbody>')
                        for row in table_rows[1:]:
                            table_html.append('<tr>')
                            for cell in row:
                                table_html.append(f'<td>{format_inline(cell)}</td>')
                            table_html.append('</tr>')
                        table_html.append('</tbody>')
                table_html.append('</table>')
                html_lines.append("\n".join(table_html))
                table_rows = []

        # Empty line
        if not stripped:
            html_lines.extend(close_lists())
            continue

        # Horizontal Rule
        if stripped in ["---", "***", "___"]:
            html_lines.extend(close_lists())
            html_lines.append("<hr />")
            continue

        # Headers
        header_match = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if header_match:
            html_lines.extend(close_lists())
            level = len(header_match.group(1))
            header_text = format_inline(header_match.group(2))
            html_lines.append(f'<h{level}>{header_text}</h{level}>')
            continue

        # Blockquote
        if stripped.startswith("> "):
            html_lines.extend(close_lists())
            quote_text = format_inline(stripped[2:])
            html_lines.append(f'<blockquote><p>{quote_text}</p></blockquote>')
            continue

        # Unordered list
        ul_match = re.match(r'^[\*\-]\s+(.*)$', stripped)
        if ul_match:
            if in_ol:
                html_lines.extend(close_lists())
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            item_text = format_inline(ul_match.group(1))
            html_lines.append(f'<li>{item_text}</li>')
            continue

        # Image block: ![alt](src)
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', stripped)
        if img_match:
            html_lines.extend(close_lists())
            alt = img_match.group(1)
            raw_src = img_match.group(2).strip('<>').strip()
            if os.path.exists(raw_src):
                abs_img_path = os.path.abspath(raw_src).replace('\\', '/')
                img_src = f"file:///{abs_img_path}"
            else:
                img_src = raw_src
            html_lines.append(f'<div class="img-container"><img src="{img_src}" alt="{html.escape(alt)}" /><div class="img-caption">{html.escape(alt)}</div></div>')
            continue

        # Ordered list
        ol_match = re.match(r'^\d+\.\s+(.*)$', stripped)
        if ol_match:
            if in_ul:
                html_lines.extend(close_lists())
            if not in_ol:
                html_lines.append('<ol>')
                in_ol = True
            item_text = format_inline(ol_match.group(1))
            html_lines.append(f'<li>{item_text}</li>')
            continue

        # Regular Paragraph
        html_lines.extend(close_lists())
        para_text = format_inline(stripped)
        html_lines.append(f'<p>{para_text}</p>')

    html_lines.extend(close_lists())
    if in_table and table_rows:
        table_html = ['<table><thead><tr>']
        for header in table_rows[0]:
            table_html.append(f'<th>{format_inline(header)}</th>')
        table_html.append('</tr></thead><tbody>')
        for row in table_rows[1:]:
            table_html.append('<tr>')
            for cell in row:
                table_html.append(f'<td>{format_inline(cell)}</td>')
            table_html.append('</tr>')
        table_html.append('</tbody></table>')
        html_lines.append("\n".join(table_html))

    return "\n".join(html_lines)


def build_full_html(body_content):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>LAB_REPORT - Quản lý Phụ thuộc và Robot Điều phối Tự động</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
  }}
  @media print {{
    body {{
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .page-break {{
      page-break-before: always;
    }}
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1f2937;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    font-size: 18pt;
    color: #1e3a8a;
    border-bottom: 2.5px solid #2563eb;
    padding-bottom: 6px;
    margin-top: 15px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h2 {{
    font-size: 13.5pt;
    color: #1e40af;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  h3 {{
    font-size: 11.5pt;
    color: #0369a1;
    margin-top: 14px;
    margin-bottom: 6px;
  }}
  h4 {{
    font-size: 10.5pt;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 4px;
  }}
  p {{
    margin: 6px 0;
    text-align: justify;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 14px 0;
  }}
  ul, ol {{
    margin: 6px 0;
    padding-left: 24px;
  }}
  li {{
    margin-bottom: 3px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }}
  tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}
  code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    color: #be123c;
    padding: 1.5px 4.5px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }}
  pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 5px;
    overflow-x: auto;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    margin: 8px 0;
    page-break-inside: avoid;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  pre code {{
    background-color: transparent;
    color: #f8fafc;
    border: none;
    padding: 0;
    font-size: inherit;
  }}
  blockquote {{
    border-left: 4px solid #3b82f6;
    margin: 8px 0;
    padding: 4px 12px;
    background-color: #eff6ff;
    color: #1e40af;
  }}
  a {{
    color: #2563eb;
    text-decoration: none;
  }}
  a:hover {{
    text-decoration: underline;
  }}
  .img-container {{
    text-align: center;
    margin: 16px 0 18px 0;
    page-break-inside: avoid;
  }}
  .img-container img {{
    max-width: 95%;
    max-height: 480px;
    object-fit: contain;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
  }}
  .img-caption {{
    font-size: 8.5pt;
    color: #475569;
    margin-top: 6px;
    font-style: italic;
    font-weight: 500;
  }}
</style>
</head>
<body>
{body_content}
</body>
</html>
"""

def main():
    with open("LAB_REPORT.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown_to_html(md_text)
    full_html = build_full_html(html_body)

    html_file = "LAB_REPORT.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated {html_file}")

    # Convert to PDF with Edge
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    pdf_file = "LAB_REPORT.pdf"
    abs_html = os.path.abspath(html_file)
    abs_pdf = os.path.abspath(pdf_file)

    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html}"
    ]

    print("Running Edge PDF compilation...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)

    if os.path.exists(pdf_file):
        size = os.path.getsize(pdf_file)
        print(f"SUCCESS: {pdf_file} created successfully, size: {size} bytes ({size/1024:.1f} KB)")
    else:
        print(f"ERROR: {pdf_file} was not generated.")

if __name__ == "__main__":
    main()
