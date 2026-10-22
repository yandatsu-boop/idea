"""index.html の画像を data URI として埋め込み、単体で開ける standalone.html を作る。"""
import base64, re, pathlib
here = pathlib.Path(__file__).parent
html = (here / "index.html").read_text(encoding="utf-8")
for name in ("pizza", "cake", "okonomiyaki"):
    data = base64.b64encode((here / f"assets/{name}.png").read_bytes()).decode()
    html = html.replace(f"assets/{name}.png", f"data:image/png;base64,{data}")
(here / "standalone.html").write_text(html, encoding="utf-8")
# Artifact 公開用: 文書タグを除いた版
body = re.sub(r"<!DOCTYPE html>\s*<html[^>]*>\s*<head>", "", html)
body = re.sub(r'<meta name="viewport"[^>]*>\s*', "", body)
body = body.replace("</head>", "").replace("<body>", "").replace("</body>", "").replace("</html>", "")
body = body.replace("<title>", '<meta name="claude:viewport-fit-sides" content="cover">\n<title>', 1)
(here / "artifact.html").write_text(body, encoding="utf-8")
