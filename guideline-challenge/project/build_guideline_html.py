# -*- coding: utf-8 -*-
"""Dựng project/02_guideline.html từ project/02_guideline.md, nhúng ảnh trực tiếp (base64).

Chạy lại mỗi khi sửa guideline:  python3 project/build_guideline_html.py
File HTML tự chứa ảnh nên mở được ở bất kỳ đâu (trình duyệt, gửi file) mà không cần thư mục ảnh đi kèm.
"""
import base64
import mimetypes
import re
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent          # project/
SRC = HERE / "02_guideline.md"
OUT = HERE / "02_guideline.html"

CSS = """
:root { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --border:#d1d9e0; --code:#f6f8fa; --accent:#0969da; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --border:#3d444d; --code:#151b23; --accent:#4493f8; }
}
* { box-sizing: border-box; }
body { background:var(--bg); color:var(--fg); margin:0;
       font:16px/1.6 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif; }
main { max-width:1100px; margin:0 auto; padding:32px 16px 64px; }
h1,h2,h3 { line-height:1.3; }
h1 { border-bottom:1px solid var(--border); padding-bottom:.3em; }
h2 { border-bottom:1px solid var(--border); padding-bottom:.3em; margin-top:2em; }
a { color:var(--accent); }
code { background:var(--code); padding:.15em .35em; border-radius:4px; font-size:.9em; }
pre { background:var(--code); padding:12px; border-radius:6px; overflow-x:auto; }
.table-wrap { overflow-x:auto; margin:1em 0; }
table { border-collapse:collapse; width:100%; }
th,td { border:1px solid var(--border); padding:8px 10px; vertical-align:top; text-align:left; }
th { background:var(--code); }
td img { max-width:100%; height:auto; border-radius:4px; border:1px solid var(--border); cursor:zoom-in; }
td img.zoom { position:fixed; inset:0; margin:auto; max-width:95vw; max-height:95vh; width:auto;
              z-index:10; cursor:zoom-out; box-shadow:0 0 0 100vmax rgba(0,0,0,.75); }
blockquote { color:var(--muted); border-left:4px solid var(--border); margin:0; padding:0 1em; }
"""

JS = """
document.querySelectorAll('td img').forEach(function (img) {
  img.addEventListener('click', function () { img.classList.toggle('zoom'); });
});
"""


def embed(match: re.Match) -> str:
    src = match.group(2)
    if src.startswith(("data:", "http://", "https://")):
        return match.group(0)
    path = (HERE / src).resolve()
    if not path.is_file():
        print(f"  ! không thấy ảnh: {src}")
        return match.group(0)
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'{match.group(1)}data:{mime};base64,{data}{match.group(3)}'


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    body = re.sub(r'(<img[^>]*?src=")([^"]+)(")', embed, body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    title_match = re.search(r"<h1>(.*?)</h1>", body)
    title = re.sub(r"<[^>]+>", "", title_match.group(1)) if title_match else "Guideline"
    html = (
        "<!doctype html>\n<html lang=\"vi\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{title}</title>\n<style>{CSS}</style>\n</head>\n<body>\n<main>\n{body}\n</main>\n"
        f"<script>{JS}</script>\n</body>\n</html>\n"
    )
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ Đã ghi {OUT.relative_to(HERE.parent)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
