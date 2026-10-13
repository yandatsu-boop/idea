#!/usr/bin/env python3
"""images/ の絵を base64 にして index.html に埋め込み、HTML 1ファイルの index-single.html を作る。
使い方:  python3 build.py
"""
import base64, glob, json, os, subprocess, tempfile
here = os.path.dirname(os.path.abspath(__file__))
imgs = {}
for path in sorted(glob.glob(os.path.join(here, 'images', '*'))):
    name, ext = os.path.splitext(os.path.basename(path))
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
        continue
    out = os.path.join(tempfile.mkdtemp(), name + '.jpg')
    # 横幅900pxに縮小してJPEG化（macOS標準のsips。失敗したら元ファイルをそのまま使う）
    try:
        r = subprocess.run(['sips', '-Z', '900', '-s', 'format', 'jpeg', '-s', 'formatOptions', '75', path, '--out', out],
                           capture_output=True)
        ok = r.returncode == 0 and os.path.exists(out)
    except FileNotFoundError:  # sips が無い環境（Linux 等）
        ok = False
    use, mime = (out, 'image/jpeg') if ok else (path, 'image/' + ext[1:].replace('jpg', 'jpeg'))
    data = base64.b64encode(open(use, 'rb').read()).decode()
    imgs[name] = f'data:{mime};base64,{data}'
    print(f'{name}: {len(data)//1024} KB')
src = open(os.path.join(here, 'index.html'), encoding='utf-8').read()
marker = 'const EMBEDDED_IMAGES = {/*EMBED*/};'
assert marker in src
dst = src.replace(marker, 'const EMBEDDED_IMAGES = ' + json.dumps(imgs, ensure_ascii=False) + ';')
open(os.path.join(here, 'index-single.html'), 'w', encoding='utf-8').write(dst)
print(f'-> index-single.html ({len(dst)//1024} KB, 画像{len(imgs)}枚)')
