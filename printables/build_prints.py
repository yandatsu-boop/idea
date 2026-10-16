#!/usr/bin/env python3
"""生活算数プリント（A4・おもて/うら 1枚）×10枚 を作る。
使い方:  python3 build_prints.py   → prints.html / answers.html を作る
PDF化:   node render_pdf.js        → こころみプリント.pdf / こたえ.pdf
絵は ../keisan/images/part-*.png（けいさんアプリと同じ部品）を使う。
"""
import os, random

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = '../keisan/images/part-%s.png'

CSS = r"""
@page { size: A4; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; font-family: 'IPAGothic','IPAPGothic',sans-serif; color: #111; background: #fff }
.page { width: 210mm; height: 297mm; padding: 9mm 12mm 7mm; display: flex; flex-direction: column; gap: 2.4mm; page-break-after: always; overflow: hidden; position: relative }
.head { display: flex; align-items: center; gap: 4mm; border-bottom: 1.4mm solid #111; padding-bottom: 1.8mm }
.no { width: 13mm; height: 13mm; border-radius: 50%; background: #111; color: #fff; font-size: 8.5mm; font-weight: bold; display: flex; align-items: center; justify-content: center }
.title { font-size: 8mm; font-weight: bold; letter-spacing: .3mm }
.side { margin-left: auto; font-size: 4.2mm; border: .6mm solid #111; border-radius: 4mm; padding: .8mm 3.5mm }
.who { display: flex; gap: 10mm; font-size: 4.6mm; align-items: flex-end }
.who span { display: inline-block; border-bottom: .5mm solid #111; min-width: 55mm; height: 7mm }
.who .d { min-width: 0; width: 38mm }
.q { border: .7mm solid #111; border-radius: 3.5mm; padding: 2.6mm 3.8mm 2.8mm; display: flex; flex-direction: column; flex: 1 1 auto }
.q > :not(.qh) { flex: 1 1 auto }
.q > .cols { align-items: center }
.q > .match, .q > .seq, .q > .checks { align-content: center; align-items: center }
.qh { font-size: 5.8mm; font-weight: bold; display: flex; align-items: center; gap: 2.2mm; margin-bottom: 1.6mm }
.qn { width: 7.6mm; height: 7.6mm; border-radius: 50%; background: #111; color: #fff; font-size: 5mm; display: flex; align-items: center; justify-content: center; flex: none }
.qs { font-size: 3.8mm; font-weight: normal; color: #333 }
.rows { display: flex; flex-direction: column; gap: 1.2mm; justify-content: space-evenly }
.row { display: flex; align-items: center; gap: 4mm; min-height: 15mm }
.row.line { border-bottom: .3mm dashed #999; padding-bottom: 1.2mm }
.row.line:last-child { border-bottom: 0; padding-bottom: 0 }
.grp { display: flex; flex-wrap: wrap; gap: .8mm; align-items: center; align-content: center }
.grp img { height: 12.5mm; width: auto; display: block }
.grp.sm img { height: 8.5mm }
.grp.lg img { height: 14mm }
.grp.tiny img { height: 6.5mm }
.cell { flex: 1 1 0; min-width: 0 }
.trace { font-size: 17mm; line-height: 1; font-weight: bold; color: transparent; -webkit-text-stroke: .38mm #666; width: 17mm; text-align: center }
.trace.w { width: auto; letter-spacing: 2mm }
.box { display: inline-flex; width: 15mm; height: 15mm; border: .7mm solid #111; border-radius: 2.2mm; align-items: center; justify-content: center; font-size: 8mm; vertical-align: middle; flex: none }
.box.s { width: 11mm; height: 11mm; font-size: 6mm; border-radius: 1.8mm }
.box.w { width: 21mm }
.t { font-size: 7mm; font-weight: bold }
.t.s { font-size: 5.6mm }
.t.k { font-size: 4.8mm; font-weight: normal }
.dot { display: inline-block; width: 8mm; height: 8mm; border: .6mm solid #111; border-radius: 50%; margin: 0 .6mm; vertical-align: middle }
.dot.sm { width: 6.5mm; height: 6.5mm }
.cols { display: flex; gap: 3mm }
.cols > * { flex: 1 1 0; min-width: 0 }
.pt { width: 3.4mm; height: 3.4mm; border-radius: 50%; border: .6mm solid #111; flex: none }
.match { display: flex; justify-content: space-between; gap: 40mm; padding: 0 6mm }
.match .col { display: flex; flex-direction: column; gap: 3mm; align-items: stretch }
.match .it { display: flex; align-items: center; gap: 3mm; min-height: 15mm }
.match .t { white-space: nowrap }
.match .it.r { justify-content: flex-end }
.x { position: relative; display: inline-block }
.x::before, .x::after { content: ''; position: absolute; left: -6%; right: -6%; top: 50%; height: 0; border-top: .9mm solid #111 }
.x::before { transform: rotate(32deg) } .x::after { transform: rotate(-32deg) }
.xs img { opacity: .5 }
.frame { display: inline-grid; grid-template-columns: repeat(5, 8.2mm); grid-auto-rows: 8.2mm; border: .6mm solid #111; background: #fff }
.frame i { border: .3mm solid #666; display: flex; align-items: center; justify-content: center }
.frame i b { width: 5.4mm; height: 5.4mm; border-radius: 50%; background: #111; display: block }
.frame i b.o { background: transparent; border: .5mm solid #111 }
.frame i b.xx { background: #fff; border: .5mm solid #111; position: relative }
.frame i b.xx::after { content: '×'; position: absolute; inset: 0; font-size: 6mm; line-height: 5mm; text-align: center; font-weight: bold }
.eq { display: flex; align-items: center; gap: 2.4mm; flex-wrap: wrap }
.op { font-size: 9mm; font-weight: bold; width: 8mm; text-align: center }
.seq { display: flex; gap: 1.4mm; align-items: center; flex-wrap: wrap }
.seq .n { width: 12.6mm; height: 12.6mm; font-size: 7mm; border: .6mm solid #111; border-radius: 2mm; display: flex; align-items: center; justify-content: center }
.seq .n.b { border-style: solid; background: #fff }
.seq .n.g { border: .4mm dashed #888 }
.hint { font-size: 3.6mm; color: #333 }
.foot { margin-top: auto; display: flex; align-items: center; gap: 4mm; border-top: .5mm dashed #666; padding-top: 2mm; font-size: 4.4mm }
.stars { font-size: 8mm; letter-spacing: 1.6mm }
.stamp { width: 14mm; height: 14mm; border: .6mm dashed #666; border-radius: 50%; display: inline-block }
.tag { display: inline-flex; align-items: center; gap: 1.2mm; border: .6mm solid #111; border-radius: 2mm; padding: .5mm 2mm; font-size: 5.6mm; font-weight: bold; background: #fff }
.item { display: flex; flex-direction: column; align-items: center; gap: 1mm; text-align: center }
.item img { height: 14mm; width: auto; max-width: 30mm; object-fit: contain }
.item.lg img { height: 24mm; max-width: 30mm }
.nm { font-size: 3.8mm }
.coin { display: inline-block }
.coins { display: flex; flex-wrap: wrap; gap: 1.2mm; align-items: center }
.plate img { height: 10mm; width: auto; display: block }
.plate { border: .6mm solid #111; border-radius: 50% / 45%; height: 21mm; flex: 1 1 0; display: flex; align-items: center; justify-content: center; gap: 1mm; flex-wrap: wrap; padding: 1mm 4mm }
.order { border: .6mm solid #111; border-radius: 2mm; padding: 1.2mm 3mm; display: flex; align-items: center; gap: 2.4mm; background: #fff; white-space: nowrap }
.order img { height: 9mm; width: auto }
.coin { filter: none }
.stack { display: flex; flex-direction: column-reverse; align-items: center; justify-content: flex-start }
.stack img { display: block; width: 32mm; height: auto; margin-top: -3.6mm }
.stack img:first-child { margin-top: 0 }
.note { font-size: 3.7mm; color: #333 }
.big { font-size: 9mm; font-weight: bold }
.blank { border-bottom: .5mm solid #111; display: inline-block; min-width: 18mm; height: 8mm; vertical-align: bottom }
.checks { display: flex; flex-wrap: wrap; gap: 2mm 6mm; font-size: 4.6mm }
.checks span::before { content: '□ '; font-size: 5.6mm }
.clock { display: inline-block }
"""

