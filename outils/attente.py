# Page d'attente de swipelearn.school (30/10/2026) : remplace le site du groupe le temps de finaliser les démarches.
# Le vrai site reste dans le dépôt : pour le remettre en ligne, relancer outils/construire.py (qui réécrit public/index.html,
# le plan du site et la page 404) et remettre l'ancien sw.js (historique git).
# Règles : aucun lien, aucune école citée par son nom, aucun financement, aucun chiffre, aucune promesse d'admission.
import os, re, json
ICI = os.path.dirname(os.path.abspath(__file__))
RAC = os.path.dirname(ICI)
PUB = os.path.join(RAC, 'public')
SITE = 'https://swipelearn.school'

# polices du site (déjà servies en local) et icônes des sept métiers, reprises du générateur du vrai site
src = open(os.path.join(ICI, 'source', 'maquette-origine.html'), encoding='utf-8').read() if os.path.exists(os.path.join(ICI, 'source', 'maquette-origine.html')) else ''
FACES = ''.join(
    "@font-face{font-family:'%s';font-style:normal;font-display:swap;font-weight:%s;src:url(/polices/%s) format('woff2')}" % (fam, w, f)
    for fam, w, f in [('Baloo 2', 700, 'baloo-2-latin-700-normal.woff2'), ('Baloo 2', 800, 'baloo-2-latin-800-normal.woff2'),
                      ('Nunito', 400, 'nunito-latin-400-normal.woff2'), ('Nunito', 700, 'nunito-latin-700-normal.woff2'),
                      ('Nunito', 800, 'nunito-latin-800-normal.woff2')])
S = 'viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
METIERS = [
    ('Cuisine', '#4A6FB5', '<path d="M10 24h28v8a8 8 0 0 1-8 8H18a8 8 0 0 1-8-8v-8z"/><path d="M10 27H5M43 27h-5"/><path d="M18 17c0-3 3-3 3-6M27 17c0-3 3-3 3-6"/>'),
    ('Vente', '#C96A2E', '<path d="M9 24v14a2 2 0 0 0 2 2h26a2 2 0 0 0 2-2V24"/><path d="M6 11h36l3 8c0 3-2.7 5-6 5s-6-2-6-5c0 3-2.7 5-6 5s-6-2-6-5c0 3-2.7 5-6 5s-6-2-6-5l3-8z"/><path d="M20 40V30h8v10"/>'),
    ('Aide à la personne', '#4E9B84', '<path d="M24 28s-7.4-4.7-9.8-9.3C12.3 15 14.2 11 18 11c2.5 0 4.4 1.4 6 3.7 1.6-2.3 3.5-3.7 6-3.7 3.8 0 5.7 4 3.8 7.7C31.4 23.3 24 28 24 28z"/><path d="M10 38c4.5-3 9-3 14-3h7a3 3 0 0 1 0 6H21"/>'),
    ('Gestion', '#9C5A80', '<rect x="6" y="15" width="36" height="24" rx="4"/><path d="M18 15v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3"/><path d="M6 26h15M27 26h15"/><rect x="21" y="23.5" width="6" height="5" rx="1.5"/>'),
    ('Numérique', '#7C6AA6', '<rect x="6" y="9" width="36" height="30" rx="4"/><path d="M6 16h36"/><path d="M17 24l-5 5 5 5M31 24l5 5-5 5M26 22l-4 14"/>'),
    ('Bâtiment', '#B8892E', '<path d="M8 31a16 16 0 0 1 12.5-15.6V13a3.5 3.5 0 0 1 7 0v2.4A16 16 0 0 1 40 31"/><path d="M5 31h38v4a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-4z"/><path d="M24 15v10"/>'),
    ('Transport', '#A8524E', '<path d="M4 13h23v19H4z"/><path d="M27 19h9l8 8v5H27"/><circle cx="12" cy="36" r="4"/><circle cx="34" cy="36" r="4"/><path d="M16 36h14"/>'),
]
tuiles = ''.join(f'<li style="--c:{c};--d:{i*.12:.2f}s"><svg {S} aria-hidden="true">{p}</svg><span>{n}</span></li>' for i, (n, c, p) in enumerate(METIERS))
I = lambda p: f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
POINTS = [
    (I('<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>'), 'Les cours en ligne', 'La théorie se suit à votre rythme, avec un formateur.'),
    (I('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'), 'Près de chez vous', 'Chaque école s’appuie sur des entreprises de votre territoire.'),
    (I('<path d="M14 7l3-3 3 3-3 3"/><path d="M17 4v7a4 4 0 0 1-4 4H4"/><path d="M7 12l-3 3 3 3"/>'), 'La pratique pour de vrai', 'Les gestes du métier s’apprennent chez nos partenaires, en situation réelle.'),
]
pts = ''.join(f'<div class="pt">{ic}<b>{t}</b><p>{d}</p></div>' for ic, t, d in POINTS)

