// Swipe Learn School : application installable.
// Le réseau d'abord, toujours ; sans connexion, la dernière version vue du site, sinon la page « hors connexion ».
// Ne touche ni aux autres sites ni aux envois (seulement les lectures GET de ce site).
const CACHE = 'sls-v1';
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