# ---------------- 部品 ----------------
def im(name, h=None):
    st = f' style="height:{h}mm"' if h else ''
    return f'<img src="{IMG % name}"{st} alt="">'

def grp(name, n, size=''):
    return f'<div class="grp {size}">' + ''.join(im(name) for _ in range(n)) + '</div>'

def mix(names, size=''):
    return f'<div class="grp {size}">' + ''.join(im(n) for n in names) + '</div>'

def box(txt='', cls=''):
    return f'<span class="box {cls}">{txt}</span>'

def trace(n):
    return f'<div class="trace{" w" if len(str(n)) > 1 else ""}">{n}</div>'

def dots(n, sm=False):
    return ''.join(f'<i class="dot{" sm" if sm else ""}"></i>' for _ in range(n))

def frame(filled, crossed=0, total=10):
    cells = []
    for i in range(total):
        if i < filled - crossed:
            cells.append('<i><b></b></i>')
        elif i < filled:
            cells.append('<i><b class="xx"></b></i>')
        else:
            cells.append('<i></i>')
    return f'<div class="frame">{"".join(cells)}</div>'

def crossed(name, n, k):
    """n こ ならべて、うしろの k こに ×"""
    out = []
    for i in range(n):
        cls = 'x xs' if i >= n - k else ''
        out.append(f'<span class="{cls}">{im(name)}</span>' if cls else im(name))
    return f'<div class="grp sm" style="flex-wrap:nowrap">{"".join(out)}</div>'

COIN = {  # 金額: (ふち, 中, もじ)
    1: ('#555', '#e8e8e8'), 5: ('#555', '#f3e2a0'), 10: ('#555', '#e3b48e'),
    50: ('#555', '#dcdcdc'), 100: ('#555', '#e8e8e8'), 500: ('#555', '#f1dc9a'),
}
def coin(v, d=14):
    ring, fill = COIN[v]
    hole = '<circle cx="50" cy="50" r="8" fill="#fff" stroke="#555" stroke-width="2"/>' if v in (5, 50) else ''
    t = f'<text x="50" y="{58 if not hole else 80}" font-size="{26 if v < 100 else 22}" text-anchor="middle" font-weight="bold" fill="#111" font-family="IPAGothic">{v}</text>' if not hole else f'<text x="50" y="82" font-size="22" text-anchor="middle" font-weight="bold" fill="#111" font-family="IPAGothic">{v}</text>'
    return (f'<svg class="coin" width="{d}mm" height="{d}mm" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{fill}" stroke="#111" stroke-width="4"/>'
            f'<circle cx="50" cy="50" r="38" fill="none" stroke="#777" stroke-width="2"/>{hole}{t}</svg>')

def coins(spec, d=13):
    """spec: [(金額, こ数), ...]"""
    return '<div class="coins">' + ''.join(coin(v, d) for v, n in spec for _ in range(n)) + '</div>'

def clock(h, m=0, size=30, hands=True):
    import math
    pts = []
    for k in range(1, 13):
        a = math.radians(k * 30 - 90)
        pts.append(f'<text x="{50 + 36 * math.cos(a):.1f}" y="{50 + 36 * math.sin(a) + 4.2:.1f}" font-size="12" text-anchor="middle" font-weight="bold" font-family="IPAGothic">{k}</text>')
    ticks = ''.join(f'<line x1="{50 + 45 * math.cos(math.radians(k * 6)):.1f}" y1="{50 + 45 * math.sin(math.radians(k * 6)):.1f}" x2="{50 + 47.5 * math.cos(math.radians(k * 6)):.1f}" y2="{50 + 47.5 * math.sin(math.radians(k * 6)):.1f}" stroke="#111" stroke-width="1"/>' for k in range(60))
    hd = ''
    if hands:
        ha = math.radians((h % 12) * 30 + m * 0.5 - 90); ma = math.radians(m * 6 - 90)
        hd = (f'<line x1="50" y1="50" x2="{50 + 22 * math.cos(ha):.1f}" y2="{50 + 22 * math.sin(ha):.1f}" stroke="#111" stroke-width="5.2" stroke-linecap="round"/>'
              f'<line x1="50" y1="50" x2="{50 + 33 * math.cos(ma):.1f}" y2="{50 + 33 * math.sin(ma):.1f}" stroke="#111" stroke-width="2.6" stroke-linecap="round"/>')
    return (f'<svg class="clock" width="{size}mm" height="{size}mm" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48.5" fill="#fff" stroke="#111" stroke-width="3"/>{ticks}'
            f'{"".join(pts)}{hd}<circle cx="50" cy="50" r="3" fill="#111"/></svg>')

def stack_html(layers):
    return '<div class="stack">' + ''.join(im(n) for n in layers) + '</div>'

def tag(price):
    return f'<span class="tag">{price}<span style="font-size:4.4mm">えん</span></span>'

def item(name, label='', lg=False):
    return f'<div class="item{" lg" if lg else ""}">{im(name)}<span class="nm">{label}</span></div>'

