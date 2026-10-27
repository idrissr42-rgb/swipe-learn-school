# Confort sur téléphone et application installable, communs aux sites Swipe Learn School.
# Utilisé par construire.py : ajoute au <head> les balises de l'application, avant </body> les styles et
# le script (carrousels à faire glisser, bandeau « Installer »), et écrit le manifeste, le service worker,
# la page hors connexion et les icônes de l'application.
import json, os
from PIL import Image

NOM, COURT = 'Swipe Learn School', 'Swipe Learn'
FOND, THEME, OR = '#FAF6EE', '#FAF6EE', (200, 155, 46)
VERSION_CACHE = 'sls-v1'


def tete():
    return ('<link rel="manifest" href="/manifest.webmanifest">'
            f'<meta name="theme-color" content="{THEME}">'
            '<link rel="apple-touch-icon" href="/logos/apple-touch-icon.png">'
            f'<meta name="apple-mobile-web-app-title" content="{COURT}">'
            '<meta name="mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="default">')


STYLE = r'''<style>/* SL_MOBILE : confort sur téléphone */
.sl-points{display:none}
#sl-installer{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:120;max-width:520px;margin:0 auto;display:flex;align-items:center;gap:12px;background:var(--brun);color:var(--creme);border-radius:18px;padding:12px 12px 12px 14px;box-shadow:0 18px 40px rgba(20,14,4,.35);transform:translateY(150%);transition:transform .4s cubic-bezier(.2,.8,.2,1)}
#sl-installer.on{transform:none}
#sl-installer img{width:42px;height:42px;border-radius:11px;flex:none}
#sl-installer .t{flex:1;min-width:0;font-size:.82rem;line-height:1.35;color:#D9CFB8}
#sl-installer .t b{display:block;font-family:'Baloo 2';font-size:.98rem;color:var(--creme)}
#sl-installer button{border:0;border-radius:999px;font-family:'Baloo 2';font-weight:700;cursor:pointer;flex:none}
#sl-installer .oui{background:var(--moutarde);color:#fff;padding:10px 16px;font-size:.9rem}
#sl-installer .non{background:none;color:#C9BE9E;padding:10px 4px;font-size:.8rem}
#sl-installer .partager{display:inline-block;vertical-align:-3px;width:16px;height:16px}
@media(prefers-reduced-motion:reduce){#sl-installer{transition:none}}
@media(max-width:700px){
  .wrap{padding:0 16px}
  section{padding:46px 0}
  .sec-titre{font-size:1.6rem;line-height:1.18}
  .sec-titre .tiret{width:44px;height:4px;margin-top:10px}
  .sec-sub{font-size:.9rem;line-height:1.5;margin-bottom:22px}
  .btn{padding:12px 20px;font-size:.95rem}
  nav .wrap{height:64px}
  .brand{gap:10px}
  .brand .lg{width:40px;height:40px;border-radius:12px}
  /* accueil */
  .hero{padding:24px 0 30px}
  .hero .wrap{gap:8px}
  .sur{font-size:.62rem;letter-spacing:.05em;padding:6px 12px;margin-bottom:14px}
  .hero h1{font-size:clamp(1.8rem,8.4vw,2.15rem);line-height:1.16}
  .hero h1 .m::after{height:9px;bottom:3px}
  .hero p{margin:14px 0 18px;font-size:.92rem;line-height:1.6}
  .hero-actions{flex-direction:column;gap:8px;margin-bottom:14px}
  .hero-actions .btn{width:100%;min-height:48px;padding:11px 18px;font-size:.95rem;justify-content:center}
  .hero-actions .btn .fl{width:14px;height:14px}
  .confiance{gap:6px 14px;font-size:.74rem}
  .scene{width:220px;height:170px}
  .scene .halo{width:150px;height:150px}
  .slide svg{width:84px;height:84px}
  .slide b{font-size:1.05rem}
  .selecteur{gap:2px}
  .selecteur button{padding:6px 5px}
  .selecteur button svg{width:24px;height:24px}
  .ruban{padding:9px 0}
  .ruban em{width:22px;height:22px;margin:0 10px}
  .chiffres{padding:24px 0}
  .chiffres .wrap{gap:16px 10px}
  .chiffres .v{font-size:1.6rem}
  .chiffres .l{font-size:.72rem;line-height:1.35}
  /* écoles */
  .modalites-legende{gap:10px;margin-bottom:18px}
  .mod-lg{padding:12px 14px;font-size:.82rem;line-height:1.45}
  .ecole{padding:18px 16px 16px;gap:10px}
  .ecole-ic{width:46px;height:46px;border-radius:14px}
  .ecole-ic svg{width:26px;height:26px}
  .ecole ul{gap:6px}
  .ecole li{padding:8px 11px;font-size:.82rem;gap:10px;border-radius:12px}
  .ecole.bientot ul li:nth-child(n+4):not(:last-child){display:none}
  .ecole .btn{padding:11px 18px;font-size:.9rem}
  /* parcours : une ligne de temps verticale */
  .etapes{grid-template-columns:1fr;row-gap:14px}
  .etape{display:grid;grid-template-columns:44px 1fr;column-gap:14px;text-align:left;padding:0;max-width:none;margin:0}
  .etape .pt{width:44px;height:44px;margin:0;font-size:1.1rem;border-width:2px;grid-row:1/3;box-shadow:none}
  .etape h4{margin:4px 0 2px;font-size:.98rem}
  .etape p{font-size:.84rem;line-height:1.5}
  /* test, méthode, CAP intensif, métiers */
  .quiz-box{padding:22px 16px}
  .meth{padding:18px 16px}
  .meth-ic{width:44px;height:44px;border-radius:13px;margin-bottom:10px}
  .meth h4{font-size:1rem}
  .meth p{font-size:.86rem;line-height:1.55}
  .intensif-grid{gap:12px;margin-top:18px}
  .intensif-grid .carte{padding:16px;font-size:.88rem;line-height:1.5}
  .intensif-cta{gap:8px}
  .intensif-cta .btn{flex:1 1 100%;justify-content:center}
  .mcard-top{padding:14px 16px}
  .mcard-body{padding:14px 16px 16px;gap:10px}
  /* comparateur : deux lignes par formation */
  .comp-filtres{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;gap:6px;margin:0 -16px 16px;padding:0 16px 4px;scrollbar-width:none}
  .comp-filtres::-webkit-scrollbar{display:none}
  .comp-filtre{flex:none;padding:7px 14px;font-size:.8rem}
  .comp-row{grid-template-columns:auto auto 1fr auto;gap:6px 10px;padding:12px 14px;align-items:center}
  .comp-row .cf-nom{grid-column:1/-1;font-size:.9rem;line-height:1.25}
  .comp-cell::before{display:none}
  .comp-cell{font-size:.8rem}
  .comp-row .btn-mini{margin:0;padding:6px 14px}
  /* financement, questions, appel final, pied de page */
  .gcard summary{padding:14px 16px;gap:12px}
  .reconv{position:static;padding:22px 18px}
  .faq-list{gap:10px}
  .faq-item summary{padding:14px 16px;font-size:.94rem}
  .grand-cta{padding:44px 0}
  .grand-cta p{margin:10px auto 20px;font-size:.92rem}
  footer{padding:34px 0 18px}
  footer .wrap{gap:22px}
  footer .wrap>div:nth-child(3) ul{display:flex;flex-wrap:wrap;gap:4px 16px}
  .legal{margin-top:6px;font-size:.72rem;line-height:1.5}
  /* carrousels à faire glisser */
  .sl-car{display:flex!important;gap:12px!important;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:16px;margin-inline:-16px;padding:4px 16px 12px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .sl-car::-webkit-scrollbar{display:none}
  .sl-car>*{flex:0 0 min(84%,340px);scroll-snap-align:start;margin:0!important;max-width:none!important}
  .sl-car>.rv{opacity:1;transform:none;transition-delay:0s!important}
  .sl-points{display:flex;justify-content:center;align-items:center;gap:2px;margin-top:4px}
  .sl-points button{width:22px;height:22px;padding:0;border:0;background:none;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:width .25s}
  .sl-points button::before{content:"";width:7px;height:7px;border-radius:99px;background:var(--beige-f);transition:width .25s,background .25s}
  .sl-points button.on{width:34px}
  .sl-points button.on::before{width:22px;background:var(--moutarde)}
  .metiers .sl-points button::before,.guide .sl-points button::before{background:#D8CBB0}
}
</style>'''

