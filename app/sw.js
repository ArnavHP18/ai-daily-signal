// AI Daily Signal swipe app: offline support.
// Network first for everything on this site (so a new edition shows as soon as it is published),
// falling back to the last copy we saw; cache first for web fonts.
const CACHE = 'ads-app-v3';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'feed.json', 'icons/icon-180.png', 'icons/icon-192.png', '../assets/logo.svg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res;
    })));
    return;
  }
  if (url.origin !== self.location.origin) return;
  // the app adds ?t=... to feed requests to skip every cache; store them under the plain URL
  const key = url.searchParams.has('t') ? url.origin + url.pathname : req;
  e.respondWith(fetch(req).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(key, copy)); }
    return res;
  }).catch(() => caches.match(key, {ignoreSearch: url.pathname.endsWith('/') || url.pathname.endsWith('index.html')})));
});
