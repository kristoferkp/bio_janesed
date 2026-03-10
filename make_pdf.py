import markdown2, weasyprint, pathlib, base64, re, os

md_path = pathlib.Path("analüüs.md")
md_text = md_path.read_text(encoding="utf-8")

def embed_image(match):
    alt = match.group(1)
    src = match.group(2)
    if os.path.exists(src):
        ext = src.rsplit(".", 1)[-1].lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
        data = base64.b64encode(pathlib.Path(src).read_bytes()).decode()
        return f'<img alt="{alt}" src="data:{mime};base64,{data}" style="max-width:100%;">'
    return match.group(0)

html_body = markdown2.markdown(md_text, extras=["tables", "fenced-code-blocks"])
html_body = re.sub(r'<img alt="([^"]*)" src="([^"]*)"[^>]*/>', embed_image, html_body)

html = """<!DOCTYPE html>
<html lang="et">
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6;
         max-width: 900px; margin: 0 auto; padding: 20px 40px; color: #222; }
  h1 { font-size: 18pt; border-bottom: 2px solid #444; padding-bottom: 6px; }
  h2 { font-size: 14pt; border-bottom: 1px solid #aaa; padding-bottom: 4px; margin-top: 28px; }
  h3 { font-size: 12pt; margin-top: 20px; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }
  th { background: #4a4a4a; color: white; padding: 6px 10px; text-align: left; }
  td { border: 1px solid #ccc; padding: 5px 10px; }
  tr:nth-child(even) { background: #f5f5f5; }
  img { max-width: 100%; margin: 10px 0; }
  hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
  code { background: #f0f0f0; padding: 1px 4px; border-radius: 3px; }
  strong { color: #111; }
</style>
</head>
<body>
""" + html_body + """
</body>
</html>"""

weasyprint.HTML(string=html, base_url=".").write_pdf("analüüs.pdf")
print("PDF created: analüüs.pdf")