SCRIPT = r'''<script>/* SL_APPLI : carrousels sur téléphone, application installable */
(function(){
  /* ---------- carrousels à faire glisser (téléphone seulement) */
  var mq=window.matchMedia('(max-width:700px)'),CIBLES=['.ecoles-grid','.intensif-grid','.meth-grid','#metiersGrid'];
  function cartes(el){return [].slice.call(el.children).filter(function(c){return c.nodeType===1;});}
  function demonter(el){if(!el.classList.contains('sl-car'))return;el.classList.remove('sl-car');if(el._slPoints){el._slPoints.remove();el._slPoints=null;}el.removeEventListener('scroll',el._slScroll);}
  function monter(el){
    var cs=cartes(el);if(cs.length<2||el.classList.contains('sl-car'))return;
    el.classList.add('sl-car');cs.forEach(function(c){c.classList.add('on');});
    var p=document.createElement('div');p.className='sl-points';
    cs.forEach(function(c,i){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Voir la carte '+(i+1)+' sur '+cs.length);
      b.onclick=function(){el.scrollTo({left:c.offsetLeft-cs[0].offsetLeft,behavior:'smooth'});};p.appendChild(b);});
    el.parentNode.insertBefore(p,el.nextSibling);el._slPoints=p;
    var attente=0;function maj(){attente=0;var pas=cs[1].offsetLeft-cs[0].offsetLeft||1,i=Math.round(el.scrollLeft/pas);
      if(el.scrollLeft+el.clientWidth>=el.scrollWidth-4)i=cs.length-1;
      [].forEach.call(p.children,function(b,j){b.classList.toggle('on',j===i);b.setAttribute('aria-current',j===i?'true':'false');});}
    el._slScroll=function(){if(!attente)attente=requestAnimationFrame(maj);};el.addEventListener('scroll',el._slScroll,{passive:true});maj();
  }
  function appliquer(){CIBLES.forEach(function(s){var el=document.querySelector(s);if(!el)return;if(mq.matches){demonter(el);monter(el);}else demonter(el);});}
  CIBLES.forEach(function(s){var el=document.querySelector(s);if(el&&window.MutationObserver)new MutationObserver(function(){if(mq.matches){demonter(el);monter(el);}}).observe(el,{childList:true});});
  if(mq.addEventListener)mq.addEventListener('change',appliquer);else if(mq.addListener)mq.addListener(appliquer);
  appliquer();

  /* ---------- application installable */
  var installee=window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  if('serviceWorker' in navigator&&location.protocol==='https:')window.addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});
  var invite=null,CLE='sl_installer_plus_tard',bandeau=null;
  var ios=/iphone|ipad|ipod/i.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  function refusRecent(){try{return Date.now()-(+localStorage.getItem(CLE)||0)<30*864e5;}catch(e){return false;}}
  function noterRefus(){try{localStorage.setItem(CLE,String(Date.now()));}catch(e){}}
  function fermer(){if(!bandeau)return;var b=bandeau;bandeau=null;b.classList.remove('on');setTimeout(function(){b.remove();},450);}
  function montrer(texte,bouton,action){
    if(bandeau||installee)return;bandeau=document.createElement('div');bandeau.id='sl-installer';bandeau.setAttribute('role','dialog');bandeau.setAttribute('aria-label','Installer l’application');
    bandeau.innerHTML='<img src="/logos/icone-groupe-192.png" alt=""><div class="t">'+texte+'</div><button class="non" type="button">Plus tard</button>'+(bouton?'<button class="oui" type="button">'+bouton+'</button>':'');
    document.body.appendChild(bandeau);requestAnimationFrame(function(){requestAnimationFrame(function(){if(bandeau)bandeau.classList.add('on');});});
    bandeau.querySelector('.non').onclick=function(){noterRefus();fermer();};
    var oui=bandeau.querySelector('.oui');if(oui)oui.onclick=function(){fermer();action&&action();};
  }
  var PARTAGER='<svg class="partager" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>';
  function lancer(){if(!invite)return;invite.prompt();var i=invite;invite=null;if(i.userChoice)i.userChoice.then(function(r){if(r&&r.outcome!=='accepted')noterRefus();majLien();});}
  function proposerAndroid(){montrer('<b>Installer Swipe Learn School</b>Sur votre écran d’accueil, comme une application.','Installer',lancer);}
  function proposerIos(){montrer('<b>Installer Swipe Learn School</b>Touchez '+PARTAGER+' Partager, puis « Sur l’écran d’accueil ».',null,null);}
  function auBonMoment(f){var fait=false;function go(){if(fait)return;fait=true;removeEventListener('scroll',sc);f();}function sc(){if(window.scrollY>window.innerHeight*.9)go();}addEventListener('scroll',sc,{passive:true});setTimeout(go,15000);}
  var lien=document.getElementById('sl-installer-lien');
  function majLien(){if(lien&&lien.parentNode)lien.parentNode.style.display=installee?'none':'';}
  if(lien)lien.addEventListener('click',function(e){e.preventDefault();if(invite)lancer();else if(ios)proposerIos();
    else montrer('<b>Installer l’application</b>Dans le menu de votre navigateur, choisissez « Installer l’application » ou « Ajouter à l’écran d’accueil ».',null,null);});
  window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();invite=e;majLien();if(!installee&&!refusRecent())auBonMoment(proposerAndroid);});
  window.addEventListener('appinstalled',function(){installee=true;invite=null;fermer();majLien();});
  if(ios&&!installee&&!refusRecent())auBonMoment(proposerIos);
  majLien();
})();
</script>'''

