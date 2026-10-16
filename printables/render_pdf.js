// prints.html / answers.html を A4 の PDF にする。はみ出し（ページに収まらない内容）も検査する。
// 使い方: node render_pdf.js   （Playwright が必要）
const path = require('path');
const {execSync} = require('child_process');
let pw;
try { pw = require('playwright'); } catch (e) { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const {chromium} = pw;
const here = __dirname;
(async () => {
  const exe = process.env.PLAYWRIGHT_BROWSERS_PATH ? undefined : undefined;
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const pg = await b.newPage();
  for (const [html, pdf] of [['prints.html', 'せいかつさんすうプリント.pdf'], ['answers.html', 'せんせいよう こたえとポイント.pdf']]) {
    await pg.goto('file://' + path.join(here, html));
    await pg.waitForLoadState('load');
    await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => {}) : 0)));
    const over = await pg.evaluate(() => [...document.querySelectorAll('.page, .ans-page')].map((p, i) => {
      // 中身の下端が、ページの下の余白をこえていないか
      const kids = [...p.children]; const last = kids[kids.length - 1];
      const pr = p.getBoundingClientRect();
      const bottoms = kids.map(k => k.getBoundingClientRect().bottom - pr.top);
      return {i: i + 1, scroll: p.scrollHeight - p.clientHeight, lastBottom: Math.round(Math.max(...bottoms)), pageH: Math.round(pr.height)};
    }));
    const bad = over.filter(o => o.scroll > 1);
    console.log(html, 'ページ数', over.length, bad.length ? 'はみ出し: ' + JSON.stringify(bad) : 'はみ出しなし');
    await pg.pdf({path: path.join(here, pdf), format: 'A4', printBackground: true, margin: {top: 0, right: 0, bottom: 0, left: 0}, preferCSSPageSize: true});
  }
  await b.close();
})();
