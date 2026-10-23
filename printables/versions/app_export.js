// アプリ（keisan/index-single.html）から、材料・値段のデータと「できあがり」の絵を書き出す。
//   node app_export.js themes   → themes.json
//   node app_export.js art      → baskets.json にある買い物ごとに art/*.png
const path = require('path'), fs = require('fs');
const {execSync} = require('child_process');
let pw;
try { pw = require('playwright'); } catch (e) { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const here = __dirname, app = path.join(here, '..', '..', 'keisan', 'index-single.html');
(async () => {
  const mode = process.argv[2];
  const b = await pw.chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const ctx = await b.newContext({viewport: {width: 900, height: 1000}, deviceScaleFactor: 2});
  const pg = await ctx.newPage();
  await pg.goto('file://' + app);
  if (mode === 'themes') {
    const t = await pg.evaluate(() => JSON.parse(JSON.stringify(THEMES)));
    fs.writeFileSync(path.join(here, 'themes.json'), JSON.stringify(t, null, 1));
    console.log('themes:', Object.keys(t).join(','));
  } else if (mode === 'art') {
    const plan = JSON.parse(fs.readFileSync(path.join(here, 'baskets.json'), 'utf8'));
    for (const d of plan) for (let i = 0; i < d.parts.length; i++) {
      const p = d.parts[i];
      await pg.evaluate(() => startApp2());
      await pg.evaluate(t => document.querySelector('[data-t=' + t + ']').click(), p.theme);
      await pg.evaluate(q => { shop.qty = q; finishApp2([{ok: true}, {ok: true}, {ok: true}]); }, p.qty);
      await pg.waitForTimeout(500);
      await pg.locator('.illust').screenshot({path: path.join(here, 'art', `day${d.day}-${i}.png`)});
    }
    console.log('art done');
  }
  await b.close();
})();