SW = '''// Swipe Learn School : application installable.
// Le réseau d'abord, toujours ; sans connexion, la dernière version vue du site, sinon la page « hors connexion ».
// Ne touche ni aux autres sites ni aux envois (seulement les lectures GET de ce site).
const CACHE = '%s';
const BASE = ['/', '/hors-ligne.html', '/logos/icone-groupe-192.png', '/favicon.ico'];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);
  if (u.origin !== self.location.origin) return;
  if (r.mode === 'navigate') {
    e.respondWith(fetch(r).then((rep) => {
      if (rep.ok) { const copie = rep.clone(); caches.open(CACHE).then((c) => c.put(u.pathname, copie)); }
      return rep;
    }).catch(() => caches.match(u.pathname).then((x) => x || caches.match('/')).then((x) => x || caches.match('/hors-ligne.html'))));
    return;
  }
  e.respondWith(caches.match(r).then((x) => {
    const reseau = fetch(r).then((rep) => {
      if (rep.ok) { const copie = rep.clone(); caches.open(CACHE).then((c) => c.put(r, copie)); }
      return rep;
    }).catch(() => x || Response.error());
    return x || reseau;
  }));
});
''' % VERSION_CACHE

HORS_LIGNE = '''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hors connexion · Swipe Learn School</title><meta name="robots" content="noindex"><meta name="theme-color" content="%s"></head>
<body style="margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:Nunito,Arial,sans-serif;background:%s;color:#2E2415;text-align:center;padding:24px;box-sizing:border-box">
<div><img src="/logos/icone-groupe-192.png" alt="" width="72" height="72" style="border-radius:18px"><h1 style="font-size:1.4rem;margin:18px 0 8px">Vous êtes hors connexion</h1><p style="margin:0 0 20px;color:#5C513C">Swipe Learn School s’affichera dès que le réseau reviendra.</p><button onclick="location.reload()" style="border:0;border-radius:999px;background:#C89B2E;color:#fff;font-weight:700;font-size:1rem;padding:12px 24px">Réessayer</button></div>
</body></html>
''' % (THEME, FOND)


