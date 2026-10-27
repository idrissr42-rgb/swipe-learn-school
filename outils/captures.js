// Captures d'écran de l'application (affichées par Android dans la fenêtre « Installer »).
// À relancer après un changement visible : node outils/captures.js && python3 outils/construire.py
// (construire.py les convertit en WebP, plus légères)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const PUB = path.join(__dirname, '..', 'public'), OUT = path.join(PUB, 'captures');
const types = { '.html': 'text/html; charset=utf-8', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const f = path.join(PUB, p); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
srv.listen(0, async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch(), c = await b.newContext({ viewport: { width: 360, height: 780 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true }), pg = await c.newPage();
  await pg.goto(`http://localhost:${srv.address().port}/`); await pg.waitForTimeout(1200);
  await pg.addStyleTag({ content: 'html{scroll-behavior:auto!important}.rv{opacity:1!important;transform:none!important}' });
  await pg.screenshot({ path: path.join(OUT, 'accueil.png') });
  await pg.evaluate(() => { const s = document.querySelector('#ecoles .sec-titre'); scrollTo(0, s.getBoundingClientRect().top + scrollY - 76); }); await pg.waitForTimeout(500);
  await pg.screenshot({ path: path.join(OUT, 'ecoles.png') });
  await b.close(); srv.close(); console.log('captures : accueil.png, ecoles.png');
});