# ---------------- ページの つくり ----------------
ANS = {}   # こたえ: シート番号 -> [(ばんごう, こたえ)]
GUIDE = {}  # シート番号 -> (たいとる, ねらい, ポイント[])
def ans(sheet, label, text):
    ANS.setdefault(sheet, []).append((label, text))

def Q(n, title, body, sub=''):
    s = f'<span class="qs">{sub}</span>' if sub else ''
    return f'<div class="q"><div class="qh"><span class="qn">{n}</span>{title}{s}</div>{body}</div>'

def page(no, title, side, blocks, foot):
    who = '<div class="who"><div>なまえ <span></span></div><div>ひづけ <span class="d"></span></div></div>'
    head = f'<div class="head"><div class="no">{no}</div><div class="title">{title}</div><div class="side">{side}</div></div>'
    return f'<section class="page">{head}{who}{"".join(blocks)}{foot}</section>'

def foot_front():
    return '<div class="foot"><span>うらにも つづくよ →</span><span class="stars" style="margin-left:auto">☆ ☆ ☆</span></div>'

def foot_back(extra=''):
    return f'<div class="foot"><span>{extra or "できたら シールを はろう"}</span><span class="stamp" style="margin-left:auto"></span><span class="stamp"></span><span class="stamp"></span></div>'

def row(*cells, line=True):
    return f'<div class="row{" line" if line else ""}">{"".join(cells)}</div>'

NIG = ['nigiri-tuna', 'nigiri-salmon', 'nigiri-egg', 'nigiri-shrimp', 'nigiri-squid', 'nigiri-ikura', 'nigiri-eel']
TOP = ['topping-salami', 'topping-corn', 'topping-shrimp', 'topping-mushroom', 'topping-pineapple', 'topping-pepper']
CAR = ['pl-car-train', 'pl-car-keihan', 'pl-car-kintetsu', 'pl-car-shinkansen', 'pl-car-sl']

PAGES = []

