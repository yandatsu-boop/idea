#!/usr/bin/env python3
"""けいさんアプリの11バージョンを、おこづかい5000円でできる「かいものプリント」にする（A4 おもて/うら 1まい×11）。
  node app_export.js themes → themes.json  /  python3 build_versions.py → baskets.json, versions.html, versions_answers.html
  node app_export.js art    → art/（見本の絵）  /  node render_versions.js → PDF（まとめ・バージョンべつ・こたえ・zip）
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(HERE, p), encoding='utf-8').read()
CSS = re.search(r'CSS = r"""(.*?)"""', rd('../build_prints.py'), re.S).group(1)
CSS2 = re.search(r'CSS2 = r"""(.*?)"""', rd('../daily/build_daily.py'), re.S).group(1)
THEMES = json.load(open(os.path.join(HERE, 'themes.json'), encoding='utf-8'))
BUDGET = 5000
fmt = lambda n: f'{n:,}'

# 見本のかいもの（おうちの人用のこたえれい）。アプリで えらべる ざいりょうだけ。
ORDER = ['curry', 'parfait', 'plarail', 'car', 'pancake', 'robot', 'pizza', 'sushi', 'burger', 'icecream', 'gyudon', 'ramen']
SAMPLE = {
 'curry':   {'chicken':1,'beef':1,'carrot':2,'potato':2,'onion':1,'sweet':1,'rice':2,'egg':1,'cheese':1},
 'parfait': {'jumbo':1,'granola':1,'vanilla':2,'strawberry':2,'banana':1,'whip':1,'sauce':1,'wafer':1},
 'plarail': {'straight':3,'curve':2,'building':1,'platform':1,'shinkansen':1,'keihan':1,'crossing':1,'tunnel':1,'tree':2,'signal':1},
 'car':     {'sports':1,'red':1,'tire':4,'wing':1,'light':2,'sticker':2,'neon':1},
 'pancake': {'plain':2,'maple':1,'honey':1,'strawberry':2,'banana':1,'butter':2,'whip':1,'icecream':1},
 'robot':   {'biped':1,'red':1,'silver':1,'battery':1,'solar':1,'arm':2,'eye':2,'antenna':1,'jet':1,'shield':1},
 'pizza':   {'thin':1,'thick':1,'tomato':2,'white':1,'mozza':2,'salami':2,'shrimp':1,'corn':2,'mushroom':2,'pineapple':1,'pepper':1},
 'sushi':   {'nigiri':2,'maki':1,'tuna':2,'salmon':2,'egg':1,'shrimp':1,'squid':1,'ikura':1,'eel':1,'wasabi':1,'shoyu':1,'gari':1,'tea':2,'miso':1},
 'burger':  {'sesame':1,'beef':2,'chicken':1,'lettuce':2,'tomato':1,'cheese':2,'bacon':1,'ketchup':1,'bbq':1,'fries':1,'drink':1},
 'icecream':{'cone':1,'waffle':1,'cup':1,'vanilla':2,'choco':1,'strawberry':1,'matcha':1,'mint':1,'cherry':2,'whip':1,'sprinkle':1,'wafer':1,'sauce':1},
 'ramen':   {'shoyu':1,'miso':1,'tonkotsu':1,'chashu':2,'ajitama':2,'negi':1,'nori':1,'menma':1,'corn':1,'gyoza':1,'chahan':1,'water':2},
 'gyudon':  {'regular':1,'large':1,'xl':1,'egg':2,'cheese':1,'negi':1,'kimchi':1,'miso':1,'salad':1,'shinko':1,'tea':2},
}
TITLE = {'curry':'カレー','parfait':'パフェ','plarail':'プラレールの えき','car':'カスタムカー','pancake':'パンケーキ','robot':'ロボット',
         'pizza':'ピザ','sushi':'おすし','burger':'ハンバーガー','icecream':'アイスクリーム','gyudon':'ぎゅうどん','ramen':'ラーメン'}
UNIT = 'こ'

CSS3 = r"""
.banner { display: flex; align-items: center; gap: 4mm; border: .8mm solid #111; border-radius: 3mm; padding: 1.6mm 4mm; font-size: 4.6mm; background: #f2f2f2 }
.banner b { font-size: 7.2mm }
.banner .goal { margin-left: auto; font-size: 3.7mm; text-align: right; line-height: 1.35 }
table.tb { width: 100%; border-collapse: collapse; font-size: 4.3mm; flex: none }
.tb th { font-size: 3.5mm; font-weight: normal; border-bottom: .5mm solid #111; padding: 0 1mm 1mm; text-align: left }
.tb td { padding: 0 1.2mm; border-bottom: .3mm dashed #999; }
.tb td.ct { font-weight: bold; font-size: 3.7mm; border-bottom: .5mm solid #111; border-right: .3mm solid #999; vertical-align: top; padding-top: 1mm; width: 29mm; line-height: 1.25 }
.tb td.ct small { display: block; font-weight: normal; font-size: 3mm; color: #333 }
.tb tr.last td { border-bottom: .5mm solid #111 }
.tb td.pr { text-align: right; white-space: nowrap; width: 24mm }
.tb td.nm2 { white-space: nowrap }
.sum { display: flex; flex-wrap: wrap; gap: 2mm 5mm; align-items: center; font-size: 4.8mm }
.sum .fill { min-width: 30mm }
.sum .mark { border: .6mm solid #111; border-radius: 50%; width: 9mm; height: 9mm; display: inline-flex; align-items: center; justify-content: center; font-size: 6mm; font-weight: bold; margin: 0 1mm }
.side { white-space: nowrap }
.qh, .qh * { white-space: nowrap }
.qh .qs { font-size: 3.3mm }
.shiki .fill { height: 8.6mm !important; line-height: 7.6mm !important }
.q { padding: 2mm 3.4mm 2.2mm !important }
.addn { display: flex; align-items: center; gap: 1.6mm; flex-wrap: wrap; font-size: 6mm }
.addn .fill { min-width: 21mm; height: 10mm; line-height: 9mm; font-size: 6mm }
.addn .fill.s { min-width: 14mm }
.addn .fill.w { min-width: 32mm }
.addn .t2 { font-size: 4.3mm }
.draw { display: flex; gap: 3mm; flex: 1 1 auto; min-height: 0 }
.draw .frame2 { flex: 1 1 0; border: .6mm dashed #666; border-radius: 3mm; position: relative; min-height: 22mm }
.draw .frame2 span { position: absolute; left: 3mm; top: 2mm; font-size: 3.6mm; color: #555 }
.draw .sample { flex: 0 0 62mm; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1mm; font-size: 3.4mm; color: #333 }
.draw .sample img { width: 100%; height: auto; border-radius: 2mm }
.pts { display: flex; gap: 3mm; font-size: 4mm; flex-wrap: wrap }
.pts div { border: .5mm solid #111; border-radius: 2mm; padding: 1mm 3mm }
.ans-t { width: 100%; border-collapse: collapse; font-size: 3.1mm; margin-top: .6mm }
.ans-t td, .ans-t th { border-bottom: .25mm dotted #999; padding: 0 1mm; font-weight: normal; text-align: left }
.ans-t td.r { text-align: right }
.dayrow .rest { display: flex; gap: 4mm }
.dayrow .rest > div { flex: 1 1 0 }
"""

def themecats(t):
    return THEMES[t]['cats']

def calc(theme):
    T = THEMES[theme]; qty = SAMPLE[theme]; lines = []
    for c in T['cats']:
        assert sum(qty.get(i['id'], 0) for i in c['items']) >= c['min'], (theme, c['id'])
        for i in c['items']:
            if qty.get(i['id'], 0): lines.append(dict(name=i['name'], price=i['price'], q=qty[i['id']], cat=c['name']))
    total = sum(l['price'] * l['q'] for l in lines); assert total <= BUDGET, (theme, total)
    multi = sorted([l for l in lines if l['q'] >= 2], key=lambda l: -l['price'] * l['q'])
    return dict(lines=lines, total=total, change=BUDGET - total, multi=multi[0] if multi else None)

OPS = '<div class="ops">' + ''.join(f'<div class="opc">{o}</div>' for o in '＋－×÷') + '</div>'
def fill(cls='', t=''): return f'<span class="fill {cls}">{t}</span>'

def front(theme, no):
    T = THEMES[theme]; n_items = sum(len(c['items']) for c in T['cats'])
    h = 11 if n_items <= 9 else 10 if n_items <= 12 else 8.0 if n_items <= 15 else 7.4 if n_items <= 18 else 6.9
    fh = min(h - 1.4, 7.2)
    rows = []
    for c in T['cats']:
        req = f'かならず {c["hint"]}' if c['min'] > 0 else 'すきなだけ'
        for k, it in enumerate(c['items']):
            first = f'<td class="ct" rowspan="{len(c["items"])}">{c["name"]}<small>（{req}）</small></td>' if k == 0 else ''
            last = ' class="last"' if k == len(c['items']) - 1 else ''
            rows.append(f'<tr{last} style="height:{h}mm">{first}<td class="nm2">{it["name"]}</td><td class="pr">{fmt(it["price"])}えん</td>'
                        f'<td><span class="fill s" style="height:{fh}mm;line-height:{fh-1}mm"></span>{UNIT}</td>'
                        f'<td><span class="fill" style="height:{fh}mm;line-height:{fh-1}mm"></span>えん</td></tr>')
    tb = ('<table class="tb"><tr><th>しゅるい</th><th>ざいりょう</th><th style="text-align:right;white-space:nowrap">1この ねだん</th><th>いくつ かう？</th><th>きんがく（ねだん×こ）</th></tr>'
          + ''.join(rows) + '</table>')
    ban = (f'<div class="banner"><span style="white-space:nowrap">おこづかい</span><b style="white-space:nowrap">{fmt(BUDGET)}えん</b><span>この なかで かいものして、{T["title"]}！</span>'
           '<div class="goal">・「かならず」の ところは そろえよう<br>・おつりが すくないほど おとくに つかえたよ</div></div>')
    sm = ('<div class="q" style="flex:0 0 auto"><div class="qh"><span class="qn">★</span>ぜんぶで いくら？ <span class="qs">きんがくを ぜんぶ たそう（うらの 3 で けいさん）</span></div>'
          f'<div class="sum"><span>ごうけい</span>{fill("", "")}<span>えん</span><span style="margin-left:4mm">おつり（{fmt(BUDGET)}－ごうけい）</span>{fill("", "")}<span>えん</span>'
          f'<span style="margin-left:4mm">{fmt(BUDGET)}えんを こえて ない？</span><span class="mark">○</span><span class="mark">×</span></div></div>')
    return [ban, f'<div class="q" style="flex:0 0 auto;padding:1.6mm 3mm">{tb}</div>', sm]

def back(theme):
    OP = lambda: '<span style="margin-left:auto;display:flex;align-items:center;gap:2mm;font-size:3.4mm;font-weight:normal">どの けいさん？ ' + OPS + '</span>'
    q1 = ('<div class="q"><div class="qh"><span class="qn">1</span>いちばん たくさん かった ものは？' + OP() + '</div>'
          '<div class="addn" style="font-size:4.6mm"><span>おなじ ものを いくつも かった もの</span>' + fill('w') + '<span style="font-size:4.6mm">は 1こ</span>' + fill('s') + '<span style="font-size:4.6mm">えん。</span>' + fill('s') + '<span style="font-size:4.6mm">こ かうと いくら？</span></div>'
          '<div class="shiki" style="margin-top:1.4mm"><span class="fill"></span><span class="fill s"></span><span class="fill"></span>＝<span class="fill w"></span><span style="font-size:5mm">えん</span></div></div>')
    boxes = lambda n: '＋'.join(fill('s', '') for _ in range(n))
    q2 = ('<div class="q"><div class="qh"><span class="qn">3</span>ぜんぶで いくら？ <span class="qs">おもての きんがくを たそう</span>' + OP() + '</div>'
          f'<div class="shiki" style="font-size:4.6mm;flex-wrap:wrap;gap:1.2mm 1mm"><span class="fill" style="min-width:14mm;height:8.4mm"></span>' +
          ''.join(f'＋<span class="fill" style="min-width:14mm;height:8.4mm"></span>' for _ in range(6)) + '</div>'
          '<div class="shiki" style="font-size:4.6mm;flex-wrap:wrap;gap:1.2mm 1mm;margin-top:1.4mm"><span class="fill" style="min-width:14mm;height:8.4mm"></span>' +
          ''.join(f'＋<span class="fill" style="min-width:14mm;height:8.4mm"></span>' for _ in range(6)) + '＝<span class="fill w" style="height:10mm"></span><span style="font-size:4.6mm">えん</span></div></div>')
    q2 = q2.replace('<span class="qn">3</span>', '<span class="qn">2</span>')
    q3 = ('<div class="q"><div class="qh"><span class="qn">3</span>おつりは いくら？ <span class="qs">ひきざん</span>' + OP() + '</div>'
          f'<div class="shiki"><span style="font-size:6.4mm">{fmt(BUDGET)}</span><span class="fill s"></span><span class="fill"></span>＝<span class="fill w"></span><span style="font-size:5mm">えん</span></div></div>')
    q4 = ('<div class="q"><div class="qh"><span class="qn">4</span>もう1つ かえるかな？ <span class="qs">ねだんひょうから さがそう</span></div>'
          '<div class="addn t2"><span class="t2">かえる もの</span>' + fill('w') + '<span class="t2">ねだん</span>' + fill('s') + '<span class="t2">えん（かえない ときは「なし」）</span></div></div>')
    q5 = ('<div class="q" style="flex:0 0 auto"><div class="qh"><span class="qn">5</span>つかいきり チェック <span class="qs">おつりの おおきさに ○（アプリと おなじ）</span></div>'
          f'<div class="pts"><div>◎ {fmt(BUDGET*0.1)}えん いか ＝ 20てん</div><div>○ {fmt(BUDGET*0.25)}えん いか ＝ 10てん</div><div>△ それより おおい ＝ 5てん</div></div></div>'.replace('500.0', '500').replace('1,250.0', '1,250'))
    q6 = ('<div class="q" style="flex:1 1 40mm"><div class="qh"><span class="qn">6</span>できあがり <span class="qs">じぶんの えを かいたり ぬったりしよう</span></div>'
          '<div class="draw"><div class="frame2"><span>じぶんの できあがり</span></div>'
          f'<div class="sample" style="flex-basis:42mm"><img src="art/{theme}.png" alt=""><span>れい</span></div></div></div>')
    return [q1, q2, q3, q4, q5, q6]

def page(no, title, side, blocks, foot):
    who = '<div class="who"><div>なまえ <span></span></div><div>ひづけ <span class="d"></span></div></div>'
    head = f'<div class="head"><div class="no">{no}</div><div class="title" style="font-size:6.6mm">{title}</div><div class="side">{side}</div></div>'
    return f'<section class="page">{head}{who}{"".join(blocks)}{foot}</section>'

FOOT_F = '<div class="foot"><span>うらにも つづくよ →</span><span class="stars" style="margin-left:auto">☆ ☆ ☆</span></div>'
FOOT_B = '<div class="foot"><span>できたら ✓：□ そろえた　□ けいさんした　□ えを かいた</span><span class="stamp" style="margin-left:auto"></span><span class="stamp"></span></div>'

def main():
    plan = [dict(day=i + 1, parts=[dict(theme=t, qty=SAMPLE[t])]) for i, t in enumerate(ORDER)]
    json.dump(plan, open(os.path.join(HERE, 'baskets.json'), 'w'), ensure_ascii=False)
    pages = []
    for i, t in enumerate(ORDER):
        ttl = f'{TITLE[t]}を つくろう！'
        pages.append(page(i + 1, ttl, 'おもて', front(t, i + 1), FOOT_F))
        pages.append(page(i + 1, ttl, 'うら', back(t), FOOT_B))
    open(os.path.join(HERE, 'versions.html'), 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>けいさんアプリ バージョンべつプリント</title><style>{CSS}{CSS2}{CSS3}</style></head><body>{"".join(pages)}</body></html>')
    # ---- こたえれい ----
    cards = []
    for i, t in enumerate(ORDER):
        c = calc(t); m = c['multi']
        if m: q1 = f'{m["name"]}：{fmt(m["price"])} × {m["q"]} ＝ <b>{fmt(m["price"]*m["q"])}えん</b>'
        else: q1 = '（おなじ ものを 2こ いじょう かったら かけざん）'
        rows = ''.join(f'<tr><td>{l["name"]}</td><td class="r">{fmt(l["price"])}えん × {l["q"]}</td><td class="r">{fmt(l["price"]*l["q"])}えん</td></tr>' for l in c['lines'])
        pts = 20 if c['change'] <= BUDGET * .1 else 10 if c['change'] <= BUDGET * .25 else 5
        cards.append(f'<div class="dayrow"><h2>{i+1}　{TITLE[t]}　（ごうけい <b>{fmt(c["total"])}えん</b>／おつり <b>{fmt(c["change"])}えん</b>／つかいきり {pts}てん）</h2>'
                     f'<table class="ans-t">{rows}</table><p><b>1：</b>{q1}</p></div>')
    guide = ('<div class="dayrow" style="background:#f2f2f2"><h2>つかいかた・ポイント</h2>'
             '<p>・12の バージョン（カレー・パフェ・プラレール・カスタムカー・パンケーキ・ロボット・ピザ・おすし・ハンバーガー・アイスクリーム・ぎゅうどん・ラーメン）それぞれ 1まい（おもて/うら）。おこづかいは ぜんぶ 5,000えんです。</p>'
             '<p>・おもての ねだんひょうの「いくつ かう？」に すきな かずを かき、「きんがく」＝ねだん×こ を かきます。「かならず」の しゅるいは アプリと おなじ ルールです。</p>'
             '<p>・うらは アプリの おかいけいと おなじ ながれ（かけざん→ごうけい→おつり→つかいきり）。じぶんが きめた かずで けいさんするので、こたえは ひとりひとり ちがいます。下は「こたえれい」で、ごうけいが 5,000えん いかなら せいかいです。</p>'
             '<p>・「ごうけい」が 5,000えんを こえたら、ざいりょうを へらして もういちど。ここが いちばんの がくしゅうポイントです。</p></div>')
    chunks = [cards[0:2], cards[2:4], cards[4:6], cards[6:8], cards[8:10], cards[10:12]]
    ans_pages = [f'<section class="ans-page"><h1>せんせいよう　こたえれい（{i+1}/6）</h1>{guide if i == 0 else ""}{"".join(ch)}</section>' for i, ch in enumerate(chunks)]
    open(os.path.join(HERE, 'versions_answers.html'), 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>こたえれい</title><style>{CSS}{CSS2}{CSS3}</style></head><body>{"".join(ans_pages)}</body></html>')
    for t in ORDER:
        c = calc(t); print(t, c['total'], c['change'])
main()
