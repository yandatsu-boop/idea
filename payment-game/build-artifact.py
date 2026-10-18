#!/usr/bin/env python3
"""index.html から、アーティファクト公開用の artifact.html を生成する。"""
import re, pathlib
d = pathlib.Path(__file__).parent
s = (d / "index.html").read_text(encoding="utf-8")
style = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
body = re.search(r"<body>(.*?)</body>", s, re.S).group(1)
script = re.search(r"<script>(.*?)</script>", body, re.S).group(1)
markup = re.sub(r"<script>.*?</script>", "", body, flags=re.S)
import json
src = json.dumps(s, ensure_ascii=False).replace("</", "<\\/")
out = ('<title>おかいけいゲーム</title>\n'
       '<meta name="claude:viewport-fit-sides" content="cover">\n'
       f'<style>{style}</style>\n{markup}\n<script>window.__APP_SOURCE__ = {src};</script>\n<script>{script}</script>\n')
(d / "artifact.html").write_text(out, encoding="utf-8")