# ===== 1 かぞえてみよう① (1〜5) =====
def s1():
    no, t = 1, 'かぞえてみよう ①（1〜5）'
    GUIDE[no] = (t, '1〜5のものを、1つずつ指さしながら数え、数字と対応させる（数量の基礎・数唱）。',
                 ['指でさわりながら「いち、に、さん」と声に出して数える。', 'うすい数字は「なぞり書き」。書くことが難しい場合は、ボックスに数字カードを置いてもよい。', '数え終わりに「ぜんぶで」と言葉を添えると、数のまとまりに気づきやすい。'])
    pick = [0, 1, 2, 3, 5]
    r = [row(grp(NIG[pick[i]], i + 1), trace(i + 1), box(), line=True) for i in range(5)]
    for i in range(5): ans(no, f'おもて①-{i+1}', str(i + 1))
    f1 = Q(1, 'かぞえて、すうじを なぞろう', f'<div class="rows">{"".join(r)}</div>', '（ゆびで さわって かぞえよう）')
    # 2 かぞえて かく
    items = [(TOP[0], 3), (TOP[1], 1), (TOP[2], 4)]
    rr = []
    for k, (nm, n) in enumerate(items):
        rr.append(row(grp(nm, n, 'lg'), '<span class="t">＝</span>', box(), '<span class="t s">こ</span>'))
        ans(no, f'おもて②-{k+1}', f'{n}こ')
    f2 = Q(2, 'いくつ あるかな？ □に かこう', f'<div class="rows">{"".join(rr)}</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    # うら
    left = [(TOP[0], 2), (TOP[1], 5), (TOP[2], 3)]
    right = [3, 2, 5]
    mm = ''.join(f'<div class="it">{grp(n, c, "sm")}<span class="pt"></span></div>' for n, c in left)
    mr = ''.join(f'<div class="it r"><span class="pt"></span><span class="t">{v}</span></div>' for v in right)
    ans(no, 'うら③', '2→2、5→5、3→3 を むすぶ')
    b3 = Q(3, 'おなじ かずを せんで むすぼう', f'<div class="match"><div class="col">{mm}</div><div class="col">{mr}</div></div>')
    asks = [(3, NIG[0]), (1, NIG[1]), (5, NIG[2])]
    ar = []
    for k, (n, nm) in enumerate(asks):
        ar.append(row(f'<div class="order">{im(nm)}<span class="t s">{n}こ</span></div>', f'<div>{dots(5, True)}</div>', '<span class="hint">（かずだけ ぬろう）</span>'))
        ans(no, f'うら④-{k+1}', f'○を {n}こ ぬる')
    b4 = Q(4, 'かずだけ ○を ぬろう', f'<div class="rows">{"".join(ar)}</div>')
    tr = []
    for k, n in enumerate([2, 4, 5]):
        tr.append(row(grp('pl-car-keihan' if k != 1 else 'pl-car-train', n, 'sm'), '<span class="t s">＝</span>', box('', 's'), '<span class="t s">りょう</span>'))
        ans(no, f'うら⑤-{k+1}', f'{n}りょう')
    b5 = Q(5, 'でんしゃは なんりょう？', f'<div class="rows">{"".join(tr)}</div>')
    b6 = Q(6, 'おうちで やってみよう', '<div class="t k" style="line-height:1.9">おうちの ひとと いっしょに かぞえよう。　コップは <span class="blank"></span> こ　　おさらは <span class="blank"></span> まい</div>')
    back = page(no, t, 'うら', [b3, b4, b5, b6], foot_back())
    PAGES.extend([front, back])

# ===== 2 かぞえてみよう② (6〜10) =====
def s2():
    no, t = 2, 'かぞえてみよう ②（6〜10）'
    GUIDE[no] = (t, '10までの数を数え、10のまとまり（十のわく）で数の大きさをとらえる。「あといくつで10」の素地。',
                 ['十のわく（2×5）に黒丸を置くと、5と5のまとまりが見えやすい。', '「あと いくつで 10？」は、空いているマスを指さして数える。', 'なぞり書きが難しい児童は、数字カードを置いて対応させる。'])
    rows = []
    for k, n in enumerate(range(6, 11)):
        rows.append(row(frame(n), trace(n), box(), '<span class="t s">こ</span>'))
        ans(no, f'おもて①-{k+1}', str(n))
    f1 = Q(1, '○の かずを かぞえて かこう', f'<div class="rows">{"".join(rows)}</div>', '（なぞってから かこう）')
    rr = []
    for k, n in enumerate([7, 8, 9, 6]):
        rr.append(row(frame(n), '<span class="t s">あと</span>', box(), '<span class="t s">こで 10</span>'))
        ans(no, f'おもて②-{k+1}', str(10 - n))
    f2 = Q(2, 'あと いくつで 10 かな？', f'<div class="rows">{"".join(rr)}</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    seqs = [[1, 2, None, 4, 5, None, 7, 8, None, 10], [2, None, 4, None, 6, 7, None, 9, None, 10]]
    sh = []
    for k, sq in enumerate(seqs):
        cells = ''.join(f'<div class="n b"></div>' if v is None else f'<div class="n">{v}</div>' for v in sq)
        sh.append(f'<div class="seq">{cells}</div>')
        ans(no, f'うら③-{k+1}', '、'.join(str(i + 1) for i, v in enumerate(sq) if v is None))
    b3 = Q(3, 'かずの ならび。□に かこう', f'<div class="rows">{"".join(sh)}</div>')
    sets = [(3, 8, 5), (10, 6, 9), (4, 7, 2)]
    sr = []
    for k, st in enumerate(sets):
        cells = ''.join(f'<div class="cell">{grp(TOP[j], v, "tiny")}<div class="hint">（　）</div></div>' for j, v in enumerate(st))
        sr.append(f'<div class="cols">{cells}</div>')
        ans(no, f'うら④-{k+1}', f'{max(st)}こ の ほう')
    b4 = Q(4, 'いちばん おおい ほうに ○', f'<div class="rows">{"".join(sr)}</div>')
    b5 = Q(5, '1から 10まで なぞって かこう', '<div class="seq" style="gap:2mm">' + ''.join(f'<div class="trace" style="font-size:12mm;width:15mm">{i}</div>' for i in range(1, 11)) + '</div>')
    b6 = Q(6, 'おうちで やってみよう', '<div class="t k" style="line-height:1.9">ゆびは ぜんぶで いくつ？ <span class="blank"></span> ほん。　おうちの かいだんは <span class="blank"></span> だん。</div>')
    back = page(no, t, 'うら', [b3, b4, b5, b6], foot_back())
    PAGES.extend([front, back])

# ===== 3 〜こ ください =====
def s3():
    no, t = 3, '「〜こ ください」'
    GUIDE[no] = (t, '注文の数だけものを取り出す（数の取り出し・基数）。買い物場面の「〜こください」と数をつなぐ。',
                 ['最初は実物（ミニチュアやブロック）で取り分け、プリントでは○で表す。', '「3こ」と声に出して言いながら○をかく。', '「あと いくつ」は、足りない分を数える加法的な考え方につながる。'])
    orders = [(NIG[0], 'まぐろ', 3), (NIG[2], 'たまご', 2), (NIG[1], 'サーモン', 4)]
    rr = []
    for k, (nm, jp, n) in enumerate(orders):
        rr.append(row(f'<div class="order">{im(nm)}<span class="t s">{jp} {n}こ</span></div>', '<div class="plate"><span class="hint">ここに ○を かこう</span></div>'))
        ans(no, f'おもて①-{k+1}', f'{n}こ ○をかく')
    f1 = Q(1, 'ちゅうもんの かずだけ おさらに ○を かこう', f'<div class="rows">{"".join(rr)}</div>', '（「〜こ ください」）')
    rows = []
    for k, (nm, jp, n, have) in enumerate([(NIG[3], 'えび', 2, 5), (NIG[5], 'いくら', 3, 6), (NIG[6], 'うなぎ', 1, 4)]):
        rows.append(row(f'<div class="order">{im(nm)}<span class="t s">{jp} {n}こ</span></div>', f'<div class="plate">{"".join(im(nm) for _ in range(have))}</div>', '<span class="hint">ちゅうもんの かずだけ のこして ×</span>'))
        ans(no, f'おもて②-{k+1}', f'{have - n}こ に ×をつける（のこり {n}こ）')
    f2 = Q(2, 'おおすぎる！ ちゅうもんの かずに あわせて ×を つけよう', f'<div class="rows">{"".join(rows)}</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    o3 = [('ピザ', 3), ('ポテト', 5), ('ジュース', 2), ('ハンバーガー', 4)]
    rr = []
    for k, (jp, n) in enumerate(o3):
        rr.append(row(f'<div class="order"><span class="t s">{jp}　{n}こ</span></div>', f'<div>{dots(6, True)}</div>', '<span class="hint">（かずだけ ぬろう）</span>'))
        ans(no, f'うら③-{k+1}', f'○を {n}こ ぬる')
    b3 = Q(3, 'もじの ちゅうもんを よんで ○を ぬろう', f'<div class="rows">{"".join(rr)}</div>')
    ps = [(TOP[0], 'サラミ', 4, 2), (TOP[2], 'えび', 5, 3), (TOP[3], 'マッシュルーム', 3, 1)]
    pr = []
    for k, (nm, jp, need, have) in enumerate(ps):
        pr.append(row(f'<div class="order">{im(nm)}<span class="t s">{jp} {need}こ</span></div>', f'<div class="plate" style="flex:none;width:55mm">{"".join(im(nm) for _ in range(have))}</div>', '<span class="t s">あと</span>', box(), '<span class="t s">こ</span>'))
        ans(no, f'うら④-{k+1}', f'{need - have}こ')
    b4 = Q(4, 'たりない！ あと いくつ いるかな？', f'<div class="rows">{"".join(pr)}</div>')
    b5 = Q(5, 'おみせやさんごっこを しよう', '<div class="t k" style="line-height:1.9">おうちの ひとが おきゃくさん。「〜こ ください」と いわれた かずを わたそう。<br>きょうの おみせ：<span class="blank" style="min-width:45mm"></span>　わたした かず <span class="blank"></span> こ</div>')
    back = page(no, t, 'うら', [b3, b4, b5], foot_back())
    PAGES.extend([front, back])

# ===== 4 くらべよう =====
def s4():
    no, t = 4, 'くらべよう'
    GUIDE[no] = (t, '数・長さ・高さを比べ、「多い／少ない」「長い／短い」「高い／低い」を判断する。数字の大小の比較へ進む。',
                 ['最初は絵（具体物）で、ひとつずつ線で結んで比べる方法を教える。', '実際に電車のおもちゃや積み木を並べて、長さや高さを比べる活動と組み合わせる。', '数が同じときは「おなじ」と答えることも教える。'])
    prs = [(NIG[0], 4, 7), (TOP[1], 6, 3), (TOP[4], 5, 8)]
    rr = []
    for k, (nm, a, b) in enumerate(prs):
        rr.append(row(f'<div class="cell">{grp(nm, a, "sm")}</div>', '<span class="t">と</span>', f'<div class="cell">{grp(nm, b, "sm")}</div>'))
        ans(no, f'おもて①-{k+1}', f'{"みぎ" if b > a else "ひだり"}（{max(a,b)}こ）')
    f1 = Q(1, 'おおい ほうに ○を つけよう', f'<div class="rows">{"".join(rr)}</div>')
    prs2 = [(TOP[5], 2, 5), (TOP[3], 8, 4), (NIG[3], 3, 6)]
    rr2 = []
    for k, (nm, a, b) in enumerate(prs2):
        rr2.append(row(f'<div class="cell">{grp(nm, a, "sm")}</div>', '<span class="t">と</span>', f'<div class="cell">{grp(nm, b, "sm")}</div>'))
        ans(no, f'おもて②-{k+1}', f'{"ひだり" if a < b else "みぎ"}（{min(a,b)}こ）')
    f2 = Q(2, 'すくない ほうに △を つけよう', f'<div class="rows">{"".join(rr2)}</div>')
    nums = [(3, 5), (8, 6), (2, 9), (7, 4), (10, 1)]
    nr = '<div class="seq" style="gap:7mm">' + ''.join(f'<div style="display:flex;gap:3mm;align-items:center;font-size:8mm"><span class="box">{a}</span>と<span class="box">{b}</span></div>' for a, b in nums) + '</div>'
    for k, (a, b) in enumerate(nums): ans(no, f'おもて③-{k+1}', f'{max(a,b)}')
    f3 = Q(3, 'すうじの おおきい ほうに ○を つけよう', nr)
    front = page(no, t, 'おもて', [f1, f2, f3], foot_front())
    tr = [(2, 5), (4, 3), (1, 6)]
    rr3 = []
    for k, (a, b) in enumerate(tr):
        rr3.append(row(f'<div class="cell">{grp(CAR[k], a, "sm")}</div>', '<span class="t">と</span>', f'<div class="cell">{grp(CAR[k + 1], b, "sm")}</div>'))
        ans(no, f'うら④-{k+1}', f'{"ひだり" if a > b else "みぎ"}（{max(a,b)}りょう）')
    b4 = Q(4, 'ながい でんしゃに ○を つけよう', '<div class="rows">' + ''.join(rr3) + '</div>')
    b5 = Q(5, 'たかい バーガーに ○を つけよう', '<div class="cols" style="justify-content:space-around;align-items:flex-end">' + ''.join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:1mm;min-height:52mm;justify-content:flex-end">{stack_html(ly)}<span class="box s"></span></div>' for ly in [
            ['bunB', 'patty-beef', 'bunT'], ['bunB', 'lettuce', 'tomato', 'patty-beef', 'cheese', 'patty-beef', 'bunT'], ['bunB', 'patty-beef', 'lettuce', 'bunT']]) + '</div>', '（1・2・3のうち、いちばん たかいのは？）')
    ans(no, 'うら⑤', '2ばんめ（7だん）')
    b6 = Q(6, 'おうちで くらべよう', '<div class="t k" style="line-height:1.9">おうちの ひとと てを くらべよう。 おおきい ひとは？ <span class="blank" style="min-width:35mm"></span>　せが たかい ひとは？ <span class="blank" style="min-width:35mm"></span></div>')
    ans(no, 'うら⑥', '（かいたものを みて ○）')
    back = page(no, t, 'うら', [b4, b5, b6], foot_back())
    PAGES.extend([front, back])

# ===== 5 ふえるよ（たしざん） =====
def s5():
    no, t = 5, 'ふえるよ（たしざん 10まで）'
    GUIDE[no] = (t, '「ふえる」「あわせる」場面を絵で理解し、10までのたし算を式で表す。', ['絵 → 十のわく → 式の順に、抽象度を上げていく。', '「2こに 1こ ふえて 3こ」と、お話の言葉で言いながら式を読む。', 'わく（■）は左から詰めて置く。'])
    pr = [(NIG[0], 2, 1), (NIG[1], 3, 2), (NIG[2], 1, 4), (NIG[3], 3, 3)]
    rr = []
    for k, (nm, a, b) in enumerate(pr):
        rr.append(row(grp(nm, a, 'sm'), '<span class="op">＋</span>', grp(nm, b, 'sm'), '<span class="op">＝</span>', box()))
        ans(no, f'おもて①-{k+1}', f'{a}＋{b}＝{a + b}')
    f1 = Q(1, 'ふえたら ぜんぶで なんこ？', f'<div class="rows">{"".join(rr)}</div>')
    pr2 = [(4, 3), (5, 2), (6, 3)]
    rr2 = []
    for k, (a, b) in enumerate(pr2):
        rr2.append(row(frame(a), '<span class="op">＋</span>', frame(b), '<span class="op">＝</span>', box()))
        ans(no, f'おもて②-{k+1}', f'{a}＋{b}＝{a + b}')
    f2 = Q(2, '□の ○を あわせて かぞえよう', f'<div class="rows">{"".join(rr2)}</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    ex = [(1, 1), (2, 3), (4, 2), (5, 4), (3, 6), (7, 2), (6, 3), (5, 5)]
    lines = []
    for k, (a, b) in enumerate(ex):
        lines.append(f'<div class="eq" style="font-size:8mm"><span>{a}</span><span class="op">＋</span><span>{b}</span><span class="op">＝</span>{box("", "s")}</div>')
        ans(no, f'うら③-{k+1}', f'{a}＋{b}＝{a + b}')
    b3 = Q(3, 'けいさんを しよう', '<div class="cols" style="flex-wrap:wrap;row-gap:4mm"><div style="flex:0 0 48%">' + lines[0] + '</div><div style="flex:0 0 48%">' + lines[1] + '</div>' + ''.join(f'<div style="flex:0 0 48%">{l}</div>' for l in lines[2:]) + '</div>')
    st = [('ピザが 3まい ありました。 2まい ふえました。 ぜんぶで なんまい？', TOP[0], 3, 2), ('おすしが 4こ ありました。 5こ ふえました。 ぜんぶで なんこ？', NIG[1], 4, 5)]
    sr = []
    for k, (txt, nm, a, b) in enumerate(st):
        sr.append(f'<div class="t k" style="line-height:1.7">{txt}</div>' + row(grp(nm, a, 'sm'), '<span class="op">＋</span>', grp(nm, b, 'sm'), line=False) + f'<div class="eq" style="font-size:8mm;margin-bottom:2mm">しき <span class="box w"></span><span class="op">＝</span>{box()}</div>')
        ans(no, f'うら④-{k+1}', f'{a}＋{b}＝{a + b}')
    b4 = Q(4, 'おはなしを よんで しきを かこう', '<div class="rows">' + ''.join(sr) + '</div>')
    back = page(no, t, 'うら', [b3, b4], foot_back())
    PAGES.extend([front, back])

# ===== 6 へるよ（ひきざん） =====
def s6():
    no, t = 6, 'へるよ（ひきざん 10まで）'
    GUIDE[no] = (t, '「へる」「のこり」の場面を絵で理解し、10までのひき算を式で表す。', ['「食べた分に×」を指でなぞってから、のこりを数える。', '0（ぜんぶ なくなる）の場面も扱う。', 'たし算との違いを「ふえる／へる」の言葉で確かめる。'])
    pr = [(NIG[0], 5, 2), (NIG[2], 4, 1), (NIG[3], 6, 3), (NIG[1], 7, 2)]
    rr = []
    for k, (nm, a, b) in enumerate(pr):
        rr.append(row(crossed(nm, a, b), '<span class="op">＝</span>', box(), '<span class="hint">（×を ひいた のこり）</span>'))
        ans(no, f'おもて①-{k+1}', f'{a}－{b}＝{a - b}')
    f1 = Q(1, '×の ぶんを たべたよ。 のこりは？', f'<div class="rows">{"".join(rr)}</div>')
    pr2 = [(8, 3), (9, 4), (7, 5)]
    rr2 = []
    for k, (a, b) in enumerate(pr2):
        rr2.append(row(frame(a, b), '<span class="op">＝</span>', box(), '<span class="hint">（×を ひいた のこり）</span>'))
        ans(no, f'おもて②-{k+1}', f'{a}－{b}＝{a - b}')
    f2 = Q(2, '○から ×を ひいて のこりは？', f'<div class="rows">{"".join(rr2)}</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    ex = [(5, 1), (6, 2), (8, 3), (9, 4), (7, 5), (10, 3), (8, 8), (10, 6)]
    lines = []
    for k, (a, b) in enumerate(ex):
        lines.append(f'<div class="eq" style="font-size:8mm"><span>{a}</span><span class="op">－</span><span>{b}</span><span class="op">＝</span>{box("", "s")}</div>')
        ans(no, f'うら③-{k+1}', f'{a}－{b}＝{a - b}')
    b3 = Q(3, 'けいさんを しよう', '<div class="cols" style="flex-wrap:wrap;row-gap:4mm">' + ''.join(f'<div style="flex:0 0 48%">{l}</div>' for l in lines) + '</div>')
    st = [('ピザが 6まい ありました。 2まい たべました。 のこりは なんまい？', TOP[0], 6, 2), ('おすしが 8こ ありました。 3こ たべました。 のこりは なんこ？', NIG[1], 8, 3)]
    sr = []
    for k, (txt, nm, a, b) in enumerate(st):
        sr.append(f'<div class="t k" style="line-height:1.7">{txt}</div>' + row(crossed(nm, a, b), line=False) + f'<div class="eq" style="font-size:8mm;margin-bottom:2mm">しき <span class="box w"></span><span class="op">＝</span>{box()}</div>')
        ans(no, f'うら④-{k+1}', f'{a}－{b}＝{a - b}')
    b4 = Q(4, 'おはなしを よんで しきを かこう', '<div class="rows">' + ''.join(sr) + '</div>')
    back = page(no, t, 'うら', [b3, b4], foot_back())
    PAGES.extend([front, back])

# ===== 7 おかね =====
def s7():
    no, t = 7, 'おかねを しろう'
    GUIDE[no] = (t, '硬貨の種類と金額を知り、同じ硬貨・異なる硬貨の合計を数える（貨幣の理解・十進位取りの素地）。',
                 ['本物の硬貨（または模型）を並べて、1円玉から順に触れる。', '10円玉は「10、20、30…」と10ずつ数える。', '10円玉と1円玉の混合は、「10円玉が何こ」と「1円玉が何こ」を分けて考える。'])
    names = {1: '1えんだま', 5: '5えんだま', 10: '10えんだま', 50: '50えんだま', 100: '100えんだま'}
    cl = '<div class="cols" style="justify-content:space-around;text-align:center">' + ''.join(f'<div class="item">{coin(v, 28)}<span class="nm" style="font-size:5mm">{names[v]}</span></div>' for v in (1, 5, 10, 50, 100)) + '</div>'
    f1 = Q(1, 'おかねの なまえを いってみよう', cl)
    rr = []
    for k, (v, n) in enumerate([(1, 3), (1, 6), (10, 2), (10, 4), (10, 5)]):
        rr.append(row(coins([(v, n)], 14), '<span class="t s">＝</span>', box('', 'w'), '<span class="t s">えん</span>'))
        ans(no, f'おもて②-{k+1}', f'{v * n}えん')
    f2 = Q(2, 'おなじ おかねを かぞえよう。 いくら？', f'<div class="rows">{"".join(rr)}</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    mx = [(2, 3), (1, 6), (3, 4), (4, 0), (5, 2)]
    mr = []
    for k, (tn, on) in enumerate(mx):
        mr.append(row(coins([(10, tn), (1, on)], 14), '<span class="t s">＝</span>', box('', 'w'), '<span class="t s">えん</span>'))
        ans(no, f'うら③-{k+1}', f'{tn * 10 + on}えん')
    b3 = Q(3, '10えんだまと 1えんだま。 いくら？', f'<div class="rows">{"".join(mr)}</div>', '（10えんだまは 10、20、30…）')
    wl = [[(50, 1), (10, 2)], [(10, 4), (5, 2)], [(100, 1)], [(50, 1), (10, 3)]]
    wr = []
    for k, sp in enumerate(wl):
        wr.append(row(coins(sp, 14), '<span class="t s">＝</span>', box('', 'w'), '<span class="t s">えん</span>'))
        ans(no, f'うら④-{k+1}', f'{sum(v * c for v, c in sp)}えん')
    b4 = Q(4, 'さいふに いくら はいって いる？', f'<div class="rows">{"".join(wr)}</div>')
    b5 = Q(5, 'おうちで みつけよう', '<div class="t k" style="line-height:1.9">おうちに ある おかねを みて、1えんだま・10えんだま・100えんだまを さがそう。 みつけた おかね <span class="blank" style="min-width:55mm"></span></div>')
    back = page(no, t, 'うら', [b3, b4, b5], foot_back())
    PAGES.extend([front, back])

# ===== 8 おかいもの =====
def s8():
    no, t = 8, 'おかいもの'
    GUIDE[no] = (t, '値段を読み、予算内で買えるか判断する。2つの値段の合計と、おつりを求める（買い物の計算）。',
                 ['実際の値札・チラシと組み合わせると、生活とつながる。', '100円単位・10円単位の数に絞って始める。', 'おつりは「出したお金 − 値段」を、お金の絵（硬貨）を引いて確かめる。'])
    it = [(NIG[0], 'おすし', 100), (TOP[0], 'ピザ', 300), (None, 'ハンバーガー', 250), ('side-tea', 'おちゃ', 80), ('side-soy', 'しょうゆ', 50)]
    def one(nm, jp, price, img=None):
        return f'<div class="item lg">{im(img or nm) if (img or nm) else ""}<span class="nm" style="font-size:4.4mm">{jp}</span>{tag(price)}</div>'
    pic = '<div class="cols" style="align-items:flex-end">' + ''.join([
        one(NIG[0], 'おすし', 100), one('pizzabase-thin-tomato', 'ピザ', 300), one('bunT', 'ハンバーガー', 250), one('side-tea', 'おちゃ', 80), one('side-soy', 'しょうゆ', 50)]) + '</div>'
    f1 = Q(1, 'ねだんを よもう。 「えん」と いって みよう', pic)
    qs = [(100, [('おちゃ', 80), ('おすし', 100), ('ピザ', 300)]), (300, [('ジュース', 150), ('ハンバーガー', 250), ('おおきい ピザ', 500), ('ステーキ', 800)])]
    rr = []
    for k, (money, lst) in enumerate(qs):
        tags = ''.join(f'<div class="order"><span class="t s">{n}</span>{tag(p)}<span class="pt"></span></div>' for n, p in lst)
        rr.append(f'<div class="t k" style="margin:1mm 0">もっている おかねは <b style="font-size:7mm">{money}えん</b>。 かえる ものに ○ を つけよう</div><div class="coins" style="gap:3mm;margin-bottom:2mm">{tags}</div>')
        ans(no, f'おもて②-{k+1}', '、'.join(n for n, p in lst if p <= money) + ' に ○')
    f2 = Q(2, 'おかねで かえる ものに ○を つけよう', ''.join(rr))
    pr = [('ポテト', 120, [(100, 1), (10, 2)]), ('ジュース', 150, [(100, 1), (50, 1)])]
    zr = []
    for k, (n, p, sp) in enumerate(pr):
        h, tt, o = (p // 100), (p % 100) // 10, 0
        zr.append(row(f'<div class="order"><span class="t s">{n}</span>{tag(p)}</div>', f'<span class="t s">100えんだま</span>{box("", "s")}<span class="t s">こ　10えんだま</span>{box("", "s")}<span class="t s">こ</span>' if p % 100 != 50 else f'<span class="t s">100えんだま</span>{box("", "s")}<span class="t s">こ　50えんだま</span>{box("", "s")}<span class="t s">こ</span>'))
        ans(no, f'おもて③-{k+1}', f'100えんだま {p // 100}こ、' + (f'10えんだま {(p % 100) // 10}こ' if p % 100 != 50 else '50えんだま 1こ'))
    f3 = Q(3, 'ちょうど はらうには？ おかねの かずを かこう', '<div class="rows">' + ''.join(zr) + '</div>')
    front = page(no, t, 'おもて', [f1, f2, f3], foot_front())
    ex = [('おすし', 100, 'ポテト', 120), ('ピザ', 300, 'ジュース', 150), ('おちゃ', 80, 'しょうゆ', 50), ('バーガー', 250, 'おちゃ', 80)]
    er = []
    for k, (a, pa, b, pb) in enumerate(ex):
        er.append(row(f'<div class="order"><span class="t s">{a}</span>{tag(pa)}</div>', '<span class="op">＋</span>', f'<div class="order"><span class="t s">{b}</span>{tag(pb)}</div>', '<span class="op">＝</span>', box('', 'w'), '<span class="t s">えん</span>'))
        ans(no, f'うら④-{k+1}', f'{pa + pb}えん')
    b4 = Q(4, 'あわせて いくら？', '<div class="rows">' + ''.join(er) + '</div>')
    ot = [(100, 70), (500, 300), (100, 60), (1000, 800), (500, 450)]
    orr = []
    for k, (pay, pr_) in enumerate(ot):
        orr.append(row(f'<div class="order">だした おかね <b style="font-size:6mm">{pay}えん</b></div>', f'<div class="order">ねだん {tag(pr_)}</div>', '<span class="t s">おつり</span>', box('', 'w'), '<span class="t s">えん</span>'))
        ans(no, f'うら⑤-{k+1}', f'{pay - pr_}えん')
    b5 = Q(5, 'おつりは いくら？', '<div class="rows">' + ''.join(orr) + '</div>', '（だした おかね − ねだん）')
    back = page(no, t, 'うら', [b4, b5], foot_back('おうちの ひとと レシートを みてみよう'))
    PAGES.extend([front, back])

# ===== 9 とけい =====
def s9():
    no, t = 9, 'とけいを よもう'
    GUIDE[no] = (t, '時計の長い針・短い針を区別し、「〜時」「〜時半」を読み、生活の場面と時刻を結びつける。',
                 ['最初は「短い針が数字を指しているときは、長い針は12」とセットで確認する。', '1日の流れ（起きる・給食・帰る・寝る）に時刻を貼り付けると、生活リズムが見える。', '時計は実物（アナログ時計）を一緒に動かしながら取り組む。'])
    tm = [3, 7, 12, 9]
    rr = '<div class="cols" style="text-align:center;justify-content:space-around">' + ''.join(f'<div class="item">{clock(h, 0, 33)}{box("", "s")}<span class="nm">じ</span></div>' for h in tm) + '</div>'
    for k, h in enumerate(tm): ans(no, f'おもて①-{k+1}', f'{h}じ')
    f1 = Q(1, 'とけいを よんで □に かこう', rr)
    ev = [('おきる', 'side-tea', 7), ('きゅうしょく', 'maki-tuna', 12), ('かえる', 'pl-car-train', 3), ('ねる', None, 9)]
    moon = '<span class="t">☾</span>'
    left = ''.join('<div class="it">' + (im(i) if i else moon) + f'<span class="t s">{n}</span><span class="pt"></span></div>' for n, i, _ in ev)
    order = [2, 0, 3, 1]
    right = ''.join(f'<div class="it r"><span class="pt"></span>{clock(ev[i][2], 0, 24)}</div>' for i in order)
    ans(no, 'おもて②', 'おきる→7じ、きゅうしょく→12じ、かえる→3じ、ねる→9じ')
    f2 = Q(2, 'いちにちの ながれと とけいを せんで むすぼう', f'<div class="match" style="gap:28mm"><div class="col">{left}</div><div class="col">{right}</div></div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    tm3 = [4, 10, 1, 6]
    bl = '<div class="cols" style="text-align:center;justify-content:space-around">' + ''.join(f'<div class="item"><span class="t">{h}じ</span>{clock(h, 0, 33, hands=False)}</div>' for h in tm3) + '</div>'
    for k, h in enumerate(tm3): ans(no, f'うら③-{k+1}', f'みじかい はりを {h}、ながい はりを 12 に かく')
    b3 = Q(3, 'はりを かこう', bl, '（みじかい はり ＝ 「じ」、ながい はり ＝ 12）')
    hm = [(2, 30), (5, 30), (8, 30)]
    hr = '<div class="cols" style="text-align:center;justify-content:space-around">' + ''.join(f'<div class="item">{clock(h, m, 33)}<span><span class="box s"></span><span class="nm">じはん</span></span></div>' for h, m in hm) + '</div>'
    for k, (h, m) in enumerate(hm): ans(no, f'うら④-{k+1}', f'{h}じはん')
    b4 = Q(4, '「〜じはん」を よもう', hr, '（ながい はりが 6 のとき ＝ はん）')
    b5 = Q(5, 'おうちで みよう', '<div class="t k" style="line-height:1.9">おうちの とけいで みよう。 あさ おきた じかん <span class="blank"></span> じ　ゆうごはんの じかん <span class="blank"></span> じ</div>')
    back = page(no, t, 'うら', [b3, b4, b5], foot_back())
    PAGES.extend([front, back])

# ===== 10 パーティーの じゅんび =====
def s10():
    no, t = 10, 'パーティーの じゅんび'
    GUIDE[no] = (t, '「1人に○こずつ」の同数のまとまりを数え、同数加（かけ算の素地）と人数分の準備を行う。',
                 ['お皿に置いた同じ数を、「2、4、6」と数え足す活動につなげる。', '「ひとり 2こ × 3にん」は、まだ式（×）にせず、お話と絵で理解する。', '実際のパーティー（学習発表会の準備・お楽しみ会）で使う数を決めると、学習が生活とつながる。'])
    pl = [(3, 2, TOP[0]), (4, 2, TOP[1]), (3, 3, NIG[3])]
    rr = []
    for k, (p, n, nm) in enumerate(pl):
        plates = ''.join(f'<div class="plate" style="flex:1 1 0;height:20mm;padding:0 2mm">{"".join(im(nm) for _ in range(n))}</div>' for _ in range(p))
        rr.append(f'<div class="t k" style="margin:1mm 0">{p}にんに ひとり {n}こずつ。 ぜんぶで？</div><div class="row" style="gap:2mm">{plates}<span class="t s">＝</span>{box("", "w")}<span class="t s">こ</span></div>')
        ans(no, f'おもて①-{k+1}', f'{p * n}こ')
    f1 = Q(1, 'おさらを みて ぜんぶで なんこ？', f'<div class="rows">{"".join(rr)}</div>', '（2、4、6 と かぞえたしてみよう）')
    ad = [(2, 3), (3, 3), (2, 4), (5, 2)]
    ar = []
    for k, (n, c) in enumerate(ad):
        ar.append(f'<div class="eq" style="font-size:8mm">' + '<span class="op">＋</span>'.join(f'<span>{n}</span>' for _ in range(c)) + f'<span class="op">＝</span>{box("", "s")}</div>')
        ans(no, f'おもて②-{k+1}', f'{n * c}')
    f2 = Q(2, 'おなじ かずを たしていこう', '<div class="rows" style="gap:4mm">' + ''.join(ar) + '</div>')
    front = page(no, t, 'おもて', [f1, f2], foot_front())
    memo = [('おさら', 5, 'まい'), ('コップ', 5, 'こ'), ('ふくろ', 5, 'まい')]
    mr = ''.join(row(f'<span class="t s">{a}</span>', '<div class="grp">' + '<span class="dot"></span>' * n + '</div>', '<span class="t s">＝</span>', box('', 'w'), f'<span class="t s">{u}</span>') for a, n, u in memo)
    for k, (a, n, u) in enumerate(memo): ans(no, f'うら③-{k+1}', f'{n}{u}')
    b3 = Q(3, 'かいものメモ（5にんぶん）', f'<div class="rows">{mr}</div>', '（ひとり 1つずつ。 ○を かぞえて □に かこう）')
    mn = [(100, 3), (50, 4), (10, 5)]
    mrw = []
    for k, (v, p) in enumerate(mn):
        mrw.append(row(f'<div class="order">ひとり <b style="font-size:6mm">{v}えん</b></div>', f'<span class="t s">{p}にん</span>', '<span class="t s">→</span>', box('', 'w'), '<span class="t s">えん</span>'))
        ans(no, f'うら④-{k+1}', f'{v * p}えん')
    b4 = Q(4, 'ひとり ○えん。 みんなで いくら？', '<div class="rows">' + ''.join(mrw) + '</div>', '（100、200、300…と たしていこう）')
    ck = ''.join(f'<span>{c}</span>' for c in ['かぞえられた', 'くらべられた', 'たしざんが できた', 'ひきざんが できた', 'おかねが わかった', 'とけいが よめた'])
    b5 = Q(5, 'ふりかえり。 できた ものに ✓ を つけよう', f'<div class="checks" style="line-height:1.9">{ck}</div>')
    back = page(no, t, 'うら', [b3, b4, b5], foot_back('10まい ぜんぶ できたね！ おめでとう！'))
    PAGES.extend([front, back])

for f in (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10):
    f()

html = f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>せいかつ さんすう プリント</title><style>{CSS}</style></head><body>{"".join(PAGES)}</body></html>'
open(os.path.join(HERE, 'prints.html'), 'w', encoding='utf-8').write(html)

# ---------------- 先生用: こたえ・ポイント ----------------
ACSS = CSS + r"""
.ans-page { width: 210mm; height: 297mm; padding: 10mm 13mm; page-break-after: always; overflow: hidden }
.ans-page h1 { font-size: 7mm; margin: 0 0 3mm; border-bottom: 1.2mm solid #111; padding-bottom: 2mm }
.sh { border: .5mm solid #111; border-radius: 2.5mm; padding: 2mm 3mm; margin-bottom: 3mm; break-inside: avoid }
.sh h2 { margin: 0 0 1mm; font-size: 4.8mm } .sh .aim { font-size: 3.6mm; margin-bottom: 1mm }
.sh ul { margin: 0 0 1.2mm; padding-left: 5mm; font-size: 3.4mm; line-height: 1.5 }
.sh .a { font-size: 3.4mm; line-height: 1.6; color: #111; columns: 2; column-gap: 6mm }
.sh .a div { break-inside: avoid }
.sh .a b { display: inline-block; min-width: 24mm; margin-right: 1.5mm }
"""
parts = []
chunks = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
for ci, ch in enumerate(chunks):
    inner = ''
    for no in ch:
        title, aim, pts = GUIDE[no]
        a = ''.join(f'<div><b>{l}</b>{v}</div>' for l, v in ANS[no])
        inner += f'<div class="sh"><h2>{no}　{title}</h2><div class="aim">ねらい：{aim}</div><ul>{"".join(f"<li>{p}</li>" for p in pts)}</ul><div class="a">{a}</div></div>'
    parts.append(f'<section class="ans-page"><h1>せんせいようの こたえと ポイント（{ci + 1}/{len(chunks)}）</h1>{inner}</section>')
open(os.path.join(HERE, 'answers.html'), 'w', encoding='utf-8').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>こたえ</title><style>{ACSS}</style></head><body>{"".join(parts)}</body></html>')
print('prints.html / answers.html を作りました（プリント', len(PAGES), 'ページ）')
