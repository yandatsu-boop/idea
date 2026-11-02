#!/usr/bin/env python3
"""けいさんアプリ（最新版）の中身で作る「毎日1まい・10日ぶん」プリント（A4 おもて/うら 1まい×10日）。
  python3 build_daily.py     → baskets.json / daily.html / daily_answers.html
  node app_export.js themes  → themes.json（アプリから ざいりょう・ねだんを書き出し）
  node app_export.js art     → art/day*.png（アプリの「できあがり」の絵）
  node render_daily.js       → PDF
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
import re
CSS = re.search(r'CSS = r"""(.*?)"""', open(os.path.join(HERE, '..', 'build_prints.py'), encoding='utf-8').read(), re.S).group(1)  # 共通の見た目

THEMES = json.load(open(os.path.join(HERE, 'themes.json'), encoding='utf-8'))
MAXQ = 4

# 10日ぶんの かいもの（アプリで えらべる ざいりょうだけを つかう）
DAYS = [
 (1, 'burger',  1000, {'plain':1,'beef':1,'lettuce':1,'tomato':1,'ketchup':1},                      'はじめての ハンバーガー'),
 (2, 'curry',   1000, {'chicken':1,'carrot':2,'sweet':1,'rice':1},                                  'とりにくカレー'),
 (3, 'parfait', 1000, {'glass':1,'corn':1,'vanilla':1,'strawberry':1,'whip':1},                     'いちごのパフェ'),
 (4, 'pizza',   1000, {'thin':1,'tomato':1,'mozza':1,'salami':2,'corn':1},                          'サラミのピザ'),
 (5, 'plarail', 1000, {'straight':2,'curve':1,'building':1,'keihan':1},                             '京阪電車の えき'),
 (6, 'pancake', 1000, {'plain':1,'maple':1,'strawberry':1,'banana':2,'butter':1},                   'バナナのパンケーキ'),
 (7, 'car',     1000, {'sports':1,'red':1,'tire':1,'wing':1,'light':2},                             'あかいスポーツカー'),
 (8, 'sushi',   1000, {'nigiri':1,'tuna':2,'salmon':1,'egg':1,'wasabi':1,'tea':1},                  'まぐろの おすし'),
 (9, 'robot',   1000, {'biped':1,'blue':1,'battery':1,'antenna':1,'eye':1},                         'あおい あるくロボ'),
 (10,'burger',  2000, {'sesame':1,'beef':3,'cheese':1,'bacon':1,'lettuce':1,'tomato':1,'ketchup':1,'fries':1,'drink':1}, 'ジャイアントバーガーセット'),
]
CATNAME = {}

def fmt(n): return f'{n:,}'

def compute(theme, budget, qty):
    T = THEMES[theme]
    items = {}
    for c in T['cats']:
        for it in c['items']: items[it['id']] = (it, c)
    # アプリの必須ルールを検査
    for c in T['cats']:
        n = sum(qty.get(it['id'], 0) for it in c['items'])
        assert n >= c['min'], (theme, c['id'], 'min')
    lines = []
    for c in T['cats']:
        for it in c['items']:
            q = qty.get(it['id'], 0)
            if q:
                assert q <= MAXQ
                lines.append(dict(id=it['id'], name=it['name'], price=it['price'], q=q, cat=c['name']))
    total = sum(l['price'] * l['q'] for l in lines)
    assert total <= budget, (theme, total, budget)
    multi = sorted([l for l in lines if l['q'] >= 2], key=lambda l: -l['price'] * l['q'])
    if multi:
        m = multi[0]; q1 = dict(op='×', a=m['price'], b=m['q'], ans=m['price'] * m['q'], item=m,
                                text=f"{m['name']}は 1こ {fmt(m['price'])}えんです。{m['q']}こ かうと、いくらですか。")
    else:
        bp = sorted(lines, key=lambda l: -l['price']); a, b = bp[0], bp[1]
        q1 = dict(op='＋', a=a['price'], b=b['price'], ans=a['price'] + b['price'],
                  text=f"{a['name']}（{fmt(a['price'])}えん）と {b['name']}（{fmt(b['price'])}えん）を あわせると、いくらですか。")
    return dict(lines=lines, total=total, change=budget - total, q1=q1, items=T['cats'])

def esc(s): return s

def chip_table(T, mark):
    out = []
    for c in T['cats']:
        req = 'かならず' if c['min'] > 0 else 'すきに'
        its = ''.join(f'<div class="chip{" on" if it["id"] in mark else ""}"><span>{it["name"]}</span><b>{fmt(it["price"])}えん</b></div>' for it in c['items'])
        out.append(f'<div class="cat"><div class="cn">{c["name"]}<small>（{req}）</small></div><div class="chips">{its}</div></div>')
    return ''.join(out)

CSS2 = r"""
.chips { display: flex; flex-wrap: wrap; gap: 1.2mm 1.6mm }
.cat { display: flex; gap: 2.4mm; align-items: flex-start; padding: .9mm 0; border-bottom: .3mm dashed #999 }
.cat:last-child { border-bottom: 0 }
.cn { width: 25mm; font-size: 4mm; font-weight: bold; flex: none; padding-top: .8mm }
.cn small { font-weight: normal; font-size: 3mm; display: block; color: #444 }
.chip { border: .4mm solid #555; border-radius: 1.6mm; padding: .5mm 1.8mm; font-size: 3.6mm; display: flex; gap: 1.6mm; align-items: baseline; background: #fff }
.chip b { font-size: 3.4mm; font-weight: bold }
.title { font-size: 6.4mm !important }
.chip.on { background: #e2e2e2; border: .8mm solid #111 }
.q > table.tbl { flex: none; margin-bottom: 1mm }
.tbl { width: 100%; border-collapse: collapse; font-size: 4.6mm }
.tbl th { font-size: 3.6mm; font-weight: normal; border-bottom: .5mm solid #111; padding: 0 1mm 1mm; text-align: left }
.tbl td { padding: .3mm 1mm; border-bottom: .3mm dashed #999; height: 8.6mm }
.many .tbl td { height: 7.6mm; font-size: 4.2mm }
.many ~ .q .art img { max-height: 40mm }
.many .fill { height: 6.4mm; line-height: 5.6mm }
.tbl td.n { font-weight: bold }
.fill { display: inline-block; min-width: 20mm; height: 7.4mm; border: .6mm solid #111; border-radius: 1.6mm; vertical-align: middle; text-align: center; line-height: 6.6mm; font-size: 5mm }
.fill.s { min-width: 12mm }
.two { display: flex; gap: 4mm; flex: 1 1 auto; align-items: stretch }
.two > .q { flex: 1 1 0 }
.art { display: flex; align-items: center; justify-content: center; flex: 1 1 auto; padding: 1mm }
.art img { max-width: 100%; max-height: 62mm; object-fit: contain }
.ops { display: flex; gap: 3mm; align-items: center }
.opc { width: 9mm; height: 9mm; border: .6mm solid #111; border-radius: 50%; font-size: 6.4mm; font-weight: bold; display: flex; align-items: center; justify-content: center }
.qtext { font-size: 4.4mm; line-height: 1.4; margin-bottom: 1.2mm }
.shiki { display: flex; align-items: center; gap: 2mm; font-size: 6.4mm }
.shiki .fill { height: 10mm; min-width: 24mm; font-size: 6.4mm; line-height: 9mm }
.shiki .fill.w { min-width: 34mm }
.lab { font-size: 4mm; margin-right: 2mm }
.recpt { border: .5mm dashed #555; border-radius: 2mm; padding: .8mm 3mm; font-size: 3.8mm; margin-bottom: 1.2mm; column-count: 2; column-gap: 8mm }
.recpt div { display: flex; justify-content: space-between; border-bottom: .25mm dotted #aaa; padding: .2mm 0; break-inside: avoid }
.recpt div:last-child { border-bottom: 0 }
.sc { display: flex; gap: 3mm; font-size: 4.4mm; align-items: center; flex-wrap: wrap }
.sc span::before { content: '□ '; font-size: 5.4mm }
.ans-page { width: 210mm; height: 297mm; padding: 10mm 13mm 8mm; page-break-after: always; overflow: hidden; display: flex; flex-direction: column; gap: 2.4mm }
.ans-page h1 { font-size: 7.2mm; margin: 0 0 1mm; border-bottom: 1.2mm solid #111; padding-bottom: 1.5mm }
.dayrow { border: .5mm solid #111; border-radius: 2.6mm; padding: 1.6mm 3.4mm; font-size: 3.9mm; line-height: 1.5 }
.dayrow h2 { margin: 0 0 .6mm; font-size: 4.7mm }
.dayrow .pt { display: inline }
.dayrow p { margin: .2mm 0 }
.dayrow b { font-weight: bold }
.cap { font-size: 3.6mm; color: #333; margin-top: 1mm }
"""

def nm_sp(n):  # 数字3けたごとの , を そのままに
    return fmt(n)

def front(d, theme, budget, qty, title, c):
    T = THEMES[theme]
    mark = set(qty)
    art = f'art/day{d}-0.png'
    blk1 = ('<div class="q" style="flex:0 0 auto"><div class="qh"><span class="qn">1</span>おみせの ねだんひょう'
            f'<span class="qs">（きょうの かいものは ■の いろの ところ）</span></div>{chip_table(T, mark)}</div>')
    rows = ''.join(
        f'<tr><td class="n">{l["name"]}</td><td><span class="fill s">{fmt(l["price"]) if False else ""}</span> えん</td>'
        f'<td>{l["q"]}こ</td><td><span class="fill"></span> えん</td></tr>' for l in c['lines'])
    many = len(c['lines']) > 6
    blk2 = ('<div class="q' + (' many' if many else '') + '"><div class="qh"><span class="qn">2</span>かごの なかみ<span class="qs">（ねだんひょうを みて ねだんを かこう。いくらに なるかな？）</span></div>'
            f'<table class="tbl"><tr><th>かうもの</th><th>1この ねだん</th><th>かず</th><th>ぜんぶで</th></tr>{rows}</table></div>')
    blk3 = (f'<div class="q" style="flex:1 1 55mm"><div class="qh"><span class="qn">3</span>おこづかいと できあがり'
            f'<span class="qs">おこづかいは <b style="font-size:5.4mm">{fmt(budget)}えん</b>。こんなものが できるよ！</span></div>'
            f'<div class="art"><img src="{art}" alt=""></div></div>')
    return blk1, blk2, blk3

def page_html(no, title, side, blocks, foot):
    who = '<div class="who"><div>なまえ <span></span></div><div>ひづけ <span class="d"></span></div></div>'
    head = f'<div class="head"><div class="no">{no}</div><div class="title">{title}</div><div class="side">{side}</div></div>'
    return f'<section class="page">{head}{who}{"".join(blocks)}{foot}</section>'

OPS = '<div class="ops">' + ''.join(f'<div class="opc">{o}</div>' for o in '＋－×÷') + '</div>'

def back(d, theme, budget, c):
    q1, total, change = c['q1'], c['total'], c['change']
    opsel = f'<div style="display:flex;align-items:center;gap:3mm"><span class="lab">どの けいさん？ ○を つけよう →</span>{OPS}</div>'
    b1 = ('<div class="q"><div class="qh"><span class="qn">4</span>おかいけい① <span class="qs">もんだいを よんで けいさんしよう</span></div>'
          f'<div class="qtext">{q1["text"]}</div>{opsel}'
          '<div class="shiki" style="margin-top:2mm"><span class="fill"></span><span class="fill s"></span><span class="fill"></span>＝<span class="fill w"></span><span style="font-size:5mm">えん</span></div></div>')
    rec = ''.join(f'<div><span>{l["name"]} {fmt(l["price"])}えん</span><span>× {l["q"]}</span></div>' for l in c['lines'])
    b2 = ('<div class="q"><div class="qh"><span class="qn">5</span>おかいけい② <span class="qs">ぜんぶで いくら？</span></div>'
          f'<div class="qtext">かごの なかの ものは、ぜんぶで いくらですか。（おもての 2 の「ぜんぶで」を たしてね）</div>'
          f'<div class="recpt">{rec}</div>{opsel}'
          '<div class="shiki" style="margin-top:2mm"><span style="font-size:5mm">ごうけい</span><span class="fill w"></span><span style="font-size:5mm">えん</span></div></div>')
    b3 = ('<div class="q"><div class="qh"><span class="qn">6</span>おかいけい③ <span class="qs">おつりは いくら？</span></div>'
          f'<div class="qtext">おこづかいは {fmt(budget)}えんです。おかいけいは {fmt(total)}えんでした。おつりは いくらですか。</div>{opsel}'
          f'<div class="shiki" style="margin-top:2mm"><span class="fill w"></span><span class="fill s"></span><span class="fill w"></span>＝<span class="fill w"></span><span style="font-size:5mm">えん</span></div></div>')
    cheap = sorted([it for cat in THEMES[theme]['cats'] for it in cat['items']], key=lambda i: i['price'])[:1]
    b4 = ('<div class="q"><div class="qh"><span class="qn">7</span>もう1つ かえるかな？ <span class="qs">おつりで かえるものを ねだんひょうから さがそう</span></div>'
          f'<div class="qtext">おつりは <span class="fill" style="min-width:22mm"></span> えん。ねだんひょうの なかで、おつりで もう1つ かえるものに ○を つけて、なまえを かこう。</div>'
          '<div class="shiki" style="font-size:5mm"><span>かえるもの：</span><span class="fill" style="min-width:60mm"></span><span style="margin-left:6mm">かえない とき：</span><span class="fill s"></span><span class="lab" style="margin-left:2mm">（かえない／ちょうど）</span></div></div>')
    b5 = ('<div class="q" style="flex:0 0 auto"><div class="qh"><span class="qn">8</span>ふりかえり <span class="qs">できたら □に チェック</span></div>'
          '<div class="sc"><span>もんだいを よめた</span><span>けいさんの しかたを えらべた</span><span>こたえを かけた</span><span>おつりが わかった</span></div></div>')
    return [b1, b2, b3, b4]

def build():
    pages = []
    plan = []
    comp = {}
    for (d, theme, budget, qty, title) in DAYS:
        c = comp[d] = compute(theme, budget, qty)
        plan.append(dict(day=d, parts=[dict(theme=theme, qty=qty)]))
    json.dump(plan, open(os.path.join(HERE, 'baskets.json'), 'w'), ensure_ascii=False)
    for (d, theme, budget, qty, title) in DAYS:
        c = comp[d]
        T = THEMES[theme]
        f1, f2, f3 = front(d, theme, budget, qty, title, c)
        ttl = f'{d}にちめ　{T["title"]}　{title}'
        pages.append(page_html(d, f'{title}', f'おもて {d}にちめ',
            [f1, f2, f3], '<div class="foot"><span>うらにも つづくよ →</span><span class="stars" style="margin-left:auto">☆ ☆ ☆</span></div>'))
        pages.append(page_html(d, f'{title}', f'うら {d}にちめ', back(d, theme, budget, c),
            '<div class="foot"><span>できたら ✓：□ よめた　□ えらべた　□ かけた</span><span class="stamp" style="margin-left:auto"></span><span class="stamp"></span><span class="stamp"></span></div>'))
    html = f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>けいさんアプリ 10日ぶんプリント</title><style>{CSS}{CSS2}</style></head><body>{"".join(pages)}</body></html>'
    open(os.path.join(HERE, 'daily.html'), 'w', encoding='utf-8').write(html)
    # ---- 先生用 ----
    cards = []
    for (d, theme, budget, qty, title) in DAYS:
        c = comp[d]; q1 = c['q1']
        lines = '、'.join(f'{l["name"]} {fmt(l["price"])}×{l["q"]}={fmt(l["price"]*l["q"])}' for l in c['lines'])
        cards.append(f'<div class="dayrow"><h2>{d}にちめ　{THEMES[theme]["name"]}：{title}　（おこづかい {fmt(budget)}えん）</h2>'
            f'<p><b>おもて 2：</b>{lines}</p>'
            f'<p><b>うら 4：</b>{q1["op"]}　{fmt(q1["a"])} {q1["op"]} {q1["b"]} ＝ <b>{fmt(q1["ans"])}えん</b>　'
            f'<b>5：</b>＋　ごうけい <b>{fmt(c["total"])}えん</b>　<b>6：</b>－　{fmt(budget)} － {fmt(c["total"])} ＝ <b>{fmt(c["change"])}えん</b></p>'
            f'<p><b>7：</b>おつり {fmt(c["change"])}えんで かえるもの（れい）：{", ".join(i["name"] for cat in THEMES[theme]["cats"] for i in cat["items"] if i["price"] <= c["change"] and i["id"] not in qty)[:60] or "なし（ちょうど）"}</p></div>')
    guide = ('<div class="dayrow" style="background:#f2f2f2"><h2>つかいかた・ポイント</h2>'
        '<p>・1にち1まい（おもて・うら）。10にちで アプリの 9つの おみせ（ハンバーガー・カレー・パフェ・ピザ・プラレール・パンケーキ・カスタムカー・おすし・ロボット）を ひとまわり、10にちめは ジャイアントバーガー（2000えん）です。</p>'
        '<p>・おもての ねだんは アプリと おなじです。まず 1この ねだんを ねだんひょうから さがして かきます（ぬりつぶした ところが きょうの かいもの）。</p>'
        '<p>・うらは アプリの おかいけいと おなじ ながれ：①かけざん（または たしざん）→ ②ごうけい → ③おつり。「どの けいさん？」で ＋－×÷から えらぶ れんしゅうも アプリと おなじです。</p>'
        '<p>・かけざんが にがてな ときは、おなじ ねだんを 2かい ならべて たす（250＋250）ことから。でんたく・おかねの おもちゃを つかっても よいです。</p>'
        '<p>・おもての 3の えは、アプリで おなじ ざいりょうを えらぶと できる えと おなじです。いっしょに アプリでも ためしてみましょう。</p></div>')
    chunks = [cards[0:3], cards[3:7], cards[7:10]]
    ans_pages = []
    for i, ch in enumerate(chunks):
        ans_pages.append(f'<section class="ans-page"><h1>せんせいよう　こたえと ポイント（{i+1}/{len(chunks)}）</h1>{guide if i == 0 else ""}{"".join(ch)}</section>')
    open(os.path.join(HERE, 'daily_answers.html'), 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>こたえ</title><style>{CSS}{CSS2}</style></head><body>{"".join(ans_pages)}</body></html>')
    for d in comp:
        print(d, DAYS[d-1][1], 'total', comp[d]['total'], 'change', comp[d]['change'], comp[d]['q1']['op'], comp[d]['q1']['ans'])

if __name__ == '__main__':
    build()