def icones(public):
    """Icône « masquable » (plein cadre, Android la découpe à sa forme) et icône Apple, depuis l'icône du groupe."""
    src = Image.open(os.path.join(public, 'logos', 'icone-groupe-512.png')).convert('RGBA')
    fond = src.getpixel((256, 40))[:3] if src.getpixel((256, 40))[3] > 200 else OR
    plein = Image.new('RGBA', (512, 512), fond + (255,))
    plein.alpha_composite(src)
    plein.convert('RGB').save(os.path.join(public, 'logos', 'icone-groupe-masquable-512.png'), optimize=True)
    plein.convert('RGB').resize((180, 180), Image.LANCZOS).save(os.path.join(public, 'logos', 'apple-touch-icon.png'), optimize=True)


def manifeste(public, description, raccourcis):
    m = {
        'id': '/', 'name': NOM, 'short_name': COURT, 'description': description, 'lang': 'fr', 'dir': 'ltr',
        'start_url': '/?source=application', 'scope': '/', 'display': 'standalone', 'orientation': 'portrait',
        'background_color': FOND, 'theme_color': THEME, 'categories': ['education'],
        'icons': [
            {'src': '/logos/icone-groupe-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': '/logos/icone-groupe-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': '/logos/icone-groupe-masquable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
        'shortcuts': [{'name': n, 'url': u, 'icons': [{'src': '/logos/icone-groupe-192.png', 'sizes': '192x192'}]} for n, u in raccourcis],
    }
    captures = os.path.join(public, 'captures')
    if os.path.isdir(captures):
        for f in os.listdir(captures):  # captures.js écrit du PNG : converti en WebP, dix fois plus léger
            if f.endswith('.png'):
                Image.open(os.path.join(captures, f)).convert('RGB').save(os.path.join(captures, f[:-4] + '.webp'), 'WEBP', quality=80, method=6)
                os.remove(os.path.join(captures, f))
        m['screenshots'] = [{'src': f'/captures/{f}', 'sizes': '1080x2340', 'type': 'image/webp', 'form_factor': 'narrow', 'label': lab}
                            for f, lab in [('accueil.webp', 'Sept écoles, une méthode'), ('ecoles.webp', 'Choisissez votre école')]
                            if os.path.exists(os.path.join(captures, f))]
    open(os.path.join(public, 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(m, ensure_ascii=False, indent=1))


def fichiers(public, description, raccourcis):
    icones(public)
    manifeste(public, description, raccourcis)
    open(os.path.join(public, 'sw.js'), 'w', encoding='utf-8').write(SW)
    open(os.path.join(public, 'hors-ligne.html'), 'w', encoding='utf-8').write(HORS_LIGNE)
    open(os.path.join(public, '_headers'), 'w', encoding='utf-8').write(
        '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
        '/sw.js\n  Cache-Control: no-cache\n/manifest.webmanifest\n  Content-Type: application/manifest+json\n')
