// versions.html / versions_answers.html を A4 PDF にして はみ出しを検査。まとめPDF・バージョンべつPDF・zip も作る。 node render_versions.js
const path = require('path'), fs = require('fs'), {execSync} = require('child_process');
let pw; try { pw = require('playwright'); } catch (e) { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const here = __dirname, ORDER = JSON.parse(fs.readFileSync(path.join(here, 'baskets.json'), 'utf8')).map(p => p.parts[0].theme);
const NAME = {curry:'カレー',parfait:'パフェ',plarail:'プラレール',car:'カスタムカー',pancake:'パンケーキ',robot:'ロボット',pizza:'ピザ',sushi:'おすし',burger:'ハンバーガー',icecream:'アイスクリーム',gyudon:'ぎゅうどん',ramen:'ラーメン'};
(async () => {
  const b = await pw.chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const pg = await b.newPage();
  const ALL = 'けいさんアプリ 全バージョン まとめプリント.pdf', ANS = 'せんせいよう こたえれい.pdf';
  for (const [html, pdf] of [['versions.html', ALL], ['versions_answers.html', ANS]]) {
    await pg.goto('file://' + path.join(here, html));
    await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => {}) : 0)));
    const over = await pg.evaluate(() => [...document.querySelectorAll('.page, .ans-page')].map((p, i) => ({i: i + 1, over: p.scrollHeight - p.clientHeight})));
    const bad = over.filter(o => o.over > 1);
    console.log(html, 'ページ数', over.length, bad.length ? 'はみ出し ' + JSON.stringify(bad) : 'はみ出しなし');
    await pg.pdf({path: path.join(here, pdf), format: 'A4', printBackground: true, margin: {top: 0, right: 0, bottom: 0, left: 0}, preferCSSPageSize: true});
  }
  await b.close();
  // バージョンべつPDF
  const dir = path.join(here, 'out'); fs.rmSync(dir, {recursive: true, force: true}); fs.mkdirSync(dir);
  const tmp = fs.mkdtempSync('/tmp/pdfsplit-');
  execSync(`pdfseparate "${path.join(here, ALL)}" "${tmp}/p-%02d.pdf"`);
  ORDER.forEach((t, i) => {
    const a = String(i * 2 + 1).padStart(2, '0'), c = String(i * 2 + 2).padStart(2, '0');
    execSync(`pdfunite "${tmp}/p-${a}.pdf" "${tmp}/p-${c}.pdf" "${dir}/${String(i + 1).padStart(2, '0')}_${NAME[t]}.pdf"`);
  });
  fs.copyFileSync(path.join(here, ANS), path.join(dir, '00_せんせいよう こたえれい.pdf'));
  fs.copyFileSync(path.join(here, ALL), path.join(dir, '全バージョン まとめプリント.pdf'));
  const zip = path.join(here, 'けいさんアプリ プリント一括ダウンロード.zip'); fs.rmSync(zip, {force: true});
  execSync(`cd "${dir}" && zip -q -r "${zip}" .`);
  console.log('zip', fs.statSync(zip).size);
})();