TITRE = 'Swipe Learn School · Sept écoles de métiers, bientôt'
DESC = 'Swipe Learn School prépare ses cours : sept écoles, sept métiers. La théorie en ligne, la pratique chez des entreprises partenaires, près de chez vous.'
LD = json.dumps({'@context': 'https://schema.org', '@type': 'EducationalOrganization', 'name': 'Swipe Learn School', 'url': SITE + '/',
                 'logo': SITE + '/logos/icone-groupe-512.png', 'description': DESC}, ensure_ascii=False)

dots = ''.join(f'<span style="--c:{c};animation-delay:{i*.3:.1f}s"></span>' for i, (n, c, p) in enumerate(METIERS))
noms = ' · '.join(n for n, c, p in METIERS)
pts1 = ''.join(f'<div class="pt">{ic}<div><b>{t}</b><p>{d}</p></div></div>' for ic, t, d in POINTS)
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITRE}</title><meta name="description" content="{DESC}"><link rel="canonical" href="{SITE}/">
<meta name="theme-color" content="#2B2213"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/logos/icone-groupe.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/logos/apple-touch-icon.png">
<meta property="og:title" content="Swipe Learn School"><meta property="og:description" content="{DESC}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}/"><meta property="og:image" content="{SITE}/logos/icone-groupe-512.png">
<link rel="preload" href="/polices/baloo-2-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">{LD}</script>
<style>{FACES}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Nunito,Arial,sans-serif;background:#2B2213;color:#F2F1EE;min-height:100vh}}
.m{{max-width:1100px;margin:0 auto;padding:28px 24px;min-height:100vh;display:flex;flex-direction:column;gap:40px}}
.marque{{display:flex;align-items:center;gap:12px;font-family:'Baloo 2';font-weight:800;letter-spacing:.04em}}.marque img{{border-radius:12px}}
.c{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px}}
h1{{font-family:'Baloo 2';font-size:clamp(3.2rem,11vw,8rem);line-height:.9;color:#fff;font-weight:800}}
.dots{{display:flex;gap:12px}}.dots span{{width:20px;height:20px;border-radius:50%;background:var(--c);animation:al 2.8s ease-in-out infinite;opacity:.3}}
@keyframes al{{30%{{opacity:1;transform:scale(1.3)}}}}
.noms{{font-family:'Baloo 2';font-weight:700;font-size:1.15rem;color:#C89B2E}}
.intro{{font-size:1.1rem;line-height:1.65;max-width:56ch;color:#E8E2D2}}
.force{{font-family:'Baloo 2';font-size:1.5rem;font-weight:700;color:#fff;max-width:32ch;line-height:1.2}}
.pts{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;border-top:1px solid rgba(255,255,255,.15);padding-top:24px}}
.pt{{display:flex;gap:12px}}.pt svg{{width:26px;height:26px;color:#C89B2E;flex:none}}.pt b{{font-family:'Baloo 2';font-size:1.1rem;display:block}}.pt p{{color:#D8D0BE;line-height:1.5;font-size:.95rem}}
footer{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:.9rem;color:#D8D0BE}}footer b{{font-family:'Baloo 2';color:#C89B2E}}
@media(max-width:760px){{.pts{{grid-template-columns:1fr}}}}
@media(prefers-reduced-motion:reduce){{.dots span{{animation:none;opacity:1}}}}
</style></head><body><main class="m">
<div class="marque"><img src="/logos/icone-groupe.svg" alt="" width="44" height="44">SWIPE LEARN SCHOOL</div>
<div class="c"><div class="dots" aria-hidden="true">{dots}</div><h1>On prépare<br>vos cours.</h1><p class="noms">{noms}</p>
<p class="intro">Swipe Learn School réunit sept écoles, une par métier. Nous finalisons tout pour vous accueillir dans les meilleures conditions.</p>
<p class="force">Sept métiers différents, une même façon d’apprendre : c’est notre force.</p><div class="pts">{pts1}</div></div>
<footer><span>© 2026 Swipe Learn School · <b>Auvergne-Rhône-Alpes</b></span><span>Prochainement dans votre région</span></footer>
</main></body></html>'''

open(os.path.join(PUB, 'index.html'), 'w', encoding='utf-8').write(page)
open(os.path.join(PUB, '404.html'), 'w', encoding='utf-8').write(page.replace(f'<link rel="canonical" href="{SITE}/">', '<meta name="robots" content="noindex">'))
open(os.path.join(PUB, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{SITE}/</loc><priority>1.0</priority></url>\n</urlset>\n')
# l'application installée : un service worker qui vide les caches de l'ancien site et se désinstalle
open(os.path.join(PUB, 'sw.js'), 'w', encoding='utf-8').write(
    "// Page d'attente : vide les caches de l'ancien site et se désinstalle, pour que personne ne garde l'ancienne version.\n"
    "self.addEventListener('install', () => self.skipWaiting());\n"
    "self.addEventListener('activate', (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.map((k) => caches.delete(k))))"
    ".then(() => self.registration.unregister()).then(() => self.clients.matchAll()).then((cs) => cs.forEach((c) => c.navigate(c.url)))); });\n")
for interdit in ['Cook', 'cook', 'Sell', 'Care', 'CPF', 'OPCO', 'Qualiopi', '<a ']:
    assert interdit not in page, interdit
print('page d\'attente écrite', len(page))
