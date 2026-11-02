// daily.html / daily_answers.html を A4 の PDF にして、はみ出しも検査する。 node render_daily.js
const path = require('path'), {execSync} = require('child_process');
let pw; try { pw = require('playwright'); } catch (e) { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
(async () => {
  const b = await pw.chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const pg = await b.newPage();
  for (const [html, pdf] of [['daily.html', 'けいさんアプリ10日ぶんプリント.pdf'], ['daily_answers.html', 'せんせいよう 10日ぶん こたえ.pdf']]) {
    await pg.goto('file://' + path.join(__dirname, html));
    await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => {}) : 0)));
    const over = await pg.evaluate(() => [...document.querySelectorAll('.page, .ans-page')].map((p, i) => ({i: i + 1, over: p.scrollHeight - p.clientHeight})));
    const bad = over.filter(o => o.over > 1);
    console.log(html, 'ページ数', over.length, bad.length ? 'はみ出し ' + JSON.stringify(bad) : 'はみ出しなし');
    await pg.pdf({path: path.join(__dirname, pdf), format: 'A4', printBackground: true, margin: {top: 0, right: 0, bottom: 0, left: 0}, preferCSSPageSize: true});
  }
  await b.close();
})();
