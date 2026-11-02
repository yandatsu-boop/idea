#!/usr/bin/env python3
"""けいさんプリント（A4 おもて/うら 1まい×12バージョン）。おこづかい5000円、買うものは きまっている。
かけざん（ぜんぶの しなもの）・たしざん・ひきざん・わりざんを たくさん とく。こたえ（先生用）も作る。
  node app_export.js themes → themes.json / python3 build_calc.py → calc.html, calc_answers.html, baskets.json
  node app_export.js art（できあがりの絵 → art/） / node render_calc.js → PDF・zip
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(HERE, p), encoding='utf-8').read()
CSS = re.search(r'CSS = r"""(.*?)"""', rd('../build_prints.py'), re.S).group(1)
CSS2 = re.search(r'CSS2 = r"""(.*?)"""', rd('../daily/build_daily.py'), re.S).group(1)
CSS3 = re.search(r'CSS3 = r"""(.*?)"""', rd('../versions/build_versions.py'), re.S).group(1)
THEMES = json.load(open(os.path.join(HERE, 'themes.json'), encoding='utf-8'))
BUDGET = 5000
fmt = lambda n: f'{n:,}'

ORDER = ['curry', 'parfait', 'plarail', 'car', 'pancake', 'robot', 'pizza', 'sushi', 'burger', 'icecream', 'gyudon', 'ramen']
TITLE = {'curry':'カレー','parfait':'パフェ','plarail':'プラレールの えき','car':'カスタムカー','pancake':'パンケーキ','robot':'ロボット',
         'pizza':'ピザ','sushi':'おすし','burger':'ハンバーガー','icecream':'アイスクリーム','gyudon':'ぎゅうどん','ramen':'ラーメン'}
BASKET = {
 'curry':   {'chicken':2,'beef':1,'carrot':3,'potato':3,'onion':2,'pepper':2,'sweet':2,'rice':3,'egg':2,'cheese':2},
 'parfait': {'jumbo':2,'corn':2,'vanilla':2,'choco':2,'strawberry':3,'banana':2,'whip':2,'custard':2,'sauce':2,'wafer':2},
 'plarail': {'straight':4,'curve':4,'building':1,'platform':2,'shinkansen':1,'keihan':1,'crossing':2,'tunnel':2,'tree':4,'signal':2,'bridge':1},
 'car':     {'sports':1,'red':2,'black':1,'tire':4,'alloy':2,'wing':2,'light':3,'sticker':4,'muffler':2,'neon':2},
 'pancake': {'plain':3,'souffle':1,'maple':2,'honey':2,'strawberry':3,'banana':2,'blueberry':2,'butter':3,'whip':2,'icecream':2},
 'robot':   {'biped':1,'wheel':1,'red':2,'silver':2,'battery':3,'solar':1,'arm':2,'eye':3,'antenna':3,'jet':2,'shield':2},
 'pizza':   {'thin':2,'thick':1,'tomato':3,'white':1,'mozza':2,'cheddar':2,'salami':3,'shrimp':2,'corn':3,'mushroom':2,'pineapple':2,'pepper':2},
 'sushi':   {'nigiri':3,'maki':2,'tuna':3,'salmon':3,'egg':2,'shrimp':2,'squid':2,'ikura':2,'eel':1,'wasabi':2,'gari':2,'tea':3,'miso':2},
 'burger':  {'sesame':2,'beef':3,'chicken':2,'lettuce':3,'tomato':2,'onion':2,'cheese':3,'bacon':2,'ketchup':2,'bbq':2,'fries':3,'drink':3},
 'icecream':{'cone':2,'waffle':1,'cup':2,'vanilla':3,'choco':2,'strawberry':3,'matcha':2,'mint':2,'cherry':3,'whip':2,'sprinkle':3,'wafer':2,'sauce':2},
 'gyudon':  {'regular':2,'large':2,'xl':1,'egg':3,'cheese':2,'negi':3,'kimchi':2,'miso':3,'salad':2,'shinko':2,'tea':3},
 'ramen':   {'shoyu':2,'miso':2,'tonkotsu':1,'chashu':3,'ajitama':3,'negi':2,'nori':3,'menma':2,'corn':2,'kimchi':2,'gyoza':2,'chahan':1,'water':3},
}

def calc(theme, idx=0):
    T = THEMES[theme]; qty = BASKET[theme]; lines = []
    for c in T['cats']:
        assert sum(qty.get(i['id'], 0) for i in c['items']) >= c['min'], (theme, c['id'])
        for i in c['items']:
            q = qty.get(i['id'], 0)
            if q: lines.append(dict(name=i['name'], price=i['price'], q=q, amt=i['price'] * q))
    assert len(lines) == len(qty), theme
    total = sum(l['amt'] for l in lines); assert total <= BUDGET, (theme, total)
    change = BUDGET - total
    top = max(lines, key=lambda l: l['amt'])
    top_q = [l for l in lines if l['q'] >= 2]
    # わりかん
    n = next(k for k in ([5, 2, 4], [2, 4, 5], [4, 5, 2])[idx % 3] if total % k == 0)
    each = total // n
    # あと なんこ
    cands = [i for c in T['cats'] for i in c['items'] if i['price'] <= min(change / 2, 300) and i['price'] >= 40]
    it = max(cands, key=lambda i: i['price']) if cands else dict(name='', price=0)
    more_q, more_r = divmod(change, it['price'])
    half = lines[:6]
    return dict(lines=lines, total=total, change=change, top=top, n=n, each=each, item=it, more_q=more_q, more_r=more_r,
                sub=sum(l['amt'] for l in half), nsub=len(half), less_total=total - top['price'], less_change=BUDGET - (total - top['price']),
                twice=total * 2, enough=total * 2 <= BUDGET)

def fill(cls='', t='', style=''): return f'<span class="fill {cls}" style="{style}">{t}</span>'

CSS4 = r"""
.cxg { display: grid; grid-template-columns: 1fr 1fr; gap: 0 3mm; align-content: space-evenly }
.cx { display: flex; align-items: center; gap: 1.6mm; border-bottom: .3mm dashed #999; padding: .8mm 0; font-size: 4.3mm; white-space: nowrap; min-height: 12.4mm }
.cx .cn { width: 26mm; overflow: hidden; font-size: 4mm }
.cx .ce { font-size: 4.5mm }
.cx .fill { min-width: 21mm; height: 9.4mm; line-height: 8.4mm }
.sm2 { font-size: 3.4mm; color: #333 }
.wrapbox { align-content: center; display: flex; flex-wrap: wrap; align-items: center; gap: 1.2mm 1mm; font-size: 4.6mm }
.wrapbox .fill { min-width: 14mm; height: 10mm; line-height: 9mm }
.pb { display: flex; align-items: center; gap: 2mm; flex-wrap: wrap; font-size: 4.8mm; margin-top: 1mm }
.pb .fill { min-width: 26mm; height: 10.4mm; line-height: 9.4mm }
.q > .pb, .q > .qtext { flex: 0 0 auto }
.q { justify-content: center }
.thumb { flex: 0 0 auto; width: 34mm; height: 25mm; object-fit: cover; border-radius: 2mm; border: .5mm solid #111 }
"""

def page(no, title, side, blocks, foot):
    who = '<div class="who"><div>なまえ <span></span></div><div>ひづけ <span class="d"></span></div></div>'
    head = f'<div class="head"><div class="no">{no}</div><div class="title" style="font-size:6.6mm">{title}</div><div class="side">{side}</div></div>'
    return f'<section class="page">{head}{who}{"".join(blocks)}{foot}</section>'

FOOT_F = '<div class="foot"><span>うらにも つづくよ →</span><span class="stars" style="margin-left:auto">☆ ☆ ☆</span></div>'
FOOT_B = '<div class="foot"><span>できたら ✓：□ ぜんぶ とけた　□ みなおしを した</span><span class="stamp" style="margin-left:auto"></span><span class="stamp"></span></div>'

def front(theme, c, no):
    n = len(c['lines'])
    ban = (f'<div class="banner" style="padding:1.2mm 4mm"><span style="white-space:nowrap">おこづかい</span><b style="white-space:nowrap">{fmt(BUDGET)}えん</b>'
           f'<span>{TITLE[theme]}の かいもの。かごに はいっている ものの きんがくを けいさんしよう！</span>'
           f'<img class="thumb" src="art/{theme}.png" alt=""></div>')
    rows = ''.join(f'<div class="cx"><span class="cn">{l["name"]}</span><span class="ce">{fmt(l["price"])} × {l["q"]} ＝</span>{fill()}<span class="sm2">えん</span></div>' for l in c['lines'])
    q1 = (f'<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">1</span>かけざん <span class="qs">1この ねだん × かず ＝ きんがく（{n}もん）</span></div>'
          f'<div class="cxg" style="flex:1 1 auto">{rows}</div></div>')
    a = lambda k: '＋'.join(fill('s', '', 'min-width:19mm') for _ in range(k))
    q2 = (f'<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">2</span>たしざん① <span class="qs">1〜{c["nsub"]}ばんめの こたえを たそう</span></div>'
          f'<div class="wrapbox">{a(c["nsub"])}＝{fill("", "", "min-width:26mm")}<span>えん</span></div></div>')
    rest = n
    per = 7
    rows3 = []
    for s in range(0, n, per):
        k = min(per, n - s)
        rows3.append('＋'.join(fill('', '', 'min-width:17mm') for _ in range(k)))
    q3 = (f'<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">3</span>たしざん② <span class="qs">ぜんぶの きんがくを たして ごうけいを だそう（{n}こ）</span></div>'
          f'<div class="wrapbox">' + '<span style="flex-basis:100%;height:0"></span>＋'.join(rows3) +
          f'＝{fill("", "", "min-width:26mm")}<span>えん</span></div></div>')
    return [ban, q1, q2, q3]

def back(theme, c, no):
    t, ch = fmt(c['total']), fmt(c['change'])
    top = c['top']
    q4 = ('<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">4</span>ひきざん① <span class="qs">おつりは いくら？</span></div>'
          f'<div class="qtext">おこづかいは {fmt(BUDGET)}えんです。おかいけいは {t}えんでした。おつりは いくらですか。</div>'
          f'<div class="pb"><span>{fmt(BUDGET)} － {t} ＝</span>{fill()}<span>えん</span></div></div>')
    q5 = ('<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">5</span>ひきざん② <span class="qs">1つ へらすと？</span></div>'
          f'<div class="qtext">{top["name"]}（1こ {fmt(top["price"])}えん）を 1こ へらします。</div>'
          f'<div class="pb"><span>ごうけい：{t} － {fmt(top["price"])} ＝</span>{fill()}<span>えん</span></div>'
          f'<div class="pb"><span>おつり：{fmt(BUDGET)} － </span>{fill()}<span>＝</span>{fill()}<span>えん</span></div></div>')
    q6 = ('<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">6</span>わりざん① <span class="qs">わりかん</span></div>'
          f'<div class="qtext">ごうけい {t}えんを、{c["n"]}にんで おなじ きんがくずつ はらいます。ひとり いくらですか。</div>'
          f'<div class="pb"><span>{t} ÷ {c["n"]} ＝</span>{fill()}<span>えん</span></div></div>')
    it = c['item']
    q7 = ('<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">7</span>わりざん② <span class="qs">あと なんこ かえる？</span></div>'
          f'<div class="qtext">おつりは {ch}えんです。{it["name"]}（1こ {fmt(it["price"])}えん）は、あと なんこ かえますか。あまりは いくらですか。</div>'
          f'<div class="pb"><span>{ch} ÷ {fmt(it["price"])} ＝</span>{fill("s")}<span>こ　あまり</span>{fill("s")}<span>えん</span></div></div>')
    q8 = ('<div class="q" style="flex:1 1 auto"><div class="qh"><span class="qn">8</span>かけざん・くらべる <span class="qs">おなじ かいものを もう 1かい したら？</span></div>'
          f'<div class="qtext">ごうけい {t}えんの かいものを 2かい すると、ぜんぶで いくらですか。おこづかい {fmt(BUDGET)}えんで たりますか。</div>'
          f'<div class="pb"><span>{t} × 2 ＝</span>{fill()}<span>えん</span><span style="margin-left:6mm">たりる？</span><span class="mark" style="border:.6mm solid #111;border-radius:50%;width:9mm;height:9mm;display:inline-flex;align-items:center;justify-content:center;font-size:6mm">○</span><span class="mark" style="border:.6mm solid #111;border-radius:50%;width:9mm;height:9mm;display:inline-flex;align-items:center;justify-content:center;font-size:6mm">×</span></div></div>')
    return [q4, q5, q6, q7, q8]

def main():
    comp = {t: calc(t, i) for i, t in enumerate(ORDER)}
    json.dump([dict(day=i + 1, parts=[dict(theme=t, qty=BASKET[t])]) for i, t in enumerate(ORDER)], open(os.path.join(HERE, 'baskets.json'), 'w'), ensure_ascii=False)
    pages = []
    for i, t in enumerate(ORDER):
        c = comp[t]; ttl = f'{TITLE[t]}の けいさん'
        pages.append(page(i + 1, ttl, 'おもて', front(t, c, i + 1), FOOT_F))
        pages.append(page(i + 1, ttl, 'うら', back(t, c, i + 1), FOOT_B))
    st = f'<style>{CSS}{CSS2}{CSS3}{CSS4}</style>'
    open(os.path.join(HERE, 'calc.html'), 'w', encoding='utf-8').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>けいさんプリント</title>{st}</head><body>{"".join(pages)}</body></html>')
    cards = []
    for i, t in enumerate(ORDER):
        c = comp[t]
        l1 = '、'.join(f'{l["name"]} {fmt(l["amt"])}' for l in c['lines'])
        cards.append(f'<div class="dayrow"><h2>{i+1}　{TITLE[t]}（{len(c["lines"])+9}もん）</h2>'
                     f'<p><b>1：</b>{l1}</p>'
                     f'<p><b>2：</b>{fmt(c["sub"])}えん　<b>3：</b>{fmt(c["total"])}えん　<b>4：</b>{fmt(c["change"])}えん　'
                     f'<b>5：</b>{fmt(c["less_total"])}えん／{fmt(c["less_change"])}えん　<b>6：</b>{c["n"]}にんで {fmt(c["each"])}えん　'
                     f'<b>7：</b>{c["more_q"]}こ あまり {fmt(c["more_r"])}えん（{c["item"]["name"]} {fmt(c["item"]["price"])}えん）　'
                     f'<b>8：</b>{fmt(c["twice"])}えん・{"たりる ○" if c["enough"] else "たりない ×"}</p></div>')
    guide = ('<div class="dayrow" style="background:#f2f2f2"><h2>つかいかた</h2>'
             '<p>・おこづかい 5,000えんの かいものが きまっていて、かけざん・たしざん・ひきざん・わりざんを たくさん けいさんする プリントです（1まい 15〜22もん。アプリの おかいけい 3もんの 5ばい前後）。</p>'
             '<p>・ねだんは アプリと おなじ。「1」の こたえを「2・3」で つかいます（まちがいに きづくと ○。こたえは ぜんぶ ここに あります）。</p>'
             '<p>・むずかしい ときは 1まいを 2にちに わけて（おもて／うら）。でんたく・おかねの おもちゃを つかっても よいです。</p></div>')
    chunks = [cards[0:3], cards[3:6], cards[6:9], cards[9:12]]
    ans = [f'<section class="ans-page"><h1>せんせいよう　こたえ（{k+1}/{len(chunks)}）</h1>{guide if k == 0 else ""}{"".join(ch)}</section>' for k, ch in enumerate(chunks)]
    open(os.path.join(HERE, 'calc_answers.html'), 'w', encoding='utf-8').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>こたえ</title>{st}</head><body>{"".join(ans)}</body></html>')
    for t in ORDER:
        c = comp[t]; print(t, len(c['lines']), c['total'], c['change'], c['n'], c['item']['name'], c['more_q'], c['more_r'], len(c['lines']) + 9)
main()
